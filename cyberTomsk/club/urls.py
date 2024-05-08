from django.urls import path
from .views import ComputersListView, ReservationsList, ReservationView, index, ComputersDetailView


app_name = 'club'

urlpatterns=[
    path('', index, name='home'),
    path('pc_list/', ComputersListView.as_view(), name='ComputersList'),
    path('res_list/', ReservationsList.as_view(), name='ReservationsList'),
    path('reserve/', ReservationView.as_view(), name='ReservationView'),
    path('res/<category>', ComputersDetailView.as_view(), name='ComputersDetailView')
]