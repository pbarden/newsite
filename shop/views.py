from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Review
from django import forms
from .forms import ReviewForm
from cart.forms import CartAddProductForm
from django.db.models import Count

# Create your views here.
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {'category': category, 'categories': categories, 'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    reviews = product.reviews.filter(approved=True)

    new_review = None

    if request.method == 'POST':
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.product = product
            if new_review.rating > 5:
                new_review.rating = 5
            new_review.save()
    else:
        review_form = ReviewForm()
    
    product_tags_ids = product.tags.values_list('id', flat=True)
    recommended_products = Product.objects.filter(available=True, tags__in=product_tags_ids).exclude(id=product.id)
    recommended_products = recommended_products.annotate(same_tags=Count('tags')).order_by('-same_tags', '-updated')[:4]

    return render(request, 'shop/product/detail.html', {'product': product, 'cart_product_form': cart_product_form, 'reviews': reviews, 'new_review': new_review, 'review_form': review_form, 'recommended_products': recommended_products})