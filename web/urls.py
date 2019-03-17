from django.urls import path

from web.views import dashboard

urlpatterns = [
    path('dashboard/', dashboard.index, name='dashboard')
]
