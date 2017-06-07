from requests import request, HTTPError

from django.core.files.base import ContentFile
from authaccount.models import Profile


def get_profile_picture(backend, user, response, details, *args, **kwargs):
  url = None

  profile = Profile.objects.get_or_create(user=user)[0]

  if backend.name == 'facebook':
    username = details.get('first_name') + '' + details.get('last_name')
    user.username = username
    user.save()
    print(response)
    profile = Profile.objects.get_or_create(user=user)[0]
    print(details.get('birthday'))
    url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])

    try:
      response = request('GET', url, params={'type': 'large'})
      response.raise_for_status()
    except HTTPError:
      pass
    else:
      profile.photo.save('{0}_social.jpg'.format(user.username),
                         ContentFile(response.content))

  elif backend.name == "twitter":
    if response['profile_image_url'] != '':

      avatar_url = response.get('profile_image_url_https')
      if avatar_url:
        avatar_url = avatar_url.replace('_normal.', '_bigger.')
        try:
          response = request('GET', avatar_url, params={'type': 'large'})
          response.raise_for_status()
        except HTTPError:
          pass
        else:
          profile.photo.save('{0}_social.jpg'.format(user.username),
                             ContentFile(response.content))

  elif backend.name == "google-oauth2":
    if response['image'].get('url') is not None:
      try:
        response = request('GET', response['image'].get('url'), params={'type': 'large'})
        response.raise_for_status()
      except HTTPError:
        pass
      else:
        profile.photo.save('{0}_social.jpg'.format(user.username),
                           ContentFile(response.content))

  profile.save()
