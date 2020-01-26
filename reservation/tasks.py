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
def send_email_task():
    print("========fdf=======")
    import pdb
    pdb.set_trace()
    send_mail('Celery Task Worked!',
              'This is proof the task worked!',
              'webmaster@localhost',
              ['gonocir224@eroyal.net'])
    return None
