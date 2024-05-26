from django.test import TestCase
from .models import Computer, Reservation
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from django.urls import reverse

from django.contrib.auth import get_user_model
User = get_user_model()

class TestCyberTomsk(TestCase):
    def test_home(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)


class ComputerModelTest(TestCase):
    def setUp(self):
        self.computer = Computer.objects.create(
            category='STD',
            number=1,
            processor='Intel Core i5',
            ram='8GB',
            graphics_card='Nvidia GTX 1060',
            vram='6GB'
        )

    def test_computer_str(self):
        self.assertEqual(str(self.computer), 'STD PC number 1')
#
#
class ReservationModelTest(TestCase):
    def setUp(self):
        self.computer = Computer.objects.create(
            category='STD',
            number=1,
            processor='Intel Core i5',
            ram='8GB',
            graphics_card='Nvidia GTX 1060',
            vram='6GB'
        )
        self.user = User.objects.create(username='testuser')
        self.reservation = Reservation.objects.create(
            user=self.user,
            computer=self.computer,
            start_session=timezone.now(),
            stop_session=timezone.now() + timedelta(hours=1)
        )

    def test_reservation_str(self):
        expected_result = f' {self.user} has reserved {self.computer} from {self.reservation.start_session} to {self.reservation.stop_session}'
        self.assertEqual(str(self.reservation), expected_result)

    def test_get_computer_category(self):
        self.assertEqual(self.reservation.get_computer_category(), 'STANDARD')



class ReservationsListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.staff_user = get_user_model().objects.create_user(username='staffuser', password='testpass', is_staff=True)
        self.computer = Computer.objects.create(
            category='STD',
            number=1,
            processor='Intel Core i5',
            ram='8GB',
            graphics_card='Nvidia GTX 1060',
            vram='6GB'
        )
        self.reservation = Reservation.objects.create(
            user=self.user,
            computer=self.computer,
            start_session=datetime.now(),
            stop_session=datetime.now() + timedelta(hours=1)
        )

    def test_non_staff_user_reservations_list(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('club:ReservationsList'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['reservation_list'], [self.reservation], transform=lambda x: x)

    def test_staff_user_reservations_list(self):
        self.client.login(username='staffuser', password='testpass')
        response = self.client.get(reverse('club:ReservationsList'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['reservation_list'], [self.reservation], transform=lambda x: x)


class ComputersDetailViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.computer = Computer.objects.create(
            category='STD',
            number=1,
            processor='Intel Core i5',
            ram='8GB',
            graphics_card='Nvidia GTX 1060',
            vram='6GB'
        )

    def test_post_computer_detail_view_successful_reservation(self):
        self.client.login(username='testuser', password='testpass')
        start_time = timezone.now() + timedelta(days=1)
        response = self.client.post(reverse('club:ComputersDetailView', kwargs={'category': 'STD'}), {
            'start_session': start_time,
            'hours': 1
        })
        self.assertRedirects(response, reverse('club:ReservationsList'))
        reservation = Reservation.objects.get(user=self.user, computer=self.computer)
        self.assertIsNotNone(reservation)
        self.assertEqual(reservation.start_session, start_time)
        self.assertEqual(reservation.stop_session, start_time + timedelta(hours=1))

    def test_post_computer_detail_view_no_available_computers(self):
        self.client.login(username='testuser', password='testpass')
        Reservation.objects.create(
            user=self.user,
            computer=self.computer,
            start_session=timezone.now() + timedelta(days=1),
            stop_session=timezone.now() + timedelta(days=1, hours=1)
        )
        response = self.client.post(reverse('club:ComputersDetailView', kwargs={'category': 'STD'}), {
            'start_session': timezone.now() + timedelta(days=1),
            'hours': 1
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(),
                         'На данное время все компьютеры этой категории заняты. Попробуйте выбрать другое время ')

    def test_post_computer_detail_view_invalid_form(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('club:ComputersDetailView', kwargs={'category': 'STD'}), {
            'start_session': 'invalid-date',
            'hours': 1
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'Форма недействительна. Пожалуйста, заполните форму корректно.')


