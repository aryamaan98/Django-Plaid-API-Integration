from celery import shared_task
from .utils import get_plaid_client


@shared_task
def get_transactions(access_token, start_date, end_date):
    client = get_plaid_client()
    transactions = client.Transactions.get(access_token, start_date, end_date)
    return transactions


@shared_task
def get_accounts(access_token):
    client = get_plaid_client()
    accounts = client.Auth.get(access_token)
    return accounts


@shared_task
def get_access_token(public_token):
    client = get_plaid_client()
    exchange_response = client.Item.public_token.exchange(public_token)
    return exchange_response
