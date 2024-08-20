from rest_framework import serializers
from DjangoProject.crypto import decrypt
from Wallet_app.models import Wallet
from Account_app.serializers import AccountSerializer


class WalletSerializer(serializers.ModelSerializer):
    icon = serializers.CharField(required=True, max_length=150)   # manually set this field

    class Meta:
        model = Wallet  # model name for backwards
        fields = ['id', 'name', 'description', 'icon', 'color', 'isDeleted']

    def update(self, instance, validated_data):
        # Decrypt fields before updating
        instance.name = decrypt(instance.name) if instance.name else None
        instance.description = decrypt(instance.description) if instance.description else None
        instance.icon = decrypt(instance.icon) if instance.icon else None
        instance.color = decrypt(instance.color) if instance.color else False

        # Now update the fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save() # Save the updated instance, the model save method will handle encryption
        return instance


    ''' decrypted wallet object/data for passing data as response to the user '''
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field in representation:
            if field not in ['id', 'isDeleted', 'created_at', 'updated_at']:
                representation[field] = decrypt(representation[field])  # decrypt the field data
        return representation
