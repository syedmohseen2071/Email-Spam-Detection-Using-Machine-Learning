from cffi import model
from django.contrib.sessions.backends import file
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .spamemail import validate
from .models import Customer, Admin, Sent, Notification
from .forms import CustomerForm, SentForm, ReplyForm, NotificationForm
from .encrypt_util import *
from django.contrib.auth import logout


# Create your views here.
def index(request):
    return render(request, 'index.html', {})


def customer_registration(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        email = request.POST['email']
        print(form.errors)
        if form.is_valid():
            mob = form.cleaned_data.get('mobile')
            print(mob)
            if Customer.objects.filter(email=email).exists():
                return render(request, "customer_registration.html", {"msg": "This Email Already Exists !"})
            elif Customer.objects.filter(mobile=mob).exists():
                return render(request, "customer_registration.html", {"msg": "This Mobile Number Already Exists !"})
            else:
                try:
                    encryptpass = encrypt(request.POST['password'])
                    data = form.save(commit=False)
                    data.password = encryptpass
                    data.save()
                    return render(request, 'customer_login.html', {"msg": "Registration Successful"})
                except Exception as e:
                    print(e)
                    return render(request, 'customer_registration.html', {"msg": "Registration Not Successful"})
        return render(request, "customer_registration.html", {})
    return render(request, "customer_registration.html", {})


def customer_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        print(email, "", password)
        if Customer.objects.filter(email=email).exists():
            user = Customer.objects.get(email=email)
            if user is not None:
                pwd = decrypt(user.password)
                print(pwd)
                if password == pwd:
                    request.session['email'] = email
                    if user.status == 1:
                        return render(request, 'customer_home.html', {"msg": email})
                    else:
                        return render(request, "active.html", {"msg": "Please Activate Your Account"})
                else:
                    return render(request, "customer_login.html", {"msg": "Wrong Password"})
            else:
                return render(request, "customer_login.html", {"msg": "hii"})
        return render(request, "customer_login.html", {"msg": "This Email Not Registered"})
    return render(request, "customer_login.html", {})


def activate_request(request):
    email = request.session["email"]
    de = Customer.objects.get(email=email)
    de.status = 3
    de.save()
    return redirect('/customerlogin')


def activate(request, email):
    de = Customer.objects.get(email=email)
    de.status = 1
    de.save()
    return redirect('/view_customer')


def deactivate(request, email):
    de = Customer.objects.get(email=email)
    de.status = 0
    de.save()
    request.session.flush()
    return redirect('/customerlogin')


# def customer_login(request):
#     if request.method == "POST":
#         email = request.POST["email"]
#         password = request.POST["password"]
#         print(email, "", password)
#         login = Customer.objects.filter(email=email, password=password)
#         if login.exists():
#             request.session['email'] = email
#             if Customer.objects.filter(status=1):
#                 return render(request, 'customer_home.html', {"msg": email})
#             else:
#                 return render(request, 'subscribe.html', {"email": email})
#         else:
#             return render(request, "customer_login.html", {"msg": "Email And Password Does Not Match"})
#     return render(request, "customer_login.html", {})


def customer_home(request):
    return render(request, "customer_home.html", {})


def customer_logout(request):
    request.session.flush()
    logout(request)
    return redirect('/customerlogin')


def customer_is_login(request):
    if request.session.__contains__("email"):
        return True
    else:
        return False


def customer_change_password(request):
    email = request.session["email"]
    if customer_is_login(request):
        if request.method == "POST":
            password = encrypt(request.POST['password'])
            print(password)
            pas = decrypt(password)
            print(pas)
            new_password = request.POST["new_password"]
            print(new_password)
            try:
                print("hii")
                user = Customer.objects.get(email=email)
                pwd = user.password
                opwd = decrypt(pwd)
                print(opwd)
                print("hello")
                if pas == opwd:
                    encryptpass = encrypt(request.POST['new_password'])
                    print(encryptpass)
                    user.password = encryptpass
                    print("hello2")
                    user.save()
                    return redirect('/customerlogin')
                else:
                    return render(request, "customer_change_password.html",
                                  {"msg": "Old Password Is Wrong", "email": email})
            except Exception as e:
                print(e)
                return render(request, "customer_change_password.html", {"msg": "Invalid Data", "email": email})
        else:
            return render(request, "customer_change_password.html", {"email": email})


def customer_profile(request):
    email = request.session["email"]
    print(email)
    customer = Customer.objects.get(email=email)
    print(customer)
    return render(request, "customer_profile.html", {"customer": customer})


def customer_edit(request, id):
    customer = Customer.objects.get(id=id)
    return render(request, "customer_edit.html", {"x": customer})


def customer_update(request):
    if request.method == "POST":
        print("error:")
        id = request.POST["id"]
        print("hello")
        users = Customer.objects.get(id=id)
        users = CustomerForm(request.POST, instance=users)
        print("error:", users.errors)
        if users.is_valid():
            print("error:", users.errors)
            users.save()
        return redirect("/customer_profile")
    return redirect("/customer_profile")


def customer_delete(request, id):
    customer = Customer.objects.get(id=id)
    request.session.flush()
    customer.delete()
    return redirect("/customerlogin")


# def send_email(request):
#     email = request.session['email']
#     cus = Customer.objects.get(email=email)
#     print("hi1")
#     if request.method == "POST":
#         print("hi2")
#         form = SentForm(request.POST, request.FILES)
#         print(form.errors)
#         try:
#             if form.is_valid():
#                 to = form.cleaned_data["to_email"]
#                 print(to)
#                 if Sent.objects.filter(from_email=to):
#                     return render(request, "send_email.html", {"cus": cus, "msg": "You Cant Send Message To Your Email"})
#                 elif Customer.objects.filter(email=to).exists():
#                     form.save()
#                     return render(request, "send_email.html", {"cus": cus, "msg": "Email Sent"})
#                 return render(request, "send_email.html", {"cus": cus, "msg": "Email Not Registered"})
#         except Exception as e:
#             print(e)
#             return render(request, "send_email.html", {"cus": cus, "msg": "Subject Not Sent"})


# return render(request, "send_email.html", {"cus": cus})
def send_email(request):
    if 'email' in request.session:
        email = request.session['email']
        try:
            cus = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return redirect('customerlogin')
        try:
            if request.method == "POST":
                form = SentForm(request.POST, request.FILES)
                if form.is_valid():
                    to_email = form.cleaned_data["to_email"]
                    if to_email == email:
                        return render(request, "send_email.html",
                                      {"cus": cus, "msg": "You can't send an email to yourself"})
                    elif Customer.objects.filter(email=to_email).exists():
                        body = form.cleaned_data["body"]
                        print(body)
                        resp = validate(body)
                        print(resp)
                        obj = Sent()
                        obj.to_email = to_email
                        obj.status = resp
                        obj.from_email = form.cleaned_data["from_email"]
                        obj.body = body
                        obj.subject = form.cleaned_data["subject"]
                        obj.file = form.cleaned_data["file"]
                        obj.save()
                        return render(request, "send_email.html", {"cus": cus, "msg": "Email Sent", "form": form})
                    else:
                        return render(request, "send_email.html",
                                      {"cus": cus, "form": form, "msg": "This Email Not Exists"})
                else:
                    return render(request, "send_email.html", {"cus": cus, "form": form, "msg": "error"})
            else:
                form = SentForm()
                return render(request, "send_email.html", {"cus": cus, "form": form})
        except Exception as e:
            print(str(e))
            form = SentForm()
            return render(request, "send_email.html", {"cus": cus, "form": form, "msg": str(e)})
    else:
        return redirect('customerlogin')


def admin_login(request):
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]
        login = Admin.objects.filter(email=email, password=password)
        if login.exists():
            request.session["email"] = email
            return render(request, "admin_home.html", {"msg": "Login Successful"})
        else:
            return render(request, "admin_login.html", {"msg": "Email And Password Does Not Match"})
    return render(request, "admin_login.html", {})


def admin_home(request):
    return render(request, "admin_home.html", {})


def admin_logout(request):
    request.session.flush()
    return redirect('/admin_login')


def view_customer(request):
    customer = Customer.objects.all()
    return render(request, "view_customer.html", {"customer": customer})


def is_login(request):
    if request.session.__contains__("email"):
        return True
    else:
        return False


def admin_change_password(request):
    email = request.session["email"]
    print(email)
    if is_login(request):
        if request.method == "POST":
            email = request.session["email"]
            password = request.POST["password"]
            newpassword = request.POST["newpassword"]
            try:
                user = Admin.objects.get(email=email, password=password)
                user.password = newpassword
                user.save()
                return redirect('/admin_login')
            except Exception as e:
                print(e)
                return render(request, "admin_change_password.html", {"msg": "Invalid Data", "email": email})
        return render(request, "admin_change_password.html", {"email": email})
    return render(request, "admin_change_password.html", {"email": email})


def admin_delete_customer(request, id):
    customer = Customer.objects.get(id=id)
    customer.delete()
    return redirect("/view_customer")


def inbox(request):
    email = request.session['email']
    cus = Customer.objects.get(email=email)
    sm = Sent.objects.filter(to_email=cus.email)
    return render(request, "inbox.html", {"sm": sm})


def reply(request, id):
    rep = Sent.objects.get(id=id)
    if request.method == "POST":
        form = ReplyForm(request.POST, instance=rep)
        print(form.errors)
        if form.is_valid():
            form.save()
            return render(request, "reply.html", {"rep": rep, "msg": "Reply Sent"})
        return render(request, "reply.html", {"rep": rep, "msg": "Reply Not Sent"})
    return render(request, "reply.html", {"rep": rep})


def sent(request):
    email = request.session['email']
    cus = Customer.objects.get(email=email)
    sm = Sent.objects.filter(from_email=cus.email)
    return render(request, "sent.html", {"sm": sm})


def active(request, id):
    customer = Customer.objects.get(id=id)
    return render(request, "active.html", {"x": customer})


def add_notification(request):
    if request.method == "POST":
        form = NotificationForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return render(request, "add_notification.html", {"msg": "Notification Added"})
        return render(request, "add_notification.html", {"msg": "Notification Not Added"})
    return render(request, "add_notification.html", {})


def view_notification(request):
    obj = Notification.objects.all()
    return render(request, 'view_notification.html', {'obj': obj})


def customer_view_notification(request):
    obj = Notification.objects.all()
    return render(request, 'customer_view_notification.html', {'obj': obj})


def delete_notification(request, id):
    obj = Notification.objects.get(id=id)
    obj.delete()
    return redirect('/view_notification')
