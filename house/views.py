from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import Photo
from rest_framework.parsers import MultiPartParser, FormParser

size = 3


class MyViewSet(ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    queryset = House.objects.all()
    serializer_class = MySerialzer

    def list(self, request):

        if request.query_params.get('page') is not None:
            page = int(request.query_params.get('page'))
            if page == 1:
                go_previos = None
                go_next = 2
                queryset = House.objects.all()[:size]
            else:
                limit = size * page
                offset = size * (page - 1)
                queryset = House.objects.all()[offset:limit]
                if House.objects.latest('id') not in queryset:
                    go_previos = page - 1
                    go_next = page + 1
                else:
                    go_previos = page - 1
                    go_next = None
        else:
            go_previos = None
            go_next = 2
            queryset = House.objects.all()[0:size]

        serializer = MySerialzer(queryset, many=True)

        obj = {
            'count': len(serializer.data),
            'previos': go_previos,
            'next': go_next,
            'result': serializer.data
        }

        return Response(obj)

    def create(self, requests):
        serializer = MySerialzer(data=requests.data)
        res = {}
        if serializer.is_valid():
            house = serializer.save()
            try:
                photos = requests.data.getlist('photos')
                accoms = requests.data.getlist('accoms')
                print(accoms)
                for photo in photos:
                    Photo.objects.create(image=photo, house_id=house.id)
                for accom in accoms:
                    AccommodationHouse.objects.create(
                        house_id=house.id, accom_id=accom)
                res['response'] = True
            except Exception:
                res['response'] = False
        else:
            res['response'] = False
            res['errors'] = serializer.errors

        return Response(res, status=status.HTTP_200_OK)
