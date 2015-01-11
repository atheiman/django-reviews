from django.contrib import admin
from django.contrib.auth.models import User

from .models import Product#, Profile



# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False
#     verbose_name_plural = 'profile'

# class UserAdmin(UserAdmin):
#     inlines = (ProfileInline,)

# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)



class ProductAdmin(admin.ModelAdmin):
    pass
admin.site.register(Product, ProductAdmin)
