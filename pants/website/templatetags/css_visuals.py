from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='css_progressbar')
def css_progressbar(value, maxvalue=100, fgclass='w3-deep-purple', bgclass='w3-black'):
   """
   Creates a w3css-style div progressbar with width = value/maxvalue %.
   The value (recieved from filter) is displayed on the element.
   Maxvalue should be specified if value is not already out of 100.

   If value (or maxvalue) is not convertable to float, will return the
   value unfiltered.
   """
   width = 100    # maximum % cap
   try:
      if value < maxvalue:
         width = int(float(100) * float(value) / float(maxvalue))
   except TypeError:
      return value  # If not a float, allow the value to be shown unaltered

   # NB: Have to use mark_safe as introducing new HTML markup. Any
   # recieved data has been converted to a float so should be safe
   return mark_safe(
      '<div class="%s"><div class="%s" style="width:%d%%">%s</div></div>'%(
         bgclass,
         fgclass,
         width,
         value,
      )
   )

