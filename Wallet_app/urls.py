from django.urls import path
from Wallet_app.views import WalletListCreateView, WalletDetailView

urlpatterns = [
    path('', WalletListCreateView.as_view(), name='wallet-list-create'),  # create a wallet & get a list of wallets
    path('<uuid:id>/', WalletDetailView.as_view(), name='wallet-detail'), # get/update/delete wallets details by id,
]
