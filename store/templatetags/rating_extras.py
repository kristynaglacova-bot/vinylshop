from django import template

register = template.Library()

@register.filter
def avg_rating(ratings):
    if not ratings:
        return 0
    total = sum([r.stars for r in ratings])
    return round(total / len(ratings))