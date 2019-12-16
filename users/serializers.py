from rest_framework import serializers
from .models import CustomUser


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(style={'input_type': 'text'})
    confirm_password = serializers.CharField(style={'input_type': 'password'})
    password = serializers.CharField(style={'input_type': 'password'})
    address = serializers.CharField(style={'base_template': 'textarea.html'})
    email = serializers.EmailField()

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'contact', 'address',
                  'pincode', 'password', 'confirm_password')

    def validate_password(self, password):
        if password != self.initial_data.get('confirm_password'):
            raise serializers.ValidationError(
                'Passwords do not match'
            )
        return password

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user =CustomUser.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})
    # token = serializers.CharField(max_length=255)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(style={'input_type': 'text'})
    address = serializers.CharField(style={'base_template': 'textarea.html'})
    email = serializers.EmailField()

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email',
                  'contact', 'address', 'pincode')
