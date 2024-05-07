from django.urls import path
from .views import ComputersList, ReservationsList, ReservationView


app_name = 'club'

urlpatterns=[
    path('pc_list/', ComputersList.as_view(), name='ComputersList'),
    path('res_list/', ReservationsList.as_view(), name='ReservationsList'),
    path('res/', ReservationView.as_view(), name='reservation_view'),
]