from rest_framework import serializers
from house import models as house_models
from account.serializers import UserShortSerializer
from account.models import User


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    house = serializers.ReadOnlyField(source='house.id')

    class Meta:
        model = house_models.Review
        fields = ('id', 'user', 'house', 'body', 'stars', 'created_at')


class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = house_models.Photo
        fields = ('image',)


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
        if self.context['request'].user.id is not None:
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
    reviews = ReviewSerializer(many=True, read_only=True)

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

    class Meta:
        model = house_models.House
        fields = (
            'id', 'name', 'description', 'rooms', 'floor',
            'address', 'longitude', 'latitude', 'house_type', 'price',
            'status', 'beds', 'guests', 'rating', 'city', 'is_favourite', 'photos',
            'accommodations', 'near_buildings', 'rules', 'user', 'reviews'
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
    # house_type_id = serializers.PrimaryKeyRelatedField(
    #     queryset=house_models.HouseType.objects.all(), source='house_type', write_only=True)
    # city_id = serializers.PrimaryKeyRelatedField(
    #     queryset=house_models.City.objects.all(), source='city', write_only=True)
    # rules = RuleRelatedField(
    #     queryset=house_models.Rule.objects.all(),
    #     many=True)
    # accommodations = AccommodationRelatedField(
    #     queryset=house_models.Accommodation.objects.all(),
    #     many=True)
    # near_buildings = NearBuildingRelatedField(
    #     queryset=house_models.NearBuilding.objects.all(),
    #     many=True)

    class Meta:
        model = house_models.House
        fields = (
            'id',
            # 'id', 'name', 'description', 'city_id', 'rooms', 'floor',
            # 'address', 'longitude', 'latitude', 'house_type_id', 'price',
            # 'beds', 'guests', 'accommodations', 'near_buildings', 'rules'
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
