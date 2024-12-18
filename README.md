# PyFlick

![Build Status](https://github.com/ZephireNZ/PyFlick/actions/workflows/build-and-deploy.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/PyFlick.svg)](https://pypi.org/project/PyFlick/)

A quick and dirty Python API for [Flick Electric](https://flickelectric.co.nz).

## Usage

```python
from pyflick import FlickAPI
from pyflick.authentication import SimpleFlickAuth
from aiohttp import ClientSession

def async get_flick_pricing():
    async with ClientSession() as session:
        auth = SimpleFlickAuth("USERNAME", "PASSWORD", session)

        api = FlickAPI(auth)

        return await api.getPricing()
```

The `SimpleFlickAuth` client can also accept custom client ID and secret (this can be found by sniffing the client).

API will return a `FlickPrice` object for accessing the price information.

You can also get the raw data via `FlickPrice.raw`.

This will return a price object that looks a little like this:

```json
{
  "kind": "mobile_provider_price",
  "customer_state": "active",
  "needle": {
    "price": "11.163",
    "status": "urn:flick:market:price:no_contract",
    "unit_code": "cents",
    "per": "kwh",
    "start_at": "2020-04-19T02:30:00Z",
    "end_at": "2020-04-19T02:59:59Z",
    "now": "2020-04-19T02:34:38.410Z",
    "type": "rated",
    "charge_methods": [
      "kwh"
    ],
    "components": [
      {
        "kind": "component",
        "charge_method": "kwh",
        "charge_setter": "retailer",
        "value": "4.26",
        "quantity": "1.0",
        "unit_code": "cents",
        "per": "kwh",
        "flow_direction": "import",
        "metadata": {
          "content_code": "UN",
          "channel_number": 1,
          "meter_serial_number": "RD1111111",
          "hours_of_availability": 24
        },
        "_links": {}
      },
      ...
    ]
  }
}
```
