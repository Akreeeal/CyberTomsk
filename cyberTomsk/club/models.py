from django.db import models
from django.conf import settings
from django.urls import reverse


class Computer(models.Model):
    PC_CATEGORIES=(
        ('STD', 'STANDARD'),
        ('VIP', 'VIP'),
        ('BTC', 'BOOTCAMP'),
    )
    category = models.CharField(max_length=4, choices=PC_CATEGORIES)
    number = models.IntegerField(default=1)
    processor = models.CharField(max_length=255)
    ram = models.CharField(max_length=255)
    graphics_card = models.CharField(max_length=255)
    vram = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.category} PC number {self.number}'


class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    start_session = models.DateTimeField()
    stop_session = models.DateTimeField()

    def __str__(self):
        return f' {self.user} has reserved {self.computer} from {self.start_session} to {self.stop_session}'

    def get_computer_category(self):
        computer_categories = dict(self.computer.PC_CATEGORIES)
        computer_category = computer_categories.get(self.computer.category)
        return computer_category

    def get_cancel_reservation_url(self):
        return reverse('club:CancelBookingView', args=[self.pk, ])

class Review(models.Model):
    email = models.EmailField()
    name = models.CharField('Имя', max_length=100)
    text = models.TextField('Сообщение', max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    computer = models.ForeignKey(Computer, verbose_name='Компьютер', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} PC number {self.computer}'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

