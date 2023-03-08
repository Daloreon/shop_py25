from rest_framework import serializers
from django.contrib.auth import get_user_model
from account.send_email import send_activation_code, send_reset_password_code
from account.tasks import send_activation_code as celery_register

User = get_user_model()  # CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        required=True,
        min_length=6,
        write_only=True 
    )

    class Meta:
        # model = CustomUser
        model = User
        fields = ('email', 'password', 'password2')
    

    def validate_email(self, email):
        print('Hello')
        return email
    
    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password2')

        if p1 != p2:
            raise serializers.ValidationError('Password did not match!!!')

        return attrs
    

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # send_activation_code(user.email, user.activation_code)
        celery_register.delay(user.email, user.activation_code)
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists(): # not False = True
            raise serializers.ValidationError('Пользователь с такой почтой не существует!')

        return email

    def send_reset_password_code(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        user.save()
        send_reset_password_code(email=email, code=user.activation_code)
        


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, min_length=6)
    password_confirm = serializers.CharField(required=True, min_length=6)
    code = serializers.CharField(required=True)

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.get('password_confirm')

        if p1 != p2:
            raise serializers.ValidationError('пароли не совпадают')
        return attrs

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Неверный код!')
        return code
    
    def set_new_password(self):
        user = User.objects.get(activation_code=self.validated_data.get('code'))
        password = self.validated_data.get('password')
        user.password = password # john123 -> fjdshfksffkjnefjhfjk
        user.set_password(password)
        user.activation_code = ''
        user.save(update_fields=['password', 'activation_code'])


