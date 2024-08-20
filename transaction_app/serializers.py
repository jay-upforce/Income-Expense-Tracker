from rest_framework import serializers
from django.db import transaction
from transaction_app.models import Transaction
from Category_app.models import Category
from CustomField_app.models import CustomField
from Category_app.serializers import CategorySerializer
from DjangoProject.crypto import encrypt, decrypt

class TransactionSerializer(serializers.ModelSerializer):
    """The PrimaryKeyRelatedField in the serializer will handle these IDs, creating the many-to-many relationship
    between the Transaction and Category models based on the provided IDs."""
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all().filter(isDeleted=False), many=True, pk_field=serializers.UUIDField(format='hex_verbose')
    )
    custom_fields = serializers.PrimaryKeyRelatedField(
        queryset=CustomField.objects.all().filter(isDeleted=False), many=True
    )

    class Meta:
        model = Transaction  # model name for backwards
        fields = [
            'id', 'account', 'client', 'categories', 'custom_fields', 'name', 'details', 'transaction_on',
            'incomeOrExpense', 'amount', 'payment_mode', 'notes', 'isDeleted', 'created_at', 'updated_at'
        ]


    def validate(self, data):
        """
            This method is called automatically during the validation process of the serializer.
        """
        categories = data.get('categories', [])
        income_or_expense = data.get('incomeOrExpense')

        # Fetch the category_type of each selected category
        category_types = [decrypt(cat.category_type) for cat in categories]

        if income_or_expense:
            # Check if all categories are 'income' or 'expense'
            if all(ct == 'income' for ct in category_types) and (income_or_expense != 'income'):
                raise serializers.ValidationError(
                    "All selected categories are income types. incomeOrExpense must be 'income'.")
            if all(ct == 'expense' for ct in category_types) and (income_or_expense != 'expense'):
                raise serializers.ValidationError(
                    "All selected categories are expense types. incomeOrExpense must be 'expense'.")
            # If categories are mixed, raise an error
            if len(set(category_types)) > 1:
                raise serializers.ValidationError("Selected categories cannot be mixed between income and expense.")

        return data

    def update(self, instance, validated_data):
        # Decrypt fields before updating
        instance.name = decrypt(instance.name) if instance.name else None
        instance.details = decrypt(instance.details) if instance.details else None
        instance.incomeOrExpense = decrypt(instance.incomeOrExpense) if instance.incomeOrExpense else False
        instance.payment_mode = decrypt(instance.payment_mode) if instance.payment_mode else None
        instance.notes = decrypt(instance.notes) if instance.notes else None

        # Now update the fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save() # Save the updated instance, the model save method will handle encryption
        return instance


    ''' decrypted account object/data for passing data as response to the user '''
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field in representation:
            if field not in ['id', 'account', 'client', 'categories', 'custom_fields', 'amount', 'transaction_on', 'isDeleted', 'created_at', 'updated_at']:
                representation[field] = decrypt(representation[field])  # decrypt the field data
        return representation

