from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# TODO: Then use this to create a tag that loops over a specified set
#       of dict keys and creates the table cells....

@register.simple_tag
def valminmaxdiv(value, min_target, max_target):
   """
   Given a value and minimum/maximum target for that value, return a
   set of nested divs using w3css styles that create a multiple-element
   progressbar showing how far away the value is from min/max.

   The divs contain the text "X (Y%-Z%)" where X is the value and Y/Z are
   the value as a percentage of the minimum/maximum target respectively.
   The bit in the brackets is put within a <small> tag.

   Exceptions:
   - Returns an empty string if the value cannot be converted to float.
   - Only shows one % if one of min/max are specified (or are
     non-floats), and does not show any brackets if neither are specified.
   - Doesn't cope with negative values for anything, this shouldn't ever
     appear in the data, if it does something is seriously wrong.
   """
   try:
      val = float(value)
   except:
      return ''   # There is literally no value in this

   # Part 1: Generate the string with the text in the cell

   try:
      min_t = float(min_target)
      min_p = int(100 * val / min_t)
   except:  # divide by zero or cannot convert to float
      min_t = 0   # For bar chart later
      min_p = None

   try:
      max_t = float(max_target)
      max_p = int(100 * val / max_t)
   except:  # divide by zero or cannot convert to float
      max_t = 0   # For bar chart later
      max_p = None

   if min_p and max_p:
      contents = '%s<small> (%s%%-%s%%)</small>'%(val,min_p,max_p)
   elif min_p:
      contents = '%s<small> (%s%%)</small>'%(val,min_p)
   elif max_p:
      contents = '%s<small> (%s%%)</small>'%(val,min_p)
   else:
      contents = '%s'%val

   # Part 2: Do the div, similar to css_progressbar but
   # with three components to the bar.

   if (min_t > max_t):   # Swap here so max >= min for CSS; note one may be 0
      min_t, max_t = max_t, min_t

   # TODO: Make these arguments?
   under_colour = 'w3-green'  # Under minimum
   warn_colour = 'w3-orange'  # Over minium
   over_colour = 'w3-red'     # Max or over

   # There are 3 possibilities:
   # val < min < max : 3 colours with val as a % of min which is % max
   # min <= val < max : 2 colours with val as a % of max using middle colour
   # val >= max : 1 colour

   if (val >= max_t):
      return mark_safe(
         '<div class="%s">%s</div>'%(
            over_colour,
            contents,
         )
      )
   elif (val >= min_t):
      return mark_safe(
         '<div class="%s"><div class="%s" style="width:%d%%">%s</div></div>'%(
            warn_colour,
            over_colour,
            max_p,
            contents,
         )
      )
   else:
      return mark_safe(
         '<div class="%s"><div class="%s" style="width:%d%%"><div class="%s" style="width:%d%%">%s</div></div>'%(
            under_colour,
            warn_colour,
            min_p,
            over_colour,
            max_p,
            contents,
         )
      )


# FIXME: deprecated; replace usage of this with the above tag
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


# TODO: This is more general than CSS visuals and should really go
# elsewhere. Preferably in the core django filters tbh.
@register.filter
def divide(num, den):
   """
   Divide num by den in a template, returns 'NaN' if denominator is 0.
   """
   return (float(num) / float(den)) if float(den)!=0 else 'NaN'

