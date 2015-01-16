from django.shortcuts import render
from reviews.models import Review
from django.contrib.auth.models import User

from .models import Product



def template_test(request):
    review = Review.objects.all()[0]
    return render(request, 'store/template_test.html', {'review':review})
