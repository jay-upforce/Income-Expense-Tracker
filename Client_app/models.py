import os
from django.db import models
from User_app.models import User, BaseModel
from Wallet_app.models import Wallet
from CustomField_app.models import CustomField
from DjangoProject.crypto import encrypt, decrypt

class Client(BaseModel):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='clients')    # foreign key
    custom_fields = models.ManyToManyField(CustomField, related_name='clients')  # M to M relationship
    name = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=255)
    email = models.EmailField()
    gst_no = models.CharField(max_length=20)
    address = models.TextField()
    avatar = models.ImageField(upload_to='client_avatar/', blank=True, null=True)
    notes = models.TextField()

    def __str__(self):
        return f'{decrypt(self.name)} - {decrypt(self.wallet.name)} - {decrypt(self.wallet.user.email)}'

    ''' encryption method used to encrypt the all the fields without below mentioned fields '''
    def save(self, *args, **kwargs):
        for field in self._meta.fields:  # get all the fields
            ''' get all the fields without below mentioned fields in list '''
            if field.name not in ['id', 'wallet', 'CustomField', 'avatar','isDeleted', 'created_at', 'updated_at']:
                value = getattr(self, field.name)  # get values
                if value is not None:
                    setattr(self, field.name, encrypt(value))  # paas field value in encrypt function

        # Handle avatar separately for encryption
        if self.avatar and hasattr(self.avatar, 'name'):  # get profile picture name
            original_name, original_extension = os.path.splitext(
                self.avatar.name)  # split image name and extension
            encrypted_name = encrypt(original_name)  # encrypted image name only
            self.avatar.name = f'{encrypted_name}{original_extension}'  # assign encrypted image name into DB

        super().save(*args, **kwargs)