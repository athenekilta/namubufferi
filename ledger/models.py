from django.conf import settings
from django.db import models
from django.db.models import F
from taggit.managers import TaggableManager
from decimal import Decimal
from accounts.models import CustomUser as User
from taggit.models import TagBase, TaggedItemBase
from django.utils.translation import gettext_lazy as _

class ProductTag(TagBase):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
    
class TaggedProducts(TaggedItemBase):
    tag = models.ForeignKey(ProductTag, on_delete=models.CASCADE, related_name='tags_translations')
    content_object = models.ForeignKey('Product', related_name='product_tags', on_delete=models.CASCADE, blank=True, null=True)

class Product(models.Model):
    name = models.CharField(max_length=128, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=Decimal('0.00'))
    tags = TaggableManager(blank=True, through=TaggedProducts, verbose_name="Tags")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"

class Transaction(models.Model):
    """
    An abstract model for a transaction.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True, null=True,
    )
    concept = models.CharField(max_length=128, blank=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=Decimal('0.00'), verbose_name="Amount (€)")
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    def delete(self, *args, **kwargs):
        self.user.balance -= self.amount
        self.user.save()
        super().delete(*args, **kwargs)
    
    class Meta:
        ordering = ["timestamp"]
        abstract = True

class Purchase(Transaction):
    """
    A purchase made by a user.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name=_('purchase_transactions'),
    )

    def save(self, *args, **kwargs):
        User.objects.filter(id=self.user.id).update(balance=F('balance') - self.product.price)
        self.concept = _("Purchased ") + self.product.name
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = _("Purchases")
    
class TransferSend(Transaction):
    """
    A transfer sent by a user.
    """
    recipient_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='transfer_recipient_user',
    )

    def save(self, *args, **kwargs):
        User.objects.filter(id=self.user.id).update(balance=F('balance') - self.amount)
        TransferReceive.objects.create(
            user=self.recipient_user,
            sender_user=self.user,
            amount=self.amount,
        )
        self.concept = _('Transfer to ') + self.recipient_user.username
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = _("Transfer sends")

class TransferReceive(Transaction):
    """
    A transfer received by a user.
    """
    sender_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='transfer_sender_user',
    )

    def save(self, *args, **kwargs):
        User.objects.filter(id=self.user.id).update(balance=F('balance') + self.amount)
        self.concept = f'Transfer from {self.sender_user.username}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = _("Transfer receives")

class Ingress(Transaction):
    """
    An ingress made by a user. Only MobilePay is supported.
    """
    id = models.CharField(max_length=100, primary_key=True)
    reference = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        User.objects.filter(id=self.user.id).update(balance=F('balance') + self.amount)
        self.concept = _('Ingress via MobilePay')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = _("Ingresses")
