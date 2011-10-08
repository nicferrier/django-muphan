from django.db import models
from django.contrib.auth.models import User

from datetime import datetime
from django.conf import settings

MIME_MAPPINGS = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/gif": "gif",
    }

class PhotoManager(models.Manager):
    def make_photo(self, user, description, media_type):
        """Use this as a convieniance method to create a record of a photo"""
        photo = self.create(of=user, description=description)
        unique = "1.2"
        timestr = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        url = "http://%(host)s/%(unique)s/%(user)s/%(timestr)s.%(type)s" % {
            "host": "%s.%s" % (unique, settings.MEDIA_DOMAIN),
            "unique": unique,
            "user": user.username,
            "timestr": timestr,
            "type": MIME_MAPPINGS[media_type.lower()]
            }
        photo.url = url
        photo.save()
        return photo

class Photo(models.Model):
    """A photo of a user captured with the camera"""
    of = models.ForeignKey(User)
    url = models.URLField()
    created = models.DateTimeField(default=datetime.utcnow, db_index=True)
    description = models.TextField(blank=True)
    objects = PhotoManager()

# End
