from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.generic import View

from .forms import CetesForm

from .utils import calculate_cetes


class CetesView(View):

    form_class = CetesForm
    template = "cetes.html"

    def get(self, request):
        projection = request.session.get('projection', False)
        if projection:
            del(request.session['projection'])
        return render(request, self.template, {'projection': projection})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            result = calculate_cetes(int(request.POST["investment"]), int(request.POST["term"]),
                                                                      int(request.POST["reinvest"]))
            request.session["projection"] = result
            return redirect(request.path)
        return HttpResponseBadRequest()
