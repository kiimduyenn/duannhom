from django.shortcuts import render

# Create your views here.
def trangchukh(request):
    return render(request, 'trangchu/trangchukh.html')
def trangchuad(request):
    return render(request, 'trangchu/trangchuad.html')