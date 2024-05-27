from django.contrib import admin
from .models import TypeObject, Object


class TypeObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'color')
    search_fields = ('name',)
    list_filter = ('parent',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'parent', 'color')
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['color'].widget.attrs['type'] = 'color'  # Включаем выбор цвета
        return form


admin.site.register(TypeObject, TypeObjectAdmin)

admin.site.register(Object)
