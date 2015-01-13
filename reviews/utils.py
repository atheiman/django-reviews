from django.contrib.contenttypes.models import ContentType

from .defaults import REVIEWABLE_MODELS



def get_reviewable_model_classes():
    """Return list of classes generated from setting REVIEWABLE_MODELS"""
    reviewable_model_classes = []
    if not REVIEWABLE_MODELS:
        return []
    for model in REVIEWABLE_MODELS:
        reviewable_model_classes.append(
            ContentType.objects.get(app_label=model['app_label'],
                                    model=model['model']).model_class()
        )

    return reviewable_model_classes
