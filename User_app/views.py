from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from User_app.models import User
from Wallet_app.models import Wallet
from User_app.serializers import UserSerializer, LoginSerializer
from DjangoProject.crypto import decrypt

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = {
            'FirstName': decrypt(serializer.data['firstname']),
            'LastName': decrypt(serializer.data['lastname']),
            'Email': decrypt(serializer.data['email']),
            'Phone_No': decrypt(serializer.data['phone_no'])
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data['token']
        return Response(tokens, status=status.HTTP_200_OK)

class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        # Ensure email is not updated
        serializer.save()

    def perform_destroy(self, instance):
        # Set isDeleted to True for all wallets related to the user
        Wallet.objects.filter(user=instance).update(isDeleted=True)
        # Set isDeleted to True for the user itself
        User.objects.filter(id=self.request.user.id).update(isDeleted=True)
        return Response(status=status.HTTP_204_NO_CONTENT)
