import os
from typing import List, Union
from requests import Response, post

FAILED_LOAD_API_KEY = "Failed to load mailgun api key."
FAILED_LOAD_DOMAIN_NAME = "Failed to load mailgun domain name."
ERROR_SENDING_EMAIL = "Error sending email"


class MailgunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Mailgun:
    DOMAIN_NAME = os.environ.get("DOMAIN_NAME")
    API_KEY = os.environ.get("API_KEY")

    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str, html: str) -> Union[MailgunException, Response]:
        if cls.API_KEY is None:
            raise MailgunException(FAILED_LOAD_API_KEY)

        if cls.DOMAIN_NAME is None:
            raise MailgunException(FAILED_LOAD_DOMAIN_NAME)

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
            return MailgunException(ERROR_SENDING_EMAIL)

        return response
