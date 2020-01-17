from rest_framework import serializers
from house import models as house_models
from account.serializers import UserShortSerializer
from account.models import User


class ReviewSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    house = serializers.ReadOnlyField(source='house.id')

    class Meta:
        model = house_models.Review
        fields = ('id', 'user', 'house', 'body', 'stars', 'created_at')


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = house_models.Photo
        fields = ('house', 'image',)


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = house_models.Rule
        fields = ('id', 'name',)


class AccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = house_models.Accommodation
        fields = ('id', 'name',)


class NearBuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = house_models.NearBuilding
        fields = ('id', 'name',)


class HouseCoordinatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = house_models.House
        fields = ('id', 'name', 'longitude', 'latitude', 'city')


class HouseListSerializer(serializers.ModelSerializer):
    city = serializers.ReadOnlyField(source='city.name')
    house_type = serializers.ReadOnlyField(source='house_type.name')
    is_favourite = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    accommodations = AccommodationSerializer(many=True)

    def get_photos(self, obj):
        p_qs = house_models.Photo.objects.filter(house=obj)
        if len(p_qs) == 0:
            return None
        photos = PhotoSerializer(p_qs, many=True).data
        return photos

    def get_is_favourite(self, obj):
        if 'request' in self.context and self.context['request'].user.id is not None:
            return house_models.Favourite.objects.filter(user=self.context['request'].user, house=obj).exists()
        return False

    class Meta:
        model = house_models.House
        fields = (
            'id', 'name', 'city', 'longitude', 'latitude', 'house_type', 'price', 'status', 'beds', 'rooms', 'rating', 'is_favourite', 'photos', 'accommodations')


class HouseDetailSerializer(serializers.ModelSerializer):
    user = UserShortSerializer()
    city = serializers.ReadOnlyField(source='city.name')
    house_type = serializers.ReadOnlyField(source='house_type.name')
    is_favourite = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    rules = RuleSerializer(many=True)
    accommodations = AccommodationSerializer(many=True)
    near_buildings = NearBuildingSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    recommendations = serializers.SerializerMethodField()

    def get_is_favourite(self, obj):
        if self.context['request'].user.id is not None:
            return house_models.Favourite.objects.filter(user=self.context['request'].user, house=obj).exists()
        return False

    def get_photos(self, obj):
        p_qs = house_models.Photo.objects.filter(house=obj)
        if len(p_qs) == 0:
            return None
        photos = PhotoSerializer(p_qs, many=True).data
        return photos

    def get_reviews(self, obj):
        qs = house_models.Review.objects.filter(house=obj)
        reviews = ReviewSerializer(qs, many=True).data[:2]
        return reviews

    def get_recommendations(self, obj):
        qs = house_models.House.objects.filter(city=obj.city)
        houses = HouseListSerializer(qs, many=True).data[:2]
        return houses

    class Meta:
        model = house_models.House
        fields = (
            'id', 'name', 'description', 'rooms', 'floor',
            'address', 'longitude', 'latitude', 'house_type', 'price',
            'status', 'beds', 'guests', 'rating', 'city', 'is_favourite', 'discount7days', 'discount30days', 'photos', 'accommodations', 'near_buildings', 'rules', 'user', 'reviews', 'recommendations'
        )


class RuleRelatedField(serializers.RelatedField):
    def display_value(self, instance):
        return instance

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        if (house_models.Rule.objects.filter(name=data).exists() == False):
            new_rule = house_models.Rule.objects.create(name=data)
        return house_models.Rule.objects.get(name=data)


class AccommodationRelatedField(serializers.RelatedField):
    def display_value(self, instance):
        return instance

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        if (house_models.Accommodation.objects.filter(name=data).exists() == False):
            new_rule = house_models.Accommodation.objects.create(name=data)
        return house_models.Accommodation.objects.get(name=data)


class NearBuildingRelatedField(serializers.RelatedField):
    def display_value(self, instance):
        return instance

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        if (house_models.NearBuilding.objects.filter(name=data).exists() == False):
            new_rule = house_models.NearBuilding.objects.create(name=data)
        return house_models.NearBuilding.objects.get(name=data)


class HouseCreateSerializer(serializers.ModelSerializer):
    house_type_id = serializers.PrimaryKeyRelatedField(
        queryset=house_models.HouseType.objects.all(), source='house_type', write_only=True)
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=house_models.City.objects.all(), source='city', write_only=True)
    rules = RuleRelatedField(
        queryset=house_models.Rule.objects.all(),
        many=True)
    accommodations = AccommodationRelatedField(
        queryset=house_models.Accommodation.objects.all(),
        many=True)
    near_buildings = NearBuildingRelatedField(
        queryset=house_models.NearBuilding.objects.all(),
        many=True)

    class Meta:
        model = house_models.House
        fields = (
            'id', 'name', 'description', 'city_id', 'rooms', 'floor',
            'address', 'longitude', 'latitude', 'house_type_id', 'price',
            'beds', 'guests', 'discount7days', 'discount30days', 'accommodations', 'near_buildings', 'rules'
        )


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = house_models.City
        fields = ('id', 'name',)


class HouseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = house_models.HouseType
        fields = ('id', 'name')


class FavouriteSerializer(serializers.ModelSerializer):
    house = HouseListSerializer(read_only=True)

    class Meta:
        model = house_models.Favourite
        fields = ('house',)


class BlockedDateIntervalSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True, source='house.user')

    class Meta:
        model = house_models.BlockedDateInterval
        fields = ('check_in', 'check_out', 'user')
