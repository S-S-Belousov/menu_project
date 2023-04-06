from django import template
from django.urls import resolve, reverse
from ..models import MenuItem

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = resolve(request.path_info).url_name
    menu_items = MenuItem.objects.filter(title=menu_name)
    menu_html = '<ul>'
    
    for item in menu_items:
        if not item.parent:
            menu_html += render_menu_item(item, current_url)
            menu_html += '<ul>'
            
            for child_item in item.children.all():
                menu_html += '<li>'
                menu_html += render_menu_item(child_item, current_url)
                menu_html += '<ul>'
                
                for grandchild_item in child_item.children.all():
                    menu_html += render_menu_item(grandchild_item, current_url)
                
                menu_html += '</ul></li>'
            
            menu_html += '</ul></li>'
    
    menu_html += '</ul>'
    return menu_html

def render_menu_item(item, current_url):
    active = 'active' if item.url == current_url or item.named_url == current_url else ''
    return f'<li class="{active}\"><a href="{item.url or reverse(item.named_url)}">{item.title}</a></li>'