import jinja2
from jinja2 import Environment
from markdownx.utils import markdownify
from django.contrib import messages


def show_markdown(text):
    return markdownify(text)

#def img_responsive(text):
#    if <t
jinja2.filters.FILTERS['show_markdown'] = show_markdown
# def environment(**options):
#     env = Environment(**options)
#     env.filters['show_markdown'] = show_markdown
#     env.globals.update({
#         'show_markdown': show_markdown,
#         })
#     return env

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'get_messages': messages.get_messages,
    })
    return env
