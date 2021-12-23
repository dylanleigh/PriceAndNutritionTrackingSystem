from django.urls import re_path

from . import views

urlpatterns = [
   # /targets/
   re_path(r'^$', views.TargetListView.as_view(), name='target-list'),

   # /targets/<slug>/
   re_path(
      r'^(?P<slug>[-\w]+)/$',
      views.TargetDetailView.as_view(),
      name='target-detail'
   ),
]

