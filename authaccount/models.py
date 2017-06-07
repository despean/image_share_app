from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from sorl.thumbnail import get_thumbnail

# from account import settings

class Profile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL)
  birthday = models.DateField(blank=True, null=True,)
  photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)



  def __str__(self):
    return 'Procfile for user {}'.format(self.user.username)

  def get_thumb(self):
    im = get_thumbnail(self.photo, '190x190', crop='center', quality=99)
    return im.url

class Contact(models.Model):
  user_from = models.ForeignKey(User,
                                related_name='rel_from_set')
  user_to = models.ForeignKey(User,
                              related_name='rel_to_set')
  created = models.DateTimeField(auto_now_add=True,
                                 db_index=True)

  class Meta:
    ordering = ('-created',)

  def __str__(self):
    return '{} follows {}'.format(self.user_from,
                                  self.user_to)


User.add_to_class('following', models.ManyToManyField('self', through=Contact, related_name='followers',
                                                      symmetrical=False))
