from django.urls import re_path

from . import views

urlpatterns = [
   # /diary/ - default breakdown
   re_path(r'^$', views.DiaryBreakdownView.as_view(), name='diarybreakdown-list'),
   # /diary/flat/ - flat list view, original /diary/
   re_path(r'^flat/', views.DiaryFoodListView.as_view(), name='diaryfood-list'),
]

