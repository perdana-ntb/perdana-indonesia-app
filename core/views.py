from django.shortcuts import redirect, render
from django.views import View

# Create your views here.


class IndexView(View):
    def get(self, request):
        return redirect('/login')
