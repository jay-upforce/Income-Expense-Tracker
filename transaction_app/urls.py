from django.urls import path
from transaction_app.views import TransactionListCreateView, TransactionDetailView

urlpatterns = [
    path('', TransactionListCreateView.as_view(), name='transaction-list-create'),  # create a transaction & get a list of transaction
    path('<uuid:id>/', TransactionDetailView.as_view(), name='account-detail'), # get/update/delete transaction details by uuid,
]
