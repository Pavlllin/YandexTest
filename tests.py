import asyncio
from unittest import TestCase, IsolatedAsyncioTestCase
from unittest.mock import patch, Mock

import pytest
from aiohttp import web

from client import CloudPaymentsClient
from test_data import SUCCESS_CARD_PAYMENT_RESPONSE, TEST_CARD_DATA, \
    SUCCESS_TOKEN_PAYMENT_RESPONSE, TEST_TOKEN_DATA


@pytest.fixture
def event_loop():
    yield asyncio.get_event_loop()


def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()


@pytest.mark.asyncio
async def test_hello(aiohttp_client):
    async with CloudPaymentsClient() as client:
        response = await client.cards_crypto_payment(TEST_CARD_DATA)
        assert response.status_code == 401


class TestClient(TestCase):
    @patch('client.CloudPaymentsClient')
    def test_card_payment(self, MockClient):
        client = MockClient()

        client.cards_crypto_payment.return_value = SUCCESS_CARD_PAYMENT_RESPONSE
        response = client.cards_crypto_payment(TEST_CARD_DATA)
        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)

    @patch('client.CloudPaymentsClient')
    def test_token_payment(self, MockClient):
        client = MockClient()

        client.tokens_crypto_payment.return_value = SUCCESS_TOKEN_PAYMENT_RESPONSE
        response = client.tokens_crypto_payment(TEST_TOKEN_DATA)
        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)
