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
    if reservation.status == 3:
        reservation.status = 6
        reservation.save()


@app.task
def set_reservation_as_inactive_after_approve(reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    if reservation.status == 1:
        reservation.status = 6
        reservation.save()


@app.task
def set_reservation_as_inactive_after_request(reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    if reservation.status == 0:
        reservation.status = 6
        reservation.save()


@app.task
def send_reservation_notification(reservation_id):
    """
    This celery task sets the 'status' flag of the reservation object 
    to 2 in the database after the reservation end time has elapsed.
    """
    reservation = Reservation.objects.get(pk=reservation_id)
    reservation.status = 2
    reservation.save()


@app.task
def send_email_on_request(house, guest, owner, owner_email, reservation_id):
    booking = Reservation.objects.get(pk=reservation_id)
    send_mail('Новая бронь на AKV',
              f'Здравствуйте, {owner}. Ваш дом {house} забронировал пользователь {guest}. Даты брони. Check in: {booking.check_in}; Check out: {booking.check_out}. Подтвердите или отклоните бронь в течение 24 часа, иначе бронь станет неактивной',
              'webmaster@localhost',
              [owner_email],
              fail_silently=False)
    return None


@app.task
def send_email_on_approve(house, guest, owner, owner_email, reservation_id):
    send_mail('Вашу бронь на AKV приняли',
              f'Здравствуйте, {owner}. Вашу бронь для дома {house} подтвердил хозяин {guest}. Оплатите бронь в течение следующих 24 часа, иначе бронь станет неактивной',
              'webmaster@localhost',
              [owner_email],
              fail_silently=False)
    return None


@app.task
def send_email_on_reject(house, guest, owner, owner_email, reservation_id):
    send_mail('Ответ по брони на AKV',
              f'Здравствуйте, {owner}. Вашу бронь для дома {house} отклонили',
              'webmaster@localhost',
              [owner_email],
              fail_silently=False)
    return None
