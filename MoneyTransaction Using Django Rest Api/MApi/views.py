from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view,permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UserRegistrationSerializer,UserLoginSerializer ,WalletSerializer,TransactionSerializer
from django.shortcuts import get_object_or_404
from .models import User,Wallet,Transactions
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from django.utils import timezone
from django.contrib.auth import authenticate


def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


## user register ##
@api_view(['POST'])
def register_user(request):
    phone=request.data.get('phone_number')
    if User.objects.filter(phone_number=phone).exists():
        return Response('phone number is exists')
    else:
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    phone_number = serializer.validated_data.get('phone_number')
    password = serializer.validated_data.get('password')

    if phone_number is not None and password is not None:
        user = authenticate(phone_number=phone_number, password=password)

        if user is not None:
            tokens = get_tokens_for_user(user)
            response_data = {
                'msg': 'Login Success',
                'tokens': tokens
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors': ['Phone number or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'msg': 'Enter the Data'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_wallet(request, id):
    phone = request.data.get('phone_number')
    user = get_object_or_404(User, pk=id)

    if user.phone_number == phone and not Wallet.objects.filter(user=user).exists():
        serializer = WalletSerializer(data=request.data)
        serializer.user = user
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({"message": "Wallet created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "A wallet for this user already exists"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_money(request, id):
    phone = request.data.get('reciver_phone_number')
    amount = float(request.data.get('amount'))
    sender_phone = get_object_or_404(User, pk=id).phone_number

    if phone == sender_phone:
        return Response({"message": "Not allowed to send money to the same phone number"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        rec_wallet = Wallet.objects.get(phone_number=phone)
        send_wallet = Wallet.objects.get(phone_number=sender_phone)
    except Wallet.DoesNotExist:
        return Response({"message": "No account found with the provided phone number"}, status=status.HTTP_400_BAD_REQUEST)
    except Wallet.MultipleObjectsReturned:
        return Response({"message": "Multiple accounts found with the provided phone number"}, status=status.HTTP_400_BAD_REQUEST)

    if send_wallet.balance >= amount:
        rec_wallet.balance += amount
        rec_wallet.save()
        send_wallet.balance -= amount
        send_wallet.save()

        transaction = Transactions.objects.create(
            wallet=send_wallet,
            sender_phone=send_wallet.phone_number,
            receiver_phone=rec_wallet.phone_number,
            amount=amount,
            date_time=timezone.now()
        )
        serializer = TransactionSerializer(transaction)
        return Response({"data": serializer.data, "message": "Amount transferred successfully"}, status=status.HTTP_201_CREATED)
    
    return Response({"message": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)



## for bank ##
@api_view(['POST'])
@permission_classes([IsAuthenticated])

def add_money(request,wallet_id):
        amount=int(request.data.get('amount'))
        wallet=get_object_or_404(Wallet,pk=wallet_id)
        wallet+=amount
        wallet.save()
        return Response({"amount added succussfully"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])

def transactions(request,id):
        user=get_object_or_404(User,pk=id)
        wallet=get_object_or_404(Wallet,user=user)
        data=Transactions.objects.filter(wallet=wallet)
        serializer=TransactionSerializer(data,many=True)
        return Response(serializer.data)