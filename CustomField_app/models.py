from django.db import models
from django.core.exceptions import ValidationError
from User_app.models import BaseModel

"""
Text & Textarea: The value must be a string.
Radio, Checkbox, Select, MultiSelect: The value must be a list, which can hold multiple options. 
                                      This is useful for fields that may have multiple selections.
Number: The value must be an integer or float.
Email: The value must be a string in a valid email format (containing an "@" symbol).
Password: The value must be a string.
Date & Time: The value must be a string that represents a date or time in the correct format. 
             (Additional validation can be added to check the actual date/time format if needed.)
File: The value must be a string that represents a file path.
"""


TYPE_CHOICES = [
    ("text", 'Text'),
    ("textarea", 'Textarea'),
    ("radio", 'Radio'),
    ("checkbox", 'Checkbox'),
    ("number", 'Number'),
    ("email", 'Email'),
    ("password", 'Password'),
    ("select", 'Select'),
    ("multiSelect", 'MultiSelect'),
    ("date", 'Date'),
    ("time", 'Time'),
    ("file", 'File')
]


class CustomField(BaseModel):
    field_type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    field_value = models.JSONField()  # This will store the value of the field
    label = models.CharField(max_length=255)
    label_value = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.label}: {self.field_value} ({self.field_type})"
