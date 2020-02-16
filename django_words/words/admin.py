from django.contrib import admin

from .models import Word, Definition


class DefinitionInine(admin.StackedInline):
    model = Definition
    extra = 3


class WordAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["word_text"]}),
        ("Date information", {"fields": ["added_date"], "classes": ["collapse"]}),
    ]
    inlines = [DefinitionInine]


admin.site.register(Word, WordAdmin)
