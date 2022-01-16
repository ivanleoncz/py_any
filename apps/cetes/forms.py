from django import forms


class CetesForm(forms.Form):
    investment = forms.IntegerField()
    term = forms.IntegerField()
    reinvest = forms.IntegerField()
