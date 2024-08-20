from rest_framework import serializers
from Category_app.models import Category
from Wallet_app.models import Wallet
from CustomField_app.models import CustomField
from DjangoProject.crypto import encrypt, decrypt

class CategorySerializer(serializers.ModelSerializer):
    """The PrimaryKeyRelatedField in the serializer will handle these IDs, creating the many-to-many relationship
    between the Category and Custom Field models based on the provided IDs."""
    custom_fields = serializers.PrimaryKeyRelatedField(
        queryset=CustomField.objects.all().filter(isDeleted=False), many=True
    )

    class Meta:
        model = Category  # model name for backwards
        fields = '__all__'


    def update(self, instance, validated_data):
        # Decrypt fields before updating
        instance.name = decrypt(instance.name) if instance.name else None
        instance.details = decrypt(instance.details) if instance.details else None
        instance.notes = decrypt(instance.notes) if instance.notes else False
        instance.category_type = decrypt(instance.category_type) if instance.category_type else None

        # Now update the fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save() # Save the updated instance, the model save method will handle encryption
        return instance


    ''' decrypted category object/data for passing data as response to the user '''
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field in representation:
            if field not in ['id', 'wallet', 'custom_fields', 'isDeleted', 'created_at', 'updated_at']:
                representation[field] = decrypt(representation[field])  # decrypt the field data
        return representation
