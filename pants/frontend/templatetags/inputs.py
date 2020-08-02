from django import template

register = template.Library()


@register.inclusion_tag("frontend/templatetags/float_input.html")
def float_input(input_type, label, name=None, multiline=False, hint=""):
    """
    hint is a paragraph explaining what could be put in, or limitations to inputs. Possibly should be made visible on focus
    """
    return {
        'type': input_type,
        'label': label,
        'multiline': multiline,
        'name': name,
        'hint': hint
    }
