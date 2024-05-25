from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.admin.panels import FieldPanel, PageChooserPanel
from wagtail.admin import blocks as wagtail_blocks
from wagtail.images.blocks import ImageChooserBlock
from streams import blocks

class FlexPage(Page):
    
    parent_page_types = ["home.HomePage", "flex.FlexPage"]
    body = StreamField([
        ("title", blocks.TitleBlock()),
        ("cards", blocks.CardsBlock()),
        ("image_and_text", blocks.ImageAndTextBlock()),
        ("cta", blocks.CallToActionBlock()),
        ("testimonial", SnippetChooserBlock(
            target_model='testimonials.Testimonial',
            template="streams/testimonial_block.html"
        )),
        ("richtext", wagtail_blocks.RichTextBlock(
            template = "streams/simple_richtext_block.html",
            # features = ["bold", "italic", "ol", "ul", "link", "h2", "h3"]
        )),
        ("large_image", blocks.ImageChooserBlock(
            help_text='This image will be cropped to 1200px by 775px',
            template="streams/large_image_block.html",
        )),
        # ("richtext_with_title", blocks.RichTextWithTitleBlock()),
    ], null=True, blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Flex (misc) page"
        verbose_name_plural = "Flex (misc) pages"