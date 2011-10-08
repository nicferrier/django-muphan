import urlparse
import os.path

from datetime import datetime

from django.test import TestCase
from django.test import Client
from django.conf import settings

from django.contrib.auth.models import User
from muphan.models import Photo

def _make_username():
    return "user%s" % datetime.utcnow().strftime("%Y%j%H%M%S%f")

def _make_user():
    username = _make_username()
    user = User.objects.create(
        username = username, 
        )
    user.set_password("secret")
    user.save()
    return username, user

# Just a test file
UPLOAD_FILE=os.path.join(
    os.path.dirname(__file__), 
    "2011-05-02-110615.jpeg"
    )

class UserMediaTest(TestCase):
    def test_make_photo(self):
        """Can we make a photo url"""
        username, user = _make_user()
        photo = Photo.objects.make_photo(user, description="picture of me", media_type="image/jpeg")
        urlparse.urlparse(photo.url)

    def test_upload(self):
        """Can we create an image on the filestore?"""
        username, user = _make_user()
        c = Client()

        with open(UPLOAD_FILE) as photo_fd:
            response = c.post("/umedia/", {
                    "title": "a picture of me I just took",
                    "photo": photo_fd
                    })
            self.assertEquals(302, response.status_code)
            parsed = urlparse.urlparse(response["Location"])
            self.assertEquals(parsed.path, settings.LOGIN_URL)

        # Now login
        loggedin = c.login(username=username, password="secret")
        self.assertTrue(loggedin)
        with open(UPLOAD_FILE) as photo_fd:
            response = c.post("/umedia/", {
                    "title": "a picture of me I just took",
                    "photo": photo_fd
                    })
            self.assertEquals(201, response.status_code)

            # What's the url
            parsed = urlparse.urlparse(response["Location"])

            # Check we've got the correct file type
            self.assertEquals(os.path.splitext(parsed.path)[1][1:], "jpg")
            
            # Check that is starts with something under the MEDIA_DOMAIN
            self.assertEquals(
                settings.MEDIA_DOMAIN, 
                ".".join(parsed.netloc.split(".")[2:])
                )

# End
