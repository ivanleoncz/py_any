from django.shortcuts import render
from django.views.generic import View


class CetesView(View):

    def get(self, request):
        return render(request, "cetes.html")

    def post(self, request):
        pass
