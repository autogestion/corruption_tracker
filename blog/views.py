from django.shortcuts import render


def entry_list(request):

    return render(request, 'entry_list.html')


def entry_add(request):

    return render(request, 'entry_add.html')


def entry(request, post_id):

    return render(request, 'entry.html', {'id': post_id})
