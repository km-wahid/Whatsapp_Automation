# views/api.py
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext as _
from web.models import UserSession, SenderID
from web.views import send_whatsapp_message     
import json


@csrf_exempt
def send_message_api(request):
    if request.method != "POST":
        return JsonResponse({"error": _("Only POST method is allowed")}, status=405)

   
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": _("Invalid JSON format")}, status=400)

    username     = data.get("username")
    password     = data.get("password")
    sender_id    = data.get("sender_id")           
    phone_numbers = data.get("phone_numbers")
    message       = data.get("message")

    if not all([username, password, sender_id, phone_numbers, message]):
        return JsonResponse(
            {"error": _("Fields 'username', 'password', 'sender_id', 'phone_numbers', and 'message' are required.")},
            status=400,
        )

    if not isinstance(phone_numbers, list):
        phone_numbers = [phone_numbers]

   
    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({"error": _("Invalid username or password")}, status=403)

  
    try:
        session = UserSession.objects.get(user_name=sender_id)
    except UserSession.DoesNotExist:
        return JsonResponse({"error": _("Sender ID not found or QR not scanned")}, status=404)
    
    try:
        sender = SenderID.objects.get(user_session__user_name=sender_id)
        session = sender.user_session
    except SenderID.DoesNotExist:
        return JsonResponse({"error": "Sender profile not found for this user"})


  
    try:
        send_whatsapp_message(phone_numbers, message, session.profile_path)
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=500)

    return JsonResponse({"success": _("Message sent successfully!")}, status=200)
