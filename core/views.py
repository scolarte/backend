from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
from products.models import Category, SubCategory, Brand, Product


# Create your views here.

def index(request):
    return HttpResponse("You're looking at question")


class ScolarteHome(TemplateView):
    template_name = "scolarte/index.html"

