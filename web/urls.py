from django.urls import path

from web.views import dashboard, boxes, specimens, catalogue, rents, photos

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
    path('specimens/detail/<uuid:id>/', specimens.detail, name='specimens-detail'),
    path('specimens/edit/<uuid:id>/', specimens.edit, name='specimens-edit'),
    path('specimens/remove/<uuid:id>/', specimens.remove, name='specimens-remove'),
    path('specimens/qr/<uuid:id>/', specimens.qr, name='specimens-qr'),
    path('specimens/add/', specimens.add, name='specimens-add'),

    # Catalogue
    path('catalogue/', catalogue.overview, name='catalogue-overview'),

    # Rents
    path('rents/', rents.overview, name='rents-overview'),

    # Photos
    path('photos/detail/<uuid:id>/', photos.detail, name='photos-detail'),
]
