from django.db import models
from django.conf import settings
class Computer(models.Model):
    PC_CATEGORIES=(
        ('STD', 'STANDARD'),
        ('VIP', 'VIP'),
        ('BTC', 'BOOTCAMP'),
        ('PS5', 'PLAYSTATION')
    )
    category = models.CharField(max_length=4, choices=PC_CATEGORIES)
    processor = models.CharField(max_length=255)
    ram = models.CharField(max_length=255)
    graphics_card = models.CharField(max_length=255)
    vram = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.category} PC with {self.processor} and {self.graphics_card}'

class Reservation(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
    start_session = models.DateTimeField()
    stop_session = models.DateTimeField()

    def __str__(self):
        return f' has reserved {self.computer} from {self.start_session} to {self.stop_session}'