from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db.models import get_models
from .models import Review



def model_name(obj):
    """Return name of reviewed model."""
    return obj.content_type.name.title()
model_name.short_description = "Reviewed model"



def reviewed_object_linked(obj):
    """Return a direct link to the reviewed object."""
    url = reverse(
        'admin:{app_label}_{model_name}_change'.format(
            app_label=obj.content_type.app_label,
            model_name=obj.content_type.model,
        ),
        args=(obj.reviewed_object.id,)
    )
    url = "<a href='%s'>%s</a>" % (url, obj.reviewed_object)
    return url
reviewed_object_linked.allow_tags = True
reviewed_object_linked.short_description = "Reviewed object"



class ReviewedModelListFilter(admin.SimpleListFilter):
    title = ('Reviewed model')
    parameter_name = 'reviewed_model'

    def lookups(self, request, model_admin):
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

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(content_type__name=self.value())



class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        model_name,
        reviewed_object_linked,
        'user',
        'score',
        'comment',
        'comment_approved',
    ]
    list_filter = [
        ReviewedModelListFilter,
        'comment_approved',
        'score',
    ]
    readonly_fields = [
        model_name,
        reviewed_object_linked,
        'user',
        'score',
        'created',
        'is_updated',
    ]
    fields = readonly_fields + [
        'comment',
        'anonymous',
        'comment_approved',
    ]
admin.site.register(Review, ReviewAdmin)
