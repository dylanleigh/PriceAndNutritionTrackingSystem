from django import template

register = template.Library()


@register.inclusion_tag("frontend/templatetags/float_input.html")
def float_input(label, name=None, multiline=False, hint="", extra="", input_type="text", input_mask=None, container_extra=""):
    """

    extra is string that will be added to the attributes area of the input, useful for disabling inputs for example
    container_extra is like extra, but for the container

    """
    return {
        'type': input_type,
        'label': label,
        'multiline': multiline,
        'name': name,
        'hint': hint,
        'extra': extra,
        'input_mask': input_mask,
        'container_extra': container_extra
    }
