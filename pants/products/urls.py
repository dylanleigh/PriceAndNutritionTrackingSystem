from django.urls import re_path

from . import views

urlpatterns = [
   # /products/      # NB: just a listview, no detail views yet
   re_path(r'^$', views.ProductListView.as_view(), name='product-list'),
]
