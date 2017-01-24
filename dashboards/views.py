from django.shortcuts import render

def index(request):
  return render(request, 'dashboards/index.html')
# Create your views here.
