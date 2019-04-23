import qrcode
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from core import status
from core.models import Box, Specimen
from web.forms.box import BoxForm


@login_required
def overview(request):
    if request.is_ajax():
        search = request.GET.get('search', '')
        offset = int(request.GET.get('offset', 0)) + 1
        limit = int(request.GET.get('limit', 10))

        # Sorting
        sort = request.GET.get('sort', 'title')
        if request.GET.get('order', 'asc') == 'desc':
            sort = f"-{sort}"

        boxes = Box.objects.filter(title__icontains=search).order_by(sort)
        paginator = Paginator(boxes, limit)

        response = {
            'rows': [row.summary for row in paginator.get_page(offset)],
            'total': paginator.count
        }

        return JsonResponse(response)

    return render(request, 'boxes/overview.html')


def detail(request, id):
    try:
        box = Box.objects.get(pk=str(id))
    except Box.DoesNotExist:
        raise Http404()

    if request.is_ajax():
        search = request.GET.get('search', '')
        offset = int(request.GET.get('offset', 0)) + 1
        limit = int(request.GET.get('limit', 10))

        # Sorting
        sort = request.GET.get('sort', 'organism__name')
        if request.GET.get('order', 'asc') == 'desc':
            sort = f"-{sort}"

        specimens = Specimen.objects \
            .filter(organism__name__icontains=search, box=box) \
            .order_by(sort)
        paginator = Paginator(specimens, limit)

        response = {
            'rows': [row.summary for row in paginator.get_page(offset)],
            'total': paginator.count
        }

        return JsonResponse(response)

    context = {
        'box': box
    }
    return render(request, 'boxes/detail.html', context)


@login_required
def edit(request, id):
    if not request.is_ajax():
        raise Http404()
    try:
        box = Box.objects.get(pk=str(id))
    except Box.DoesNotExist:
        raise Http404()

    if request.method == 'GET':
        box_form = BoxForm(initial=model_to_dict(box))
        return render(request, 'boxes/form.html', {
            'form': box_form,
            'box': box
        })
    elif request.method == 'POST':
        box_form = BoxForm(request.POST, instance=box)

        if box_form.is_valid():
            box_form.save()
            return JsonResponse(box.summary, status=status.HTTP_200_OK)

        return render(request, 'boxes/form.html', {
            'form': box_form,
            'box': box
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    raise Http404()


@login_required
def add(request):
    if not request.is_ajax():
        raise Http404()

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
            return JsonResponse(box.summary, status=status.HTTP_201_CREATED)

        return render(request, 'boxes/form.html', {
            'form': box_form
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    raise Http404()


@login_required
def remove(request, id):
    try:
        box = Box.objects.get(pk=str(id))
    except Box.DoesNotExist:
        raise Http404()

    box.delete()

    return redirect('boxes-overview')


def qr(request, id):
    try:
        box = Box.objects.get(pk=str(id))
    except Box.DoesNotExist:
        raise Http404()

    img = qrcode.make(request.build_absolute_uri(reverse('boxes-detail', None, [box.id])))

    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response
