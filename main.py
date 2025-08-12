import telebot
import requests
import random

BOT_TOKEN = "8357890435:AAE-agJ6aqHsDY9SMfuDwR2FI6mZnVOc-VA"
TMDB_API_KEY = "dbf1663d349c5e02a4908212e77363a0"

bot = telebot.TeleBot(BOT_TOKEN)

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

user_state = {}

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
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = telebot.types.KeyboardButton("▶️ Start")
    markup.add(start_button)
    bot.send_message(message.chat.id, "Welcome! Press ▶️ Start to begin.", reply_markup=markup)


def show_main_menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        telebot.types.KeyboardButton("🎬 Movie Genres"),
        telebot.types.KeyboardButton("🎲 Random Movie"),
        telebot.types.KeyboardButton("🏆 Top rated films"),
        telebot.types.KeyboardButton("📅 2025 Movies"),
        telebot.types.KeyboardButton("📺 Series")
    )
    bot.send_message(message.chat.id, "Hello 👋 Select an option", reply_markup=markup)
    user_state[message.chat.id] = "main"


@bot.message_handler(func=lambda m: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text

    if text == "▶️ Start":
        show_main_menu(message)
    elif text == "🎬 Movie Genres":
        send_genre_buttons(message)
        user_state[chat_id] = "genres"
    elif text == "📺 Series":
        send_series_categories(message)
        user_state[chat_id] = "series"
    elif text == "🔙 Back":
        show_main_menu(message)
        user_state[chat_id] = "main"
    elif text in GENRES:
        send_random_movie(message, genre_id=GENRES[text])
    elif text in SERIES_CATEGORIES:
        send_random_series(message, genre_id=SERIES_CATEGORIES[text])
    elif text == "🎲 Random Movie":
        send_random_movie(message)
    elif text == "🏆 Top rated films":
        send_oscar_movies(message)
    elif text == "📅 2025 Movies":
        send_2025_movies(message)
    else:
        bot.send_message(chat_id, "Select an option from the list.")


def send_genre_buttons(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [telebot.types.KeyboardButton(name) for name in GENRES]
    buttons.append(telebot.types.KeyboardButton("🔙 Back"))
    markup.add(*buttons)
    bot.send_message(message.chat.id, "Select the movie genre", reply_markup=markup)


def send_series_categories(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [telebot.types.KeyboardButton(name) for name in SERIES_CATEGORIES]
    buttons.append(telebot.types.KeyboardButton("🔙 Back"))
    markup.add(*buttons)
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

    response = requests.get(url, params=params).json()
    results = response.get("results", [])
    if not results:
        bot.send_message(message.chat.id, "No movies found.")
        return
    send_movie_details(message, random.choice(results))


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

    response = requests.get(url, params=params).json()
    results = response.get("results", [])
    if not results:
        bot.send_message(message.chat.id, "No series found.")
        return

    series = random.choice(results)
    caption = (
        f"📺 <b>{series.get('name')}</b> ({series.get('first_air_date', '')[:4]})\n"
        f"⭐ Rating: {series.get('vote_average', 'N/A')}/10\n\n"
        f"📝 {series.get('overview', 'Overview not available.')}"
    )
    poster_path = series.get("poster_path")
    if poster_path:
        photo_url = f"{TMDB_IMAGE_URL}{poster_path}"
        bot.send_photo(message.chat.id, photo_url, caption=caption, parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, caption, parse_mode="HTML")


def send_oscar_movies(message):
    url = f"{TMDB_BASE_URL}/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "sort_by": "vote_average.desc",
        "vote_count.gte": 878,
        "with_original_language": "en",
        "vote_average.gte": 8,
        "page": random.randint(1, 5)
    }
    response = requests.get(url, params=params).json()
    results = response.get("results", [])
    if not results:
        bot.send_message(message.chat.id, "No high rated movies found.")
        return
    send_movie_details(message, random.choice(results))


def send_2025_movies(message):
    url = f"{TMDB_BASE_URL}/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "primary_release_year": "2025",
        "sort_by": "popularity.desc",
        "with_original_language": "en
