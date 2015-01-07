from decimal import *

from django.db import models
from django.contrib.auth.models import User



MAX_SCORE = 5   # TODO: import MAX_SCORE from django settings
MIN_SCORE = 1   # TODO: import MIN_SCORE from django settings
SCORE_CHOICES = zip(
    range(MIN_SCORE, MAX_SCORE + 1),
    range(MIN_SCORE, MAX_SCORE + 1)
)
MAX_COMMENT_LENGTH = 1000



class Reviewable(models.Model):
    # reviews = models.ManyToManyField(
    #     'User',
    #     through='Review',
    #     related_name='%(app_label)s_%(class)s_reviews',
    # )

    def avg_review_score(self):
        getcontext().prec = 2
        avg_review_score = Decimal()
        for review in self.reviews.all():
            avg_review_score += review.score
        return avg_review_score / self.reviews.all().count()

    class Meta:
        abstract = True



class Review(models.Model):
    # reviewed_object = models.ForeignKey('Reviewable')
    user = models.ForeignKey('User')
    score = models.PositiveSmallIntegerField(
        choices=SCORE_CHOICES,
    )
    comment = models.TextField(
        max_length=MAX_COMMENT_LENGTH,
        blank=True,
    )
    anonymous = models.BooleanField(
        default=False,
    )

    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True
        # unique_together = ("reviewed_object", "user")
