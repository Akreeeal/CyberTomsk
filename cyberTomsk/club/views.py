from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, FormView, View
from .models import Computer, Reservation
from django.urls import reverse
from .forms import AvailabilityForm
from datetime import timedelta
# from reservations_functions.availability import check_availability

# Create your views here.

menu = ['Аренда', 'Отзывы', 'Войти']

def index(request):
    return render(request, 'club/index.html', {'title': 'Главная страница'}, {'menu': menu})

def check_availability(computer, start_session, stop_session):
    avail_list = []
    reservations_list = Reservation.objects.filter(computer=computer)
    for reservation in reservations_list:
        if reservation.start_session > stop_session or reservation.stop_session < start_session:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)

def ComputersListView(request):
    computer = Computer.objects.all()[0]
    computer_categories = dict(computer.PC_CATEGORIES)
    computer_values = computer_categories.values()
    computer_list = []
    for computer_category in computer_categories:
        computer = computer_categories.get(computer_category)
        computer_url = reverse('club:ComputersDetailView', kwargs={'category': computer_category})
        computer_list.append((computer, computer_url))
    context={
        'computer_list': computer_list
    }
    return render(request, 'club/computer_list.html', context)

class ReservationsList(ListView):
    model = Reservation


class ComputersDetailView(View):
    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        computer_list = Computer.objects.filter(category=category)
        form = AvailabilityForm()
        if len(computer_list) > 0:
            computer = computer_list[0]
            computer_category = dict(computer.PC_CATEGORIES).get(computer.category, None)
            context = {
                'computer_category': computer_category,
                'form': form,
            }

            return render(request, 'club/computer_detail_view.html', context)
        else:
            return HttpResponse('Нет такой категории')
    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        computer_list = Computer.objects.filter(category=category)
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            hours = data.get('hours')

        available_computers = []
        for computer in computer_list:
            stop_session = data['start_session'] + timedelta(hours=hours)
            if check_availability(computer, data['start_session'], stop_session):
                available_computers.append(computer)
        if len(available_computers) > 0:
            computer = available_computers[0]
            reserve = Reservation.objects.create(
                # user=self.request.user,
                # user = None,
                computer=computer,
                start_session=data['start_session'],
                stop_session=stop_session
            )
            reserve.save()
            return HttpResponse(reserve)
        else:
            return HttpResponse('NON-Done')





class ReservationView(FormView):
    form_class = AvailabilityForm
    template_name = 'club/availability_form.html'

    def form_valid(self, form):
        data = form.cleaned_data
        computer_list = Computer.objects.filter(category=data['pc_category'])
        available_computers = []
        for computer in computer_list:
            if check_availability(computer, data['start_session'], data['stop_session']):
                available_computers.append(computer)
        if len(available_computers) > 0:
            computer = available_computers[0]
            reserve = Reservation.objects.create(
                # user=self.request.user,
                # user = None,
                computer=computer,
                start_session=data['start_session'],
                stop_session=data['stop_session']
            )
            reserve.save()
            return HttpResponse(reserve)
        else:
            return HttpResponse('NON-Done')


