from django.db import models
from User_app.models import BaseModel, User
from DjangoProject.crypto import encrypt,decrypt


class Wallet(BaseModel):
    user = models.ForeignKey(User, related_name='wallets', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=150, blank=True, null=True)
    color = models.CharField(max_length=7)  # e.g., #FFFFFF for white

    def __str__(self):
        return decrypt(self.name) + ' - ' + decrypt(self.user.email)

    ''' encryption method used to encrypt the all the fields without below mentioned fields '''
    def save(self, *args, **kwargs):
        for field in self._meta.fields: # get all the fields
            ''' get all the fields without below mentioned fields in list '''
            if field.name not in ['id', 'user', 'isDeleted', 'created_at', 'updated_at']:
                value = getattr(self, field.name)   # get values
                if value is not None:
                    setattr(self, field.name, encrypt(value))   # paas field value in encrypt function
        super().save(*args, **kwargs)