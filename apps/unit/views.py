from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
# Create your views here.
from django.views.generic import (DetailView, FormView, ListView, TemplateView,
                                  UpdateView, View)

from orm.club import Unit

from .forms import UnitForm


# Create your views here.
class UnitListView(ListView):
    model = Unit
    queryset = Unit.objects.all()
    context_object_name = 'units'
    template_name = 'unit_list.html'


class UnitAddFormView(FormView):
    form_class = UnitForm
    template_name = 'unit_add.html'
    success_url = 'unit:list'

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


class UnitEditFormView(FormView):
    form_class = UnitForm
    template_name = 'unit_edit.html'
    success_url = 'unit:list'

    def get_object(self, **kwargs):
        return get_object_or_404(Unit, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(UnitEditFormView, self).get_context_data(**kwargs)
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

        Unit.objects.filter(pk=object.pk).update(**form.cleaned_data)
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.info(self.request, form.errors)
        print(form.errors)
        return redirect(self.success_url)


class UnitDeleteView(View):
    def get(self, request, pk):
        unit = get_object_or_404(Unit, pk=pk)
        unit.delete()
        return redirect('unit:list')


# class UnitLeadSelectFormView(FormView):
#     form_class = UnitLeadForm
#     template_name = 'select_lead.html'
#     success_url = 'organization:units'

#     def get_object(self, **kwargs):
#         return get_object_or_404(Unit, pk=self.kwargs.get('pk'))

#     def get_context_data(self, **kwargs):
#         context = super(UnitLeadSelectFormView, self).get_context_data(**kwargs)
#         context['object'] = self.get_object()
#         context['members'] = Member.objects.filter(unit=self.get_object())
#         return context

#     def form_valid(self, form, **kwargs):
#         member = get_object_or_404(Member, pk=form.cleaned_data['member_id'])
#         unit = self.get_object()
#         unit.lead = member
#         unit.save()
#         return redirect(self.success_url)

#     def form_invalid(self, form):
#         messages.info(self.request, form.errors)
#         return self.get(self.request)


class UnitDetailView(DetailView):
    model = Unit
    template_name = 'unit_detail.html'
