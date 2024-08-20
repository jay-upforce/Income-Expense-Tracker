from django.urls import path
from Client_app.views import ClientListCreateView, ClientDetailView

urlpatterns = [
    path('', ClientListCreateView.as_view(), name='client-list-create'),  # create a client & get a list of clients
    path('<uuid:id>/', ClientDetailView.as_view(), name='client-detail'), # get/update/delete client details by uuid
]
