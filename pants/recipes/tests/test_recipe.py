
from decimal import Decimal
from django.test import TestCase
from ingredients.models import Ingredient
from products.models import Product, Price   # FIXME
from recipes.models import Recipe, Component

class RecipeTestCase(TestCase):
   def setUp(self):
      # our ingredients
      milk = Ingredient.objects.create(
         name="milk",
         kilojoules=10000,
         protein=40,
         fibre=0,
         carbohydrate=50,
         sugar=40,
         fat=20,
         serving=250,
      )
      flour = Ingredient.objects.create(
         name="flour",
         kilojoules=20000,
         protein=120,
         fibre=40,
         carbohydrate=750,
         sugar=40,
         fat=20,
      )
      butter = Ingredient.objects.create(
         name="butter",
         kilojoules=30000,
         protein=100,
         fibre=0,
         carbohydrate=50,
         sugar=40,
         fat=800,
      )

      # recipe with just ingredients
      dough = Recipe.objects.create(
         name="dough",
         serves=2,
      )
      Component.objects.create(
         in_recipe=dough,
         of_ingredient=milk,
         weight=125,
      )
      Component.objects.create(
         in_recipe=dough,
         of_ingredient=flour,
         weight=120,
      )

      # recipe with another recipe
      flatbread = Recipe.objects.create(
         name="flatbread",
         serves=4,
      )
      Component.objects.create(
         in_recipe=flatbread,
         of_recipe=dough,
         servings=2,         # serves of a recipe
      )
      Component.objects.create(
         in_recipe=flatbread,
         of_ingredient=butter,
         weight=50,        # weight of an ingredient
      )

   def test_nutrition_data_serve(self):
      """Test per-serve nutrition data returned correctly, including ratios, per serve etc"""
      dough = Recipe.objects.get(name='dough')
      ndata = dough.nutrition_data

      # basic
      self.assertEqual(ndata['kilojoules_serve'], Decimal('3650')/2) # (10000/1000*125+20000/1000*120) / 2 serves
      self.assertEqual(ndata['protein_serve'], Decimal('9.70'))
      self.assertEqual(ndata['fibre_serve'], Decimal('2.4'))
      self.assertEqual(ndata['carbohydrate_serve'], Decimal('48.12'))
      self.assertEqual(ndata['sugar_serve'], Decimal('4.9'))
      self.assertEqual(ndata['fat_serve'], Decimal('2.45'))

      # also required
      self.assertEqual(ndata['cost'], None)
      self.assertEqual(ndata['grams_serve'], Decimal('122.5')) # (120+125)/2 serves

      # ratios / calculated
      self.assertEqual(ndata['protein_per_j'], Decimal('5.32'))
      self.assertEqual(ndata['fibre_per_j'], Decimal('1.32'))
      self.assertEqual(ndata['kilocalories'], Decimal('872.37'))

   def test_recipe_in_recipe(self):
      """Test nutrition data of a recipe in another recipe works correctly"""
      flatbread = Recipe.objects.get(name='flatbread')
      ndata = flatbread.nutrition_data

      # basic
      self.assertEqual(ndata['kilojoules_serve'], Decimal('1287.50'))
      self.assertEqual(ndata['protein_serve'], Decimal('6.1'))
      self.assertEqual(ndata['fibre_serve'], Decimal('1.2'))
      self.assertEqual(ndata['carbohydrate_serve'], Decimal('24.68'))
      self.assertEqual(ndata['sugar_serve'], Decimal('2.95'))
      self.assertEqual(ndata['fat_serve'], Decimal('11.22'))

      # also required
      self.assertEqual(ndata['cost'], None)
      self.assertEqual(ndata['grams_serve'], Decimal('73.75'))

      # ratios / calculated
      self.assertEqual(ndata['protein_per_j'], Decimal('4.74'))
      self.assertEqual(ndata['fibre_per_j'], Decimal('0.93'))
      self.assertEqual(ndata['kilocalories'], Decimal('1230.88'))
