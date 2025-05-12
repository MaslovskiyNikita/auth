import json
from typing import Any, Dict

import aioboto3

from src.auth.application.repositories.verificatation.verificate_email import (
    EmailServiceABC,
)
from src.auth.main.settings.settings import settings


class SESEmailService(EmailServiceABC):
    def __init__(
        self,
        aws_access_key: str,
        aws_secret_key: str,
        region: str,
        endpoint_url: str,
        source_email: str,
    ):
        self.session = aioboto3.Session(
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region,
        )
        self.endpoint_url = endpoint_url
        self.source_email = source_email

    async def send_confirmation_email(self, to_email: str, token: str) -> None:
        confirmation_url = f"{settings.backend_url}/confirm-email?token={token}"

        async with self.session.client(
            settings.services, endpoint_url=self.endpoint_url
        ) as client:
            await client.send_templated_email(
                Source=self.source_email,
                Destination={"ToAddresses": [to_email]},
                Template="RegistrationNotificationTemplate",
                TemplateData=json.dumps({"confirmation_url": confirmation_url}),
            )
