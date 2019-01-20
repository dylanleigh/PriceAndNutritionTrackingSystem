
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

from .models import DiaryFood
from ingredients.utils import add_nutrition_ratios

class DiaryFoodListView(LoginRequiredMixin, ListView):
   model = DiaryFood

   # ALWAYS filter to logged in user
   def get_queryset(self):
      user = self.request.user
      return DiaryFood.objects.filter(user=user)

   def get_context_data(self, **kwargs):
      context = super(DiaryFoodListView, self).get_context_data(**kwargs)
      return context


class DiaryBreakdownView(LoginRequiredMixin, TemplateView):

   template_name='diary/diarybreakdown_list.html'

   def get_context_data(self, **kwargs):
      context = super(DiaryBreakdownView, self).get_context_data(**kwargs)
      user = self.request.user

      # Get aggregate data for last 2 calendar days and add to context
      diarydata = DiaryFood.get_recent_diary_aggs(user)
      context.update(diarydata)

      return context

