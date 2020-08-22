from django.contrib import admin

# Register your models here.
from .models import Element, Parentship, Attribute

class ElementModelAdmin(admin.ModelAdmin):
    list_display = ["tag"]
    list_display_links = ["tag"]
    list_editable = []
    list_filter = ["tag"]

    search_fields = ["tag","text","tail"]
    class Meta:
        model = Element

class ParentshipModelAdmin(admin.ModelAdmin):
    list_display = ["parentElement", "currentElement"]
    list_display_links = ["parentElement"]
    list_editable = []
    list_filter = ["parentElement", "currentElement"]

    search_fields = ["parentElement", "currentElement"]
    class Meta:
        model = Parentship

class AttributeModelAdmin(admin.ModelAdmin):
    list_display = ["element", "key"]
    list_display_links = ["key"]
    list_editable = []
    list_filter = ["element", "key"]

    search_fields = ["element", "key"]
    class Meta:
        model = Attribute


admin.site.register(Element, ElementModelAdmin)
admin.site.register(Parentship, ParentshipModelAdmin)
admin.site.register(Attribute, AttributeModelAdmin)