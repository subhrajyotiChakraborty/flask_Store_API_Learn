import os
from typing import List, Union
from requests import Response, post
from libs.strings import gettext


class MailgunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Mailgun:
    DOMAIN_NAME = os.environ.get("DOMAIN_NAME")
    API_KEY = os.environ.get("API_KEY")

    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str, html: str) -> Union[MailgunException, Response]:
        if cls.API_KEY is None:
            raise MailgunException(gettext("mailgun_failed_load_api_key"))

        if cls.DOMAIN_NAME is None:
            raise MailgunException(gettext("mailgun_failed_load_domain"))

        response = post(
            f"https://api.mailgun.net/v3/{cls.DOMAIN_NAME}/messages",
            auth=("api", f"{cls.API_KEY}"),
            data={"from": f"Stores REST API <mailgun@{cls.DOMAIN_NAME}>",
                  "to": email,
                  "subject": subject,
                  "text": text,
                  "html": html
                  },
        )

        if response.status_code != 200:
            return MailgunException(gettext("mailgun_error_send_email"))

        return response
