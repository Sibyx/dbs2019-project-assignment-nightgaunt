import qrcode
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from core.models import Specimen


@login_required
def overview(request):
    if request.is_ajax():
        search = request.GET.get('search', '')
        offset = int(request.GET.get('offset', 0)) + 1
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
    return render(request, 'specimens/form.html')


def detail(request, id):
    try:
        specimen = Specimen.objects.get(pk=str(id))
    except Specimen.DoesNotExist:
        raise Http404()

    context = {
        'specimen': specimen
    }

    return render(request, 'specimens/detail.html', context)


def edit(request, id):
    try:
        specimen = Specimen.objects.get(pk=str(id))
    except Specimen.DoesNotExist:
        raise Http404()

    return render(request, 'specimens/form.html')


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
