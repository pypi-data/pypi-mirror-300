import asyncio
import base64
import logging
import os
from urllib import request

import pandas as pd

from notify.msgraph import Graph

from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.message import Message
from msgraph.generated.models.email_address import EmailAddress
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.recipient import Recipient
from msgraph.generated.users.item.send_mail.send_mail_post_request_body import SendMailPostRequestBody
from msgraph.generated.models.o_data_errors.o_data_error import ODataError

from msgraph.generated.models.file_attachment import FileAttachment
from notify.utils import check_environment_variables, dataframe_to_html


class NotifyMail:
    def __init__(
        self,
        to: str,
        subject: str,
        message: str,
        cc: str = None,
        bcc: str = None,
        files: dict = None,
        df: pd.DataFrame = pd.DataFrame(),
    ):
        """
        This function sends an e-mail from Microsoft Exchange server

        Parameters
        ----------
        to: str
            the e-mail adress to send email to
        subject: str
            subject of the message
        message:
            HTML or plain text content of the message
        cc: str
            e-mail address to add as cc
        bcc: str
            e-mail address to add as bcc
        files: str, list
            Path(s) to file(s) to add as attachment
        df: pd.DataFrame
            dataframe that needs to be added to the HTML message.
        """

        check_environment_variables(["EMAIL_USER", "MAIL_TENANT_ID", "MAIL_CLIENT_ID", "MAIL_CLIENT_SECRET"])
        self.sender = os.environ.get("EMAIL_USER")
        self.to = to.replace(";", ",")
        self.cc = cc.replace(";", ",") if cc is not None else cc
        self.bcc = bcc.replace(";", ",") if bcc is not None else bcc
        self.subject = subject
        self.message = message
        self.files = [files] if isinstance(files, str) else files
        self.df = df
        self.graph = Graph()
        self.graph.ensure_graph_for_app_only_auth()

    @staticmethod
    def read_file_content(path):
        if path.startswith("http") or path.startswith("www"):
            with request.urlopen(path) as download:
                content = base64.b64encode(download.read())
        else:
            with open(path, "rb") as f:
                content = base64.b64encode(f.read())

        return content

    def send_email(self):
        """
        This function sends an e-mail from Microsoft Exchange server

        Returns
        -------
        response: requests.Response
        """

        sender = EmailAddress(address=self.sender)
        sender_recipient = Recipient(email_address=sender)
        recipients = []
        tos = self.to.split(",")
        for to in tos:
            to_email = EmailAddress(address=to)
            to_recipient = Recipient(email_address=to_email)
            recipients.append(to_recipient)
        message = Message(
            to_recipients=recipients, subject=self.subject, sender=sender_recipient, from_=sender_recipient
        )
        # CC if present
        if self.cc:
            ccs = self.cc.split(",")
            cc_recipients = []
            for cc in ccs:
                cc_email = EmailAddress(address=cc)
                cc_recipient = Recipient(email_address=cc_email)
                cc_recipients.append(cc_recipient)
            message.cc_recipients = cc_recipients
        # BCC if present
        if self.bcc:
            bccs = self.bcc.split(",")
            bcc_recipients = []
            for bcc in bccs:
                bcc_email = EmailAddress(address=bcc)
                bcc_recipient = Recipient(email_address=bcc_email)
                bcc_recipients.append(bcc_recipient)
            message.bcc_recipients = bcc_recipients
        email_body = ItemBody(content=self.message, content_type=BodyType.Html)
        # add html table (if table less than 30 records)
        if self.df.shape[0] in range(1, 31):
            html_table = dataframe_to_html(df=self.df)
        elif self.df.shape[0] > 30:
            logging.warning(f"Only first 30 records will be added. ({self.df.shape[0]} > the limit of 30).")
            html_table = dataframe_to_html(df=self.df.head(n=30))
        else:
            html_table = ""  # no data in dataframe (0 records)

        email_body.content += html_table
        message.body = email_body
        if self.files:
            # There might be a more safe way to check if a string is an url, but for our purposes, this suffices.
            attachments = list()
            for name, path in self.files.items():
                content = self.read_file_content(path)
                attachment = FileAttachment(
                    odata_type="#microsoft.graph.fileAttachment",
                    name=name,
                    content_bytes=base64.urlsafe_b64decode(content),
                )
                attachments.append(attachment)
            message.attachments = attachments
        request_body = SendMailPostRequestBody(message=message, save_to_sent_items=True)
        success = asyncio.run(self.get_mail_response(request_body))
        return success

    async def get_mail_response(self, request_body):
        try:
            await self.graph.app_client.users.by_user_id(self.sender).send_mail.post(request_body)
        except ODataError as e:
            # Handle Microsoft Graph API errors
            raise ODataError(f"Error sending email: {e.message}")

        except Exception as e:
            # Catch any other exceptions
            raise Exception(f"An unexpected error occurred: {str(e)}")

        return True
