from django.shortcuts import render
import json

def ingredient_manager(request):
    return render(request, 'frontend/ingredient_manager.html', {})

