from django.urls import reverse

from .models import Computer

def get_room_list():
    computer = Computer.objects.all()[0]
    computer_list = []
    computer_categories = dict(computer.PC_CATEGORIES)

    for category in computer_categories:
        computer_category = computer_categories.get(category)
        computer_url = reverse('club:ComputersDetailView', kwargs={'category': category})
        computer_list.append((computer_category, computer_url))

    return computer_list