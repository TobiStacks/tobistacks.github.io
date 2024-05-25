from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.admin.panels import FieldPanel, PageChooserPanel
from streams import blocks

class HomePage(Page):

    # Setting Field Options that are available whenever editing the homepage
    
    parent_page_types = ["wagtailcore.Page"] # there can't be another home page
    max_count = 1 # there can only be 1 home page
    subpage_types = ["flex.FlexPage", "services.ServiceListingPage", "contact.ContactPage"]

    lead_text = models.CharField(max_length=140, # models. -> django module
                                 blank=True,
                                 help_text='Subheading text under the banner title',
    )

    button = models.ForeignKey( # Links to another page (will be on top right corner displaying Page name)
        'wagtailcore.Page',
        blank=True,
        null=True,
        related_name='+',
        help_text='Select an optional page to link to',
        on_delete=models.SET_NULL, # when linked page is deleted
    )

    button_text = models.CharField( # CharField since its for text, ForeignKey for objects like a button or img
        max_length=50,
        default='Read More',
        blank=False,
        help_text='Button text'
    )

    banner_background_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False, # form has to have a value or text
        null=True, # can have nothing in database
        related_name='+',
        help_text='The banner background image',
        on_delete=models.SET_NULL,
    )
    
    # body of homepage consists of 
    body = StreamField([ 
        ("title", blocks.TitleBlock()),
        ("cards", blocks.CardsBlock()),
        ("image_and_text", blocks.ImageAndTextBlock()),
        ("cta", blocks.CallToActionBlock()),
        ("testimonial", SnippetChooserBlock(
            target_model='testimonials.Testimonial',
            template="streams/testimonial_block.html",
        )),
        # ("pricing_table", blocks.PricingTableBlock()), <- feature is buggy, wagtail built in but not working
    ], null=True, blank=True, use_json_field=True)

    content_panels = Page.content_panels + [ # updates page
        FieldPanel("lead_text"),
        PageChooserPanel('button'),
        FieldPanel("button_text"),
        FieldPanel("banner_background_image"),
        FieldPanel("body"),
    ]

    def save(self, *args, **kwargs):

        key = make_template_fragment_key(
            "home_page_streams",
            [self.id],
        )
        cache.delete(key)

        return super().save(*args, **kwargs)

# to add updated models to server -> python manage.py makemigrations
#                                    python manage.py migrate