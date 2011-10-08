
from os import makedirs
from os.path import join 
from os.path import dirname
from urlparse import urlparse

from django import forms
from django.http import HttpResponse
from django.http import Http404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from djangoxslt.xslt import render_to_response
from muphan.models import Photo


HTTP_CREATED = 201

def handle(photo, content_type, uploaded_file):
    """This sends data in uploaded_file to the the specified photo url.

    FIXME Right now this is just file storage. But it will have to use
    HTTP to send the file to whatever server maps to the generated
    shard.
    """
    url = urlparse(photo.url)
    path = url.path
    filename = join(settings.MEDIA_ROOT, path[1:] if path[0] == "/" else path)
    try:
        makedirs(dirname(filename))
    except OSError:
        # We should check this is error 17
        pass

    with open(filename, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

class Upload(forms.Form):
    title = forms.CharField(max_length=150)
    photo  = forms.FileField()

@login_required
def upload_photo(request):
    if request.method == "POST":
        form = Upload(request.POST, request.FILES)
        if form.is_valid():
            content_type = form.files["photo"].content_type
            photo = Photo.objects.make_photo(
                request.user, 
                media_type = content_type,
                description = form["title"]
                )
            file_data = request.FILES["photo"]
            handle(photo, content_type, file_data)
            response = HttpResponse(status=HTTP_CREATED)
            response["Location"] = photo.url
            return response

    form = Upload()
    return HttpResponse()

def photo_list(request, username):
    pass

def photo(request, username, dbid):
    try:
        photo = Photo.objects.get(id=dbid)
    except Photo.DoesNotExist:
        raise Http404
    else:
        return render_to_response("photo.xslt", RequestContext(request, {
                    "photo": photo,
                    }))

# End
