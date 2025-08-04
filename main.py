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
# import telebot
# import yt_dlp

# BOT_TOKEN = "6847465146:AAF-uSyAO4SSyxe90rWBp-HaUFu_sSvi0uI"
# bot = telebot.TeleBot(BOT_TOKEN)

# def get_youtube_url(query):
#     ydl_opts = {
#         'quiet': True,
#         'skip_download': True,
#         'default_search': 'ytsearch1',  # Սահմանափակենք առաջին արդյունքին
#         # 'extract_flat': False,  # Լրիվ տվյալներ քաշենք
#     }
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(query, download=False)
#         if 'entries' in info and len(info['entries']) > 0:
#             video = info['entries'][0]
#             return f"https://www.youtube.com/watch?v={video['id']}"
#         elif 'id' in info:
#             return f"https://www.youtube.com/watch?v={info['id']}"
#         else:
#             return None

# @bot.message_handler(func=lambda message: True)
# def handle_search(message):
#     query = message.text.strip()
#     bot.send_chat_action(message.chat.id, 'typing')

#     url = get_youtube_url(query)
#     if url:
#         bot.send_message(message.chat.id, f"🎵 Ահա քո երգը՝\n{url}")
#     else:
#         bot.send_message(message.chat.id, "Չհաջողվեց գտնել երգի YouTube հղումը 😔")

# print("Բոտը ակտիվ է...")
# bot.polling()

import logging
import requests
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ========== CONFIG ==========
API_KEY = 'dbf1663d349c5e02a4908212e77363a0'  # Your TMDb API Key
BOT_TOKEN = '6847465146:AAF-uSyAO4SSyxe90rWBp-HaUFu_sSvi0uI'  # Your Telegram Bot Token

TMDB_URL = 'https://api.themoviedb.org/3/movie/popular'
IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

logging.basicConfig(level=logging.INFO)

# ========== MOVIE FETCH FUNCTION ==========
def get_random_movie():
    response = requests.get(TMDB_URL, params={'api_key': API_KEY, 'language': 'en-US', 'page': 1})
    data = response.json()
    movies = data.get('results', [])

    if not movies:
        return None

    movie = random.choice(movies)

    return {
        'title': movie.get('title'),
        'overview': movie.get('overview'),
        'poster': IMAGE_BASE_URL + movie['poster_path'] if movie.get('poster_path') else None,
        'release_date': movie.get('release_date') or 'Unknown'
    }


# ========== START COMMAND ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie = get_random_movie()
    if movie:
        year = movie['release_date'][:4] if movie.get('release_date') else 'Unknown Year'
        caption = f"🎬 *{movie['title']}* ({year})\n📝 {movie['overview']}"
        if movie['poster']:
            await update.message.reply_photo(photo=movie['poster'], caption=caption, parse_mode="Markdown")
        else:
            await update.message.reply_text(caption, parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Couldn't load a movie. Please try again.")

# ========== RUN THE BOT ==========
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    print("🎬 Movie bot is running...")
    app.run_polling()


