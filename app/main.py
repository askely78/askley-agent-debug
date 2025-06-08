
from fastapi import FastAPI, Request
from twilio.rest import Client
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")
twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(twilio_sid, twilio_token)

@app.post("/whatsapp-webhook")
async def whatsapp_webhook_raw(request: Request):
    form_data = await request.form()
    print("✅ Form Data reçu depuis Twilio :")
    for key, value in form_data.items():
        print(f"{key}: {value}")

    Body = form_data.get("Body", "").strip()
    From = form_data.get("From", "")

    try:
        if Body.lower() == "bonjour":
            reply = "👋 Bienvenue chez Askley. Tapez 1 pour réserver un hôtel, 2 pour un restaurant."
        else:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Tu es Askley, un assistant intelligent de réservation."},
                    {"role": "user", "content": Body}
                ]
            )
            reply = response.choices[0].message["content"]

        client.messages.create(
            body=reply,
            from_=twilio_number,
            to=From
        )

        return {"status": "envoyé"}

    except Exception as e:
        print("❌ Erreur OpenAI :", str(e))
        return {"status": "erreur", "détail": str(e)}
