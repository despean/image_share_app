from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='class_placeholder')
def cssplaceholder(field, args):
  value = args.split(',')
  return field.as_widget(attrs={"class": value[0].strip(), 'placeholder': value[1].strip().capitalize()})


@register.filter
def addstr(arg1, arg2):
  """concatenate arg1 & arg2"""
  return str(arg1) + str(arg2)


@register.filter(name='Capitalize')
def capitalise_text(text):
  words = text.split(' ')
  out = ''
  for w in words:
    f = w[0].upper()
    word = '' + f + '' + w[1:]
    out += word + ' '
  return out

@register.filter(name='addclass')
def cssplaceholder(field, args):
  return field.as_widget(attrs={"class": args })
