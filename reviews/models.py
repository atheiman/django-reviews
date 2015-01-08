import datetime
from decimal import *

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey#, GenericRelation
from django.contrib.contenttypes.models import ContentType

from .defaults import *



class Review(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    reviewed_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User, related_name='reviews')
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

    def is_updated(self):
        """Return false if review not updated, otherwise return datetime of update."""
        if self.updated - self.created > datetime.timedelta(0, UPDATED_COMPARISON_SECONDS):
            # updated datetime is within 10 sec of created datetime
            return self.updated
        else:
            return False

    def __unicode__(self):
        return "object: {o}, score: {s}, user: {u}".format(
                 o=self.reviewed_object, s=self.score, u=self.user.username)

    # class Meta:
    #     unique_together = ("reviewed_object", "user")



class Reviewable(models.Model):
    # http://stackoverflow.com/a/2752194/3343740
    # http://stackoverflow.com/questions/2752184/python-grab-class-in-class-definition/2752194#2752194
    # reviews = GenericRelation(Review, related_query_name='%(class)ss')

    def avg_review_score(self):
        """Return None for no reviews, or 2 digit Decimal review score avg."""
        if self.reviews.all().count() < 1:
            return None
        getcontext().prec = AVG_SCORE_DIGITS
        avg_review_score = Decimal()
        for review in self.reviews.all():
            avg_review_score += review.score
        return avg_review_score / self.reviews.count()

    class Meta:
        abstract = True
