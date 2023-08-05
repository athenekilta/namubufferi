import requests
from django.conf import settings
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Ingress

ERROR_CODES = {
    1: "Transaction is not from the correct payment point.",
    2: "Transaction is earlier than 7 days ago.",
    3: "Transaction already exists.",
}

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
    return response

def check_transaction(response):
    """
    Extract the transaction from the JSON response.
    """
    if _check_paymentpointid(response): return 1
    if _check_date(response): return 2
    if _check_transaction_in_database(response): return 3
    return 0

def _check_paymentpointid(response):
    """
    Check if the response is from the correct payment point. If not, raise an exception.
    """
    return response['paymentPointId'] != settings.MOBILEPAY_PAYMENTPOINTID

def _check_date(response):
    """
    Check if the response is from 7 days from today. If not, raise an exception.
    """
    date = datetime.strptime(response['date'], '%Y-%m-%d')
    return date < datetime.now() - timedelta(days=7)

def _check_transaction_in_database(response):
    """
    Check if the transaction is already in the database. If yes, raise an exception.
    """
    return Ingress.objects.filter(id=response['id']).exists()
    
def create_transaction(transaction: dict, user):
    """
    Create the transaction in the database.
    """
    Ingress.objects.create(
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

