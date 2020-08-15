"""pants URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from rest_framework import routers

from targets.views import TargetViewSet
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
router.register(r'target', TargetViewSet, 'target')
router.register(r'user', UserViewSet, 'user')

urlpatterns = [
    url(r'^$', website.index, name='website-index'),
    url(r'^wearpants/', auth_views.LoginView.as_view(template_name='website/login.html'), name='website-login'),
    url(r'^logout/', auth_views.LogoutView.as_view(template_name="website/logout.html"), name='website-logout'),
    url(r'^about/', website.about, name='website-about'),

    # REST Framework API
    path('api/1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Django template Frontend
    url(r'^diary/', include('diary.urls')),
    url(r'^recipes/', include('recipes.urls')),
    url(r'^ingredients/', include('ingredients.urls')),
    url(r'^targets/', include('targets.urls')),
    url(r'^products/', include('products.urls')),

    url(r'^adminbackend/', admin.site.urls),

    # Experimental Frontend
    url(r'^frontend/', include('frontend.urls'))
]
