
from decimal import Decimal
from collections import defaultdict

from django.conf import settings

# Utility functions for ingredients/nutrient data

# TODO This could be its own class that generates/caches individual
# ratios as required and enforces access/validation/etc, and does
# operations like summing.

THOUSAND=Decimal(1000)

def add_nutrition_ratios(data):
   """
   Given a dict of nutrition data, calculate the ratios
   of protein and fibre to J and $, plus misc ranks.

   Returns the dict with all the ratios added
   (note some may be missing if the data to calculate them wasn't supplied)
   All values in the dict (including original data) are also quantized per SETTINGS.

   Keys used only: 'cost', 'protein', 'fibre', 'kilojoules'
   """
   try:
      if data['cost']:  # per-dollar TODO make currency symbol in settings
         if data['protein'] is not None:
            data['protein_per_cost']=data['protein']/data['cost']
         if data['fibre'] is not None:
            data['fibre_per_cost']=data['fibre']/data['cost']
   except KeyError:
      pass  # no cost data

   try:
      if data['kilojoules']: # actually per-megajoule (note the *1000)
         if data['protein'] is not None:
            data['protein_per_j']=THOUSAND*data['protein']/data['kilojoules']
         if data['fibre'] is not None:
            data['fibre_per_j']=THOUSAND*data['fibre']/data['kilojoules']
         # While we are here, also determine the kcal amounts
         data['kilocalories']=data['kilojoules'] / settings.KJ_PER_KCAL

         if data['protein'] is not None and data['fibre'] is not None:
            # Combined protein_per_j and fibre_per_j TODO better here or template/FE?
            data['pf_per_j']=data['protein_per_j']+data['fibre_per_j']

            # Arbitrary "rank" - (2*protein + fibre) / 3*joules
            # (Given we want at least twice as much protein as fibre -
            #  probably even more, but weighting protein too much diminishes
            #  the high fibre recipes too much)
            data['rank']=THOUSAND * (data['protein'] * 2 + data['fibre']) / ( 3 * data['kilojoules'] )
   except KeyError:
      pass  # no nutrition data to calc

   # Finally normalize values except those with custom quantize FIXME list -> SETTINGS
   for key in data:
      if data[key] and key not in ('cost', 'kilojoules', 'grams'):
         data[key] = Decimal.quantize(data[key], settings.DECIMAL_PLACES)
   return data

def get_nutrition_limits(qset):
   """
   Given a queryset of objects with nutrition data values, return the maximum
   values found (as a dict). Includes ratio values (protein per KJ etc).
   """

   limits = defaultdict(float)
   items = settings.NUTRITION_DATA_ITEMS_EXTENDED

   for obj in qset:
      ndata = obj.nutrition_data
      for item in items:
         try:
            val = ndata[item]
            if val > limits[item]:
               limits[item] = val
         except (KeyError,TypeError):
            pass  # missing data and Nones ignored

   return limits
