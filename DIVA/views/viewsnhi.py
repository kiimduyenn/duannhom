from django.shortcuts import render


# Create your views here.
def customer(request):
    return render(request,'layout/customer.html')


def admin(request):
    return render(request,'layout/admin.html')
