from django.db import models
from django.contrib.auth.models import User


def user_profile_path(instance, filename):
    return 'avatar_pics/{0}/{1}'.format(instance.user.id, filename) # create a personal folder for each user under media/avatar_pics folder and copy the pic there


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=user_profile_path, default="default_avatar.png")
    bio = models.TextField(blank=True, help_text="write about yourself")

    def __str__(self):
        return "{} {}".format(self.user, 'Profile')