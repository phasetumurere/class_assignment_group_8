from django.shortcuts import render
from store.models import *

def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('-date_created')

    # Get the reviews
    reviews = None
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'products': products,
        'reviews': reviews,
    }
    template_name = 'frontEnd/index.html'
    return render(request, template_name, context)
