# import requests

# GENIUS_API_TOKEN = "HrfZsg7_a0REbmTA6XtWHhHPeIc3P9F7bSlYtvyhnYRwJACkZ6vOmPheCAsUMpGl"

# def search_song(query):
#     base_url = "https://api.genius.com/search"
#     headers = {
#         "Authorization": f"Bearer {GENIUS_API_TOKEN}"
#     }
#     params = {"q": query}
    
#     response = requests.get(base_url, headers=headers, params=params)
#     data = response.json()
    
#     results = []
#     for hit in data["response"]["hits"][:1]:  # Վերադարձնենք միայն առաջին 3-ը
#         title = hit["result"]["full_title"]
#         url = hit["result"]["url"]
#         results.append(f"{title}\n{url}")
    
#     return results

# import telebot

# TOKEN = '6847465146:AAF-uSyAO4SSyxe90rWBp-HaUFu_sSvi0uI'
# bot = telebot.TeleBot(TOKEN)

# @bot.message_handler(func=lambda message: True)
# def handle_message(message):
#     query = message.text
#     songs = search_song(query)
    
#     if songs:
#         reply = "\n\n".join(songs)
#     else:
#         reply = "Չգտա համապատասխան երգեր 😔"
    
#     bot.send_message(message.chat.id, reply)

# bot.polling()
import telebot
import yt_dlp

BOT_TOKEN = "6847465146:AAF-uSyAO4SSyxe90rWBp-HaUFu_sSvi0uI"
bot = telebot.TeleBot(BOT_TOKEN)

def get_youtube_url(query):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'default_search': 'ytsearch1',  # Սահմանափակենք առաջին արդյունքին
        # 'extract_flat': False,  # Լրիվ տվյալներ քաշենք
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        if 'entries' in info and len(info['entries']) > 0:
            video = info['entries'][0]
            return f"https://www.youtube.com/watch?v={video['id']}"
        elif 'id' in info:
            return f"https://www.youtube.com/watch?v={info['id']}"
        else:
            return None

@bot.message_handler(func=lambda message: True)
def handle_search(message):
    query = message.text.strip()
    bot.send_chat_action(message.chat.id, 'typing')

    url = get_youtube_url(query)
    if url:
        bot.send_message(message.chat.id, f"🎵 Ահա քո երգը՝\n{url}")
    else:
        bot.send_message(message.chat.id, "Չհաջողվեց գտնել երգի YouTube հղումը 😔")

print("Բոտը ակտիվ է...")
bot.polling()


