from django.shortcuts import render

def profile(request, user_id):

    return render(request, 'profile.html', {'id': user_id})
