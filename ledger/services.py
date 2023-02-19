API_KEY = ''
MY_SHOP_NUMBER = ''
#from requests import get
import requests
from .models import LedgerSettings, Transaction, Product, Account

def test():
  pass


def fetch_mp_transactions():
  ls = LedgerSettings.load()
  print("mp_last", ls.mp_last)
  mp_new = None
  page = 1
  pagesize = 10
  while page != None:
    print(f"Fetching page {page}")
    r = requests.get(f"https://api.mobilepay.dk/v3/reporting/transactions?pagesize={pagesize}&pagenumber={page}", headers= {'Authorization': f"Bearer {API_KEY}"})
    json = r.json()
    page = json['nextPageNumber']
    for t in json['transactions']:
      timestamp = t['timestamp']
      # Store timestamp from the latest transaction
      if mp_new == None:
        mp_new = timestamp
      # Stop processing once we hit an already processed transaction, or if this is the first run
      if timestamp == ls.mp_last or not ls.mp_last:
        page = None
        break
      if t['type'] != 'Payment' or t['myShopNumber'] != MY_SHOP_NUMBER:
        continue

      print(t['amount'])
      account = Account.objects.filter(name = t['message']).first()
      product = Product.objects.get_or_create(
        name = 'MobilePay',
        price = 0)
      if account and product:
        Transaction.objects.create(
          account = account,
          product = product,
          price = 1,
          quantity = 1
        )



  ls.mp_last = mp_new
  ls.save()
