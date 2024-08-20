from django.db import models
from User_app.models import BaseModel
from Wallet_app.models import Wallet
from CustomField_app.models import CustomField
from DjangoProject.crypto import encrypt, decrypt

class Category(BaseModel):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='categories')
    custom_fields = models.ManyToManyField(CustomField, related_name='categories')  # M to M relationship
    name = models.CharField(max_length=255)
    details = models.TextField()
    notes = models.TextField()
    category_type = models.CharField(max_length=20, choices=(('income', 'income'), ('expense', 'expense')))

    def __str__(self):
        return f'{decrypt(self.name)} - {decrypt(self.wallet.name)} - {decrypt(self.wallet.user.firstname)}'

    ''' encryption method used to encrypt the all the fields without below mentioned fields '''

    def save(self, *args, **kwargs):
        for field in self._meta.fields:  # get all the fields
            ''' get all the fields without below mentioned fields in list '''
            if field.name not in ['id', 'wallet', 'custom_fields', 'isDeleted', 'created_at', 'updated_at']:
                value = getattr(self, field.name)  # get values
                if value is not None:
                    setattr(self, field.name, encrypt(value))  # paas field value in encrypt function
        super().save(*args, **kwargs)