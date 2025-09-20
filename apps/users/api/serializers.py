from rest_framework import serializers
from apps.users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.
    Used for listing, retrieving, and creating/updating users via the API.
    """
    class Meta:
        model = CustomUser
        # Fields to be exposed in the API
        fields = [
            'id', 
            'username', 
            'email', 
            'full_name', 
            'role', 
            'is_active', 
            'date_joined',
            'password' # Include password field for creation
        ]
        # Make certain fields read-only for security and integrity
        read_only_fields = ['id', 'date_joined']
        # Ensure password is not readable (write-only)
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }

    def create(self, validated_data):
        # Override the create method to handle password hashing.
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # Override the update method to handle optional password updates.
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        return super().update(instance, validated_data)