from fastapi import FastAPI, Form
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
async def whatsapp_webhook(Body: str = Form(...), From: str = Form(...)):
    print(f"📥 Message reçu de {From} : {Body}")

    try:
        if Body.strip().lower() == "bonjour":
            reply = "👋 Bienvenue chez Askley !\n1️⃣ Réserver un hôtel\n2️⃣ Réserver un restaurant\n3️⃣ Aide"
        else:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Tu es Askley, un assistant intelligent pour réserver hôtels et restaurants, et répondre aux demandes utiles des voyageurs."},
                    {"role": "user", "content": Body}
                ]
            )
            reply = response.choices[0].message["content"]

        print(f"📤 Réponse : {reply}")

        client.messages.create(
            body=reply,
            from_=twilio_number,
            to=From
        )

        return {"status": "envoyé"}

    except Exception as e:
        print("❌ Erreur :", str(e))
        return {"status": "erreur", "détail": str(e)}
