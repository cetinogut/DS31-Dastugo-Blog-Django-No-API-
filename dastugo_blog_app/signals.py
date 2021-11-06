from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from .models import Post
from .utils import get_random_code


@receiver(pre_save, sender=Post) # before saving do this action first
def pre_save_create_slug(sender, instance, **kwargs): # instance is the Post instance, *kwargs required because we don't know the # of args in the background
    if not instance.slug:
        instance.slug = slugify(
            #instance.title + " " + get_random_code())
            instance.title + " " + instance.blogger.username)

