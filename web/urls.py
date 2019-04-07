from django.urls import path

from web.views import dashboard, boxes, specimens

urlpatterns = [
    path('', dashboard.index, name='dashboard'),

    path('boxes/', boxes.overview, name='boxes-overview'),
    path('boxes/detail/<uuid:id>/', boxes.detail, name='boxes-detail'),
    path('boxes/edit/<uuid:id>/', boxes.edit, name='boxes-edit'),
    path('boxes/remove/<uuid:id>/', boxes.remove, name='boxes-remove'),
    path('boxes/add/', boxes.add, name='boxes-add'),

    path('specimens/', specimens.overview, name='specimens-overview'),
]
