from django.shortcuts import render
from contact.forms import ContactForm
from contact.models import Contact
from django.http.response import HttpResponse


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Thank you for your message. We will get back to you soon.")