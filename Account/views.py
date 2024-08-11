from rest_framework.views import APIView
from .models import Account, User
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from django.shortcuts import get_object_or_404
from rest_framework import status
import random
import string
from django.utils import timezone
import datetime
from django.core.mail import send_mail
from django.template.loader import get_template
from rest_framework.permissions import IsAuthenticated
from .serializers import SignUpSerializer
from backend.settings import EMAIL_HOST_USER
from rest_framework_simplejwt.tokens import RefreshToken
import after_response


def rand_ascii(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))


@after_response.enable
def send_email(title, html_content, receiver):
    try:
        # return
        res = send_mail(title, '', EMAIL_HOST_USER, receiver, fail_silently=False, html_message=html_content)
        print(f"send mail to {receiver}: ", title, f"\nstatus: {res}")
    except Exception as e:
        print(f"error in sending email to {receiver} for reason: {str(e)}")



class UserSecThrottle(UserRateThrottle):
    scope = 'signup'


class SignUp(APIView):
    throttle_classes = [UserSecThrottle]

    def post(self, request):
        try:
            ser = SignUpSerializer(data=request.data)
            if not ser.is_valid():
                return Response({"message": "مقادیر ایمیل یا پسورد قابل قبول نیست", "detail": f"مقادیر نادرست برای: {' ,'.join(ser.errors)}"}, status=status.HTTP_400_BAD_REQUEST)
            email = request.data.get('email')
            username = request.data.get('username')
            password = request.data.get('password')

            if User.objects.filter(email=email).exists():
                return Response({"message": "این ایمیل قبلا ثبت شده"}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(username=username).exists():
                return Response({"message": "این نام کاربری قبلا ثبت شده"}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(username=username, email=email, password=password)

            token = rand_ascii(100)
            Account(user=user, email_verify_token=token, email_verify_generate_time=timezone.now()).save()
            refresh = RefreshToken.for_user(user)

            htmly = get_template('email-confirmation.html')
            d = {'token': token, 'id': user.id}
            html_content = htmly.render(d)
            send_email.after_response("تایید ایمیل Amoot", html_content, [user.email])

            return Response({"access": str(refresh.access_token), "refresh": str(refresh)}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)



class CreateEmailToken(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            user = request.user
            account = Account.objects.get(user=user)
            if account.email_verified:
                return Response({"message": "ایمیل شما قبلا تایید شده"}, status=status.HTTP_400_BAD_REQUEST)
            if account.email_verify_generate_time and account.email_verify_generate_time + datetime.timedelta(minutes=2) > timezone.now():
                return Response({"message": "شما هر دو دقیقه یکبار قادر به درخواست ایمیل تایید هستید.",
                                 "detail": "لطفا کمی صبر کرده و مجددا امتحان نمایید."},
                                status=status.HTTP_400_BAD_REQUEST)
            token = rand_ascii(100)
            account.email_verify_token = token
            account.email_verify_generate_time = timezone.now()
            account.save()
            htmly = get_template('email-confirmation.html')
            d = {'token': token, 'id': user.id}
            print(d)
            html_content = htmly.render(d)
            send_email.after_response("تایید ایمیل Amoot", html_content, [user.email])
            return Response({"message": "لینک تایید ایمیل برای شما ارسال شد.", "detail": "بخش اسپم را درصورت عدم ارسال بررسی نمایید."})

        except Exception as e:
            print(e)
        

class VerifyEmail(APIView):

    def post(self, request):
        try:
            token = request.data.get("token")
            userId = request.data.get("id")
            try:
                account = Account.objects.get(user__id=userId, email_verify_token=token)
            except:
                return Response({"message": "ایمیل مورد نظر یافت نشد", "detail": "ممکن است قبلا تایید شده باشد."}, status=status.HTTP_400_BAD_REQUEST)
            account.email_verified = True
            account.email_verify_token = None
            account.save()
            return Response()
        except Exception as e:
            print(e)
        

class ForgetPassword(APIView):
    throttle_classes = [UserSecThrottle]

    def post(self, request):
        try:
            try:
                user = User.objects.get(email=request.data.get("email"))
                account = Account.objects.get(user=user)
            except:
                return Response({"message": "ایمیل وارد شده وجود ندارد"}, status=status.HTTP_400_BAD_REQUEST)

            if account.reset_token_created_at and account.reset_token_created_at + datetime.timedelta(minutes=5) > timezone.now():
                return Response({"message": "هر پنج دقیقه یکبار قادر به درخواست بازیابی رمز عبور هستید"}, status=status.HTTP_400_BAD_REQUEST)

            token = rand_ascii(100)
            account.reset_password_token = token
            account.reset_token_created_at = timezone.now()

            htmly = get_template('email-forget.html')
            d = {'token': token, 'id': user.id}
            html_content = htmly.render(d)
            send_email.after_response("فراموشی رمز عبور Amoot", html_content, [user.email])
            account.save()
            return Response()

        except Exception as e:
            print(e)
        

class SetPassword(APIView):

    def post(self, request):
        try:
            token = request.data.get("token")
            userId = request.data.get("id")
            newPass = request.data.get("password")

            try:
                user = User.objects.get(id=userId)
                account = Account.objects.get(reset_password_token=token, user=user)
            except:
                return Response({"message": "لینک فراموشی رمز منقضی یا استفاده شده, لطفا مجددا درخواست لینک بازنشانی رمز کنید."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(newPass)
            account.reset_password_token = None
            user.save()
            account.save()

            return Response()

        except Exception as e:
            print(e)        



class UserInfo(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            account = get_object_or_404(Account, user=self.request.user)
            return Response({"data": {
                    "email_verified": account.email_verified,
                    "username": account.user.username,
                    "email": account.user.email,
                    }
                }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
