from django.urls import path
from CustomField_app.views import CustomFieldListCreateView, CustomFieldDetailView

urlpatterns = [
    path('', CustomFieldListCreateView.as_view(), name='customfield-list-create'),
    path('<uuid:id>/', CustomFieldDetailView.as_view(), name='customfield-detail'),
]