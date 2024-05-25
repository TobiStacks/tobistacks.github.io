from django.db import models

from wagtail.snippets.models import register_snippet

@register_snippet
# Create your models here.
class Testimonial(models.Model):
    # Testimonial Class

    quote = models.TextField(
        max_length=500, 
        blank=False, 
        null=False
    )
    
    attribution = models.CharField(
        max_length=50, 
        blank=False, 
        null=False
    )

    def __str__(self):
        # String representation of this class
    
        return f"{self.quote} by {self.attribution}"
    
    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"