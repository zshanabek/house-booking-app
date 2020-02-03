
from rest_framework.decorators import api_view
from .models import Order
from django.shortcuts import get_object_or_404
from reservation.models import Reservation
from utils.payment import Payment
from rest_framework import status
from rest_framework.response import Response


@api_view(['POST'])
def create_payment(request):
    reservation_id = request.data.get('reservation_id')
    reserv = get_object_or_404(Reservation, pk=reservation_id)
    order = Order.objects.create(amount=reserv.income, reservation=reserv)
    p = Payment(reserv.income, "KZT", "Оплата за проживание в доме", str(order.id))
    r = p.create_payment()
    if r.status_code == status.HTTP_201_CREATED:
        return Response(r.json(), status.HTTP_200_OK)
    else:
        return Response({'response': False, 'error_message': r.json()}, status.HTTP_500_INTERNAL_SERVER_ERROR)