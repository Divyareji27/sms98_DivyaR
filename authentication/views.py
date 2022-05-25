from urllib import request
from django.urls import reverse
import json
import requests
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout,authenticate
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.template import RequestContext

from authentication.EmailBackEnd import EmailBackEnd
from authentication.models import Courses, CustomUser, SessionYearModel


def showDemoPage(request):
    return render(request, 'demo.html')

def showLoginPage(request):
    return render(request,'login_page.html')

def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method not allowed!</h2>")
    else:
        captcha_token=request.POST.get("g-recaptcha-response")
        cap_url="https://www.google.com/recaptcha/api/siteverify"
        cap_secret="6LdkS94fAAAAADDNaCcigTmBG7ijiJrTR0_6UaE5"
        cap_data={"secret":cap_secret,"response":captcha_token}
        cap_server_response=requests.post(url=cap_url,data=cap_data)
        cap_json=json.loads(cap_server_response.text)

        if cap_json['success']==False:
            messages.error(request,"Invalid Captcha! Try Again!")
            return HttpResponseRedirect("/")

        user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type=="1":
               return HttpResponseRedirect('/admin_home')
            elif user.user_type=="2":
               return HttpResponseRedirect("staff_home")
            else:
                return HttpResponseRedirect("student_home")
        else:
            messages.error(request,"Invalid Login Details!")
            return HttpResponseRedirect("/")

def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User :"+request.user.email+" usertype: "+request.user.user_type)
    else:
        return HttpResponse("Please login first!")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup_admin(request):
    return render(request,"signup_admin_page.html")

def do_admin_signup(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    email=request.POST.get("email")
    
    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=1)
        user.save()
        messages.success(request,"Successfully Created Admin!")
        return HttpResponseRedirect(reverse("show_login"))
    except:
            messages.error(request,"Failed To Create Admin")
            return HttpResponseRedirect(reverse("show_login"))


def signup_staff(request):
    return render(request,"signup_staff_page.html")

def do_staff_signup(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")
    address=request.POST.get("address")

    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=2)
        user.staffs.address=address
        user.save()
        messages.success(request,"Successfully Created Staff")
        return HttpResponseRedirect(reverse("show_login"))
    except:
        messages.error(request,"Failed to Create Staff")
        return HttpResponseRedirect(reverse("show_login"))

def signup_student(request):
    courses=Courses.objects.all()
    session_years=SessionYearModel.object.all()
    return render(request,"signup_student_page.html",{"courses":courses,"session_years":session_years})

def do_student_signup(request):
   first_name = request.POST.get("first_name")
   last_name = request.POST.get("last_name")
   username = request.POST.get("username")
   email = request.POST.get("email")
   password = request.POST.get("password")
   address = request.POST.get("address")
   session_year_id = request.POST.get("session_year")
   course_id = request.POST.get("course")
   sex = request.POST.get("sex")

   profile_pic = request.FILES['profile_pic']
   fs = FileSystemStorage()
   filename = fs.save(profile_pic.name, profile_pic)
   profile_pic_url = fs.url(filename)

    #try:
   user = CustomUser.objects.create_user(username=username, password=password, email=email, last_name=last_name,
                                          first_name=first_name, user_type=3)
   user.students.address = address
   course_obj = Courses.objects.get(id=course_id)
   user.students.course_id = course_obj
   session_year = SessionYearModel.object.get(id=session_year_id)
   user.students.session_year_id = session_year
   user.students.gender = sex
   user.students.profile_pic = profile_pic_url
   user.save()
   messages.success(request, "Successfully Added Student")
   return HttpResponseRedirect(reverse("show_login"))
    #except:
     #   messages.error(request, "Failed to Add Student")
      #  return HttpResponseRedirect(reverse("show_login"))