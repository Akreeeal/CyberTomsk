from django.urls import path
from .views import ComputersListView, ReservationsList, index, ComputersDetailView, about, feedback, home_page, CancelBookingView, AddReview


app_name = 'club'

urlpatterns=[
    path('', home_page, name='home'),
    path('about/', about, name='about'),
    path('feedback/', feedback, name='feedback'),
    path('pc_list/', ComputersListView, name='ComputersList'),
    path('res_list/', ReservationsList.as_view(), name='ReservationsList'),
    path('res/<category>', ComputersDetailView.as_view(), name='ComputersDetailView'),
    path('res/cancel/<pk>', CancelBookingView.as_view(), name='CancelBookingView'),
    path('review/<int:category>/', AddReview.as_view(), name='add_review'),
]