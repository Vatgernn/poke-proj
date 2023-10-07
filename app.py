from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Глобальная переменная для хранения данных
cached_pokemon_list = None

# Функция для получения списка покемонов с кэшированием
def get_pokemon_list():
    global cached_pokemon_list

    if cached_pokemon_list is None:
        url = "https://pokeapi.co/api/v2/pokemon"
        all_pokemon = []

        while url:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                pokemon_list = data.get("results", [])
                all_pokemon.extend(pokemon_list)
                url = data.get("next")

        cached_pokemon_list = all_pokemon

    return cached_pokemon_list

@app.route("/", methods=["GET", "POST"])
def index():
    # Получаем список покемонов
    pokemon_list = get_pokemon_list()

    # Обработка поискового запроса
    search_query = request.form.get("search")
    if search_query:
        filtered_pokemon_list = [
            pokemon for pokemon in pokemon_list if search_query.lower() in pokemon["name"].lower()
        ]
    else:
        filtered_pokemon_list = pokemon_list

    return render_template("index.html", pokemon_list=filtered_pokemon_list, search_query=search_query)

if __name__ == "__main__":
    app.run(debug=True)
