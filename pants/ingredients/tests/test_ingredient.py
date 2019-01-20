
from decimal import Decimal
from django.test import TestCase
from ingredients.models import Ingredient

class IngredientTestCase(TestCase):
   def setUp(self):
      Ingredient.objects.create(
         name="milk",
         kilojoules=10000,
         protein=40,
         fibre=0,
         carbohydrate=50,
         sugar=40,
         fat=20,
         serving=250,
      )

   def test_nutrition_data(self):
      """Test nutrition data returned correctly, including ratios, per serve etc"""
      milk = Ingredient.objects.get(name='milk')
      ndata = milk.nutrition_data

      # basic
      self.assertEqual(ndata['kilojoules'], 10000)
      self.assertEqual(ndata['protein'], 40)
      self.assertEqual(ndata['fibre'], 0)
      self.assertEqual(ndata['carbohydrate'], 50)
      self.assertEqual(ndata['sugar'], 40)
      self.assertEqual(ndata['fat'], 20)

      # also required
      self.assertEqual(ndata['cost'], None)
      self.assertEqual(ndata['grams'], 1000) # per-KG

      # ratios / calculated
      self.assertEqual(ndata['protein_per_j'], 4)
      self.assertEqual(ndata['fibre_per_j'], 0)
      self.assertEqual(ndata['kilocalories'], Decimal('2390.06'))


