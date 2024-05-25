'''
Stream Fields work as blocks and bars of content you see as you scroll down
on the page. Its great because these blocks can easily be moved up or down
without tedious reformatting
'''

from django import forms
from wagtail import blocks
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.images.blocks import ImageChooserBlock
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

class TitleBlock(blocks.StructBlock):
    
    text = blocks.CharBlock( # Display title of page
        required=True, # block must display
        help_text='Text to display',
    )

    class Meta: 
        template = "streams/title_block.html"
        icon = "edit"
        label = "Title"
        help_text = "Centered text to display on page"

class LinkValue(blocks.StructValue):

    # checks if there is an internal page or external link within a link, else returns nothing
    def url(self):
        internal_page = self.get("internal_page") # gets link value from link class
        external_link = self.get("external_link")
        
        if internal_page:
            return internal_page.url # goes to internal page
        elif external_link:
            return external_link
        return ""


class Link(blocks.StructBlock): # Creates a struct block for links
    link_text = blocks.CharBlock(
        max_length=50, 
        default="More Details",
    )
    internal_page = blocks.PageChooserBlock( # the link can direct to another page within the site directory (optional)
        required=False,
    )
    external_link = blocks.URLBlock( # the link can direct to a page outside the site directory (optional)
        required=False,
    )

    class Meta: # ties in LinkValue class with url checker
        value_class = LinkValue # -> either " ", internal_page.url, or external_link

    def clean(self, value):
        internal_page = value.get("internal_page")
        external_link = value.get("external_link")
        errors = {}
        
        if internal_page and external_link:
            errors["internal_page"] = ErrorList(["error over here"])
            errors["external_link"] = ErrorList(["error over here"])

        elif not internal_page and not external_link:
            errors["internal_page"] = ErrorList(["Please select a page or enter a URL for one of these options"])
            errors["external_link"] = ErrorList(["Please select a page or enter a URL for one of these options"])

        if errors:
            raise ValidationError("Validation error in your link", params=errors)
        
        return super().clean(value)

class Card(blocks.StructBlock): # Creates the block format for a card (repeating type) StreamField and passes in a Struct block type
    title = blocks.CharBlock(
        max_length=100, 
        help_text="Bold title text for this card. Max length of 100 characters.",
    )
    text = blocks.TextBlock(
        max_length=255, 
        help_text="Optional text for this card. Max length is 255 characters", 
        required=False,
        )
    image = ImageChooserBlock(
        help_text="Image will be auto-cropped to 570x370px",
    )
    link = Link(help_text="Enter a link or select a page") # brings in link class instead of having link as a struct block. Will also have a nested internal page and external link options


class CardsBlock(blocks.StructBlock):
    cards = blocks.ListBlock( # Creates a list of card struct blocks via the ListBlock method
        Card()
    )

    class Meta:
        template = "streams/cards_block.html" # links this class to the html interface
        icon = "image"
        label = "Standard Cards"

class RadioSelectBlock(blocks.ChoiceBlock): # inherits the same as image alignment
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field.widget = forms.RadioSelect(
            choices = self.field.widget.choices
        )

class ImageAndTextBlock(blocks.StructBlock): # gives the image/text option choices when adding new block

    image = ImageChooserBlock(help_text='Image auto-cropped to 786x552px')
    image_alignment = RadioSelectBlock( # instead of blocks.ChoiceBlock, you can use RSB so it shows up as a radio option
        choices = (  # kwargs being passed with __init__ constructor from RSB
            ("left", "Image to the left"), # ([template display], [what you see on screen])
            ("right", "Image to the right"),
        ), 
        default='left',
        help_text='Image on Left w/ rightmost text or vice versa',
    )
    title = blocks.CharBlock(max_length=60, help_text='Max length of 60 characters')
    text = blocks.CharBlock(max_length=140, required=False)
    link = Link()
      

    class Meta:
        template = 'streams/image_and_text_block.html'
        icon = "image"
        label = "Image & Text"

class CallToActionBlock(blocks.StructBlock):

    title = blocks.CharBlock(max_length=200, help_text='Max length of 200 characters.')
    link = Link()

    class Meta:
        template = "streams/call_to_action_block.html"
        icon = "plus"
        label = "Call to Action"

class RichTextWithTitleBlock(blocks.StructBlock):
    
    title = blocks.CharBlock(max_length=50)
    context = blocks.RichTextBlock(features=[])

    class Meta:
        template = "streams/simple_richtext_block.html"

class PricingTableBlock(TableBlock):
    """Pricing table block."""

    class Meta:
        template = "streams/pricing_table_block.html"
        label = "Pricing Table"
        icon = "table"
        help_text = "Your pricing tables should always have 4 columns"