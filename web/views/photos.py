from django.http import Http404
from django.shortcuts import render

from core.models import Photo


def detail(request, id):
    if not request.is_ajax():
        raise Http404()
    try:
        photo = Photo.objects.get(pk=str(id))
    except Photo.DoesNotExist:
        raise Http404()

    context = {
        'photo': photo
    }
    return render(request, 'photos/detail.html', context)
