import requests

GENIUS_API_TOKEN = "HrfZsg7_a0REbmTA6XtWHhHPeIc3P9F7bSlYtvyhnYRwJACkZ6vOmPheCAsUMpGl"

def search_song(query):
    base_url = "https://api.genius.com/search"
    headers = {
        "Authorization": f"Bearer {GENIUS_API_TOKEN}"
    }
    params = {"q": query}
    
    response = requests.get(base_url, headers=headers, params=params)
    data = response.json()
    
    results = []
    for hit in data["response"]["hits"][:3]:  # Վերադարձնենք միայն առաջին 3-ը
        title = hit["result"]["full_title"]
        url = hit["result"]["url"]
        results.append(f"{title}\n{url}")
    
    return results

import telebot

TOKEN = '6847465146:AAF-uSyAO4SSyxe90rWBp-HaUFu_sSvi0uI'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    query = message.text
    songs = search_song(query)
    
    if songs:
        reply = "\n\n".join(songs)
    else:
        reply = "Չգտա համապատասխան երգեր 😔"
    
    bot.send_message(message.chat.id, reply)

bot.polling()
