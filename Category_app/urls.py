from django.urls import path
from Category_app.views import CategoryListCreateView, CategoryDetailView

urlpatterns = [
    path('', CategoryListCreateView.as_view(), name='category-list-create'),  # create a category & get a list of categories
    path('<uuid:id>/', CategoryDetailView.as_view(), name='category-detail'), # get/update/delete category details by uuid,
]
