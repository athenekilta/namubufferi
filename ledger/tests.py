from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from .models import Product, Purchase, TransferReceive, TransferSend, Ingress, TermsOfService, PrivacyPolicy
from accounts.models import CustomUser
from accounts.tests import create_test_user_in_db
from unittest.mock import patch
from datetime import datetime, timedelta
from django.conf import settings

class TestBuyProduct(TestCase):

    def setUp(self):
        user = create_test_user_in_db()
        CustomUser.objects.filter(id=user.id).update(balance=Decimal(100))
        self.client.login( username='testuser', password='testpassword')
        self.product = Product.objects.create(name='testproduct', price=1)
        self.url = reverse('ledger:buy')

    def test_buy_product(self):
        data = {
            'product': self.product.pk,
        }
        response = self.client.post(self.url, data)
        user = CustomUser.objects.get(username='testuser')
        self.assertEqual(user.balance, Decimal(99))

        # check created transaction
        transaction = Purchase.objects.first()
        self.assertEqual(transaction.user, user)
        self.assertEqual(transaction.product, self.product)
        self.assertEqual(transaction.amount, 1)
        
    def test_form_submission_insufficient_funds(self):
        CustomUser.objects.filter(username='testuser').update(balance=Decimal(0))
        data = {
            'product': self.product.pk,
        }
        response = self.client.post(self.url, data)
        user = CustomUser.objects.get(username='testuser')
        self.assertEqual(user.balance, Decimal(0))

        # check no transaction created
        transaction = Purchase.objects.filter(user=user).first()
        self.assertIsNone(transaction)

class TestTransferMoney(TestCase):
    def setUp(self):
        self.sender = create_test_user_in_db()
        CustomUser.objects.filter(id=self.sender.id).update(balance=Decimal(100))
        self.recipient = create_test_user_in_db(username='testuser2', email='test2@example.com')
        self.client.login(username='testuser', password='testpassword')
        self.url = reverse('ledger:transfer')

    def test_form_submission(self):
        data = {
            'username': self.recipient.username,
            'amount': 1,
        }
        response = self.client.post(self.url, data)
        sender = CustomUser.objects.get(username='testuser')
        recipient = CustomUser.objects.get(username='testuser2')
        self.assertEqual(sender.balance, Decimal(99))
        self.assertEqual(recipient.balance, Decimal(1))

        # check created transaction
        transaction = TransferSend.objects.first()
        self.assertEqual(transaction.user, sender)
        self.assertEqual(transaction.recipient_user, recipient)
        self.assertEqual(transaction.amount, 1)

        # check created transaction
        transaction = TransferReceive.objects.first()
        self.assertEqual(transaction.user, recipient)
        self.assertEqual(transaction.sender_user, sender)
        self.assertEqual(transaction.amount, 1)

    def test_form_submission_insufficient_funds(self):
        CustomUser.objects.filter(username='testuser').update(balance=Decimal(0))
        data = {
            'username': self.recipient.username,
            'amount': 1,
        }
        response = self.client.post(self.url, data)
        sender = CustomUser.objects.get(username='testuser')
        recipient = CustomUser.objects.get(username='testuser2')
        self.assertEqual(sender.balance, Decimal(0))
        self.assertEqual(recipient.balance, Decimal(0))

        # check no transaction created
        transaction = TransferSend.objects.filter(user=sender).first()
        self.assertIsNone(transaction)

        # check no transaction created
        transaction = TransferReceive.objects.filter(user=recipient).first()
        self.assertIsNone(transaction)

class TestAddFunds(TestCase):
    def setUp(self):
        self.user = create_test_user_in_db()
        self.client.login(username='testuser', password='testpassword')
        self.url = reverse('ledger:funds')

    def test_add_funds(self):
        with patch('requests.get') as mock_mobilepay_api:
            mock_response = mock_mobilepay_api.return_value
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "id": "e68fd8b1-fb33-4b7a-8b1f-0b3b8b1f0b3b",
                "reference": "02850591194510208278",
                "date": datetime.now().strftime('%Y-%m-%d'),
                "totalTransferredAmount": 4.94,
                "currencyCode": "EUR",
                "paymentPointId": settings.MOBILEPAY_PAYMENTPOINTID,
            }

            response = self.client.post(self.url, {'id': "e68fd8b1-fb33-4b7a-8b1f-0b3b8b1f0b3b"})

        self.assertRedirects(response, reverse('ledger:buy'))
        ingress = Ingress.objects.filter(user=self.user).first()
        user = CustomUser.objects.get(username='testuser')
        self.assertEqual(user.balance, ingress.amount)

    def test_add_funds_invalid_id(self):
        with patch('requests.get') as mock_mobilepay_api:
            mock_response = mock_mobilepay_api.return_value
            mock_response.status_code = 404

            response = self.client.post(self.url, {'id': "e68fd8b1-fb33-4b7a-8b1f-0b3b8b1f0b3b"})

        ingress = Ingress.objects.filter(user=self.user).first()
        self.assertIsNone(ingress)
        user = CustomUser.objects.get(username='testuser')
        self.assertEqual(user.balance, 0)

    def test_add_funds_old_transaction(self):
        with patch('requests.get') as mock_mobilepay_api:
            old_date = datetime.now() + timedelta(days=-30)
            mock_response = mock_mobilepay_api.return_value
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "id": "e68fd8b1-fb33-4b7a-8b1f-0b3b8b1f0b3b",
                "reference": "02850591194510208278",
                "date": old_date.strftime('%Y-%m-%d'),
                "totalTransferredAmount": 4.94,
                "currencyCode": "EUR",
                "paymentPointId": settings.MOBILEPAY_PAYMENTPOINTID,
            }
            response = self.client.post(self.url, {'id': "e68fd8b1-fb33-4b7a-8b1f-0b3b8b1f0b3b"})

        ingress = Ingress.objects.filter(user=self.user).first()
        self.assertIsNone(ingress)
        user = CustomUser.objects.get(username='testuser')
        self.assertEqual(user.balance, 0)

    def test_add_funds_already_used(self):
        old_ingress = Ingress.objects.create(
            id="e68fd8b1-fb33-4b7a-8b1f-0b3b8b1f0b3b",
            user=self.user,
            amount=Decimal(5),
        )
        with patch('requests.get') as mock_mobilepay_api:
            mock_response = mock_mobilepay_api.return_value
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "id": "e68fd8b1-fb33-4b7a-8b1f-0b3b8b1f0b3b",
                "reference": "02850591194510208278",
                "date": datetime.now().strftime('%Y-%m-%d'),
                "totalTransferredAmount": 4.94,
                "currencyCode": "EUR",
                "paymentPointId": settings.MOBILEPAY_PAYMENTPOINTID,
            }
            response = self.client.post(self.url, {'id': "e68fd8b1-fb33-4b7a-8b1f-0b3b8b1f0b3b"})

        ingress = Ingress.objects.filter(user=self.user).count()
        self.assertEqual(ingress, 1)
        user = CustomUser.objects.get(username='testuser')
        self.assertEqual(user.balance, old_ingress.amount)