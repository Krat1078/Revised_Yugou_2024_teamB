from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'founditem_index.html')

def tofounditemregister(request):
    return render(request, 'founditem_index.html')
