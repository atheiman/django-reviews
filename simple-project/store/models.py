from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from reviews.models import Review#, Reviewable
from reviews.decorators import reviewable



@reviewable
class Product(models.Model):
    name = models.CharField(max_length=40, unique=True)

    reviews = GenericRelation(Review, related_query_name="product")

    def __unicode__(self):
        return self.name
