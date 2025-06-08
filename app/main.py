<<<<<<< HEAD
from fastapi import FastAPI, Request, Form
=======

from fastapi import FastAPI, Request
>>>>>>> 629d0183c6c852b71ba1f9192f4ef4cd414fa5ad
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
<<<<<<< HEAD
async def whatsapp_webhook(request: Request):
    try:
        form = await request.form()
        body = form.get("Body")
        sender = form.get("From")

        print(f"📥 Message reçu de {sender} : {body}")

        if not body:
            return {"status": "erreur", "message": "Champ 'Body' manquant"}

        if body.strip().lower() == "bonjour":
=======
async def whatsapp_webhook_raw(request: Request):
    form_data = await request.form()
    print("✅ Form Data reçu depuis Twilio :")
    for key, value in form_data.items():
        print(f"{key}: {value}")

    Body = form_data.get("Body", "").strip()
    From = form_data.get("From", "")

    try:
        if Body.lower() == "bonjour":
>>>>>>> 629d0183c6c852b71ba1f9192f4ef4cd414fa5ad
            reply = "👋 Bienvenue chez Askley. Tapez 1 pour réserver un hôtel, 2 pour un restaurant."
        else:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
<<<<<<< HEAD
                    {"role": "system", "content": "Tu es Askley, un assistant de réservation intelligent pour hôtels et restaurants."},
                    {"role": "user", "content": body}
=======
                    {"role": "system", "content": "Tu es Askley, un assistant intelligent de réservation."},
                    {"role": "user", "content": Body}
>>>>>>> 629d0183c6c852b71ba1f9192f4ef4cd414fa5ad
                ]
            )
            reply = response.choices[0].message["content"]

<<<<<<< HEAD
        print(f"📤 Réponse : {reply}")

        client.messages.create(
            body=reply,
            from_=twilio_number,
            to=sender
=======
        client.messages.create(
            body=reply,
            from_=twilio_number,
            to=From
>>>>>>> 629d0183c6c852b71ba1f9192f4ef4cd414fa5ad
        )

        return {"status": "envoyé"}

    except Exception as e:
<<<<<<< HEAD
        print("❌ Erreur serveur :", str(e))
        return {"status": "erreur", "message": str(e)}
=======
        print("❌ Erreur OpenAI :", str(e))
        return {"status": "erreur", "détail": str(e)}
>>>>>>> 629d0183c6c852b71ba1f9192f4ef4cd414fa5ad
