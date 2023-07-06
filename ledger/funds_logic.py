import requests
from django.conf import settings
from datetime import datetime, timedelta
from decimal import Decimal

from .models import MobilePayTransaction

def retrieve_transaction(id: str):
    """
    Check transaction in MobilePay Reporting. It makes an API request
    to MobilePay and return a JSON response.
    """
    if settings.MOBILEPAY_TOKEN is None:
        raise Exception("MobilePay token is not set.")
    response = requests.get(
        f"https://api.mobilepay.dk/v3/reporting/transfers/{id}",
        headers = {
            'Authorization': f'Bearer {settings.MOBILEPAY_TOKEN}',
            'Content-Type': 'application/json'
        })
    if response.status_code != 200:
        raise Exception("Transaction not found.")
    _check_paymentpointid(response)
    _check_date(response)
    return response.json()

def _check_paymentpointid(response):
    """
    Check if the response is from the correct payment point. If not, raise an exception.
    """
    if response.json()['paymentPointId'] != settings.MOBILEPAY_PAYMENTPOINTID:
        raise Exception("Transaction is not from the correct payment point.")

def _check_date(response):
    """
    Check if the response is from 7 days from today. If not, raise an exception.
    """
    date = datetime.strptime(response.json()['date'], '%Y-%m-%d')
    if date < datetime.now() - timedelta(days=14):
        raise Exception("Transaction is earlier than 7 days ago.")   


def create_transaction(transaction: dict, user):
    """
    Create the transaction in the database.
    """
    # Check if there is a transaction with the same reference
    if MobilePayTransaction.objects.filter(reference=transaction['id']).exists():
        raise Exception("Transaction already exists.")
    MobilePayTransaction.objects.create(
        user = user,
        amount = _get_amount(Decimal(transaction['totalTransferredAmount'])),
        reference = transaction['reference'],
        id = transaction['id'],
    )

def _get_amount(amount: Decimal):
    """
    Return the amount adding the mobilepay fee.
    """
    fee = round(amount * settings.MOBILEPAY_FEE, 2)
    if fee < settings.MOBILEPAY_MIN_FEE:
        fee = settings.MOBILEPAY_MIN_FEE
    return round(amount + fee, 2)

