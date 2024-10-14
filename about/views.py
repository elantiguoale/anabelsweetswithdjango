from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.shortcuts import render

# Create your views here.
def about(request):
    return render(request, "about/about_me.html")