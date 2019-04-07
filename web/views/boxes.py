from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import render

from core import status
from core.models import Box
from web.forms.box import BoxForm


@login_required
def overview(request):
    if request.is_ajax():
        boxes = Box.objects.all()
        response = {
            'rows': [],
            'total': len(boxes)
        }

        for box in boxes:
            response['rows'].append(box.dict)

        return JsonResponse(response)

    return render(request, 'boxes/overview.html')


@login_required
def detail(request, id):
    context = {
        'id': id
    }
    return render(request, 'boxes/detail.html', context)


@login_required
def add(request):
    if not request.is_ajax():
        raise Http404

    if request.method == 'GET':
        box_form = BoxForm()
        return render(request, 'boxes/form.html', {
            'form': box_form
        })
    elif request.method == 'POST':
        box = Box()
        box.creator = request.user
        box_form = BoxForm(request.POST, instance=box)

        if box_form.is_valid():
            box_form.save()
            return JsonResponse(box.dict, status=status.HTTP_201_CREATED)

        return render(request, 'boxes/form.html', {
            'form': box_form
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    raise Http404
