from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, FormView, View, DeleteView
from .models import Computer, Reservation
from django.urls import reverse, reverse_lazy
from .forms import AvailabilityForm
from datetime import timedelta


# Create your views here.

menu = [{'title': "О нас", 'url_name': 'about'},
        {'title': "Отзывы", 'url_name': 'feedback'},
        {'title': "Войти", 'url_name': 'login'}
]


def about(request):
    return HttpResponse("О нас")

def feedback(request):
    return HttpResponse("Отзывы")

def index(request):
    return render(request, 'club/index.html', {'title': 'Главная страница', 'menu': menu})


def home_page(request):
    return render(request, 'club/home_page.html', {'menu': menu})

def check_availability(computer, start_session, stop_session):
    avail_list = []
    reservations_list = Reservation.objects.filter(computer=computer)
    for reservation in reservations_list:
        if reservation.start_session > stop_session or reservation.stop_session < start_session:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)

@login_required
def ComputersListView(request):
    computer_objects  = Computer.objects.all()[0]
    computer_categories = dict(computer_objects.PC_CATEGORIES)
    computer_values = computer_categories.values()
    photo_urls = ['https://avatars.mds.yandex.net/get-altay/9793917/2a0000018ca0a79371fd21a158b1d9264858/L_height',
                  'https://i2.wp.com/media.wired.com/photos/5ebc3972d965c2a1fbff9f51/1:1/w_1600,h_1600,c_limit/Business-Gamers-Romania-Singapore-1202642094.jpg',
                  'https://sun9-18.userapi.com/impf/c836430/v836430788/5bc49/R5XHXMIX9o0.jpg?size=604x604&quality=96&sign=b74a58a31d0967259a72c4a226ccb323&type=album']
    computer_list = []
    for computer_category in computer_categories:
        computer = computer_categories.get(computer_category)
        computer_url = reverse('club:ComputersDetailView', kwargs={'category': computer_category})
        computer_list.append((computer, computer_url))
    context = {
        'computer_list': computer_list,
        'photo_urls': photo_urls,
        'computer': computer_objects
    }
    return render(request, 'club/computer_list.html', context)

class ReservationsList(ListView):
    model = Reservation
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            reservation_list = Reservation.objects.all()
            return reservation_list
        else:
            reservation_list = Reservation.objects.filter(user=self.request.user)
            return reservation_list


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
                user=request.user,
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
                user=request.user,
                computer=computer,
                start_session=data['start_session'],
                stop_session=data['stop_session']
            )
            reserve.save()
            return HttpResponse(reserve)
        else:
            return HttpResponse('NON-Done')


class CancelBookingView(DeleteView):
    model = Reservation
    template_name = 'club/booking_cancel_view.html'
    success_url = reverse_lazy('club:ReservationsList')