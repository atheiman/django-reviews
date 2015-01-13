from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from .models import Review
from .utils import get_reviewable_model_classes



def model_name(obj):
    """Return name of reviewed model.

    obj is a Review object."""
    return obj.content_type.name.title()
model_name.short_description = "Reviewed model"



def reviewed_object_linked(obj):
    """Return a direct link to the reviewed object.

    obj is a Review object."""
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



def get_reviewable_models():
    """Generate list of tuple pairs for custom filter.

    Example output:

    [(u'user', u'User'), (u'product', u'Product')]"""
    model_classes = get_reviewable_model_classes()
    reviewable_models = []
    for klass in model_classes:
        reviewable_models.append(
            (
                ContentType.objects.get_for_model(klass).name,
                ContentType.objects.get_for_model(klass).name.title(),
            )
        )
    return reviewable_models



class ReviewedModelListFilter(admin.SimpleListFilter):
    title = ('Reviewed model')
    parameter_name = 'reviewed_model'

    def lookups(self, request, model_admin):
        if len(get_reviewable_models()) < 2:
            return None
        else:
            return get_reviewable_models()

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
