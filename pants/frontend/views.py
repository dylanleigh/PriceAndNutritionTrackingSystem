from django.shortcuts import render

def ingredient_manager(request):
    context = {
        #@todo austin Not sure how to handle this, the only way to define this template var is in python, but it will be executed in js, so it has to be a js string.
        # Mask that ensures only 6 total digits, max 3 decimals
        'nutrition_mask': r"{mask: /^(?=^[\d.]{0,7}$)\d{0,6}(\.\d{0,3})?$/}",
        # Mask that ensures only lowercase letters, numbers and dashes
        "slug_mask": r"{mask: /^[0-9a-z-]*$/}",
        # Ensures only lowercase letters, numbers, dashes, and commas
        "tag_mask": r"{mask: /^[0-9a-z,-]*$/}"
    }
    return render(request, 'frontend/ingredient_manager.html', context)

def recipe_manager(request):
    context = {
        # Mask that ensures only lowercase letters, numbers and dashes
        "slug_mask": r"{mask: /^[0-9a-z-]*$/}",
        # Ensures only lowercase letters, numbers, dashes, and commas
        "tag_mask": r"{mask: /^[0-9a-z,-]*$/}"
    }
    return render(request, 'frontend/recipe_manager.html', context)

