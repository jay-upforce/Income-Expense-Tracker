from rest_framework import serializers
from CustomField_app.models import CustomField


class CustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomField
        fields = '__all__'

    def validate(self, data):
        """
        Validate the entire custom field data, ensuring the field_value matches the field_type.
        """
        field_type = data.get('field_type')
        field_value = data.get('field_value')

        if field_type == "text" and not isinstance(field_value, str):
            raise serializers.ValidationError("field_value must be a string for 'text' type.")

        if field_type == "textarea" and not isinstance(field_value, str):
            raise serializers.ValidationError("field_value must be a string for 'textarea' type.")

        if field_type in ["radio", "checkbox", "select", "multiSelect"] and not isinstance(field_value, list):
            raise serializers.ValidationError(f"field_value must be a list for '{field_type}' type.")

        if field_type == "number":
            if not isinstance(field_value, (int, float)):
                raise serializers.ValidationError("field_value must be a number (int or float) for 'number' type.")

        if field_type == "email":
            if not isinstance(field_value, str) or "@" not in field_value:
                raise serializers.ValidationError("field_value must be a valid email format for 'email' type.")

        if field_type == "password" and not isinstance(field_value, str):
            raise serializers.ValidationError("field_value must be a string for 'password' type.")

        if field_type in ["date", "time"] and not isinstance(field_value, str):
            raise serializers.ValidationError(
                f"field_value must be a string for '{field_type}' type in the correct format.")

        if field_type == "file" and not isinstance(field_value, str):
            raise serializers.ValidationError("field_value must be a file path as a string for 'file' type.")

        return data
