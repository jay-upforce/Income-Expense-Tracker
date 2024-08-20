from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Wallet_app.models import Wallet
from Account_app.models import Account
from Category_app.models import Category
from transaction_app.models import Transaction
from Client_app.models import Client
from transaction_app.serializers import TransactionSerializer


class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        # check account object
        account = self.request.data.get('account')  # get request account object
        account = Account.objects.get(id=account) # get account object
        if account and account.isDeleted: # check account exists and whether isDelete is True.
            raise ValidationError({"message": "Your Selected account is deleted and cannot be used to create an account."})
        if account.wallet.user != self.request.user:
            raise ValidationError("The account does not belong to the user.")

        # check client object
        client = self.request.data.get('client')  # get request client object
        client = Client.objects.get(id=client)  # get client object
        if client and client.isDeleted:  # check account exists and whether isDelete is True.
            raise ValidationError(
                {"message": "Your Selected client is deleted and cannot be used to create an account."})
        if client.wallet.user != self.request.user:
            raise ValidationError("The client does not belong to the user.")

        # Check categories
        categories = self.request.data.get('categories')  # get request categories
        if categories:
            for category_id in categories:
                category = Category.objects.get(id=category_id)  # get each category object
                if category.isDeleted:  # check if category is marked as deleted
                    raise ValidationError(
                        {"message": f"Category {category.name} is deleted and cannot be used."}
                    )
                if category.wallet.user != self.request.user:  # check if category belongs to the user
                    raise ValidationError(
                        {"message": f"Category {category.name} does not belong to the user."}
                    )

        serializer.save()   # save transaction object

    def get_queryset(self):
        # Filter transaction by the logged-in user and where isDeleted is False
        return Transaction.objects.filter(account__wallet__user=self.request.user, isDeleted=False)


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = 'id'  # Use UUID field as the lookup field

    # override method
    def get_queryset(self):
        '''
            show all transactions where user==request.user & isDeleted==False
            we getr user from account->wallet->user
        '''
        return Transaction.objects.filter(account__wallet__user=self.request.user, isDeleted=False)

    # override method
    def perform_update(self, serializer):
        serializer.save()  # save account object

    # override method
    def perform_destroy(self, instance):
        # Set isDeleted to True for the wallet instead of deleting it
        instance.isDeleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
