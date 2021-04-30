from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .admin_forms import MyUserCreationForm, MyUserChangeForm
from .models import Profile

User = get_user_model()


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'admin', 'staff', 'joined', 'profile')
    list_filter = ('admin', 'staff',  'joined')
    fieldsets = (
            ('Main', {'fields': ('email', 'password')}),
            ('Permissions', {'fields': ('admin', 'staff', 'is_active')}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('joined',)


admin.site.register(User, MyUserAdmin)
admin.site.register(Profile)



