import json
from django.shortcuts import render, get_object_or_404
from django.urls  import reverse
from django.views.generic import TemplateView, View
from users.forms import UserRegisterForm, LoginForm
from .models import User, TokenGenerator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.core.mail import EmailMultiAlternatives 
from django.template.loader import render_to_string


class SignUpView(TemplateView):
    template_name = 'account/signup.html'


    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        else:
            form = UserRegisterForm()
            return render(self.request, self.template_name, {'form': form})


    def post(self, *args, **kwargs):
        form = UserRegisterForm(self.request.POST)
        if form.is_valid():
            try: 
                first_name = self.request.POST['first_name']
                last_name = self.request.POST['last_name']
                email = self.request.POST['email']
                user = form.save()
                token = user.generate_token()
                url = self.request.build_absolute_uri(reverse('verify_token',args=(token.token,)))
                html_content = render_to_string('account/dummy.html',{'url':url, 'full_name': first_name+" "+last_name, 'email': email})
                subject, from_email, to = 'Atrax Verification Email', settings.EMAIL_HOST_USER, [email]
                text_content = "yes"
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return HttpResponseRedirect(reverse('verify_email'))
            except IntegrityError as e:
                context ={
                    'error_messages' : 'Something went wrong please try again.',
                }
                return render(self.request, self.template_name, context)
        return render(self.request, self.template_name, {'form': form})


class VerifyTokenView(TemplateView):


    def get(self, *args, **kwargs):
        form = LoginForm()
        token = TokenGenerator.objects.filter(token=kwargs.get('token'), is_used=False)
        if token.exists():  
            token_obj = token.first()
            user = User.objects.get(email=token_obj.user)
            user.is_confirmed = True
            user.save()
            token_obj.is_used = True 
            token_obj.save()
            TokenGenerator.objects.filter(user=user,is_used=False).delete()
            return render(self.request, 'portal/index.html', {'form': form})
        return render(self.request,'portal/index.html', {'error_messages' : 'Token has already expired/already used.', 'form': form})


    def post(self, *args, **kwargs):
        form = LoginForm(self.request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('index'))
        return render(self.request, 'portal/index.html', {'form':form})


class LogoutView(View):
    def get(self, *args, **kwargs):
        logout(self.request)
        return HttpResponseRedirect(reverse('index'))


class VerifyEmailView(TemplateView):
    template_name = 'account/verify_email.html'


class TermsAndConditionView(TemplateView):
    template_name = 'account/terms_and_conditions.html'