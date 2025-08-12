import telebot
import requests
import random

BOT_TOKEN = "8357890435:AAH2r5OlHxxYm5i-DuEIYOYjJwLuYSjlWjA"
TMDB_API_KEY = "dbf1663d349c5e02a4908212e77363a0"

bot = telebot.TeleBot(BOT_TOKEN)

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

# A dictionary to store user's current state
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
    btn1 = telebot.types.KeyboardButton("🎬 Movie Genres")
    btn2 = telebot.types.KeyboardButton("🎲 Random Movie")
    btn3 = telebot.types.KeyboardButton("🏆 Top rated films")
    btn4 = telebot.types.KeyboardButton("📅 2025 Movies")
    btn5 = telebot.types.KeyboardButton("📺 Series")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, "Hello 👋 Select an option", reply_markup=markup)
    user_state[message.chat.id] = "main"  # Save the current state


@bot.message_handler(func=lambda m: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text

    if text == "▶️ Start":
        show_main_menu(message)

    elif text == "🎬 Movie Genres":
        send_genre_buttons(message)
        user_state[chat_id] = "genres"  # Set the state to genres

    elif text == "📺 Series":
        send_series_categories(message)
        user_state[chat_id] = "series"  # Set the state to series

    elif text == "🔙 Back":
        state = user_state.get(chat_id, "main")
        if state == "genres":
            show_main_menu(message)  # Return to the main menu
            user_state[chat_id] = "main"  # Reset to main menu state
        elif state == "series":
            show_main_menu(message)  # Return to the main menu
            user_state[chat_id] = "main"  # Reset to main menu state
        else:
            show_main_menu(message)  # In case user is at the main menu, just show it again

    elif text in GENRES:
        send_random_movie(message, genre_id=GENRES[text])
        user_state[chat_id] = "genres"  # Set the state to genres

    elif text in SERIES_CATEGORIES:
        send_random_series(message, genre_id=SERIES_CATEGORIES[text])
        user_state[chat_id] = "series"  # Set the state to series

    elif text == "🎲 Random Movie":
        send_random_movie(message)
        user_state[chat_id] = "main"  # Set the state back to main menu

    elif text == "🏆 Top rated films":
        send_oscar_movies(message)
        user_state[chat_id] = "main"  # Set the state back to main menu

    elif text == "📅 2025 Movies":
        send_2025_movies(message)
        user_state[chat_id] = "main"  # Set the state back to main menu

    else:
        bot.send_message(chat_id, "Select an option from the list.")


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

    response = requests.get(url, params=params)
    data = response.json()

    movies = data.get("results", [])
    if not movies:
        bot.send_message(message.chat.id, "No high rated movies found.")
        return

    selected_movie = random.choice(movies)
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
        bot.send_photo(
            message.chat.id,
            photo_url,
            caption=caption,
            parse_mode="HTML",
            disable_web_page_preview=True  # 👈 Ավելացվեց սա
        )
    else:
        bot.send_message(
            message.chat.id,
            caption,
            parse_mode="HTML",
            disable_web_page_preview=True  # 👈 Ավելացվեց սա
        )


if __name__ == "__main__":
    bot.polling(none_stop=True)
