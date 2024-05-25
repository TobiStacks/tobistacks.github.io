from django.db import models
from django.core.exceptions import ValidationError

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, PageChooserPanel


# Create your models here.
class ServiceListingPage(Page):
    # specifies service listing page to this html v
    parent_page_types = ["home.HomePage"] 
    subpage_types = ["services.ServicePage"]

    max_count = 1 # there can only be 1 service listing page
    template = "services/service_listing_page.html"
    subtitle = models.TextField(
        blank=True, # does not need to be added in ( {{page.}} ) into the html file
        max_length=500,
    )

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['services'] = ServicePage.objects.live().public() # grabs all live and public pages into services variable
        # space_company = 'X'
        # import pudb; pu.db()
        return context
    
class ServicePage(Page):
    # secifies service page to this html v
    parent_page_types = ["services.ServiceListingPage"] 
    # subpage_types = []
    template = "services/service_page.html"
    
    description = models.TextField( blank=True, max_length=500 )

    internal_page = models.ForeignKey(
        'wagtailcore.Page',
        blank=True,
        null=True,
        related_name='+',
        help_text='Select an internal Wagtail page',
        on_delete=models.SET_NULL
    )
    external_page = models.URLField(blank=True)
    button_text = models.CharField(blank=True, max_length=50)
    service_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        help_text='This image will be used on Service Listing Page and will be cropped to 570px by 370px on this page',
        related_name='+',
    )

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        PageChooserPanel("internal_page"),
        FieldPanel("external_page"),
        FieldPanel("button_text"),
        FieldPanel("service_image")
    ]

    # filter for internal/external page errors
    def clean(self):
        super().clean() # allows content to safely be added into database, prevents SQL injections

        if self.internal_page and self.external_page:
            # if both fields are filled out
            raise ValidationError({
                'internal_page': ValidationError("Please only select a page OR enter an external URL"),
                'external_page': ValidationError("Please only select a page OR enter an external URL")
            })
        
        if not self.internal_page and not self.external_page:
            # if both fields are missing
            raise ValidationError({
                'internal_page': ValidationError("You must always select a page OR enter an external URL"),
                'external_page': ValidationError("You must always select a page OR enter an external URL")
            })