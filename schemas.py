from dataclasses import dataclass
from typing import Optional

from marshmallow import Schema, fields, validate


class Payment(Schema):
    amount = fields.Integer(required=True, validate=validate.Range(min=0.01),
                            attribute="Amount", data_key="Amount")
    currency = fields.String(attribute="Currency", data_key="Currency")
    ip_address = fields.String(required=True, attribute="IpAddress",
                              data_key="IpAddress")
    card_cryptogram_packet = fields.String(required=True,
                                          attribute="CardCryptogramPacket",
                                          data_key="CardCryptogramPacket")
    name = fields.String(attribute="Name", data_key="Name")
    payment_url = fields.String(attribute="PaymentUrl", data_key="PaymentUrl")
    invoice_id = fields.String(attribute="InvoiceId", data_key="InvoiceId")
    description = fields.String(attribute="Description", data_key="Description")
    culture_name = fields.String(attribute="CultureName", data_key="CultureName")
    account_id = fields.String(attribute="AccountId", data_key="AccountId")
    email = fields.String(attribute="Email", data_key="Email")
    payer = fields.Dict(attribute="Payer", data_key="Payer")
    json_data = fields.String(attribute="JsonData", data_key="JsonData")


class ResponseData(Schema):
    success = fields.String(required=True)
    message = fields.String()
    model = fields.Dict()


class AuthHeader(Schema):
    token = fields.String(data_key="Authorization")