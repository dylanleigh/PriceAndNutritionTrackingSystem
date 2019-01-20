from django.conf.urls import url

from . import views

urlpatterns = [
   # /recipes/
   url(r'^$', views.RecipeListView.as_view(), name='recipe-list'),

   # /recipe/csvexport/
   url(
      r'^csvexport/$',
      views.RecipeCSVExportView,
      name='recipe-csv-export',
   ),

   # /recipes/tag/<tag>/
   url(
      r'^tag/([0-9A-Za-z_-]+)/$',
      views.RecipeListByTagView.as_view(),
      name='recipe-list-by-tag',
   ),

   # /recipes/<slug>/
   url(
      r'^(?P<slug>[-\w]+)/$',
      views.RecipeDetailView.as_view(),
      name='recipe-detail'
   ),
]

