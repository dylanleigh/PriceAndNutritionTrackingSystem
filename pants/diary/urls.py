from django.conf.urls import url

from . import views

urlpatterns = [
   # /diary/ - default breakdown
   url(r'^$', views.DiaryBreakdownView.as_view(), name='diarybreakdown-list'),
   # /diary/flat/ - flat list view, original /diary/
   url(r'^twoday/', views.DiaryBreakdownView.as_view(), name='diarybreakdowntwoday-list'),
   # /diary/flat/ - flat list view, original /diary/
   url(r'^flat/', views.DiaryFoodListView.as_view(), name='diaryfood-list'),
]

