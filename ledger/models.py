from django.conf import settings
from django.db import models
from django.db.models import F
from taggit.managers import TaggableManager
from decimal import Decimal

from accounts.models import CustomUser as User

class Product(models.Model):
    name = models.CharField(max_length=128, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=Decimal('0.00'))
    hidden = models.BooleanField(default=False)
    tags = TaggableManager()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"

class Transaction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='transactions',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='product_transactions'
    )
    recipient_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='received_transactions',
    )
    ingress_system = models.CharField(max_length=128, blank=True)
    concept = models.CharField(max_length=128, blank=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=Decimal('0.00'), verbose_name="Amount (€)")
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.timestamp}"

    def save(self, *args, **kwargs):
        if self.product:
            self.concept = f"Purchased {self.product.name}"
            User.objects.filter(id=self.user.id).update(balance=F('balance') - self.product.price)
        
        elif self.recipient_user:
            User.objects.filter(id=self.user.id).update(balance=F('balance') - self.amount)
            User.objects.filter(id=self.recipient_user.id).update(balance=F('balance') + self.amount)
            self.concept = f'Transfer to {self.recipient_user.username}'
        
        elif self.ingress_system:
            User.objects.filter(id=self.user.id).update(balance=F('balance') + self.amount)
            self.concept = f'Ingress via {self.ingress_system}'
        
        else:
            self.concept = f'Not specified'            
        
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.user.balance -= self.amount
        self.user.save()
        super().delete(*args, **kwargs)

class MobilePayTransaction(models.Model):
    """
    A transaction made with MobilePay.
    """
    id = models.CharField(max_length=100, primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mobilepay_transactions'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0))
    reference = models.CharField(max_length=100)
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name='mobilepay_transactions',
        blank=True, null=True,
    )

    def save(self, *args, **kwargs):
        self.transaction = Transaction.objects.create(
            user = self.user,
            amount = self.amount,
            ingress_system = 'MobilePay',
        )
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.transaction:
            self.transaction.delete()
        super().delete(*args, **kwargs)