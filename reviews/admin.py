from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils import formats

from .models import Review
from .utils import get_reviewable_model_classes



def reviewed_model_linked(obj):
    """Return a direct link to the reviewed model admin.

    obj is a Review object."""
    url = reverse(
        'admin:{app_label}_{model_name}_changelist'.format(
            app_label=obj.content_type.app_label,
            model_name=obj.content_type.model,
        )
    )
    return "{text} (<a href='{url}'>link</a>)".format(text=obj.content_type.name.title(),
                                                      url=url)
reviewed_model_linked.allow_tags = True
reviewed_model_linked.short_description = "Reviewed model"



def reviewed_object_linked(obj):
    """Return a direct link to the reviewed object admin.

    obj is a Review object."""
    url = reverse(
        'admin:{app_label}_{model_name}_change'.format(
            app_label=obj.content_type.app_label,
            model_name=obj.content_type.model,
        ),
        args=(obj.reviewed_object.id,)
    )
    return "{text} (<a href='{url}'>link</a>)".format(text=obj.reviewed_object,
                                                      url=url)
reviewed_object_linked.allow_tags = True
reviewed_object_linked.short_description = "Reviewed object"



def review_user_linked(obj):
    """Return a direct link to the reviewer admin.

    obj is a Review object."""
    url = reverse(
        'admin:{app_label}_{model_name}_change'.format(
            app_label=ContentType.objects.get_for_model(obj.user.__class__).app_label,
            model_name=ContentType.objects.get_for_model(obj.user.__class__).model,
        ),
        # ContentType.objects.get_for_model(user.__class__).app_label
        args=(obj.user.id,)
    )
    return "{text} (<a href='{url}'>link</a>)".format(text=obj.user,url=url)
review_user_linked.allow_tags = True
review_user_linked.short_description = "Reviewer"



def get_reviewable_models():
    """Generate list of tuple pairs for custom filter.

    Example output:

    [(u'seller', u'Seller'), (u'product', u'Product')]"""
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
        reviewed_model_linked,
        reviewed_object_linked,
        review_user_linked,
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
        reviewed_model_linked,
        reviewed_object_linked,
        review_user_linked,
        'score',
        'created',
        'modified',
    ]
    fields = readonly_fields + [
        'comment',
        'anonymous',
        'comment_approved',
    ]

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults.update({
                'fields': [
                    'content_type',
                    'object_id',
                    'user',
                    'score',
                    'comment',
                    'anonymous',
                    'comment_approved',
                ],
            })
        defaults.update(kwargs)
        return super(ReviewAdmin, self).get_form(request, obj, **defaults)

admin.site.register(Review, ReviewAdmin)
