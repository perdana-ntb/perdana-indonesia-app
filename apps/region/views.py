from django.contrib import messages
from django.shortcuts import redirect, render
# Create your views here.
from django.views.generic import FormView

from orm.club import Branch
from orm.region import Region

from .forms import RegionForm


class RegionFormView(FormView):
    template_name = 'region.html'
    form_class = RegionForm
    success_url = 'region:view'

    def get_object(self):
        try:
            return Region.objects.get(pk=self.request.GET.get('region'))
        except Region.DoesNotExists:
            return None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['regions'] = Region.objects.all()

        if 'region' in self.request.GET:
            ctx['object'] = self.get_object()
        return ctx

    def form_valid(self, form):
        if not 'region' in self.request.GET:
            form.save()
        else:
            obj = self.get_object()
            obj.name = form.cleaned_data['name']
            obj.save()

        return redirect(self.success_url)

    def form_invalid(self, form):
        print(form.errors)
        messages.info(self.request, form.errors)
        return redirect(self.success_url)
