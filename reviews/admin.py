from django.contrib import admin
from django.core.urlresolvers import reverse
from .models import Review



def model_name(obj):
    """Return name of related model."""
    return obj.content_type.name.title()
model_name.short_description = "Related model"



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
