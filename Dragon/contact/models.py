from django.db import models
from django.utils.translation import gettext_lazy as _ 

from modelcluster.models import ParentalKey

from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField

FORM_FIELD_CHOICES = (
    ("singleline", _("Single line text")),
    ("multiline", _("Multi-line text")),
    ("email", _("Email")),
    ("url", _("URL")),
)

class CustomAbstractFormField(AbstractFormField):
    field_type = models.CharField(
        verbose_name="Field Type",
        max_length=16,
        choices=FORM_FIELD_CHOICES,
    )


class FormField(AbstractFormField):
    page = ParentalKey(
        "ContactPage",
        on_delete=models.CASCADE,
        related_name='form_fields'
    )

class ContactPage(AbstractEmailForm):

    template = "contact/contact_page.html"
    landing_page_template = "contact/contact_page_landing.html"
    subpage_types = []
    max_count = 1

    intro = RichTextField(blank=True, features=["bold", "link", "ol", "ul"])
    thank_you_text = RichTextField(
        blank=True,
        features=["bold","link","ol","ul"]
    )
    map_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        help_text='Image will be cropped to 580px by 355px',
        related_name='+',
    ) 
    map_url = models.URLField(
        blank=True,
        help_text='Optional. If you provide a link here the map image will become a link',
    ) 

    content_panels = AbstractEmailForm.content_panels + [ 
        FieldPanel("intro"),
        FieldPanel("map_image"),
        FieldPanel("map_url"),
        InlinePanel("form_fields", label='Form Fields'),
        FieldPanel("thank_you_text"),
        FieldPanel("from_address"),
        FieldPanel("to_address"),
        FieldPanel("subject"),
    ]