from plaid import Client
from .config import PLAID_CLIENT_ID, PLAID_SECRET, PLAID_ENV


def get_plaid_client():
    return Client(
        client_id=PLAID_CLIENT_ID,
        secret=PLAID_SECRET,
        environment=PLAID_ENV
    )
