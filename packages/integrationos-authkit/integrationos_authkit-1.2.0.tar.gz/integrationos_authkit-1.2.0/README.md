# IntegrationOS AuthKit SDK for Python

Secure token generation for [IntegrationOS AuthKit](https://docs.integrationos.com/docs/authkit) using [PyPI](https://pypi.org/).

## Installation

You can install the IntegrationOS AuthKit SDK using pip:

```
pip install integrationos-authkit
```

## Usage

Here's a quick example of how to use the SDK:

```python
from integrationos import AuthKitToken

@app.route('/authkit-token', methods=['POST'])
def create():
    authKitToken = AuthKitToken("sk_live_12345")
    token = authKitToken.create()

    return token
```

You'll want to switch out the API Key for your own, which will later tell your frontend which integrations you'd like to make available to your users.

If you pass an `identity` or `identityType` (`user`, `team`, or `organization`), you'll be able to query for all connections scoped to that identity. 
The identity is used to generate the unique [Connection Key](https://docs.integrationos.com/docs/setup) for the user once they successfully connect an account.

## Full Documentation

Please refer to the official [IntegrationOS AuthKit](https://docs.integrationos.com/docs/authkit) docs for a more holistic understanding of IntegrationOS AuthKit.