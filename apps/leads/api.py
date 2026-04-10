from rest_framework import serializers, generics, permissions
from .models import Subscriber


class SubscriberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ["email", "first_name", "source", "lead_magnet"]
        extra_kwargs = {
            "source": {"default": Subscriber.Source.API},
            "lead_magnet": {"required": False},
        }


class SubscriberCreateView(generics.CreateAPIView):
    serializer_class = SubscriberCreateSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # Silently update existing subscribers rather than erroring
        email = serializer.validated_data["email"]
        existing = Subscriber.objects.filter(email=email).first()
        if existing:
            existing.is_active = True
            existing.save(update_fields=["is_active"])
        else:
            serializer.save()
