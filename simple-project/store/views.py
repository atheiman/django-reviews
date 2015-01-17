from django.shortcuts import render
from reviews.models import Review
from django.shortcuts import get_object_or_404



def template_test(request, review_id=None):
    if review_id:
        review = get_object_or_404(Review, pk=review_id)
    else:
        review = Review.objects.all()[0]
    return render(request, 'store/template_test.html', {'review':review})
