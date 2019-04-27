from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.models import Box, Specimen, Photo, User


@login_required
def index(request):
    stats = {
        'boxes': Box.objects.count(),
        'specimens': Specimen.objects.count(),
        'organisms': Specimen.objects.distinct('organism').count(),
        'photos': Photo.objects.count(),
        'users': User.objects.count()
    }

    context = {
        'stats': stats
    }

    return render(request, 'dashboard/index.html', context)
