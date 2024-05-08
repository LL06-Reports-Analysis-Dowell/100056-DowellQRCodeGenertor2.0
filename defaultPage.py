from django.shortcuts import render

def openPage(request,qrid):
    return render(request, 'index.html')
