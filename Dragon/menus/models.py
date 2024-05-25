from django.db import models
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from wagtail.models import Orderable
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.panels import FieldPanel, PageChooserPanel, InlinePanel
# Clusterable Model

class MenuItem(Orderable):
    link_title = models.CharField(blank=True, max_length=50)
    link_url = models.CharField(max_length=500, blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.CASCADE,
    )

    open_in_new_tab = models.BooleanField(default=False, blank=True)

    panels = [
        FieldPanel("link_title"),
        FieldPanel("link_url"),
        PageChooserPanel("link_page"),
        FieldPanel("open_in_new_tab")
    ]

    page = ParentalKey("Menu", related_name="menu_items")

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return '#'
    

    @property
    def title(self):
        if self.link_page and not self.link_title:
            return self.link_page.title
        elif self.link_title:
            return self.link_title
        return "Missing Title"

class Menu(ClusterableModel):

    title = models.CharField(max_length=100)
    slug = models.CharField(
        verbose_name = "Slug", 
        editable = True,
        max_length = 40
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("slug"),
        InlinePanel("menu_items", label="Menu Item")
    ]

    def __str__(self):
        return self.title
    
    def save(self, **kwargs):

        key = make_template_fragment_key("site_header")
        cache.delete(key)

        key = make_template_fragment_key("site_footer")
        cache.delete(key)

        return super().save(**kwargs)