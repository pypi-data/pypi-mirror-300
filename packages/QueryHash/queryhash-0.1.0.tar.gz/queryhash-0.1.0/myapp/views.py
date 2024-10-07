from django.http import HttpResponse
from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')  # Render a template with a form to input the query