# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
# Create your views here.
from django.views.generic import (DetailView, FormView, ListView, TemplateView,
                                  UpdateView, View)

from orm.club import Club
from orm.member import Member

from .forms import MemberForm


class LoginView(TemplateView):
    template_name = 'login.html'


class MemberListView(ListView):
    model = Member
    queryset = Member.objects.all()
    context_object_name = 'members'
    template_name = 'member_list.html'


class MemberDetailView(DetailView):
    model = Member
    template_name = 'member_detail.html'


class MemberAddFormView(FormView):
    form_class = MemberForm
    template_name = 'member_add.html'
    success_url = 'organization:members'

    def get_context_data(self, **kwargs):
        context = super(MemberAddFormView, self).get_context_data(**kwargs)
        context['clubs'] = Club.objects.all()
        return context

    def form_valid(self, form):
        try:
            form.cleaned_data.pop('photo')
        except KeyError:
            pass

        user_data = {
            'username':  form.cleaned_data.pop('username'),
            'password': form.cleaned_data.pop('password'),
            'first_name': form.cleaned_data.pop('first_name'),
            'last_name': form.cleaned_data.pop('last_name'),
            'email': form.cleaned_data.pop('email')
        }
        user = User.objects.create_user(**user_data)

        # try:
        #     lead = form.cleaned_data.pop('lead') == '1'
        # except KeyError:
        #     form.cleaned_data['lead'] = False

        club_id = form.cleaned_data.pop('club_id')
        club = get_object_or_404(Club, pk=club_id)
        member = Member.objects.create(user=user, club=club, **form.cleaned_data)

        try:
            photo = self.request.FILES['photo']
            member.photo = photo
            member.save()
        except KeyError:
            pass

        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.info(self.request, form.errors)
        return self.get(self.request)


class MemberEditFormView(FormView):
    form_class = MemberForm
    template_name = 'member_edit.html'
    success_url = 'organization:members'

    def get_object(self, **kwargs):
        return get_object_or_404(Member, **self.kwargs)

    def get_context_data(self, **kwargs):
        context = super(MemberEditFormView, self).get_context_data(**kwargs)
        context['object'] = self.get_object()
        context['clubs'] = Club.objects.all()
        return context

    def form_valid(self, form, **kwargs):
        object = self.get_object()
        try:
            form.cleaned_data.pop('password')
            form.cleaned_data.pop('photo')
        except KeyError:
            pass
        user_data = {
            'username':  form.cleaned_data.pop('username'),
            'first_name': form.cleaned_data.pop('first_name'),
            'last_name': form.cleaned_data.pop('last_name'),
            'email': form.cleaned_data.pop('email')
        }
        user = User.objects.filter(pk=object.user.pk).update(**user_data)

        club_id = form.cleaned_data.pop('club_id')
        club = get_object_or_404(Club, pk=club_id)

        try:
            photo = self.request.FILES['photo']
            object.photo = photo
            object.save()
        except KeyError:
            pass

        Member.objects.filter(pk=object.pk).update(user=object.user, club=club, **form.cleaned_data)
        return redirect(self.success_url)

    def form_invalid(self, form, **kwargs):
        messages.info(self.request, form.errors)
        return redirect('organization:member_edit', pk=self.kwargs.get('pk'))


class MemberDeleteView(View):
    def get(self, request, pk):
        member = get_object_or_404(Member, pk=pk)
        if member.delete():
            member.user.delete()

        return redirect('organization:members')
