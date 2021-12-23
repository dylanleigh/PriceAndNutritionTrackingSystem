"""pants URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  re_path(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from rest_framework import routers

from website import views as website

# Viewsets for API added here, not in included 'app.urls' links
# as they are all under the /api/ space
from ingredients.views import IngredientViewSet, IngredientTagViewSet
from recipes.views import RecipeViewSet, RecipeNestedViewSet, RecipeTagViewSet, RecipeFlagViewSet
from diary.views import DiaryFoodViewSet
from pants.views import UserViewSet
router = routers.DefaultRouter()
router.register(r'ingredient', IngredientViewSet, 'ingredient')
router.register(r'ingredienttag', IngredientTagViewSet, 'ingredienttag')
router.register(r'recipe', RecipeViewSet, 'recipe')
router.register(r'recipe_full', RecipeNestedViewSet, 'recipef')
router.register(r'recipe_tag', RecipeTagViewSet, 'recipe_tag')
router.register(r'recipe_flag', RecipeFlagViewSet, 'recipe_flag')
router.register(r'diaryfood', DiaryFoodViewSet, 'diaryfood')
router.register(r'user', UserViewSet, 'user')

urlpatterns = [
    re_path(r'^$', website.index, name='website-index'),
    re_path(r'^wearpants/', auth_views.LoginView.as_view(template_name='website/login.html'), name='website-login'),
    re_path(r'^logout/', auth_views.LogoutView.as_view(template_name="website/logout.html"), name='website-logout'),
    re_path(r'^about/', website.about, name='website-about'),

    # REST Framework API
    path('api/1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Django template Frontend
    re_path(r'^diary/', include('diary.urls')),
    re_path(r'^recipes/', include('recipes.urls')),
    re_path(r'^ingredients/', include('ingredients.urls')),
    re_path(r'^targets/', include('targets.urls')),
    re_path(r'^products/', include('products.urls')),

    re_path(r'^adminbackend/', admin.site.urls),

    # Experimental Frontend
    re_path(r'^frontend/', include('frontend.urls'))
]
