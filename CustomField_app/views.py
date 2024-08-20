from rest_framework import generics
from CustomField_app.models import CustomField
from CustomField_app.serializers import CustomFieldSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# CustomField Views
class CustomFieldListCreateView(generics.ListCreateAPIView):
    queryset = CustomField.objects.all()
    serializer_class = CustomFieldSerializer
    permission_classes = [IsAuthenticated]

class CustomFieldDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomField.objects.all()
    serializer_class = CustomFieldSerializer
    permission_classes = [IsAuthenticated]