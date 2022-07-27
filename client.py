import asyncio

import aiohttp.connector

from abstract_client import AbstractInteractionClient, InteractionResponseError
from schemas import CardPayment, AuthHeader, TokenPayment, ResponseData
import base64
from logging import getLogger

from test_data import TEST_CARD_DATA, TEST_TOKEN_DATA

logger = getLogger(__name__)


class CloudPaymentsClient(AbstractInteractionClient):
    BASE_URL = "https://api.cloudpayments.ru"
    CONNECTOR = aiohttp.connector.TCPConnector()
    SERVICE = "MyClient"

    def __init__(self, public_id: str,
                 api_secret: str,
                 yandex_pay_token: str):
        super(CloudPaymentsClient, self).__init__()
        self.public_id = public_id
        self.api_secret = api_secret
        self.yandex_pay_token = self.decode_token(yandex_pay_token)

    async def __aenter__(self):
        await self.session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def cards_crypto_payment(self,
                                   data: dict) -> InteractionResponseError | ResponseData:
        url = self.endpoint_url("/payments/cards/charge")
        result = CardPayment().load(data)
        try:
            response = await self.post(url=url, interaction_method="POST",
                                       data=result,
                                       headers=self.create_header(
                                           self.public_id,
                                           self.api_secret))
            response = ResponseData().load(response)
            return response
        except InteractionResponseError as ex:
            logger.error(ex)
            return ex

    async def tokens_crypto_payment(self,
                                    data: dict) -> InteractionResponseError | ResponseData:
        url = self.endpoint_url("/payments/tokens/charge")
        result = TokenPayment().load(data)
        try:
            response = await self.post(url=url, interaction_method="POST",
                                       data=result,
                                       headers=self.create_header(
                                           self.public_id,
                                           self.api_secret))
            response = ResponseData().load(response)
            return response
        except InteractionResponseError as ex:
            logger.error(ex)
            return ex

    @staticmethod
    def create_header(public_id, api_secret):
        base_token = "Basic " + base64.b64encode(
            f"{public_id}:{api_secret}".encode('ascii')).decode(
            "ascii")
        header = AuthHeader().load({"Authorization": base_token})
        return header

    @staticmethod
    def decode_token(encode_token):
        token = base64.b64decode(encode_token.encode("ascii")).decode(
            "ascii")
        return token


async def main():
    async with CloudPaymentsClient() as client:
        await client.cards_crypto_payment(TEST_CARD_DATA)
        await client.tokens_crypto_payment(TEST_TOKEN_DATA)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
