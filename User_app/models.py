import os
import uuid
from django.db import models
from User_app.user_manager import UserManager
from django.contrib.auth.models import AbstractBaseUser
from DjangoProject.crypto import decrypt, encrypt
from functools import cached_property

''' base model for all models i don't have to mention below fields in all models. simply i inherit from BaseModel. '''
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Auto-generated UUID primary key
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    isDeleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

''' User model with inheriting AbstractBaseUser and BaseModel '''
class User(AbstractBaseUser, BaseModel):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    personalEmail = models.EmailField(blank=True, null=True)
    phone_no = models.CharField(max_length=15)
    alternatePhone = models.CharField(max_length=15, blank=True, null=True)
    profilePicture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    password = models.CharField(max_length=128)
    token = models.CharField(max_length=256, blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otpExpire = models.DateTimeField(blank=True, null=True)
    financialYear = models.CharField(max_length=20, blank=True, null=True)
    isGoogleSignup = models.BooleanField(default=False)
    googleCredential = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    objects = UserManager()

    def __str__(self):
        return decrypt(self.email)


    # to decrypt firstname and cache it then when we call this function i got descrypted firstname
    @cached_property
    def decrypted_firstname(self):
        return decrypt(self.firstname)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    ''' encryption method used to encrypt the all the fields without below mentioned fields '''
    def save(self, *args, **kwargs):
        for field in self._meta.fields: # get all the fields
            ''' get all the fields without below mentioned fields in list '''
            if field.name not in ['id', 'password', 'last_login', 'is_active', 'is_staff', 'is_superuser', 'created_at',
                                  'updated_at', 'isDeleted', 'isGoogleSignup', 'profilePicture']:
                value = getattr(self, field.name)   # get values
                if value is not None:
                    setattr(self, field.name, encrypt(str(value)))  # paas field value in encrypt function

        # Handle profilePicture separately for encryption
        if self.profilePicture and hasattr(self.profilePicture, 'name'):    # get profile picture name
            original_name, original_extension = os.path.splitext(self.profilePicture.name)  # split image name and extension
            encrypted_name = encrypt(original_name) # encrypted image name only
            self.profilePicture.name = f'{encrypted_name}{original_extension}'  # assign encrypted image name into DB

        super().save(*args, **kwargs)   # save data in DB
