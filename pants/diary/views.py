
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from rest_framework import viewsets, permissions

from .models import DiaryFood
from .serializers import DiaryFoodSerializer
from targets.models import Target
from ingredients.utils import add_nutrition_ratios

class DiaryFoodListView(LoginRequiredMixin, ListView):
   '''Flat diary list view showing all items in the past'''
   model = DiaryFood

   # ALWAYS filter to logged in user
   def get_queryset(self):
      user = self.request.user
      return DiaryFood.objects.filter(user=user)

   def get_context_data(self, **kwargs):
      context = super(DiaryFoodListView, self).get_context_data(**kwargs)
      return context


class DiaryBreakdownView(LoginRequiredMixin, TemplateView):
   '''Main /diary/ list view, split over this calendar day, last 24
      hours, last calendar day.'''

   template_name='diary/diarybreakdown_list.html'

   def get_context_data(self, **kwargs):
      context = super(DiaryBreakdownView, self).get_context_data(**kwargs)
      user = self.request.user

      # Get aggregate data for last 2 calendar days and add to context
      diarydata = DiaryFood.get_recent_diary_aggs(user)
      context.update(diarydata)

      # Current daily target
      daily_target = Target.get_primary_target(user)
      context.update({'daily_target': daily_target})

      return context

class DiaryFoodViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Diary Food entries to be viewed and altered.
    """
    serializer_class = DiaryFoodSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    queryset = DiaryFood.objects.none()  # Required for DjangoModelPermissions to get Model
    filterset_fields = {
        'start_time': ['gte', 'lte', 'exact', 'gt', 'lt'],
    }

    def get_queryset(self):
       user = self.request.user
       return DiaryFood.objects.filter(user=user)
