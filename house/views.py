from rest_framework import filters
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from house.serializers import MySerialzer
from house.models import (
    House, Photo, AccommodationHouse
)


class MyViewSet(ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    queryset = House.objects.all()
    serializer_class = MySerialzer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('address', 'city')
    filterset_fields = ('floor', 'rooms')

    def create(self, requests):
        serializer = MySerialzer(data=requests.data)
        res = {}
        if serializer.is_valid():
            house = serializer.save()
            try:
                photos = requests.data.getlist('photos')
                accoms = requests.data.getlist('accoms')
                for photo in photos:
                    Photo.objects.create(
                        image=photo, house_id=house.id
                    )
                for accom in accoms:
                    AccommodationHouse.objects.create(
                        house_id=house.id, accom_id=accom
                    )
                res['response'] = True
            except Exception:
                res['response'] = False
        else:
            res['response'] = False
            res['errors'] = serializer.errors

        return Response(res, status=status.HTTP_200_OK)
