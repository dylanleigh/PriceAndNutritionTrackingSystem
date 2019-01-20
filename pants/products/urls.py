from django.conf.urls import url

from . import views

urlpatterns = [
   # /products/      # NB: just a listview, no detail views yet
   url(r'^$', views.ProductListView.as_view(), name='product-list'),
]
