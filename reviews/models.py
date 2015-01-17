import datetime, operator
from decimal import *

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import formats
from django.utils.html import format_html, mark_safe

from .defaults import *



class Review(models.Model):
    if REVIEWABLE_MODELS:
        limit = reduce(operator.or_, (models.Q(**condition) for condition in REVIEWABLE_MODELS))
    else:
        limit = None
    content_type = models.ForeignKey(
        ContentType,
        limit_choices_to=limit,
        help_text="Reviewed model",
    )
    object_id = models.PositiveIntegerField()
    reviewed_object = GenericForeignKey(
        'content_type',
        'object_id',
    )

    user = models.ForeignKey(
        User,
        related_name='reviews',
        help_text="User that submitted the review",
    )
    score = models.PositiveSmallIntegerField(
        choices=SCORE_CHOICES,
        help_text="Integer score in a range from %d through %d" % (MIN_SCORE, MAX_SCORE),
    )
    comment = models.TextField(
        max_length=MAX_COMMENT_LENGTH,
        blank=not COMMENT_REQUIRED,
        help_text="A comment explaining the score for the review",
    )
    anonymous = models.BooleanField(
        default=False,
        help_text="Keep the reviewer identity anonymous",
    )
    comment_approved = models.BooleanField(
        default=not COMMENT_APPROVAL_REQUIRED,
        help_text="The comment has been approved by an admin",
    )

    created = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time created",
    )
    modified = models.DateTimeField(
        auto_now=True,
        help_text="Date and time last modified",
    )

    def is_updated(self):
        """
        Return false if review not modified, otherwise return datetime of update.
        """
        if self.modified - self.created > datetime.timedelta(0, UPDATED_COMPARISON_SECONDS):
            # modified datetime is within 10 sec of created datetime
            return self.modified
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

    def _html(self, tag, comment_html_tag='blockquote', datetime_format='DATETIME_FORMAT'):
        """
        Return an html string with review fields wrapped in the provided tag.

        comment_html_tag is the html tag used to wrap the review comment.

        datetime_format is used to output review.created or review.modified. To overide, define an alternative to DATETIME_FORMAT in the settings and pass the string name of the setting here. Or simply override DATETIME_FORMAT everywhere in a project by changing its value in the settings.
        Also available by default for use in this arg is DATE_FORMAT, TIME_FORMAT, or SHORT_DATE_FORMAT, although they will obviously limit the output to only DATE or TIME.
        documented here https://docs.djangoproject.com/en/1.7/ref/settings/#datetime-format
        """
        element_list = []

        user = self.user if not self.anonymous else "Anonymous"
        element = format_html("<{tag} class='review-user'>",tag=tag)
        if hasattr(user, 'get_absolute_url'):
            element += format_html("<a href='{url}'>{user}</a>",
                                user=self.user,
                                url=self.user.get_absolute_url(),)
        else:
            element += format_html("{user}", user=self.user)
        element += format_html("</{tag}>", tag=tag)
        element_list.append(element)

        element = format_html("<{tag} class='review-datetime'>", tag=tag)
        if self.is_updated():
            element += format_html("Updated {datetime}",
                datetime=formats.date_format(
                    self.modified,
                    datetime_format
                )
            )
        else:
            element += format_html("Reviewed {datetime}",
                datetime=formats.date_format(
                    self.created,
                    datetime_format
                )
            )
        element += format_html("</{tag}>", tag=tag)
        element_list.append(element)

        element = format_html("<{tag} class='review-score'>{score}</{tag}>",
                            tag=tag,
                            score=self.score)
        element_list.append(element)

        if self.comment and self.comment_approved:
            element = format_html("<{tag} class='review-comment'>{comment}</{tag}>",
                                tag=comment_html_tag,
                                comment=self.comment)
            element_list.append(element)

        return "\n".join(element_list)

    def as_p(self, **kwargs):
        return format_html(self._html('p', **kwargs))
    as_p.allow_tags = True

    def as_div(self, **kwargs):
        return format_html(self._html('div', **kwargs))
    as_div.allow_tags = True

    # class Meta:
    #     unique_together = ("reviewed_object", "user")
