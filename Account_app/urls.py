from django.urls import path
from Account_app.views import AccountListCreateView, AccountDetailView

urlpatterns = [
    path('', AccountListCreateView.as_view(), name='account-list-create'),  # create a account & get a list of accounts
    path('<uuid:id>/', AccountDetailView.as_view(), name='account-detail'), # get/update/delete account details by uuid,
]
