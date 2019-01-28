from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# TODO: This is not CSS and should probably go elsewhere
# TODO: Replace with just 'xx%' when both are the same or one is not specified
# TODO: Combine this with progressbar to create an all-in-one tag that
#       creates a table cell with content and CSS
# TODO: Then use that to create a tag that loops over a specified set
#       of dict keys and creates the table cells....
@register.simple_tag
def percminmax(value, min_target, max_target):
   """
   Returns a string like 'x%-y%' where x is the value/min_target% and y is
   the value/max_target%.

   E.g. 30|perc_min_max:100 150 returns "30%-20%".

   Returns an empty string in place of results of any arguments which
   cannot be converted to a float.

   You can just specify the min/max the other way around if you
   prefer the lower percentage to be on the left (it defaults to the
   other way to emphasise that a lower percentage has a higher base).
   """
   try:
      num = float(value)*100
   except:
      return ''

   try:
      minp = int(num / float(min_target))
   except:     # divide by zero or cannot convert to float
      minp=''

   try:
      maxp = int(num / float(max_target))
   except:
      maxp=''

   return '%s%%-%s%%'%(minp,maxp)

@register.filter
def css_progressbar(value, maxvalue=100, fgclass='w3-deep-purple', bgclass='w3-black'):
   """
   Creates a w3css-style div progressbar with width = value/maxvalue %.
   The value (recieved from filter) is displayed on the element.
   Maxvalue should be specified if value is not already out of 100.

   If value is not convertable to float, will return the value unfiltered.
   """
   if not maxvalue:
      maxvalue=100   # If maxvalue is passed explicitly as None e.g. for targets

   try:
      if value < maxvalue:
         width = int(float(100) * float(value) / float(maxvalue))
      else:
         width=100   # Cap % at maximum
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


# FIXME unused...
# TODO: This is more general than CSS visuals and should really go elsewhere
@register.filter
def divide(num, den):
   """
   Divide num by den in a template, returns 'NaN' if denominator is 0.
   """
   return (float(num) / float(den)) if float(den)!=0 else 'NaN'

