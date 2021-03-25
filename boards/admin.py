from django.contrib import admin

# Register your models here.

from .models import Essay, Answer

class EssayAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Essay, EssayAdmin)
admin.site.register(Answer)