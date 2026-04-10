from rest_framework import serializers, generics, permissions
from .models import AccreditedInvestor


class AccreditedInvestorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = AccreditedInvestor
        fields = [
            "first_name", "last_name", "email", "country",
            "capital_range", "referral_source",
            "confirmed_accredited", "consent_contact",
        ]

    def validate(self, data):
        if not data.get("confirmed_accredited"):
            raise serializers.ValidationError(
                {"confirmed_accredited": "Accredited investor confirmation is required."}
            )
        if not data.get("consent_contact"):
            raise serializers.ValidationError(
                {"consent_contact": "Contact consent is required."}
            )
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        instance = super().create(validated_data)
        if request:
            x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
            instance.consent_ip = (
                x_forwarded.split(",")[0].strip() if x_forwarded
                else request.META.get("REMOTE_ADDR")
            )
            instance.save(update_fields=["consent_ip"])
        return instance


class AccreditedInvestorCreateView(generics.CreateAPIView):
    serializer_class   = AccreditedInvestorCreateSerializer
    permission_classes = [permissions.AllowAny]
