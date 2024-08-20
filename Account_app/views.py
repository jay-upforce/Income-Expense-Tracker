from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Wallet_app.models import Wallet
from Account_app.models import Account
from Account_app.serializers import AccountSerializer


class AccountListCreateView(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        wallet = self.request.data.get('wallet')    # get request wallet object
        if wallet:  # if wallet found
            wallet_obj = Wallet.objects.get(id=wallet)  # get wallet object
            if wallet_obj.isDeleted:    # if wallet is deleted
                raise ValidationError(
                    {"message": "Your Selected wallet is deleted and cannot be used to create an account."})

            '''filter wallet object like select * from wallet where id=wallet and user=request.user'''
            if wallet_obj.user != self.request.user:
                raise ValidationError("The wallet does not belong to the user.")
        serializer.save()

    def get_queryset(self):
        # Filter account by the logged-in user and where isDeleted is False
        return Account.objects.filter(wallet__user=self.request.user, isDeleted=False)


class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = 'id'  # Use UUID field as the lookup field

    # override method
    def get_queryset(self):
        return Account.objects.filter(wallet__user=self.request.user, isDeleted=False)

    # override method
    def perform_update(self, serializer):
        wallet = serializer.validated_data.get('wallet')  # wallet instance is retrieved from the validated_data of the serializer
        if wallet and wallet.isDeleted:  # check wallet exists and whether isDelete is True.
            raise ValidationError("Your Selected wallet is deleted and cannot be used to create an account.")
        serializer.save()  # save account object

    # override method
    def perform_destroy(self, instance):
        # Set isDeleted to True for the wallet instead of deleting it
        instance.isDeleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
