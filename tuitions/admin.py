from django.contrib import admin
from . import models
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('classes',)}
    list_display = ['classes', 'slug']


admin.site.register(models.Tution, CategoryAdmin)
admin.site.register(models.TutionDetails)
admin.site.register(models.TuitionApplication)
admin.site.register(models.ContactUs)
admin.site.register(models.Comment)
