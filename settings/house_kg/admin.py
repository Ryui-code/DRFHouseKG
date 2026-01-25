from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from modeltranslation.admin import TranslationAdmin

@admin.register(UserProfile)
class CustomUserAdmin(UserAdmin):
    fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password', 'email', 'status', 'phone_number', 'registered_date',
            ),
        }),
    ]
    readonly_fields = ['registered_date']

admin.register(Property)
class PropertyAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

admin.register(Review)
class ReviewAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
