from .models import Reservation

def check_availability(computer, start_session, stop_session):
    avail_list = []
    reservations_list = Reservation.objects.filter(computer=computer)
    for reservation in reservations_list:
        if reservation.start_session > stop_session or reservation.stop_session < start_session:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)