from django.shortcuts import render

# Create your views here.

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
#from customuser.models import user_type, User
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required

from .forms import CustomerSignUpForm, LoginForm,SellerSignUpForm,UpdateProfile
from .models import Profile, User,CustomerAppointments
from django.http import HttpResponse  
from django.shortcuts import render, redirect  
from django.contrib.auth import login, authenticate ,logout 
 
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes,force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token
from django.core.mail import EmailMessage   

def CustomerSignUpView(request):  
    if request.method == 'POST':  
        form = CustomerSignUpForm(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration')  
    else:  
        form = CustomerSignUpForm 
    return render(request, 'signup_form.html', {'form': form}) 

# class CustomerSignUpView(CreateView):
#     model = User
#     form_class = CustomerSignUpForm
#     template_name = 'signup_form.html'

#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'customer'
#         return super().get_context_data(**kwargs)

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('students:quiz_list')

# class SellerSignUpView(CreateView):
#     model = User
#     form_class = SellerSignUpForm
#     template_name = 'signup_form.html'

#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'seller'
#         return super().get_context_data(**kwargs)

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('teachers:quiz_change_list')

def SellerSignUpView(request):  
    if request.method == 'POST':  
        form = SellerSignUpForm(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration')  
    else:  
        form = CustomerSignUpForm 
    return render(request, 'signup_form.html', {'form': form}) 

def activate(request, uidb64, token):  
    #User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!') 

def loginUser(request):
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None and user.is_active and user.is_seller:
                #if user.is_active and user.is_seller:
                 login(request, user)
                 return HttpResponse('you are logged in')
                #message = f'Hello {user.username}! You have been logged in'
            elif user is not None and user.is_active and user.is_customer:
                login(request,user)
                return HttpResponse('you are logged in as a customer')
            else:
                message = 'Login failed!'
    return render(
        request, 'login.html', context={'form': form, 'message': message})

def logout_user(request):
    logout(request)
    return HttpResponse('you are logged out')
@login_required
def profilepage(request):
    return render(request,'profile.html')

def index(request):
    item_list= Profile.objects.all()
    #template = loader.get_template('food/index.html')
    context = {
        'item_list':item_list
    }
    #if we want to use line 1 we have to write it
    #return HttpResponse(template.render(context,request))

    return render(request,'index.html',context)

def updateprofile(request):
    item=Profile.objects.get(user = request.user)
    form = UpdateProfile(request.POST or None,instance=item)
    obj = Profile
    if form.is_valid():
        # obj=form.save()
        obj=form.save(commit=False)
        obj.user = request.user
        obj.save()
        return HttpResponse('profile is updated')

    return render(request,'profile_update_form.html',{'form':form})

def home(request):
    return render(request,'home/base.html')

def details(request,username):
    hi = User.objects.get(username = username)
    prof = Profile.objects.filter(user=hi).first()
    context = {
            'prof':prof,
        }
    return render(request,'details.html',context)


def Customer_Appoinment(request,username):
    hi = User.objects.get(username = username)
    #obj = CustomerAppointments(customer = request.user)
    obj = CustomerAppointments.objects.get(customer = request.user)
    obj.appnts.add(hi)
    #obj.appnts.add(hi)
    # obj.user=request.user
    
    #obj.save()

    return redirect('customuser:index')

