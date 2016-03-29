# coding: utf-8

import os
from models import Invoice

data = {
    'lines': [
        {
            'quantity': 1.000,
            'amount': 123.12,
            'description': 'product description',
            'price': 123.12,
            'tax_percentage': 18.00,
            'tax_amount': 9958.10
        }
    ],
    'certificate': '123',
    'signature_value': '123',
    'digest_value': '123',
    'supplier': {
        'ruc': 1012323123,
        'name': 'supplier name',
        'address': 'address'
    },
    'customer': {
        'ruc': 1012323123,
        'name': 'customer name',
        'address': 'customer address'
    },
    'aditional_data': [
        {
            'code': '01',
            'value': 'value'
        }
    ]
}

doc = Invoice(data, 'F001-23')
doc.render()
print doc.send()
