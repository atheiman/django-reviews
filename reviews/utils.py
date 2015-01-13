from django.db.models import get_models

def get_reviewable_models():
    models = get_models(include_auto_created=True)
    reviewable_models = []
    for model in models:
        if hasattr(model, 'reviews'):
            reviewable_models.append(
                (
                    ContentType.objects.get_for_model(model).name,
                    ContentType.objects.get_for_model(model).name.title(),
                )
            )

    return reviewable_models
