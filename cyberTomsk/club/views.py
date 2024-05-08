from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, FormView
from .models import Computer, Reservation
from .forms import AvailabilityForm
# from reservations_functions.availability import check_availability

def check_availability(computer, start_session, stop_session):
    avail_list = []
    reservations_list = Reservation.objects.filter(computer=computer)
    for reservation in reservations_list:
        if reservation.start_session > stop_session or reservation.stop_session < start_session:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)

# Create your views here.
class ComputersList(ListView):
    model = Computer

class ReservationsList(ListView):
    model = Reservation

class ReservationView(FormView):
    form_class = AvailabilityForm
    template_name = 'club/availability_form.html'

    def form_valid(self, form):
        data = form.cleaned_data
        computer_list = Computer.objects.filter(category=data['computer_category'])
        available_computers = []
        for computer in computer_list:
            if check_availability(computer, data['start_session'], data['stop_session']):
                available_computers.append(computer)
        if len(available_computers) > 0:
            computer = available_computers[0]
            reservation = Reservation.object.create(
                user=self.request.user,
                computer=computer,
                start_session=data['start_session'],
                stop_session=data['stop_session']
            )
            reservation.save()
            return HttpResponse(reservation)
        else:
            return HttpResponse('NON-Done')


