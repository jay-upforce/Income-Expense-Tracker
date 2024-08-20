from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Wallet_app.models import Wallet
from Wallet_app.serializers import WalletSerializer

class WalletListCreateView(generics.ListCreateAPIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Filter wallets by the logged-in user and where isDeleted is False
        return Wallet.objects.filter(user=self.request.user, isDeleted=False)

class WalletDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = 'id'  # Use UUID field as the lookup field

    # override method
    def get_queryset(self):
        # Filter wallets by the logged-in user and where isDeleted is False
        return Wallet.objects.filter(user=self.request.user, isDeleted=False)

    # override method
    def perform_update(self, serializer):
        # Ensure user is not updated
        serializer.save(user=self.request.user)

    # override method
    def perform_destroy(self, instance):
        # Set isDeleted to True for the wallet instead of deleting it
        instance.isDeleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

