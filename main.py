# # import requests

# # GENIUS_API_TOKEN = "HrfZsg7_a0REbmTA6XtWHhHPeIc3P9F7bSlYtvyhnYRwJACkZ6vOmPheCAsUMpGl"

# # def search_song(query):
# #     base_url = "https://api.genius.com/search"
# #     headers = {
# #         "Authorization": f"Bearer {GENIUS_API_TOKEN}"
# #     }
# #     params = {"q": query}
    
# #     response = requests.get(base_url, headers=headers, params=params)
# #     data = response.json()
    
# #     results = []
# #     for hit in data["response"]["hits"][:1]:  # Վերադարձնենք միայն առաջին 3-ը
# #         title = hit["result"]["full_title"]
# #         url = hit["result"]["url"]
# #         results.append(f"{title}\n{url}")
    
# #     return results

# # import telebot

# # TOKEN = '6847465146:AAF-uSyAO4SSyxe90rWBp-HaUFu_sSvi0uI'
# # bot = telebot.TeleBot(TOKEN)

# # @bot.message_handler(func=lambda message: True)
# # def handle_message(message):
# #     query = message.text
# #     songs = search_song(query)
    
# #     if songs:
# #         reply = "\n\n".join(songs)
# #     else:
# #         reply = "Չգտա համապատասխան երգեր 😔"
    
# #     bot.send_message(message.chat.id, reply)

# # bot.polling()
# # import telebot
# # import yt_dlp

# # BOT_TOKEN = "6847465146:AAF-uSyAO4SSyxe90rWBp-HaUFu_sSvi0uI"
# # bot = telebot.TeleBot(BOT_TOKEN)

# # def get_youtube_url(query):
# #     ydl_opts = {
# #         'quiet': True,
# #         'skip_download': True,
# #         'default_search': 'ytsearch1',  # Սահմանափակենք առաջին արդյունքին
# #         # 'extract_flat': False,  # Լրիվ տվյալներ քաշենք
# #     }
# #     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
# #         info = ydl.extract_info(query, download=False)
# #         if 'entries' in info and len(info['entries']) > 0:
# #             video = info['entries'][0]
# #             return f"https://www.youtube.com/watch?v={video['id']}"
# #         elif 'id' in info:
# #             return f"https://www.youtube.com/watch?v={info['id']}"
# #         else:
# #             return None

# # @bot.message_handler(func=lambda message: True)
# # def handle_search(message):
# #     query = message.text.strip()
# #     bot.send_chat_action(message.chat.id, 'typing')

# #     url = get_youtube_url(query)
# #     if url:
# #         bot.send_message(message.chat.id, f"🎵 Ահա քո երգը՝\n{url}")
# #     else:
# #         bot.send_message(message.chat.id, "Չհաջողվեց գտնել երգի YouTube հղումը 😔")

# # print("Բոտը ակտիվ է...")
# # bot.polling()


# # ========== CONFIG ==========
# import telebot
# import requests
# import random

# # Այստեղ տեղադրիր քո տելեգրամ բոթի թոքենը և TMDb API Key-ը
# BOT_TOKEN = "6847465146:AAF-uSyAO4SSyxe90rWBp-HaUFu_sSvi0uI"
# TMDB_API_KEY = "dbf1663d349c5e02a4908212e77363a0"

# bot = telebot.TeleBot(BOT_TOKEN)

# # TMDb Base URLs
# TMDB_BASE_URL = "https://api.themoviedb.org/3"
# TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

# # Ժանրերի ID-ների mapping (TMDb Genre IDs)
# GENRES = {
#     "Action": 28,
#     "Comedy": 35,
#     "Drama": 18,
#     "Thriller": 53,
#     "Romance": 10749,
#     "Sci-Fi": 878,
#     "Horror": 27,
#     "Animation": 16,
#     "Adventure": 12,
#     "Documentary": 99
# }

# # Ստարտ հրամանը
# @bot.message_handler(commands=["start"])
# def start(message):
#     markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     btn1 = telebot.types.KeyboardButton("🎬 Ժանրեր")
#     btn2 = telebot.types.KeyboardButton("🎲 Պատահական ֆիլմ")
#     btn3 = telebot.types.KeyboardButton("🏆 Օսկարակիր ֆիլմեր")
#     btn4 = telebot.types.KeyboardButton("📅 2025 ֆիլմեր")
#     markup.add(btn1, btn2, btn3, btn4)
#     bot.send_message(message.chat.id, "Ողջույն 👋 Ընտրիր տարբերակը", reply_markup=markup)

# # Հաղորդագրությունների հիմնական մշակողը
# @bot.message_handler(func=lambda m: True)
# def handle_message(message):
#     text = message.text

#     if text == "🎬 Ժանրեր":
#         send_genre_buttons(message)
#     elif text in GENRES:
#         send_random_movie(message, genre_id=GENRES[text])
#     elif text == "🎲 Պատահական ֆիլմ":
#         send_random_movie(message)
#     elif text == "🏆 Օսկարակիր ֆիլմեր":
#         send_oscar_movies(message)
#     elif text == "📅 2025 ֆիլմեր":
#         send_2025_movies(message)
#     else:
#         bot.send_message(message.chat.id, "Ընտրեք ցանկից տարբերակ։")

# # Ժանրերի կոճակներ
# def send_genre_buttons(message):
#     markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     buttons = [telebot.types.KeyboardButton(name) for name in GENRES.keys()]
#     markup.add(*buttons)
#     bot.send_message(message.chat.id, "Ընտրեք ժանրը", reply_markup=markup)

# # Պատահական ֆիլմ ըստ ժանրի կամ առանց
# def send_random_movie(message, genre_id=None):
#     url = f"{TMDB_BASE_URL}/discover/movie"
#     params = {
#         "api_key": TMDB_API_KEY,
#         "sort_by": "popularity.desc",
#         "vote_count.gte": 50,
#         "with_original_language": "en",
#         "page": random.randint(1, 5)
#     }
#     if genre_id:
#         params["with_genres"] = genre_id

#     response = requests.get(url, params=params)
#     data = response.json()

#     if "results" not in data or not data["results"]:
#         bot.send_message(message.chat.id, "Չգտնվեց ֆիլմ։")
#         return

#     movie = random.choice(data["results"])

#     title = movie.get("title")
#     year = movie.get("release_date", "")[:4]
#     overview = movie.get("overview", "Նկարագրություն չկա։")
#     rating = movie.get("vote_average", "N/A")
#     poster_path = movie.get("poster_path")

#     # Թրեյլեր բերելու համար ֆիլմի հավելյալ տվյալներ
#     trailer_url = "Չկա թրեյլեր։"
#     movie_id = movie.get("id")
#     if movie_id:
#         video_url = f"{TMDB_BASE_URL}/movie/{movie_id}/videos"
#         video_params = {"api_key": TMDB_API_KEY}
#         video_resp = requests.get(video_url, params=video_params).json()
#         videos = video_resp.get("results", [])
#         trailer = next((v for v in videos if v["type"] == "Trailer" and v["site"] == "YouTube"), None)
#         if trailer:
#             trailer_url = f"https://www.youtube.com/watch?v={trailer['key']}"

#     caption = (
#         f"🎬 <b>{title}</b> ({year})\n"
#         f"⭐ Վարկանիշ: {rating}/10\n\n"
#         f"📝 {overview}\n\n"
#         f"▶️ <a href='{trailer_url}'>Դիտել Թրեյլերը</a>"
#     )

#     if poster_path:
#         photo_url = f"{TMDB_IMAGE_URL}{poster_path}"
#         bot.send_photo(message.chat.id, photo_url, caption=caption, parse_mode="HTML")
#     else:
#         bot.send_message(message.chat.id, caption, parse_mode="HTML")

# # Օսկարակիր ֆիլմերի ցուցակ
# def send_oscar_movies(message):
#     url = f"{TMDB_BASE_URL}/discover/movie"
#     params = {
#         "api_key": TMDB_API_KEY,
#         "sort_by": "vote_average.desc",
#         "vote_count.gte": 5000,
#         "with_original_language": "en",
#         "page": 1
#     }
#     response = requests.get(url, params=params)
#     data = response.json()

#     movies = data.get("results", [])
#     if not movies:
#         bot.send_message(message.chat.id, "Չկան Օսկարակիր ֆիլմեր։")
#         return

#     top_movie = movies[0]
#     send_movie_details(message, top_movie)

# # 2025 տարվա ֆիլմեր
# def send_2025_movies(message):
#     url = f"{TMDB_BASE_URL}/discover/movie"
#     params = {
#         "api_key": TMDB_API_KEY,
#         "primary_release_year": "2025",
#         "sort_by": "popularity.desc",
#         "with_original_language": "en",
#         "page": 1
#     }
#     response = requests.get(url, params=params)
#     data = response.json()

#     movies = data.get("results", [])
#     if not movies:
#         bot.send_message(message.chat.id, "Չկան 2025 թվականի ֆիլմեր։")
#         return

#     movie = random.choice(movies)
#     send_movie_details(message, movie)

# # Ընդհանուր ֆունկցիա ֆիլմ ցույց տալու համար
# def send_movie_details(message, movie):
#     title = movie.get("title")
#     year = movie.get("release_date", "")[:4]
#     overview = movie.get("overview", "Նկարագրություն չկա։")
#     rating = movie.get("vote_average", "N/A")
#     poster_path = movie.get("poster_path")

#     # Թրեյլեր
#     trailer_url = "Չկա թրեյլեր։"
#     movie_id = movie.get("id")
#     if movie_id:
#         video_url = f"{TMDB_BASE_URL}/movie/{movie_id}/videos"
#         video_params = {"api_key": TMDB_API_KEY}
#         video_resp = requests.get(video_url, params=video_params).json()
#         videos = video_resp.get("results", [])
#         trailer = next((v for v in videos if v["type"] == "Trailer" and v["site"] == "YouTube"), None)
#         if trailer:
#             trailer_url = f"https://www.youtube.com/watch?v={trailer['key']}"

#     caption = (
#         f"🎬 <b>{title}</b> ({year})\n"
#         f"⭐ Վարկանիշ: {rating}/10\n\n"
#         f"📝 {overview}\n\n"
#         f"▶️ <a href='{trailer_url}'>Դիտել Թրեյլերը</a>"
#     )

#     if poster_path:
#         photo_url = f"{TMDB_IMAGE_URL}{poster_path}"
#         bot.send_photo(message.chat.id, photo_url, caption=caption, parse_mode="HTML")
#     else:
#         bot.send_message(message.chat.id, caption, parse_mode="HTML")

# # Ռանը
# if __name__ == "__main__":
#     bot.polling(none_stop=True)



import telebot
import requests
import random

BOT_TOKEN = "6847465146:AAF-uSyAO4SSyxe90rWBp-HaUFu_sSvi0uI"
TMDB_API_KEY = "dbf1663d349c5e02a4908212e77363a0"

bot = telebot.TeleBot(BOT_TOKEN)

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

GENRES = {
   "Action 🏃‍♂️🔥": 28,
    "Comedy 😂🎭": 35,
    "Drama 🎬😢": 18,
    "Thriller 😱🔪": 53,
    "Romance ❤️💑": 10749,
    "Sci-Fi 👽🚀": 878,
    "Horror 👻🔪": 27,
    "Animation 🐭🎨": 16,
    "Adventure 🗺️🏞️": 12,
    "Documentary 🎥📚": 99
}

SERIES_CATEGORIES = {
    "Drama Series 🎭": 18,
    "Comedy Series 😂": 35,
    "Reality Series 📺": 10764,
    "Action Series 🔥": 10759,
    "Sci-Fi Series 👽": 10765,
    "Mystery Series 🕵️‍♂️": 9648,
    "Crime Series 🚓": 80,
    "War & Politics ⚔️": 10768
}

@bot.message_handler(commands=["start"])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = telebot.types.KeyboardButton("🎬 Movie Gernes")
    btn2 = telebot.types.KeyboardButton("🎲 Random Movie")
    btn3 = telebot.types.KeyboardButton("🏆 Top raited films")
    btn4 = telebot.types.KeyboardButton("📅 2025 Movies")
    btn5 = telebot.types.KeyboardButton("📺 Series")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, "Hello 👋 Select an option", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    text = message.text

    if text == "🎬 Gernes":
        send_genre_buttons(message)
    elif text == "📺 Series":
        send_series_categories(message)
    elif text in GENRES:
        send_random_movie(message, genre_id=GENRES[text])
    elif text in SERIES_CATEGORIES:
        send_random_series(message, genre_id=SERIES_CATEGORIES[text])
    elif text == "🎲 Random Movie":
        send_random_movie(message)
    elif text == "🏆 Top raited films":
        send_oscar_movies(message)
    elif text == "📅 2025 Movies":
        send_2025_movies(message)
    elif text == "🔙 Back":
        start(message)
    else:
        bot.send_message(message.chat.id, "Select an option from the list.")

def send_genre_buttons(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [telebot.types.KeyboardButton(name) for name in GENRES.keys()]
    btn_back = telebot.types.KeyboardButton("🔙 Back")
    markup.add(*buttons)
    markup.add(btn_back)
    bot.send_message(message.chat.id, "Select the movie genre", reply_markup=markup)

def send_series_categories(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [telebot.types.KeyboardButton(name) for name in SERIES_CATEGORIES.keys()]
    btn_back = telebot.types.KeyboardButton("🔙 Back")
    markup.add(*buttons)
    markup.add(btn_back)
    bot.send_message(message.chat.id, "Select the series genre", reply_markup=markup)

def send_random_movie(message, genre_id=None):
    url = f"{TMDB_BASE_URL}/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "sort_by": "popularity.desc",
        "vote_count.gte": 50,
        "with_original_language": "en",
        "page": random.randint(1, 5)
    }
    if genre_id:
        params["with_genres"] = genre_id

    response = requests.get(url, params=params)
    data = response.json()

    if "results" not in data or not data["results"]:
        bot.send_message(message.chat.id, "No movies found.")
        return

    movie = random.choice(data["results"])
    send_movie_details(message, movie)

def send_random_series(message, genre_id=None):
    url = f"{TMDB_BASE_URL}/discover/tv"
    params = {
        "api_key": TMDB_API_KEY,
        "sort_by": "popularity.desc",
        "vote_count.gte": 50,
        "with_original_language": "en",
        "page": random.randint(1, 5)
    }
    if genre_id:
        params["with_genres"] = genre_id

    response = requests.get(url, params=params)
    data = response.json()

    if "results" not in data or not data["results"]:
        bot.send_message(message.chat.id, "No series found.")
        return

    series = random.choice(data["results"])

    title = series.get("name")
    year = series.get("first_air_date", "")[:4]
    overview = series.get("overview", "Overview not available")
    rating = series.get("vote_average", "N/A")
    poster_path = series.get("poster_path")

    caption = (
        f"📺 <b>{title}</b> ({year})\n"
        f"⭐ Rating: {rating}/10\n\n"
        f"📝 {overview}"
    )

    if poster_path:
        photo_url = f"{TMDB_IMAGE_URL}{poster_path}"
        bot.send_photo(message.chat.id, photo_url, caption=caption, parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, caption, parse_mode="HTML")

# def send_oscar_movies(message):
    # url = f"{TMDB_BASE_URL}/discover/movie"
    # params = {
    #     "api_key": TMDB_API_KEY,
    #     "sort_by": "vote_average.desc",
    #     "vote_count.gte": 878,
    #     "with_original_language": "en",
    #     "page": 1
    # }
    # response = requests.get(url, params=params)
    # data = response.json()

    # movies = data.get("results", [])
    # if not movies:
    #     bot.send_message(message.chat.id, "No high raited movies")
    #     return

    # top_movie = movies[0]
    # send_movie_details(message, top_movie)

def send_oscar_movies(message):
    url = f"{TMDB_BASE_URL}/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "sort_by": "vote_average.desc",
        "vote_count.gte": 878,
        "with_original_language": "en",
        "vote_average.gte": 8,  # Ստուգում՝ >=8
        "page": random.randint(1, 5)  # պատահական էջ՝ 1-ից 5 (կարող ես ավելացնել մինչև 10)
    }

    response = requests.get(url, params=params)
    data = response.json()

    movies = data.get("results", [])
    if not movies:
        bot.send_message(message.chat.id, "No high rated movies found.")
        return

    selected_movie = random.choice(movies)  # պատահական ֆիլմ ընտրված էջից
    send_movie_details(message, selected_movie)

def send_2025_movies(message):
    url = f"{TMDB_BASE_URL}/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "primary_release_year": "2025",
        "sort_by": "popularity.desc",
        "with_original_language": "en",
        "page": 1
    }
    response = requests.get(url, params=params)
    data = response.json()

    movies = data.get("results", [])
    if not movies:
        bot.send_message(message.chat.id, "No 2025 year movies")
        return

    movie = random.choice(movies)
    send_movie_details(message, movie)

def send_movie_details(message, movie):
    title = movie.get("title")
    year = movie.get("release_date", "")[:4]
    overview = movie.get("overview", "Overview not available.")
    rating = movie.get("vote_average", "N/A")
    poster_path = movie.get("poster_path")

    trailer_url = "No trailer movies"
    movie_id = movie.get("id")
    if movie_id:
        video_url = f"{TMDB_BASE_URL}/movie/{movie_id}/videos"
        video_params = {"api_key": TMDB_API_KEY}
        video_resp = requests.get(video_url, params=video_params).json()
        videos = video_resp.get("results", [])
        trailer = next((v for v in videos if v["type"] == "Trailer" and v["site"] == "YouTube"), None)
        if trailer:
            trailer_url = f"https://www.youtube.com/watch?v={trailer['key']}"

    caption = (
        f"🎬 <b>{title}</b> ({year})\n"
        f"⭐ Rating: {rating}/10\n\n"
        f"📝 {overview}\n\n"
        f"▶️ <a href='{trailer_url}'>Watch trailer</a>"
    )

    if poster_path:
        photo_url = f"{TMDB_IMAGE_URL}{poster_path}"
        bot.send_photo(message.chat.id, photo_url, caption=caption, parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, caption, parse_mode="HTML")

if __name__ == "__main__":
    bot.polling(none_stop=True)
