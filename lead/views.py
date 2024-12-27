from django.http import HttpResponse
from django.shortcuts import render,resolve_url,redirect
from datetime import datetime
from django.conf import settings
# Create your views here.
def home(request):
    year = datetime.now().year
    context = {
        'year': year,
    }
    return render(request, 'index.html', context)
