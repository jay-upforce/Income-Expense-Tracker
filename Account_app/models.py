from django.db import models
from User_app.models import BaseModel
from Wallet_app.models import Wallet
from CustomField_app.models import CustomField
from DjangoProject.crypto import encrypt, decrypt

class Account(BaseModel):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='accounts')   # foreign key (0 to M)
    custom_fields = models.ManyToManyField(CustomField, related_name='accounts') # M to M relationship
    name = models.CharField(max_length=255)
    acc_num = models.CharField(max_length=255)
    gst_no = models.CharField(max_length=20)
    pan_no = models.CharField(max_length=255)
    bank_Details = models.TextField()
    address = models.TextField()
    phone_no = models.CharField(max_length=255)
    email = models.EmailField()
    notes = models.TextField()

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