from django import template
from vacancies.models import *

register = template.Library()


@register.filter
def count_specialty(specialty):
    return len(Vacancy.objects.filter(specialty=specialty))


@register.filter
def count_company(company):
    return len(Vacancy.objects.filter(company=company))
