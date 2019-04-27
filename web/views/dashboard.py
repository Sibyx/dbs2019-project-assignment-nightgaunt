from django.contrib.auth.decorators import login_required
from django.db.models import Count, F
from django.db.models.functions import TruncYear
from django.http import JsonResponse
from django.shortcuts import render

from core.models import Box, Specimen, Photo, User


@login_required
def index(request):
    # TODO: tu sprav abstrakciu inak sa zabijem
    if request.is_ajax():
        chart_type = request.GET.get('chart')

        if chart_type == 'distributionChart':
            distribution = list(
                Specimen.objects.values(taxonomic_class=F(
                    'organism__taxonomic_species__taxonomic_genus__taxonomic_family__taxonomic_order__taxonomic_class__name'
                ))
                    .annotate(count=Count('organism__taxonomic_species__taxonomic_genus__taxonomic_family__taxonomic_order__taxonomic_class'))
            )

            return JsonResponse({
                'data': {
                    'labels': [row['taxonomic_class'] for row in distribution],
                    'datasets': [
                        {
                            'label': 'Specimens',
                            'data': [row['count'] for row in distribution],
                            'backgroundColor': [
                                'rgba(255, 99, 132, 0.2)',
                                'rgba(54, 162, 235, 0.2)',
                                'rgba(255, 206, 86, 0.2)',
                                'rgba(75, 192, 192, 0.2)',
                                'rgba(153, 102, 255, 0.2)',
                                'rgba(255, 159, 64, 0.2)'
                            ],
                            'borderColor': [
                                'rgba(255, 99, 132, 1)',
                                'rgba(54, 162, 235, 1)',
                                'rgba(255, 206, 86, 1)',
                                'rgba(75, 192, 192, 1)',
                                'rgba(153, 102, 255, 1)',
                                'rgba(255, 159, 64, 1)'
                            ],
                            'borderWidth': 1
                        }
                    ]
                }
            })
        elif chart_type == 'databaseEvolutionChart':
            evolution = list(Specimen.objects.annotate(year=TruncYear('happened_at')).order_by('year').values('year').annotate(c=Count('id')).values('year', 'c'))

            return JsonResponse({
                'data': {
                    'labels': [row['year'].year for row in evolution],
                    'datasets': [
                        {
                            'label': 'Specimens',
                            'data': [row['c'] for row in evolution],
                            'borderColor': 'rgba(255, 99, 132, 1)',
                            'borderWidth': 1,
                            'fill': False
                        }
                    ]
                },
                'options': {
                    'scales': {
                        'yAxes': [{
                            'ticks': {
                                'beginAtZero': True
                            }
                        }]
                    }
                }
            })

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
