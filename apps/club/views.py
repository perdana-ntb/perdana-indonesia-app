from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
# Create your views here.
from django.views.generic import (DetailView, FormView, ListView, TemplateView,
                                  UpdateView, View)

from orm.club import Club

from .forms import ClubForm


# Create your views here.
class ClubListView(ListView):
    model = Club
    queryset = Club.objects.all()
    context_object_name = 'clubs'
    template_name = 'club_list.html'


class ClubAddFormView(FormView):
    form_class = ClubForm
    template_name = 'club_add.html'
    success_url = 'club:list'

    def form_valid(self, form):
        object = form.save(commit=False)
        try:
            form.cleaned_data.pop('logo')
            object.logo = self.request.FILES['logo']
        except KeyError:
            pass

        object.save()
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.info(self.request, form.errors)
        return redirect(self.success_url)


class ClubEditFormView(FormView):
    form_class = ClubForm
    template_name = 'club_edit.html'
    success_url = 'club:list'

    def get_object(self, **kwargs):
        return get_object_or_404(Club, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(ClubEditFormView, self).get_context_data(**kwargs)
        context['object'] = self.get_object()
        return context

    def form_valid(self, form):
        object = self.get_object()
        try:
            form.cleaned_data.pop('logo')
            object.logo = self.request.FILES['logo']
        except KeyError:
            pass
        object.save()

        Club.objects.filter(pk=object.pk).update(**form.cleaned_data)
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.info(self.request, form.errors)
        print(form.errors)
        return redirect(self.success_url)


class CLubDeleteView(View):
    def get(self, request, pk):
        club = get_object_or_404(Club, pk=pk)
        club.delete()
        return redirect('club:list')


# class ClubLeadSelectFormView(FormView):
#     form_class = ClubLeadForm
#     template_name = 'select_lead.html'
#     success_url = 'organization:clubs'

#     def get_object(self, **kwargs):
#         return get_object_or_404(Club, pk=self.kwargs.get('pk'))

#     def get_context_data(self, **kwargs):
#         context = super(ClubLeadSelectFormView, self).get_context_data(**kwargs)
#         context['object'] = self.get_object()
#         context['members'] = Member.objects.filter(club=self.get_object())
#         return context

#     def form_valid(self, form, **kwargs):
#         member = get_object_or_404(Member, pk=form.cleaned_data['member_id'])
#         club = self.get_object()
#         club.lead = member
#         club.save()
#         return redirect(self.success_url)

#     def form_invalid(self, form):
#         messages.info(self.request, form.errors)
#         return self.get(self.request)


class ClubDetailView(DetailView):
    model = Club
    template_name = 'club_detail.html'
