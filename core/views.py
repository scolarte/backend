from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.

def index(request):
    return HttpResponse("You're looking at question")


class ScolarteHome(TemplateView):
    template_name = "scolarte/index.html"