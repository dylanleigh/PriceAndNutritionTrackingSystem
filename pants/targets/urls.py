from django.conf.urls import url

from . import views

urlpatterns = [
   # /targets/
   url(r'^$', views.TargetListView.as_view(), name='target-list'),

   # /targets/<slug>/
   url(
      r'^(?P<slug>[-\w]+)/$',
      views.TargetDetailView.as_view(),
      name='target-detail'
   ),
]

