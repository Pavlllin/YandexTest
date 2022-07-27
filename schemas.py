from dataclasses import dataclass
from typing import Optional

from marshmallow import Schema, fields, validate

CURRENCY = ["RUB", "EUR", "USD", "GRB", "UAH", "BYR", "BYN", "KZT", "AZN",
            "CHF",
            "CZK", "CAD", "PLN", "SEK", "TRY", "CNY", "INR", "BRL", "ZAR",
            "UZS",
            "BGN", "RON", "AUD", "HKD", "GEL", "KGS", "AMD", "AED"]

CULTURE_NAME = ["ru-RU", "en-US", "lv", "az", "kk", "uk", "pl", "vi", "tr"]


class Payer(Schema):
    first_name = fields.String(attribute="FirstName", data_key="FirstName")
    last_name = fields.String(attribute="LastName", data_key="LastName")
    middle_name = fields.String(attribute="MiddleName", data_key="MiddleName")
    birth = fields.String(attribute="Birth", data_key="Birth")
    street = fields.String(attribute="Street", data_key="Street")
    address = fields.String(attribute="Address", data_key="Address")
    city = fields.String(attribute="City", data_key="City")
    country = fields.String(attribute="Country", data_key="Country")
    phone = fields.String(attribute="Phone", data_key="Phone")
    postcode = fields.String(attribute="Postcode", data_key="Postcode")


class BasePayment(Schema):
    amount = fields.Integer(required=True, validate=validate.Range(min=0.01),
                            attribute="Amount", data_key="Amount")
    currency = fields.String(attribute="Currency", data_key="Currency",
                             validate=validate.OneOf(CURRENCY),
                             load_default="RUB")
    invoice_id = fields.String(attribute="InvoiceId", data_key="InvoiceId")
    description = fields.String(attribute="Description", data_key="Description")
    email = fields.String(attribute="Email", data_key="Email")
    json_data = fields.String(attribute="JsonData", data_key="JsonData")


class CardPayment(BasePayment):
    ip_address = fields.String(required=True, attribute="IpAddress",
                               data_key="IpAddress")
    card_cryptogram_packet = fields.String(required=True,
                                           attribute="CardCryptogramPacket",
                                           data_key="CardCryptogramPacket")
    name = fields.String(attribute="Name", data_key="Name")
    payment_url = fields.String(attribute="PaymentUrl", data_key="PaymentUrl")

    culture_name = fields.String(attribute="CultureName",
                                 data_key="CultureName",
                                 validate=validate.OneOf(CULTURE_NAME))
    account_id = fields.String(attribute="AccountId", data_key="AccountId")

    payer = fields.Nested(Payer, attribute="Payer", data_key="Payer")


class TokenPayment(BasePayment):
    token = fields.String(required=True, attribute="Token",
                          data_key="Token")
    account_id = fields.String(attribute="AccountId", data_key="AccountId",
                               required=True)
    ip_address = fields.String(attribute="IpAddress",
                               data_key="IpAddress")


class ResponseData(Schema):
    success = fields.String(required=True)
    message = fields.String()
    model = fields.Dict()


class AuthHeader(Schema):
    authorization = fields.String(attribute="Authorization",
                                 data_key="Authorization")
