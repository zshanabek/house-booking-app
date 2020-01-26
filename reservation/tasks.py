from __future__ import absolute_import, unicode_literals
from akv.celery import app
from reservation.models import Reservation
from django.core.mail import send_mail
from time import sleep
from celery import shared_task


@app.task
def set_reservation_as_inactive(reservation_id):
    """
    This celery task sets the 'status' flag of the reservation object 
    to 2 in the database after the reservation end time has elapsed.
    """
    reservation = Reservation.objects.get(pk=reservation_id)
    reservation.status = 2
    reservation.save()


@app.task
def send_email_task(house, guest, house_owner, reservation_id):
    sleep(5)
    send_mail('У вас новая бронь!!!',
              f'Ваш дом {house} забронировал пользователь {guest.full_name()}!',
              'webmaster@localhost',
              [house_owner.email],
              fail_silently=False)
    return None
