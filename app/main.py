from fastapi import FastAPI, Request, Form
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
async def whatsapp_webhook(request: Request):
    try:
        form = await request.form()
        body = form.get("Body")
        sender = form.get("From")

        print(f"📥 Message reçu de {sender} : {body}")

        if not body:
            return {"status": "erreur", "message": "Champ 'Body' manquant"}

        if body.strip().lower() == "bonjour":
            reply = "👋 Bienvenue chez Askley. Tapez 1 pour réserver un hôtel, 2 pour un restaurant."
        else:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Tu es Askley, un assistant de réservation intelligent pour hôtels et restaurants."},
                    {"role": "user", "content": body}
                ]
            )
            reply = response.choices[0].message["content"]

        print(f"📤 Réponse : {reply}")

        client.messages.create(
            body=reply,
            from_=twilio_number,
            to=sender
        )

        return {"status": "envoyé"}

    except Exception as e:
        print("❌ Erreur serveur :", str(e))
        return {"status": "erreur", "message": str(e)}