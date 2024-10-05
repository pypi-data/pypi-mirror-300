import re

from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.forms.widgets import CheckboxInput
from django.utils.functional import SimpleLazyObject

from zero_theme.widgets import zero_widget_registry

register = template.Library()


@register.simple_tag
def get_admin_widget_registry():
    return zero_widget_registry.get_widgets()


@register.filter
def get_user_full_name(user):
    if isinstance(user, SimpleLazyObject):
        return user

    # Check if there's a 'get_full_name' method (default User model)
    if hasattr(user, 'get_full_name') and callable(user.get_full_name):
        return user.get_full_name().strip()

    # If the user has a 'full_name' field
    if hasattr(user, 'full_name'):
        return user.full_name.strip()

    # If the user has both 'first_name' and 'last_name' fields
    if hasattr(user, 'first_name') and hasattr(user, 'last_name'):
        return f"{user.first_name} {user.last_name}".strip()

    # If the user has a 'name' field (common in custom models)
    if hasattr(user, 'name'):
        return user.name.strip()

    # Fallback: return username or a default message
    return user or "Anonymous User"


def bootstrap_switch(field):
    if isinstance(field.field.widget, CheckboxInput):
        attrs = field.field.widget.attrs.copy()
        attrs['class'] = attrs.get('class', '') + ' form-check-input'
        switch_html = field.field.widget.render(field.name, field.value(), attrs)

        # Wrap in switch container and use field.label directly
        switch_html = f'''
        <div class="form-check form-switch">
            {switch_html}
        </div>
        '''
        return mark_safe(switch_html)
    return field


@register.filter
def add_class(field, css_class):
    if (field.widget_type == 'admintextinput'
            or field.widget_type == 'number'
            or field.widget_type == 'adminfile'
            or field.widget_type == 'admintextarea'
            or field.widget_type == 'adminintegerfield'
            or field.widget_type == 'color'
            or field.widget_type == 'password'
            or field.widget_type == 'adminemailinput'
    ):
        return field.as_widget(attrs={"class": css_class})

    elif field.widget_type == 'checkbox':
        """(checkbox) is boolean"""
        return bootstrap_switch(field)
    elif (field.widget_type == 'relatedfieldwidgetwrapper'
          or field.widget_type == 'select'):
        """
        (relatedfieldwidgetwrapper) is one to one field
        (select) is many to many fields
        """
        return field.as_widget(attrs={"class": f"{css_class} select2"})
    elif (field.widget_type == 'adminsplitdatetime'
          or field.widget_type == 'radioselect'):
        return field

    try:
        return field.as_widget(attrs={"class": css_class})
    except:
        return field


@register.filter
def simple_add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})


@register.filter
def required(field):
    if field.field.field.required:
        return mark_safe('<span style="color: red;">*</span>')
    return mark_safe('')


@register.filter
def row_clean(item):
    anchor_tag_pattern = r'(<a\s[^>]*>)(.*?)(</a>)'
    img_tag_pattern = r'<img\s[^>]*alt="(True|False)"[^>]*>'

    def add_red_color(match):
        return f'{match.group(1)}<span style="color: #67757c;">{match.group(2)}</span>{match.group(3)}'

    modified_html = re.sub(anchor_tag_pattern, add_red_color, item)

    def replace_with_switch(match):
        alt_value = match.group(1)
        checked = ''
        if alt_value == 'True':
            checked = 'checked'

        switch_html = f'''
        <div class="form-check form-switch">
          <input class="form-check-input" type="checkbox" role="switch"
          id="flexSwitchCheckChecked" {checked} disabled style="opacity: 1"">
        </div>
        '''
        return switch_html

    modified_html = re.sub(img_tag_pattern, replace_with_switch, modified_html)

    html_replaced = re.sub(r'<th\b([^>]*)>', r'<td\1>', modified_html)
    html_replaced = re.sub(r'</th>', '</td>', html_replaced)
    return mark_safe(html_replaced)


@register.filter
def get_row_pk(checkbox):
    pattern = r'<input type="checkbox"[^>]*value="([^"]*)"'
    match = re.search(pattern, checkbox)
    if match:
        return match.group(1)
    return None


@register.simple_tag()
def get_delete_url(app_label, model_name, object_id):
    return reverse(f'admin:{app_label}_{model_name}_delete', args=[object_id])


@register.simple_tag()
def get_change_url(app_label, model_name, object_id):
    return reverse(f'admin:{app_label}_{model_name}_change', args=[object_id])


@register.filter
def widget_class_name(widget):
    return widget.__class__.__name__


@register.simple_tag
def get_field_class(field):
    """Return a CSS class based on whether a ManyToMany field has items."""
    if field.field.queryset.exists():
        return 'has-items'
    else:
        return 'no-items'


@register.filter
def get_verbose_name(model_class):
    return model_class._meta.verbose_name
