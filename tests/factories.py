from factory.django import DjangoModelFactory
from factory import SubFactory
from factory.fuzzy import FuzzyText, FuzzyInteger

from .models import Product
from reviews.models import Review
from django.contrib.auth.models import User

from django.conf import settings


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = FuzzyText()



class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = FuzzyText()



class ReviewFactory(DjangoModelFactory):
    class Meta:
        model = Review

    reviewed_object = SubFactory(ProductFactory)
    user = SubFactory(UserFactory)
    score = FuzzyInteger(
        settings.DJANGO_REVIEWS.get('MIN_SCORE'),
        settings.DJANGO_REVIEWS.get('MAX_SCORE'),
    )
    comment = FuzzyText()
