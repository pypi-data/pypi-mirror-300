# -*- coding: utf-8 -*-

"""
Usage: process_mails FILE [--requeue_errors] [--list_emails=<number>] [--get_eml=<mail_id>] [--gen_pdf=<mail_id>]
                          [--get_eml_orig] [--reset_flags=<mail_id>] [--test_eml=<path>] [--stats] [--mail_id=<mail_id>]

Arguments:
    FILE         config file

Options:
    -h --help               Show this screen.
    --requeue_errors        Put email in error status back in waiting for processing.
    --list_emails=<number>  List last xx emails.
    --get_eml=<mail_id>     Get eml of original/contained email id.
    --get_eml_orig          Get eml of original email id (otherwise contained).
    --gen_pdf=<mail_id>     Generate pdf of contained email id.
    --reset_flags=<mail_id> Reset all flags of email id.
    --test_eml=<path>       Test an eml handling.
    --stats                 Get email stats following stats.
    --mail_id=<mail_id>     Use this mail id.
"""

from datetime import datetime
from datetime import timedelta
from docopt import docopt
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from hashlib import md5
from imio.email.dms import dev_mode
from imio.email.dms import email_policy
from imio.email.dms import logger
from imio.email.dms.imap import IMAPEmailHandler
from imio.email.dms.imap import MailData
from imio.email.dms.utils import get_next_id
from imio.email.dms.utils import get_reduced_size
from imio.email.dms.utils import get_unique_name
from imio.email.dms.utils import safe_unicode
from imio.email.dms.utils import save_as_eml
from imio.email.dms.utils import set_next_id
from imio.email.parser.parser import Parser  # noqa
from imio.email.parser.utils import stop  # noqa
from imio.email.parser.utils import structure  # noqa
from io import BytesIO
from PIL import Image
from PIL import ImageFile
from PIL import ImageOps
from PIL import UnidentifiedImageError
from smtplib import SMTP
from time import sleep
from xml.etree.ElementTree import ParseError

import configparser
import email
import imaplib
import json
import os
import re
import requests
import six
import sys
import tarfile
import zc.lockfile


try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path  # noqa


dev_infos = {"nid": None}
img_size_limit = 1024
# originally 89478485 => blocks at > 13300 pixels square
Image.MAX_IMAGE_PIXELS = None
# OSError: broken data stream when reading image file
ImageFile.LOAD_TRUNCATED_IMAGES = True
EXIF_ORIENTATION = 0x0112
MAX_SIZE_ATTACH = 19000000

ERROR_MAIL = """
Problematic mail is attached.\n
Client ID : {0}
IMAP login : {1}\n
mail id : {2}\n
Corresponding exception : {3}
{4}\n
{5}\n
"""

UNSUPPORTED_ORIGIN_EMAIL_EN = """
Dear user,

The attached email has been refused because it wasn't sent to us as an attachment.\n
\n
Please try again, by following one of these methods.\n
\n
If you are using Microsoft Outlook:\n
- In the ribbon, click on the More dropdown button next to the standard Forward button\n
- Choose Forward as Attachment\n
- Send the opened draft to the GED import address.\n
\n
If you are using Mozilla Thunderbird:\n
- Open the email you want to import into the GED.\n
- Click on the menu Message > Forward As > Attachment.\n
- Send the opened draft to the GED import address.\n
\n
Please excuse us for the inconvenience.\n
{0}\n
"""

UNSUPPORTED_ORIGIN_EMAIL = """
Cher utilisateur d'iA.Docs,

Le transfert de l'email attaché ("{1}") a été rejeté car il n'a pas été transféré correctement.\n
Veuillez refaire le transfert du mail original en transférant "en tant que pièce jointe".\n
Si vous utilisez Microsoft Outlook:\n
- Dans le ruban, cliquez sur la flèche du ménu déroulant située sur le bouton de transfert\n
- Choisissez le transfert en tant que pièce jointe\n
- Envoyez le mail sans rien compléter d'autre à l'adresse prévue pour iA.Docs.\n
\n
Si vous utilisez Mozilla Thunderbird:\n
- Faites un clic droit sur l'email pour ouvrir le menu contextuel\n
- Sélectionnez "Transférer au format" > "Pièce jointe".\n
- Envoyez le mail sans rien compléter d'autre à l'adresse prévue pour iA.Docs.\n
\n
Cordialement.\n
{0}\n
"""

IGNORED_MAIL = """
Bonjour,
Votre adresse email {3} n'est pas autorisée à transférer un email vers iA.docs.
Si cette action est justifiée, veuillez prendre contact avec votre référent interne.\n
Le mail concerné est en pièce jointe.\n
Client ID : {0}
IMAP login : {1}
mail id : {2}
pattern : "caché"
{4}\n
"""

RESULT_MAIL = """
Client ID : {0}
IMAP login : {1}\n
{2}\n
"""


class DmsMetadataError(Exception):
    """The response from the webservice dms_metadata route is not successful"""


class FileUploadError(Exception):
    """The response from the webservice file_upload route is not successful"""


class OperationalError(Exception):
    """The response from the webservice failed due to an OperationalError"""


def get_mail_len_status(mail, additional):
    """Returns some info following mail length regarding max length.

    :param mail: mail object
    :param additional: unicode message to return if mail is bigger than max size
    :return: mail as string, bool indicating if len is smaller, message for the user
    """
    mail_string = mail.as_string()
    if len(mail_string) > MAX_SIZE_ATTACH:
        return mail_string, False, additional
    return mail_string, True, ""


def notify_exception(config, mail_id, mail, error):
    client_id = config["webservice"]["client_id"]
    login = config["mailbox"]["login"]
    smtp_infos = config["smtp"]
    sender = smtp_infos["sender"]
    recipient = smtp_infos["recipient"]

    msg = MIMEMultipart()
    msg["Subject"] = "Error handling an email for client {}".format(client_id)
    msg["From"] = sender
    msg["To"] = recipient

    error_msg = error
    if hasattr(error, "message"):
        error_msg = safe_unicode(error.message)
    elif hasattr(error, "reason"):
        try:
            error_msg = "'{}', {}, {}, {}".format(error.reason, error.start, error.end, error.object)
        except Exception:
            error_msg = error.reason

    mail_string, len_ok, additional = get_mail_len_status(
        mail, "The attachment is too big: so it cannot be sent by mail !"
    )
    main_text = MIMEText(ERROR_MAIL.format(client_id, login, mail_id, error.__class__, error_msg, additional), "plain")
    msg.attach(main_text)

    if len_ok:
        attachment = MIMEBase("message", "rfc822")
        attachment.set_payload(mail_string, "utf8")
        attachment.add_header("Content-Disposition", "inline")
        msg.attach(attachment)

    smtp = SMTP(str(smtp_infos["host"]), int(smtp_infos["port"]))
    smtp.send_message(msg)
    smtp.quit()


def notify_unsupported_origin(config, mail, headers):
    smtp_infos = config["smtp"]
    sender = smtp_infos["sender"]
    from_ = headers["From"][0][1]

    msg = MIMEMultipart()
    msg["Subject"] = "Error importing email into iA.docs"
    msg["Subject"] = "Erreur de transfert de votre email dans iA.Docs"
    msg["From"] = sender
    msg["To"] = from_

    mail_string, len_ok, additional = get_mail_len_status(
        mail, "La pièce jointe est trop grosse: on ne sait pas l'envoyer par mail !"
    )
    main_text = MIMEText(UNSUPPORTED_ORIGIN_EMAIL.format(additional, headers["Subject"]), "plain")
    msg.attach(main_text)

    if len_ok:
        attachment = MIMEBase("message", "rfc822")
        attachment.set_payload(mail_string, "utf8")
        attachment.add_header("Content-Disposition", "inline")
        msg.attach(attachment)

    smtp = SMTP(str(smtp_infos["host"]), int(smtp_infos["port"]))
    smtp.send_message(msg)
    smtp.quit()


def notify_ignored(config, mail_id, mail, from_):
    client_id = config["webservice"]["client_id"]
    login = config["mailbox"]["login"]
    smtp_infos = config["smtp"]
    sender = smtp_infos["sender"]
    recipient = smtp_infos["recipient"]

    msg = MIMEMultipart()
    msg["Subject"] = "Transfert non autorisé de {} pour le client {}".format(from_, client_id)
    msg["From"] = sender
    msg["To"] = from_
    msg["Bcc"] = recipient

    mail_string, len_ok, additional = get_mail_len_status(
        mail, "La pièce jointe est trop grosse: on ne sait pas l'envoyer par mail !"
    )
    # main_text = MIMEText(IGNORED_MAIL.format(client_id, login, mail_id, from_, config['mailinfos']['sender-pattern']),
    main_text = MIMEText(IGNORED_MAIL.format(client_id, login, mail_id, from_, additional), "plain")
    msg.attach(main_text)

    if len_ok:
        attachment = MIMEBase("message", "rfc822")
        attachment.set_payload(mail_string, "utf8")
        attachment.add_header("Content-Disposition", "inline")
        msg.attach(attachment)

    smtp = SMTP(str(smtp_infos["host"]), int(smtp_infos["port"]))
    smtp.send_message(msg)
    smtp.quit()


def notify_result(config, subject, message):
    client_id = config["webservice"]["client_id"]
    login = config["mailbox"]["login"]
    smtp_infos = config["smtp"]
    sender = smtp_infos["sender"]
    recipient = smtp_infos["recipient"]

    msg = MIMEMultipart()
    msg["Subject"] = "{} for client {}".format(subject, client_id)
    msg["From"] = sender
    msg["To"] = recipient

    main_text = MIMEText(RESULT_MAIL.format(client_id, login, message), "plain")
    msg.attach(main_text)

    smtp = SMTP(str(smtp_infos["host"]), int(smtp_infos["port"]))
    smtp.send_message(msg)
    smtp.quit()


def check_transferer(sender, pattern):
    if re.match(pattern, sender, re.I):
        return True
    return False


def get_mailbox_infos(config):
    mailbox_infos = config["mailbox"]
    host = str(mailbox_infos["host"])
    port = int(mailbox_infos["port"])
    ssl = mailbox_infos["ssl"] == "true" and True or False
    login = mailbox_infos["login"]
    password = mailbox_infos["pass"]
    return host, port, ssl, login, password


def get_preview_pdf_path(config, mail_id):
    mail_infos = config["mailinfos"]
    output_dir = mail_infos["pdf-output-dir"]
    if isinstance(mail_id, bytes):
        filename = "{0}.pdf".format(mail_id.decode("UTF-8"))
    else:
        filename = "{0}.pdf".format(mail_id)
    return os.path.join(output_dir, filename)


def modify_attachments(mail_id, attachments):
    """Remove inline attachments and reduce size attachments"""
    new_lst = []
    for dic in attachments:
        # we pass inline image, often used in signature. This image will be in generated pdf
        if dic["type"].startswith("image/") and dic["disp"] == "inline":
            if dev_mode:
                logger.info("{}: skipped inline image '{}' of size {}".format(mail_id, dic["filename"], dic["len"]))
            continue
        if dic["type"].startswith("image/"):
            orient_mod = size_mod = False
            try:
                img = Image.open(BytesIO(dic["content"]))
            except UnidentifiedImageError:
                new_lst.append(dic)  # kept original image
                continue
            except Image.DecompressionBombError:  # never append because Image.MAX_IMAGE_PIXELS is set to None
                continue
            try:
                exif = img.getexif()
                orient = exif.get(EXIF_ORIENTATION, 0)
            except ParseError:
                logger.warning(
                    "{}: error getting exif info for image '{}', ignored orientation".format(mail_id, dic["filename"])
                )
                orient = 0
            new_img = img
            # if problem, si ImageMagik use https://github.com/IMIO/appy/blob/master/appy/pod/doc_importers.py#L545
            if orient and orient != 1:
                try:
                    new_img = ImageOps.exif_transpose(img)
                    orient_mod = True
                    if dev_mode:
                        logger.info("{}: reoriented image '{}' from {}".format(mail_id, dic["filename"], orient))
                except Exception:
                    pass
            if dic["len"] > 100000:
                is_reduced, new_size = get_reduced_size(new_img.size, img_size_limit)
                if is_reduced:
                    if dev_mode:
                        logger.info("{}: resized image '{}'".format(mail_id, dic["filename"]))
                    # see https://pillow.readthedocs.io/en/stable/handbook/concepts.html#filters
                    new_img = new_img.resize(new_size, Image.BICUBIC)
                    size_mod = True

            if size_mod or orient_mod:
                new_bytes = BytesIO()
                # save the image in new_bytes
                try:
                    new_img.save(new_bytes, format=img.format, optimize=True, quality=75)
                except ValueError:
                    new_img.save(new_bytes, format=img.format, optimize=True)
                new_content = new_bytes.getvalue()
                new_len = len(new_content)
                if orient_mod or (new_len < dic["len"] and float(new_len / dic["len"]) < 0.9):
                    #                                      more than 10% of difference
                    dic["filename"] = re.sub(r"(\.\w+)$", r"-(redimensionné)\1", dic["filename"])
                    if dev_mode:
                        logger.info(
                            "{}: new image '{}' ({} => {})".format(mail_id, dic["filename"], dic["len"], new_len)
                        )
                    dic["len"] = new_len
                    dic["content"] = new_content
        new_lst.append(dic)
    return new_lst


def post_with_retries(url, auth, action, mail_id, json_data=None, files=None, retries=5, delay=20):
    for attempt in range(1, retries + 1):
        try:
            response = requests.post(url, auth=auth, json=json_data, files=files)
            # can simulate an empty response when webservice communication problems
            # response._content = b""
            if not response.content:
                raise requests.exceptions.RequestException("Empty response")
            response.raise_for_status()  # Raise an HTTPError for bad responses
            req_content = json.loads(response.content)
            # can be simulated by stopping postgresql
            if "error" in req_content and "(OperationalError) " in req_content["error"]:
                raise OperationalError(req_content["error"])
            return req_content
        except (OperationalError, requests.exceptions.RequestException) as e:
            if attempt < retries:
                sleep(delay)
                logger.info(f"{mail_id}: failed attempt {attempt} to {action}: '{e}'")
            else:
                raise e


def send_to_ws(config, headers, main_file_path, attachments, mail_id):
    ws = config["webservice"]
    next_id, client_id = get_next_id(config, dev_infos)
    external_id = "{0}{1:08d}".format(client_id, next_id)

    tar_path = Path("/tmp") / "{}.tar".format(external_id)
    with tarfile.open(str(tar_path), "w") as tar:
        # 1) email pdf printout or eml file
        mf_contents = Path(main_file_path).open("rb").read()
        basename, ext = os.path.splitext(main_file_path)
        mf_info = tarfile.TarInfo(name="email{}".format(ext))
        mf_info.size = len(mf_contents)
        tar.addfile(tarinfo=mf_info, fileobj=BytesIO(mf_contents))

        # 2) metadata.json
        metadata_contents = json.dumps(headers).encode("utf8") if six.PY3 else json.dumps(headers)
        metadata_info = tarfile.TarInfo(name="metadata.json")
        metadata_info.size = len(metadata_contents)
        tar.addfile(tarinfo=metadata_info, fileobj=BytesIO(metadata_contents))

        # 3) every attachment file
        files = []
        for attachment in attachments:
            attachment_contents = attachment["content"]
            attachment_info = tarfile.TarInfo(
                name="/attachments/{}".format(get_unique_name(attachment["filename"], files))
            )
            attachment_info.size = len(attachment_contents)
            tar.addfile(tarinfo=attachment_info, fileobj=BytesIO(attachment_contents))
    if dev_mode:
        logger.info("tar file '{}' created".format(tar_path))
    else:  # we send to the ws
        tar_content = tar_path.read_bytes()
        now = datetime.now()
        metadata = {
            "external_id": external_id,
            "client_id": client_id,
            "scan_date": now.strftime("%Y-%m-%d"),
            "scan_hour": now.strftime("%H:%M:%S"),
            "user": "testuser",
            "pc": "pc-scan01",
            "creator": "scanner",
            "filesize": len(tar_content),
            "filename": tar_path.name,
            "filemd5": md5(tar_content).hexdigest(),
        }

        auth = (ws["login"], ws["pass"])
        proto = ws["port"] == "443" and "https" or "http"
        metadata_url = "{proto}://{ws[host]}:{ws[port]}/dms_metadata/{client_id}/{ws[version]}".format(
            proto=proto,
            ws=ws,
            client_id=client_id,
        )
        metadata_req_content = post_with_retries(metadata_url, auth, "post metadata", mail_id, json_data=metadata)
        # {'message': 'Well done', 'external_id': '05Z507000024176', 'id': 2557054, 'success': True}
        if not metadata_req_content["success"] or "id" not in metadata_req_content:
            msg = "mail_id: {}, code: '{}', error: '{}', metadata: '{}'".format(
                mail_id, metadata_req_content["error_code"], metadata_req_content["error"], metadata
            ).encode("utf8")
            raise DmsMetadataError(msg)
        response_id = metadata_req_content["id"]

        upload_url = "{proto}://{ws[host]}:{ws[port]}/file_upload/{ws[version]}/{id}".format(
            proto=proto, ws=ws, id=response_id
        )
        files = {"filedata": ("archive.tar", tar_content, "application/tar", {"Expires": "0"})}
        upload_req_content = post_with_retries(upload_url, auth, "upload file", mail_id, files=files, retries=5)
        if not upload_req_content["success"]:
            msg = "mail_id: {}, code: '{}', error: '{}'".format(
                mail_id,
                upload_req_content["error_code"],
                upload_req_content.get("error") or upload_req_content["message"],
            ).encode("utf8")
            raise FileUploadError(msg)

        set_next_id(config, next_id)


def process_mails():
    arguments = docopt(__doc__)
    config = configparser.ConfigParser()
    config_file = arguments["FILE"]
    config.read(config_file)

    host, port, ssl, login, password = get_mailbox_infos(config)
    counter_dir = Path(config["webservice"]["counter_dir"])
    counter_dir.mkdir(exist_ok=True)
    lock_filepath = counter_dir / "lock_{0}".format(config["webservice"]["client_id"])
    lock = zc.lockfile.LockFile(lock_filepath.as_posix())

    handler = IMAPEmailHandler()
    handler.connect(host, port, ssl, login, password)

    if arguments.get("--requeue_errors"):
        amount = handler.reset_errors()
        logger.info("{} emails in error were put back in waiting state".format(amount))
        handler.disconnect()
        lock.close()
        sys.exit()
    elif arguments.get("--list_emails"):
        handler.list_last_emails(nb=int(arguments.get("--list_emails")))
        # import ipdb; ipdb.set_trace()
        # handler.mark_reset_error('58')
        # handler.mark_reset_ignored('77')
        # handler.mark_mail_as_imported('594')
        # res, data = handler.connection.search(None, 'SUBJECT "FAIGNART MARION"')
        # for mail_id in data[0].split():
        #      omail = handler.get_mail(mail_id)
        #      parser = Parser(omail, dev_mode, mail_id)
        #      headers = parser.headers
        #      amail = parser.message
        #      parsed = MailParser(omail)
        #     logger.info(headers['Subject'])
        handler.disconnect()
        lock.close()
        sys.exit()
    elif arguments.get("--get_eml"):
        mail_id = arguments["--get_eml"]
        if not mail_id:
            stop("Error: you must give an email id (--get_eml=25 by example)", logger)
        try:
            mail = handler.get_mail(mail_id)
            parsed = Parser(mail, dev_mode, mail_id)
            logger.info(parsed.headers)
            message = parsed.message
            # structure(message)
            filename = "{}.eml".format(mail_id)
            if login:
                filename = "{}_{}".format(login, filename)
            if arguments.get("--get_eml_orig"):
                message = parsed.initial_message
                filename = filename.replace(".eml", "_o.eml")
            logger.info("Writing {} file".format(filename))
            # o_attachments = parsed.attachments(False, set())
            # attachments = modify_attachments(mail_id, o_attachments)
            save_as_eml(filename, message)
        except Exception as e:
            logger.error(e, exc_info=True)
            # notify_exception(config, mail_id, mail, e)
            if not dev_mode:
                handler.mark_mail_as_error(mail_id)
        handler.disconnect()
        lock.close()
        sys.exit()
    elif arguments.get("--gen_pdf"):
        mail_id = arguments["--gen_pdf"]
        if not mail_id:
            stop("Error: you must give an email id (--gen_pdf=25 by example)", logger)
        mail = handler.get_mail(mail_id)
        parsed = Parser(mail, dev_mode, mail_id)
        logger.info(parsed.headers)
        pdf_path = get_preview_pdf_path(config, mail_id.encode("utf8"))
        logger.info("Generating {} file".format(pdf_path))
        payload, cid_parts_used = parsed.generate_pdf(pdf_path)
        handler.disconnect()
        lock.close()
        sys.exit()
    elif arguments.get("--reset_flags"):
        mail_id = arguments["--reset_flags"]
        if not mail_id:
            stop("Error: you must give an email id (--reset_flags=25 by example)", logger)
        # handler.mark_mail_as_error(mail_id)
        handler.mark_reset_all(mail_id)
        handler.disconnect()
        lock.close()
        sys.exit()
    elif arguments.get("--test_eml"):
        handler.disconnect()
        eml_path = arguments["--test_eml"]
        if not eml_path or not os.path.exists(eml_path):
            stop(
                "Error: you must give an existing eml path '{}' (--test_eml=123.eml by example)".format(eml_path),
                logger,
            )
        if not dev_mode:
            stop("Error: You must activate dev mode to test an eml file", logger)
        with open(eml_path) as fp:
            mail = email.message_from_file(fp, policy=email_policy)
        mail_id = os.path.splitext(os.path.basename(eml_path))[0]
        mail.__setitem__("X-Forwarded-For", "0.0.0.0")  # to be considered as main mail
        parser = Parser(mail, dev_mode, "")
        headers = parser.headers
        main_file_path = get_preview_pdf_path(config, mail_id)
        logger.info("pdf file {}".format(main_file_path))
        cid_parts_used = set()
        try:
            payload, cid_parts_used = parser.generate_pdf(main_file_path)
            pdf_gen = True
        except Exception:
            main_file_path = main_file_path.replace(".pdf", ".eml")
            save_as_eml(main_file_path, parser.message)
            pdf_gen = False
        # structure(mail)
        o_attachments = parser.attachments(pdf_gen, cid_parts_used)
        # [{tup[0]: tup[1] for tup in at.items() if tup[0] != 'content'} for at in o_attachments]
        attachments = modify_attachments(mail_id, o_attachments)
        send_to_ws(config, headers, main_file_path, attachments, mail_id)
        lock.close()
        sys.exit()
    elif arguments.get("--stats"):
        logger.info("Started at {}".format(datetime.now()))
        stats = handler.stats()
        logger.info("Total mails: {}".format(stats.pop("tot")))
        for flag in sorted(stats["flags"]):
            logger.info("Flag '{}' => {}".format(flag, stats["flags"][flag]))
        handler.disconnect()
        lock.close()
        logger.info("Ended at {}".format(datetime.now()))
        sys.exit()

    imported = errors = unsupported = ignored = total = 0
    if arguments.get("--mail_id"):
        mail_id = arguments["--mail_id"]
        if not mail_id:
            stop("Error: you must give an email id (--mail_id=25 by example)", logger)
        mail = handler.get_mail(mail_id)
        if not mail:
            stop("Error: no mail found for id {}".format(mail_id), logger)
        emails = [MailData(mail_id, mail)]
    else:
        emails = handler.get_waiting_emails()
    for mail_info in emails:
        total += 1
        mail_id = mail_info.id
        mail = mail_info.mail
        main_file_path = get_preview_pdf_path(config, mail_id)
        try:
            parser = Parser(mail, dev_mode, mail_id)
            headers = parser.headers
            if parser.origin == "Generic inbox":
                if not dev_mode:
                    handler.mark_mail_as_unsupported(mail_id)
                unsupported += 1
                try:
                    notify_unsupported_origin(config, mail, headers)
                except Exception:  # better to continue than advise user
                    pass
                continue
            # we check if the pushing agent has a permitted email format
            if "Agent" in headers and not check_transferer(
                headers["Agent"][0][1], config["mailinfos"].get("sender-pattern", ".+")
            ):
                if not dev_mode:
                    handler.mark_mail_as_ignored(mail_id)
                # logger.error('Rejecting {}: {}'.format(headers['Agent'][0][1], headers['Subject']))
                ignored += 1
                try:
                    notify_ignored(config, mail_id, mail, headers["Agent"][0][1])
                except Exception:  # better to continue than advise user
                    pass
                continue
            # logger.info('Accepting {}: {}'.format(headers['Agent'][0][1], headers['Subject']))
            cid_parts_used = set()
            try:
                payload, cid_parts_used = parser.generate_pdf(main_file_path)
                pdf_gen = True
            except Exception:
                # if 'XDG_SESSION_TYPE=wayland' not in str(pdf_exc):
                main_file_path = main_file_path.replace(".pdf", ".eml")
                save_as_eml(main_file_path, parser.message)
                pdf_gen = False
            o_attachments = parser.attachments(pdf_gen, cid_parts_used)
            attachments = modify_attachments(mail_id, o_attachments)
            send_to_ws(config, headers, main_file_path, attachments, mail_id)
            if not dev_mode:
                handler.mark_mail_as_imported(mail_id)
            imported += 1
        except Exception as e:
            logger.error(e, exc_info=True)
            notify_exception(config, mail_id, mail, e)
            if not dev_mode:
                handler.mark_mail_as_error(mail_id)
            errors += 1

    if total:
        logger.info(
            "Treated {} emails: {} imported. {} unsupported. {} in error. {} ignored.".format(
                total, imported, unsupported, errors, ignored
            )
        )
    else:
        logger.info("Treated no email.")
    handler.disconnect()
    lock.close()


def clean_mails():
    """Clean mails from imap box.

    Usage: clean_mails FILE [-h] [--kept_days=<number>] [--ignored_too] [--list_only]

    Arguments:
        FILE         config file

    Options:
        -h --help               Show this screen.
        --kept_days=<number>    Days to keep [default: 30]
        --ignored_too           Get also not imported emails
        --list_only             Only list related emails, do not delete
    """
    arguments = docopt(clean_mails.__doc__)
    config = configparser.ConfigParser()
    config.read(arguments["FILE"])
    days = int(arguments["--kept_days"])
    doit = not arguments["--list_only"]
    host, port, ssl, login, password = get_mailbox_infos(config)
    handler = IMAPEmailHandler()
    handler.connect(host, port, ssl, login, password)
    before_date = (datetime.now() - timedelta(days)).strftime("%d-%b-%Y")  # date string 01-Jan-2021
    # before_date = '01-Jun-2021'
    res, data = handler.connection.search(None, "(BEFORE {0})".format(before_date))
    if res != "OK":
        logger.error("Unable to fetch mails before '{}'".format(before_date))
        handler.disconnect()
        sys.exit()
    deleted = ignored = error = 0
    mail_ids = data[0].split()
    mail_ids_len = len(mail_ids)
    out = ["Get '{}' emails older than '{}'".format(mail_ids_len, before_date)]
    logger.info("Get '{}' emails older than '{}'".format(mail_ids_len, before_date))
    # sys.exit()
    for mail_id in mail_ids:
        res, flags_data = handler.connection.fetch(mail_id, "(FLAGS)")
        if res != "OK":
            logger.error("Unable to fetch flags for mail {0}".format(mail_id))
            error += 1
            continue
        flags = imaplib.ParseFlags(flags_data[0])
        if not arguments["--ignored_too"] and b"imported" not in flags:
            ignored += 1
            continue
        mail = handler.get_mail(mail_id)
        if not mail:
            error += 1
            continue
        parser = Parser(mail, dev_mode, mail_id)
        logger.info("{}: '{}'".format(mail_id, parser.headers["Subject"]))
        out.append("{}: '{}'".format(mail_id, parser.headers["Subject"]))
        if doit:
            handler.connection.store(mail_id, "+FLAGS", "\\Deleted")
        deleted += 1
    if deleted:
        logger.info("Get '{}' emails older than '{}'".format(mail_ids_len, before_date))
        if doit:
            res, data = handler.connection.expunge()
            if res != "OK":
                out.append("ERROR: Unable to delete mails !!")
                logger.error("Unable to delete mails")
    handler.disconnect()
    out.append(
        "{} emails have been deleted. {} emails are ignored. {} emails have caused an error.".format(
            deleted, ignored, error
        )
    )
    logger.info(
        "{} emails have been deleted. {} emails are ignored. {} emails have caused an error.".format(
            deleted, ignored, error
        )
    )
    notify_result(config, "Result of clean_mails", "\n".join(out))
