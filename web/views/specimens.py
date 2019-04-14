from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from core.models import Specimen


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

        specimens = Specimen.objects \
            .filter(Q(nickname__icontains=search) | Q(organism__name__icontains=search)) \
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
