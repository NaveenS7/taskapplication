from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,ListView
from todos.forms import TaskForm,RegistrationForm,LoginForm
from todos.models import Tasks
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django_filters import FilterSet
# Create your views here.

from django import forms


class IndexView(TemplateView):

    template_name="index.html"


class TaskCreateView(View):
    def get(self,request,*args,**kwargs):
        form=TaskForm()
        return render(request,"task-add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=TaskForm(request.POST,files=request.FILES)


        if form.is_valid():
            form.save()
            print("Data saved")
            return redirect("task-list")

        else:
            return render(request,"task-add.html",{"form":form})

class UserFilter(FilterSet):
    class Meta:
        model=Tasks
        fields=["user"]



class TaskListView(ListView):
    model=Tasks
    template_name="task-list.html"
    context_object_name="tasks"

    # def get(self,request,*args,**kwargs):
    #     f=UserFilter(request.GET,queryset=Tasks.objects.all())
    #     return render(request,self.template_name,{"filter":f})          


class TaskDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Tasks.objects.get(id=id)
        return render(request,"task-detail.html",{"tasks":qs})


class TaskDeleteView(View):
        def get(self,request,*args,**kwargs):
            id=kwargs.get("pk")
            qs=Tasks.objects.get(id=id).delete()
            return redirect("task-list")



class TaskEditView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Tasks.objects.get(id=id)
        form=TaskForm(instance=obj)
        return render(request,"task-edit.html",{"form":form})


    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Tasks.objects.get(id=id)
        form=TaskForm(request.POST,instance=obj,files=request.FILES)


        if form.is_valid():
            form.save()
            # Tasks.objects.filter(id=id).update(**form.cleaned_data)
            return redirect("task-list")
            

        else:
            return render(request,"task-edit.html",{"form":form})



class RegistrationView(View):

    def get(self,request,*args,**kw): 
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    
    
    def post(self,request,*args,**kw):
        form=RegistrationForm(request.POST)
        if form.is_valid():

            # form.save()
            User.objects.create_user(**form.cleaned_data)
            return redirect("home")
        else:
            return render(request,"register.html",{"form":form})


class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                 login(request,usr)
                 print(request.user)
                 messages.success(request,"signin success")
                 return redirect("home")
            else:
                messages.error(request,"invalid credentials")


                return render(request,"login.html",{"form":form})  



class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

class TaskHome(TemplateView):
    template_name="taskhome.html"        
        