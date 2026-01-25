from modeltranslation.translator import TranslationOptions, register
from .models import Property, Review

@register(Property)
class PropertyTranslationOptions(TranslationOptions):
    fields = ('description',)

@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ('comment',)