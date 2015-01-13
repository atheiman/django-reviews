import datetime, operator
from decimal import *

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from .defaults import *



class Review(models.Model):
    if REVIEWABLE_MODELS:
        limit = reduce(operator.or_, (models.Q(**condition) for condition in REVIEWABLE_MODELS))
    else:
        limit = None
    content_type = models.ForeignKey(ContentType, limit_choices_to=limit)
    object_id = models.PositiveIntegerField()
    reviewed_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User, related_name='reviews')
    score = models.PositiveSmallIntegerField(
        choices=SCORE_CHOICES,
    )
    comment = models.TextField(
        max_length=MAX_COMMENT_LENGTH,
        blank=not COMMENT_REQUIRED,
    )
    anonymous = models.BooleanField(
        default=False,
    )
    comment_approved = models.BooleanField(
        default=not COMMENT_APPROVAL_REQUIRED,
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

    def save(self, *args, **kwargs):
        # set self.comment_approved if no comment
        if not self.comment:
            self.comment_approved = True

        super(Review, self).save(*args, **kwargs)

    # class Meta:
    #     unique_together = ("reviewed_object", "user")



class Reviewable(models.Model):
    """Generic reviewable model to be subclassed.

    To be deprecated in favor of reviews.decorators.reviewable.
    """

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
