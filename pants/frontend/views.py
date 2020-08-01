from django.shortcuts import render

def ingredient_manager(request):
    return render(request, 'frontend/ingredient_manager.html')

