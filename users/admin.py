from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _

from users.models import User, TokenGenerator


class UserAdmin(BaseUserAdmin):
    """ Modified the UserAdmin to remove the username field
    """
    ordering = ('email',)

    list_display = ('email', 'is_staff',)
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_confirmed')}),
        (_('Important dates'), {'fields': ('date_joined','school')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',),
        }),
    )

admin.site.register(User, UserAdmin)
admin.site.register(TokenGenerator)