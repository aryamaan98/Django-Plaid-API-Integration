from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from datetime import datetime, timedelta
import plaid
from uuid import uuid4
from .models import User
from .utils import get_plaid_client
from .tasks import get_transactions, get_accounts, get_access_token


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(max_length=8)

    class Meta:
        model = User
        fields = (
            'email',
            'password'
        )


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField()
    token = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        if not email and not password:
            raise ValidationError('Details not entered.')

        user = None
        try:
            user = User.objects.get(email=email, password=password)
            if user.is_logged_in:
                raise ValidationError('User already logged in.')
        except ObjectDoesNotExist:
            raise ValidationError('User credentials are not correct.')

        user.is_logged_in = True
        data['token'] = uuid4()
        user.token = data['token']
        user.save()
        return data

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'token',
        )

        read_only_fields = (
            'token',
        )


class UserLogoutSerializer(serializers.ModelSerializer):
    token = serializers.CharField()
    status = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        token = data.get("token", None)
        print(token)
        user = None
        try:
            user = User.objects.get(token=token)
            if not user.is_logged_in:
                raise ValidationError("User is not logged in.")
        except Exception as e:
            raise ValidationError(str(e))
        user.is_logged_in = False
        user.token = ""
        user.access_token = ""
        user.save()
        data['status'] = "User is logged out."
        return data

    class Meta:
        model = User
        fields = (
            'token',
            'status',
        )


class TokenExchangeSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=100)
    public_token = serializers.CharField()
    item_id = serializers.CharField(required=False, read_only=True)
    access_token = serializers.CharField(required=False, read_only=True)
    request_id = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        email = None
        public_token = None
        try:
            email = data.get('email')
            public_token = data.get('public_token')
            if not email or not public_token:
                raise ValidationError('Invalid Credentials for Token Exchange')
        except Exception as e:
            raise ValidationError(str(e))

        user = None

        try:
            user = User.objects.get(email=email)
            if user.access_token:
                raise ValidationError('Access token already generated')
        except ObjectDoesNotExist:
            raise ValidationError('Invalid user email')

        exchange_response = {}

        try:
            exchange_response = get_access_token.delay(public_token)
            exchange_response = exchange_response.get()
            user.access_token = exchange_response['access_token']
            user.save()
        except Exception as e:
            raise ValidationError(str(e))
        exchange_response['email'] = email
        exchange_response['public_token'] = public_token
        return exchange_response

    class Meta:
        model = User
        fields = (
            'email',
            'public_token',
            'item_id',
            'request_id',
            'access_token',
        )


class GetTransactionsSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    start_date = serializers.DateField(format="%Y-%m-%d")
    end_date = serializers.DateField(format="%Y-%m-%d")
    transactions = serializers.JSONField(required=False, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        start_date = data.get('start_date', None)
        end_date = data.get('end_date', None)
        try:
            if not email:
                raise ValidationError('Invalid Credentials')
            if not start_date:
                raise ValidationError('Start Date not provided')
            if not end_date:
                raise ValidationError('End date not provided')
        except Exception as e:
            raise ValidationError(str(e))

        start_date = "{:%Y-%m-%d}".format(start_date)
        end_date = "{:%Y-%m-%d}".format(end_date)
        user = None

        try:
            user = User.objects.get(email=email)
            if not user.access_token:
                raise ValidationError('Access Token not generated')
        except ObjectDoesNotExist:
            raise ValidationError('User Does not exist.')
        except Exception as e:
            raise ValidationError(str(e))

        access_token = user.access_token
        output = {}
        transactions = {}

        try:
            transactions = get_transactions.delay(
                access_token, start_date, end_date)
            transactions = transactions.get()
        except plaid.errors.PlaidError as e:
            raise ValidationError(str(e))
        output['email'] = email
        output['start_date'] = start_date
        output['end_date'] = end_date
        output['transactions'] = transactions.get('transactions')
        return output

    class Meta:
        model = User
        fields = (
            'email',
            'start_date',
            'end_date',
            'transactions',
        )


class GetAccountSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    accounts = serializers.JSONField(required=False, read_only=True)
    item = serializers.JSONField(required=False, read_only=True)
    numbers = serializers.JSONField(required=False, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        try:
            if not email:
                raise ValidationError('Invalid Credentials')
        except Exception as e:
            raise ValidationError(str(e))

        user = None

        try:
            user = User.objects.get(email=email)
            if not user.access_token:
                raise ValidationError('Access Token not generated')
        except ObjectDoesNotExist:
            raise ValidationError('User Does not exist.')

        access_token = user.access_token
        accounts = {}

        try:
            accounts = get_accounts.delay(access_token)
            accounts = accounts.get()
        except plaid.errors.PlaidError as e:
            raise ValidationError(str(e))
        accounts['email'] = email
        return accounts

    class Meta:
        model = User
        fields = (
            'email',
            'accounts',
            'item',
            'numbers'
        )


class TransactionUpdateSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    transaction_id = serializers.CharField()
    transaction = serializers.JSONField(required=False, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        transaction_id = data.get('transaction_id', None)
        user = None
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise ValidationError('User Does not exist')

        access_token = user.access_token
        transaction = {}
        try:
            start_date = '{:%Y-%m-%d}'.format(datetime.now() + timedelta(-30))
            end_date = '{:%Y-%m-%d}'.format(datetime.now())
            transactions = get_transactions.delay(
                access_token, start_date, end_date)
            transactions = transactions.get()
            transactions = transactions['transactions']
            transaction = next(
                filter(lambda x: x.get('transaction_id') == transaction_id, transactions))
            if not transaction:
                raise ValidationError('Invalid Transaction')
        except plaid.errors.PlaidError as e:
            raise ValidationError(str(e))
        except Exception as e:
            raise ValidationError(str(e))

        if not transaction.get('pending'):
            send_mail(
                'Transaction Successful',
                'Your Transaction was successful.',
                'noreply@example.com',
                [email],
                fail_silently=True,
            )
        else:
            send_mail(
                'Transaction NOT Successful',
                'Your Transaction was not successful.Currently pending.',
                'noreply@example.com',
                [email],
                fail_silently=True,
            )
        data = {}
        data['email'] = email
        data['transaction_id'] = transaction_id
        data['transaction'] = transaction
        return data

    class Meta:
        model = User
        fields = (
            'email',
            'transaction_id',
            'transaction'
        )
