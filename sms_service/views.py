from django.http import HttpResponse
from django.shortcuts import render
from .utility import send_sms


from .forms import SendSMSForm


def broadcast_sms(request):
    if request.method == "POST":
        message_to_broadcast = request.POST["message"]
        recipient_number = request.POST["phone_number"]
        response = send_sms(message_to_broadcast, recipient_number)
        return HttpResponse(response, status=200, content_type="text/html; charset=utf-8")

    if request.method == "GET":
        form = SendSMSForm()
        return render(request, "send_sms.html", context={"form": form})
