import qrcode
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from core import status
from core.models import Specimen, Box, Organism
from core.models.specimen import GenderChoice
from web.forms.specimen import SpecimenForm


@login_required
def overview(request):
    if request.is_ajax():
        search = request.GET.get('search', '')
        offset = int(request.GET.get('page', 0)) + 1
        limit = int(request.GET.get('limit', 10))

        # Sorting
        sort = request.GET.get('sort', 'organism__name')
        if request.GET.get('order', 'asc') == 'desc':
            sort = f"-{sort}"

        specimens = Specimen.objects \
            .filter(organism__name__icontains=search) \
            .order_by(sort)
        paginator = Paginator(specimens, limit)

        response = {
            'rows': [row.summary for row in paginator.get_page(offset)],
            'total': paginator.count
        }

        return JsonResponse(response)

    return render(request, 'specimens/overview.html')


@login_required
def add(request):
    if request.is_ajax() and request.GET.get('type', False):
        return _process_select2(request)

    if request.method == 'GET':
        specimen_form = SpecimenForm()
        return render(request, 'specimens/form.html', {
            'form': specimen_form
        })
    elif request.method == 'POST':
        specimen = Specimen()
        specimen.creator = request.user
        specimen_form = SpecimenForm(request.POST, instance=specimen)

        if specimen_form.is_valid():
            specimen_form.save()
            redirect('specimens-detail', specimen.id)

        return render(request, 'specimens/form.html', {
            'form': specimen_form
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    raise Http404()


def detail(request, id):
    try:
        specimen = Specimen.objects.get(pk=str(id))
    except Specimen.DoesNotExist:
        raise Http404()

    context = {
        'specimen': specimen
    }

    return render(request, 'specimens/detail.html', context)


@login_required
def edit(request, id):
    try:
        specimen = Specimen.objects.get(pk=str(id))
    except Specimen.DoesNotExist:
        raise Http404()

    context = {
        'specimen': specimen
    }

    return render(request, 'specimens/form.html', context)


@login_required
def remove(request, id):
    try:
        specimen = Specimen.objects.get(pk=str(id))
    except Specimen.DoesNotExist:
        raise Http404()

    specimen.delete()

    return redirect('specimens-overview')


def qr(request, id):
    try:
        specimen = Specimen.objects.get(pk=str(id))
    except Specimen.DoesNotExist:
        raise Http404()

    img = qrcode.make(request.build_absolute_uri(reverse('specimens-detail', None, [specimen.id])))

    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


def _process_select2(request):
    """
    TODO: sprav na to nejaky servis/helper, takto to je neskutocne trapne
    :param request:
    :return:
    """
    search = request.GET.get('search', '')
    offset = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))
    result = []

    if request.GET.get('type') == 'box':
        items = Box.objects.filter(title__icontains=search).order_by('title')
    elif request.GET.get('type') == 'organism':
        items = Organism.objects.filter(name__icontains=search).order_by('name')
    elif request.GET.get('type') == 'gender':
        for tag in GenderChoice:
            result.append({
                'id': tag.value,
                'text': tag.value
            })
        return JsonResponse({
            'items': result,
            'pagination': {
                'more': False
            }
        })
    else:
        raise Http404()

    paginator = Paginator(items, limit)

    for row in paginator.get_page(offset):
        result.append({
            'id': str(row.id),
            'text': str(row)
        })

    return JsonResponse({
        'items': result,
        'pagination': {
            'more': paginator.get_page(offset).has_next()
        }
    })
