from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse

from core.models import Box


@login_required
def overview(request):
    if request.is_ajax():
        boxes = Box.objects.all()
        response = {
            'rows': [],
            'total': len(boxes)
        }

        for box in boxes:
            response['rows'].append({
                "id": box.id,
                "title": box.title,
                "description": box.description,
                "size": box.specimen_set.count(),
                "detail-url": reverse('boxes-detail', None, [box.id])
            })

        return JsonResponse(response)

    return render(request, 'boxes/overview.html')


def detail(request, id):
    return render(request, 'boxes/detail.html')
