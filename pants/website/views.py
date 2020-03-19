# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned

from ingredients.models import Ingredient
from products.models import Product,Price,Supplier
from recipes.models import Recipe
from targets.models import Target
from diary.models import DiaryFood

# Views to handle basic website pages (home,login,logout etc)

@login_required
def index(request):
   """
   View for home page - show summary of daily target and nutrition for
   today (since midnight) and last 24 hours
   """
   user=request.user

   # TODO: This does a lot of unneccesary calculation for what we want
   # - consider new get_diary_aggs() which can be more targeted. We
   # can also use that to get more recent data - last 1/2/4 hours
   diarydata = DiaryFood.get_recent_diary_aggs(user)

   context = {
      'daily_target': Target.get_primary_target(user),
      'diary_today': diarydata['today_total'],
      'diary_last24': diarydata['last24_sum'],
   }
   return render(request, 'website/home.html', context)

def login(request):
   # FIXME logged in already?
   # if request.user.is_authenticated:
   context = {}
   return render(request, 'website/login.html', context)

@login_required
def logout(request):
   # FIXME logout stuff
   # if request.user.is_authenticated:
   context = {}
   return render(request, 'website/login.html', context)

# NB: About page includes statistics on DB etc
@login_required
def about(request):
   # Define QS we will use multiple times
   all_ings = Ingredient.objects.all()
   all_rec = Recipe.objects.all()
   all_prod = Product.objects.all()
   all_diary = DiaryFood.objects.all()
   all_targ = Target.objects.all()

   context = {
      'ing_count': all_ings.count(),
      'ing_count_no_kj': all_ings.filter(kilojoules=None).count(),
      'ing_count_no_price': all_ings.filter(product__price__isnull=True).count(),
      # TODO: Do single-product and multiple-product with aggregate count

      'price_count': Price.objects.count(),
      'supplier_count': Supplier.objects.count(),

      'recipe_count': all_rec.count(),
      'recipe_count_sub_rec': all_rec.filter(components__of_recipe__isnull=False).distinct().count(),

      'diary_count': all_diary.count(),
      'target_count': all_targ.count(),      # TODO show more stats on these

      'prod_count': all_prod.count(),
   }
   return render(request, 'website/about.html', context)
