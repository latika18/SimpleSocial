from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import (LoginRequiredMixin, PermissionRequiredMixin)
from django.contrib import messages

from django.urls import reverse
from django.db import IntegrityError
from django.views import generic 

from django.shortcuts import get_object_or_404
from .models import Group, GroupMember
from . import models

class CreateGroup(LoginRequiredMixin,generic.CreateView):
 	fields = ('name','description')
 	model = Group

class SingleGroup(generic.DetailView):
 	model = Group

class ListGroups(generic.ListView):
 	model = Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):

 	def get_redirect_url(self,*args,**kwargs):
 		return reverse("groups:single",kwargs={"slug":self.kwargs.get("slug")})

 	def get(self,request,*args,**kwargs):
 		group = get_object_or_404(Group,slug=self.kwargs.get("slug"))

 		try:
 			GroupMember.objects.create(user=self.request.user,group=group)
 		except IntegrityError:
 			messages.warning(self.request,('Warning already a member of {}'.format(group.name)))
 		else:
 			messages.success(self.request,'You are now a member!')

 		return super().get(request,*args,**kwargs)


class LeaveGroup(LoginRequiredMixin,generic.RedirectView):

	def get_redirect_url(self,*args,**kwargs):
 		return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

	def get(self,request,*args,**kwargs):
 		pass





















