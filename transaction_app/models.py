from django.db import models
from User_app.models import BaseModel, User
from Account_app.models import Account
from Client_app.models import Client
from Category_app.models import Category
from CustomField_app.models import CustomField
from DjangoProject.crypto import encrypt, decrypt


class Transaction(BaseModel):
    # foreign keys (1 to M relationship)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='transactions')

    # many to many field (M to M relationship)
    """The through argument in a ManyToMany field allows you to specify an intermediate model that stores additional 
    data about the relationship between the two models."""
    categories = models.ManyToManyField(Category, through='TransactionCategory', related_name='transactions')
    custom_fields = models.ManyToManyField(CustomField, related_name='transactions')  # M to M relationship

    # other fields
    name = models.CharField(max_length=255)
    details = models.TextField()
    transaction_on = models.DateField()
    incomeOrExpense = models.CharField(max_length=20, choices=(('income', 'income'), ('expense', 'expense')))
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=255)  # like cash, online, etc..,
    notes = models.TextField()

    def __str__(self):
        return f'{decrypt(self.name)} - A/C::{decrypt(self.account.name)} - WLT::{decrypt(self.account.wallet.name)} - CLT::{decrypt(self.client.name)} - usr::{decrypt(self.account.wallet.user.email)}'

    ''' encryption method used to encrypt the all the fields without below mentioned fields '''
    def save(self, *args, **kwargs):
        for field in self._meta.fields:  # get all the fields
            ''' get all the fields without below mentioned fields in list '''
            if field.name not in ['id', 'account', 'client', 'categories', 'custom_fields', 'amount', 'transaction_on', 'isDeleted', 'created_at', 'updated_at']:
                value = getattr(self, field.name)  # get values
                if value is not None:
                    setattr(self, field.name, encrypt(value))  # paas field value in encrypt function
        super().save(*args, **kwargs)


class TransactionCategory(BaseModel):
    """
        This model is used to implement the through relationship between Transaction and Category
    """
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.transaction.name}"
