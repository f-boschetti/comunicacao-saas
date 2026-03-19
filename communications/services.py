"""Integration services for WhatsApp, Instagram, Email, and AI."""

import logging
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_reminder(appointment):
    """Send appointment reminder via configured channels."""
    client = appointment.client
    message = (
        f"Olá {client.name}! Lembramos que você tem um agendamento "
        f"'{appointment.title}' em {appointment.date_time:%d/%m/%Y às %H:%M}. "
        f"Caso precise reagendar, entre em contato conosco."
    )

    if client.email:
        send_email_message(
            to_email=client.email,
            subject=f"Lembrete: {appointment.title}",
            message=message,
        )

    if client.phone:
        send_whatsapp_message(phone=client.phone, message=message)

    from .models import Interaction
    Interaction.objects.create(
        company=appointment.company,
        client=client,
        channel="system",
        direction="outbound",
        subject=f"Lembrete: {appointment.title}",
        content=message,
        is_automated=True,
    )


def send_email_message(to_email, subject, message, from_email=None):
    """Send an email message."""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email or settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            fail_silently=False,
        )
        logger.info("Email sent to %s: %s", to_email, subject)
        return True
    except Exception as e:
        logger.error("Failed to send email to %s: %s", to_email, e)
        return False


def send_whatsapp_message(phone, message):
    """Send a WhatsApp message via the WhatsApp Business API.

    This is a stub implementation. To use in production, configure:
    - WHATSAPP_API_TOKEN
    - WHATSAPP_PHONE_NUMBER_ID
    """
    token = settings.WHATSAPP_API_TOKEN
    phone_id = settings.WHATSAPP_PHONE_NUMBER_ID

    if not token or not phone_id:
        logger.warning("WhatsApp API not configured. Message not sent to %s", phone)
        return False

    logger.info("WhatsApp message would be sent to %s: %s", phone, message[:50])
    # Production implementation:
    # import requests
    # url = f"https://graph.facebook.com/v17.0/{phone_id}/messages"
    # headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    # data = {"messaging_product": "whatsapp", "to": phone, "type": "text", "text": {"body": message}}
    # response = requests.post(url, headers=headers, json=data)
    # return response.status_code == 200
    return False


def send_instagram_message(recipient_id, message):
    """Send an Instagram Direct message via the Instagram Graph API.

    This is a stub implementation. To use in production, configure:
    - INSTAGRAM_ACCESS_TOKEN
    """
    token = settings.INSTAGRAM_ACCESS_TOKEN

    if not token:
        logger.warning("Instagram API not configured. Message not sent to %s", recipient_id)
        return False

    logger.info("Instagram message would be sent to %s: %s", recipient_id, message[:50])
    # Production implementation:
    # import requests
    # url = f"https://graph.facebook.com/v17.0/me/messages"
    # headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    # data = {"recipient": {"id": recipient_id}, "message": {"text": message}}
    # response = requests.post(url, headers=headers, json=data)
    # return response.status_code == 200
    return False


def generate_ai_response(prompt, context=""):
    """Generate an AI-powered response using OpenAI API.

    This is a stub implementation. To use in production, configure:
    - OPENAI_API_KEY
    """
    api_key = settings.OPENAI_API_KEY

    if not api_key:
        logger.warning("OpenAI API not configured. Using fallback response.")
        return _fallback_response(prompt)

    logger.info("AI response would be generated for prompt: %s", prompt[:50])
    # Production implementation:
    # import openai
    # openai.api_key = api_key
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": context or "Você é um assistente de atendimento ao cliente."},
    #         {"role": "user", "content": prompt}
    #     ]
    # )
    # return response.choices[0].message.content
    return _fallback_response(prompt)


def _fallback_response(prompt):
    """Generate a simple fallback response when AI is not configured."""
    prompt_lower = prompt.lower()
    if any(word in prompt_lower for word in ["agendar", "marcar", "horário", "consulta"]):
        return "Ficaremos felizes em agendar um horário para você! Por favor, entre em contato conosco para verificar a disponibilidade."
    elif any(word in prompt_lower for word in ["cancelar", "desmarcar"]):
        return "Para cancelar ou reagendar, por favor entre em contato conosco com antecedência."
    elif any(word in prompt_lower for word in ["preço", "valor", "custo", "quanto"]):
        return "Para informações sobre valores, por favor entre em contato diretamente conosco."
    elif any(word in prompt_lower for word in ["obrigado", "obrigada", "valeu"]):
        return "Por nada! Estamos à disposição. Qualquer dúvida, não hesite em nos contatar."
    return "Obrigado pelo contato! Um de nossos atendentes retornará em breve."
