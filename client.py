import asyncio

import aiohttp.connector
from aiohttp import web

from abstract_client import AbstractInteractionClient
from schemas import Payment, AuthHeader
import base64

test_data = {
    "Amount": 10,
    "Currency": "RUB",
    "InvoiceId": "1234567",
    "IpAddress": "123.123.123.123",
    "Description": "Оплата товаров в example.com",
    "AccountId": "user_x",
    "Name": "CARDHOLDER NAME",
    "CardCryptogramPacket": "01492500008719030128SMfLeYdKp5dSQVIiO5l6ZCJiPdel4uDjdFTTz1UnXY+3QaZcNOW8lmXg0H670MclS4lI+qLkujKF4pR5Ri+T/E04Ufq3t5ntMUVLuZ998DLm+OVHV7FxIGR7snckpg47A73v7/y88Q5dxxvVZtDVi0qCcJAiZrgKLyLCqypnMfhjsgCEPF6d4OMzkgNQiynZvKysI2q+xc9cL0+CMmQTUPytnxX52k9qLNZ55cnE8kuLvqSK+TOG7Fz03moGcVvbb9XTg1oTDL4pl9rgkG3XvvTJOwol3JDxL1i6x+VpaRxpLJg0Zd9/9xRJOBMGmwAxo8/xyvGuAj85sxLJL6fA==",
    "Payer":
        {
            "FirstName": "Тест",
            "LastName": "Тестов",
            "MiddleName": "Тестович",
            "Birth": "1955-02-24",
            "Address": "тестовый проезд дом тест",
            "Street": "Lenina",
            "City": "MO",
            "Country": "RU",
            "Phone": "123",
            "Postcode": "345"
        }
}

test_header = {
    "Authorization": "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
}


class CloudPaymentsClient(AbstractInteractionClient):
    BASE_URL = "https://api.cloudpayments.ru"
    CONNECTOR = aiohttp.connector.TCPConnector()
    SERVICE = "MyClient"

    def __init__(self, public_id: str = "Aladdin",
                 api_secret: str = "open sesame",
                 yandex_pay_token: str = "QWxhZGRpbjpvcGVuIHNlc2FtZQ=="):
        super(CloudPaymentsClient, self).__init__()
        self.public_id = public_id
        self.api_secret = api_secret
        self.yandex_pay_token = self.decode_token(yandex_pay_token)

    async def crypto_payment(self, data):
        url = self.endpoint_url("/payments/cards/charge")
        result = Payment().load(data)
        async with self.CONNECTOR:
            async with self.session:
                await self.post(url=url, interaction_method="GET", data=result,
                                headers=self.create_header(self.public_id,
                                                           self.api_secret))

    @staticmethod
    def create_header(public_id, api_secret):
        base_token = "Basic " + base64.b64encode(
            f"{public_id}:{api_secret}".encode('ascii')).decode(
            "ascii")
        header_schema = AuthHeader()
        header = header_schema.dump({"token": base_token})
        return header

    @staticmethod
    def decode_token(encode_token):
        token = base64.b64decode(encode_token.encode("ascii")).decode(
            "ascii")
        return token


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(CloudPaymentsClient().crypto_payment(test_data))
