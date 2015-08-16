from django.shortcuts import render

def get_claims(request):    
    return render(request, 'about.html')


def add_claim(request):    
    return render(request, 'about.html')