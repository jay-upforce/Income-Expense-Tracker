from rest_framework import serializers
from Account_app.models import Account
from Wallet_app.models import Wallet
from CustomField_app.models import CustomField
from CustomField_app.serializers import CustomFieldSerializer
from DjangoProject.crypto import encrypt, decrypt

class AccountSerializer(serializers.ModelSerializer):
    """The PrimaryKeyRelatedField in the serializer will handle these IDs, creating the many-to-many relationship
    between the Account and Custom Field models based on the provided IDs."""
    custom_fields = serializers.PrimaryKeyRelatedField(
        queryset=CustomField.objects.all().filter(isDeleted=False), many=True
    )

    class Meta:
        model = Account  # model name for backwards
        fields = '__all__'

    def update(self, instance, validated_data):
        # Decrypt fields before updating
        instance.name = decrypt(instance.name) if instance.name else None
        instance.acc_num = decrypt(instance.acc_num) if instance.acc_num else None
        instance.gst_no = decrypt(instance.gst_no) if instance.gst_no else None
        instance.pan_no = decrypt(instance.pan_no) if instance.pan_no else None
        instance.bank_Details = decrypt(instance.bank_Details) if instance.bank_Details else False
        instance.address = decrypt(instance.address) if instance.address else None
        instance.phone_no = decrypt(instance.phone_no) if instance.phone_no else None
        instance.email = decrypt(instance.email) if instance.email else None
        instance.notes = decrypt(instance.notes) if instance.notes else False

        # Now update the fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save() # Save the updated instance, the model save method will handle encryption
        return instance


    ''' decrypted account object/data for passing data as response to the user '''
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field in representation:
            if field not in ['id', 'wallet', 'custom_fields', 'isDeleted', 'created_at', 'updated_at']:
                representation[field] = decrypt(representation[field])  # decrypt the field data
        return representation