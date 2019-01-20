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
from django.conf.urls import include,url
from django.contrib import admin
from website import views as website

urlpatterns = [
    url(r'^$', website.index, name='website-index'),
    url(r'^wearpants/', website.login, name='website-login'),
    #url(r'^logout/', website.login, name='website-logout'),  # FIXME
    url(r'^about/', website.about, name='website-about'),

    url(r'^diary/', include('diary.urls')),
    url(r'^recipes/', include('recipes.urls')),
    url(r'^ingredients/', include('ingredients.urls')),
    url(r'^targets/', include('targets.urls')),
    url(r'^products/', include('products.urls')),

    url(r'^adminbackend/', admin.site.urls),
]
