from django.shortcuts import render
from .models import Remedy

def filtered_remedies(request, severity_level):
    remedies = Remedy.objects.filter(severity=severity_level)
    return render(request, 'remedies.html', {'remedies': remedies})

