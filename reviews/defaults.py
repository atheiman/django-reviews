from django.conf import settings
from django.core.checks import register, Error, Warning
from django.db.models import Q



DJANGO_REVIEWS = getattr(settings, "DJANGO_REVIEWS", {})

MAX_SCORE = DJANGO_REVIEWS.get('MAX_SCORE', 5)
MIN_SCORE = DJANGO_REVIEWS.get('MIN_SCORE', 1)
SCORE_CHOICES = DJANGO_REVIEWS.get('SCORE_CHOICES', zip(
    range(MIN_SCORE, MAX_SCORE + 1),
    range(MIN_SCORE, MAX_SCORE + 1)
))
MAX_COMMENT_LENGTH = DJANGO_REVIEWS.get('MAX_COMMENT_LENGTH', 1000)
UPDATED_COMPARISON_SECONDS = DJANGO_REVIEWS.get('UPDATED_COMPARISON_SECONDS', 10)
AVG_SCORE_DIGITS = DJANGO_REVIEWS.get('AVG_SCORE_DIGITS', 2)
COMMENT_REQUIRED = DJANGO_REVIEWS.get('COMMENT_REQUIRED', False)
COMMENT_APPROVAL_REQUIRED = DJANGO_REVIEWS.get('COMMENT_APPROVAL_REQUIRED', False)
REVIEWABLE_MODELS = DJANGO_REVIEWS.get('REVIEWABLE_MODELS', [])


@register('reviews')
def django_reviews_settings_check(app_configs, **kwargs):
    errors = []
    msg = "DJANGO_REVIEWS settings: "

    if MAX_SCORE <= MIN_SCORE:
        errors.append(
            Error(
                msg + 'MAX_SCORE less than or equal to MIN_SCORE',
                'Adjust settings.DJANGO_REVIEWS dict so that MAX_SCORE > MIN_SCORE',
                obj=settings,
                id='reviews.E001',
            )
        )

    if not REVIEWABLE_MODELS:
        errors.append(
            Warning(
                msg + 'Missing recommended setting: REVIEWABLE_MODELS',
                obj=settings,
                id='reviews.W001',
            )
        )

    if REVIEWABLE_MODELS:
        for reviewable in REVIEWABLE_MODELS:
            if ('app_label' not in reviewable) or ('model' not in reviewable):
                errors.append(
                    Error(
                        msg + "REVIEWABLE_MODELS elements must have keys 'app_label' and 'model'",
                        obj=settings,
                        id='reviews.E002',
                    )
                )

    return errors

