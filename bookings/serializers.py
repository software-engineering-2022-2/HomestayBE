from rest_framework.serializers import ModelSerializer
from bookings.models import Booking
from homestays.models import Service


class ServiceIdSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = ['id']


class BookingSerializer(ModelSerializer):
    services = ServiceIdSerializer(many=True)

    class Meta:
        model = Booking
        fields = '__all__'

    def create(self, validated_data):
        services_data = validated_data.pop('services', [])
        booking = Booking.objects.create(**validated_data)

        service_ids = []
        for service_data in services_data:
            try:
                service_id = service_data.get('id')
                print(service_id)
                service_ids.append(service_id)
            except KeyError:
                print(f"Missing 'id' key in service_data: {service_data}")

        return booking

    def update(self, instance, validated_data):
        services_data = validated_data.pop('services', [])
        services_ids = [service_data.get('id') for service_data in services_data]

        # Copy all fields from validated_data to instance
        for field, value in validated_data.items():
            setattr(instance, field, value)

        # Update related services
        instance.services.set(Service.objects.filter(id__in=services_ids))

        return instance
