from django import template

register = template.Library()

def convertime(value):
    m, s = divmod(value , 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s);

register.filter('convertime', convertime)
