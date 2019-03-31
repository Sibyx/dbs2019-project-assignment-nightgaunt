from django.urls import path

from web.views import dashboard, boxes, specimens

urlpatterns = [
    path('dashboard/', dashboard.index, name='dashboard'),

    path('boxes/', boxes.overview, name='boxes-overview'),
    path('boxes/detail/<uuid:id>/', boxes.detail, name='boxes-detail'),

    path('specimens/', specimens.overview, name='specimens-overview'),
]
