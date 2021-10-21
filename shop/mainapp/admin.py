from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *

from PIL import Image

class MacbookAdminForm(ModelForm):


    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTIN = (800, 800)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields('image').help_text = mark_safe('<span style="color:red;">Загружайте изображение с минимальным разрешением {}x{}'.format(
            *self.MIN_RESOLUTION
            ))

    def clean_image(self):
        image = self.cleaned_data('image')
        img = Image.open(image)
        max_height, max_width = self.MAX_RESOLUTIN
        min_height, min_width = self.MIN_RESOLUTION
        if img.height > min_height or img.width > min_width:
            raise ValidationError('Разрешение изображения больше максимального!')
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Разрешение изображения меньше минимального!')
        return image



class MacbookAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='Macbook'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class IphoneAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='Iphone'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



admin.site.register(Category)
admin.site.register(Macbook)
admin.site.register(Iphone)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
