from rest_framework import serializers
from Client_app.models import Client
from Wallet_app.models import Wallet
from CustomField_app.models import CustomField
from DjangoProject.crypto import encrypt, decrypt

class ClientSerializer(serializers.ModelSerializer):
    """The PrimaryKeyRelatedField in the serializer will handle these IDs, creating the many-to-many relationship
    between the Client and Custom Field models based on the provided IDs."""
    custom_fields = serializers.PrimaryKeyRelatedField(
        queryset=CustomField.objects.all().filter(isDeleted=False), many=True
    )
    avatar = serializers.ImageField(required=False)  # manually set this field

    class Meta:
        model = Client  # model name for backwards
        fields = '__all__'

    def update(self, instance, validated_data):
        # Handle profilePicture separately
        avatar = validated_data.pop('profilePicture', None)

        # Decrypt fields before updating
        instance.name = decrypt(instance.name) if instance.name else None
        instance.phone_no = decrypt(instance.phone_no) if instance.phone_no else None
        instance.email = decrypt(instance.email) if instance.email else None
        instance.gst_no = decrypt(instance.gst_no) if instance.gst_no else None
        instance.address = decrypt(instance.address) if instance.address else None
        instance.notes = decrypt(instance.notes) if instance.notes else None

        # Now update the fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Handle profilePicture updates
        if avatar:
            instance.avatar = avatar

        instance.save() # Save the updated instance, the model save method will handle encryption
        return instance


    ''' decrypted client object/data for passing data as response to the user '''
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field in representation:
            if field not in ['id', 'wallet', 'custom_fields', 'avatar', 'isDeleted', 'created_at', 'updated_at']:
                representation[field] = decrypt(representation[field])  # decrypt the field data

        # Handle profilePicture separately
        if instance.avatar:
            representation['avatar'] = decrypt(instance.avatar.name)  # decrypt the field data

        return representation