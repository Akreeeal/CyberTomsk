from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView, FormView, View, DeleteView
from .models import Computer, Reservation
from django.urls import reverse, reverse_lazy
from .forms import AvailabilityForm
from datetime import timedelta
from .get_computer_list import get_room_list
from .check_availability import check_availability


# Create your views here.

menu = [{'title': "О нас", 'url_name': 'about'},
        {'title': "Отзывы", 'url_name': 'feedback'},
        {'title': "Войти", 'url_name': 'login'}
]

photo_urls = ['https://avatars.mds.yandex.net/get-altay/9793917/2a0000018ca0a79371fd21a158b1d9264858/L_height',
              'https://i2.wp.com/media.wired.com/photos/5ebc3972d965c2a1fbff9f51/1:1/w_1600,h_1600,c_limit/Business-Gamers-Romania-Singapore-1202642094.jpg',
              'https://sun9-18.userapi.com/impf/c836430/v836430788/5bc49/R5XHXMIX9o0.jpg?size=604x604&quality=96&sign=b74a58a31d0967259a72c4a226ccb323&type=album']


def about(request):
    return HttpResponse("О нас")

def feedback(request):
    return HttpResponse("Отзывы")

def index(request):
    return render(request, 'club/index.html', {'title': 'Главная страница', 'menu': menu})


def home_page(request):
    return render(request, 'club/home_page.html', {'menu': menu})

@login_required
def ComputersListView(request):
    computer_list = get_room_list()
    context = {
        'computer_list': computer_list,
        'photo_urls': photo_urls,
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
            hours = request.POST.get('hours')
            if hours:
                hours = int(hours)
            else:
                hours = 1

            available_computers = []
            for computer in computer_list:
                stop_session = data['start_session'] + timedelta(hours=hours)
                if check_availability(computer, data['start_session'], stop_session):
                    available_computers.append(computer)
            if len(available_computers) > 0:
                computer = available_computers[0]
                total_cost = hours * computer.hours_cost
                reserve = Reservation.objects.create(
                    user=request.user,
                    computer=computer,
                    start_session=data['start_session'],
                    stop_session=stop_session,
                    total_cost=total_cost
                )
                reserve.save()
                return redirect('club:ReservationsList')
            else:
                context = {
                    'form': form,
                    'alert_message': 'На данное время все компьютеры этой категории заняты. Попробуйте выбрать другое время'
                }
            return render(request, 'club/computer_detail_view.html', context)
        else:
            context = {
                'form': form,
                'alert_message': 'Форма недействительна. Пожалуйста, заполните форму корректно. Выберете количесво часов сессии'
            }
            return render(request, 'club/computer_detail_view.html', context)


class CancelBookingView(DeleteView):
    model = Reservation
    template_name = 'club/reservation_cancel_view.html'
    success_url = reverse_lazy('club:ReservationsList')


class AddReview(View):
    def post(self, request, category):
        print(request.POST)
        return redirect('/')
