from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Company, Request, Query

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'is_admin', 'is_company', 'is_active')
    list_filter = ('is_admin', 'is_company', 'is_active')
    ordering = ('email',)
    search_fields = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin', 'is_company')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('user', 'approved')
    list_filter = ('approved',)
    search_fields = ('user__email',)
    actions = ['approve_companies']

    def approve_companies(self, request, queryset):
        queryset.update(approved=True)
    approve_companies.short_description = "Approve selected companies"

admin.site.register(Request)
admin.site.register(Query)
