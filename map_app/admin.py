from django.contrib import admin
from .models import TypeObject, Category, Object, CustomUser
from django.contrib.auth.admin import UserAdmin


class TypeObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'color')
    search_fields = ('name',)
    list_filter = ('category',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'category', 'color')
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['color'].widget.attrs['type'] = 'color'  # Включаем выбор цвета
        return form


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'auto_publish')
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'color', 'auto_publish')
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['color'].widget.attrs['type'] = 'color'  # Включаем выбор цвета
        return form


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'profession', 'workplace', 'position')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone', 'profession', 'workplace', 'position')}),
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(TypeObject, TypeObjectAdmin)
admin.site.register(Object)
admin.site.register(CustomUser, CustomUserAdmin)
