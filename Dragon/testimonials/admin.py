from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register
)

from .models import Testimonial

# Register your models here.

@modeladmin_register
class TestimonialAdmin(ModelAdmin):
    # Testimonial Admin

    model = Testimonial
    menu_label = "Testimonials"
    menu_icon = "placeholder"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("quote", "attribution") #organizes the quote and attribution field so its not just text 
    search_fields = ("quote", "attribution") 

