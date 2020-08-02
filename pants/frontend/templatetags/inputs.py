from django import template

register = template.Library()


@register.inclusion_tag("frontend/templatetags/float_input.html")
def float_input(label, name=None, multiline=False, hint="", extra="", input_type="text"):
    """
    hint is a paragraph explaining what could be put in, or limitations to inputs. Possibly should be made visible on focus
    extra is string that will be added to the attributes area of the input, useful for disabling inputs for example
    """
    return {
        'type': input_type,
        'label': label,
        'multiline': multiline,
        'name': name,
        'hint': hint,
        'extra': extra
    }
