from django import forms
from .models import Image
from io import BytesIO
from urllib2 import urlopen
# from urllib import request
from django.core.files.base import ContentFile, File
from django.core.files.temp import NamedTemporaryFile
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
  class Meta:
    model = Image
    fields = ('title', 'url', 'description')
    widgets = {
      'url': forms.HiddenInput,
      'title': forms.TextInput(attrs={'class': 'form-control'}),
      'description': forms.Textarea(attrs={'class': 'form-control'})
    }

  def clean_url(self):
    url = self.cleaned_data['url']

    valid_extensions = ['jpg', 'jpeg', 'png']
    extension = url.rsplit('.', 1)[1].lower()
    if extension not in valid_extensions:
      raise forms.ValidationError('The given URL does not ' \
                                  'match valid image extensions.')
    return url

  def save(self, force_insert=False, force_update=False, commit=True):
    img_temp = NamedTemporaryFile()
    Image = super(ImageCreateForm, self).save(commit=False)
    image_url = self.cleaned_data['url']
    image_name = '{}.{}'.format(slugify(Image.title),
                                image_url.rsplit('.', 1)[1].lower())
    # download image from the given URL
    # response = request.urlopen(image_url)
    response = urlopen(image_url)
    img_temp.write(response.read())
    img_temp.flush()
    Image.image.save(image_name, File(img_temp),
                     save=False)
    if commit:
      Image.save()
    return Image
