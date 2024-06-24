# admin.py
from django.contrib import admin
from .models import TypeObject, Category, Object, CustomUser
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.utils.translation import gettext_lazy as _
from .forms import CategoryForm

class TypeObjectInline(admin.TabularInline):
    model = TypeObject
    extra = 1

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
    form = CategoryForm
    list_display = ('name', 'description', 'auto_publish', 'icon')
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'color', 'icon', 'auto_publish')
        }),
    )
    inlines = [TypeObjectInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['color'].widget.attrs['type'] = 'color'  # Включаем выбор цвета
        return form

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone', 'profession', 'workplace', 'position')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

class ObjectResource(resources.ModelResource):
    class Meta:
        model = Object
        fields = ('id', 'name', 'description', 'latitude', 'longitude', 'type_object__name', 'user__email', 'is_published')
        export_order = ('id', 'name', 'description', 'latitude', 'longitude', 'type_object__name', 'user__email', 'is_published')

class ObjectAdmin(ImportExportModelAdmin):
    resource_class = ObjectResource
    list_display = ('name', 'description', 'latitude', 'longitude', 'type_object', 'user', 'is_published')
    list_filter = ('type_object', 'user', 'is_published')
    search_fields = ('name', 'description', 'type_object__name', 'user__email')

admin.site.register(Category, CategoryAdmin)
admin.site.register(TypeObject, TypeObjectAdmin)
admin.site.register(Object, ObjectAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
