import json
from typing import Any, Dict

import aioboto3

from src.auth.application.repositories.verificatation.verificate_email import (
    EmailServiceABC,
)
from src.auth.main.settings.settings import AppSettings


class SESEmailService(EmailServiceABC):
    def __init__(self, session: aioboto3.Session, settings: AppSettings):
        self.session = session
        self.endpoint_url = settings.aws_settings.aws_ses_endpoint_url
        self.source_email = settings.aws_settings.email_host_user
        self.services = settings.aws_settings.services
        self.backend_url = settings.aws_settings.backend_url

    async def send_confirmation_email(self, to_email: str, token: str) -> None:
        confirmation_url = f"{self.backend_url}/confirm-email?token={token}"

        async with self.session.client(
            self.services, endpoint_url=self.endpoint_url
        ) as client:
            await client.send_templated_email(
                Source=self.source_email,
                Destination={"ToAddresses": [to_email]},
                Template="RegistrationNotificationTemplate",
                TemplateData=json.dumps({"confirmation_url": confirmation_url}),
            )
