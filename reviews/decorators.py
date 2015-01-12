from decimal import *

from django.contrib.contenttypes.fields import GenericRelation

from .models import Review
from .defaults import *



def avg_review_score(self):
    """Return None for no reviews, or 2 digit Decimal review score avg."""
    if self.reviews.all().count() < 1:
        return None
    getcontext().prec = AVG_SCORE_DIGITS
    avg_review_score = Decimal()
    for review in self.reviews.all():
        avg_review_score += review.score
    return avg_review_score / self.reviews.count()



def reviewable(cls):
    """Decorator that adds useful functions for reviewable models.

    Example usage:

    @reviewable
    class Product(models.Model):
        name = models.CharField(max_length=50)

        reviews = GenericRelation(Review, related_query_name="product")

        def __unicode__(self):
            return self.name

    """
    cls.avg_review_score = avg_review_score
    # cls.reviews = GenericRelation(Review, related_query_name=cls.__name__)
    return cls
