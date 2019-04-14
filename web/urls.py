from django.urls import path

from web.views import dashboard, boxes, specimens, catalogue, rents

urlpatterns = [
    path('', dashboard.index, name='dashboard'),

    # Boxes
    path('boxes/', boxes.overview, name='boxes-overview'),
    path('boxes/detail/<uuid:id>/', boxes.detail, name='boxes-detail'),
    path('boxes/edit/<uuid:id>/', boxes.edit, name='boxes-edit'),
    path('boxes/remove/<uuid:id>/', boxes.remove, name='boxes-remove'),
    path('boxes/qr/<uuid:id>/', boxes.qr, name='boxes-qr'),
    path('boxes/add/', boxes.add, name='boxes-add'),

    # Specimens
    path('specimens/', specimens.overview, name='specimens-overview'),

    # Catalogue
    path('catalogue/', catalogue.overview, name='catalogue-overview'),

    # Rents
    path('rents/', rents.overview, name='rents-overview'),
]
