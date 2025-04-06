# Telegram Bot: search for information about films and TV shows in the database of the [kinopoisk.ru](https://www.kinopoisk.ru/)

---

## About the project

---
This bot can help you find info about films, documentary films, cartoons and TV shows in the
database of the [kinopoisk.ru](https://www.kinopoisk.ru/) site. Also, it saves the history of results of user's
queries to database and can show this history to user.

The code is written for educational purposes, it is part of a course on learning the Python programming language.

### Built with

- pyTelegramBotAPI: to interact with Telegram Bot API
- requests: to make HTTP requests
- python-telegram-bot-pagination: to create pagination for results of user's query
- peewee: to interact with SQLite database

## Getting started

---
To get a local copy up and running follow these simple example steps.

### Installation

1. Get a free API key from [kinopoisk.dev](https://kinopoisk.dev)
2. Get a free bot token from @BotFather at Telegram
3. Clone the repo

    ```
    git clone https://github.com/github_username/repo_name.git
    ```
4. Create a virtual environment in the root folder of your local repo

   ```
   python3 -m venv venv
   ```
5. Activate virtual environment
    1. Windows
       ```
       venv\Scripts\activate
       ```
    2. macOS and Linux
       ```
       source venv/bin/activate
       ```

6. Install required packages
   ```
   pip install -r requirements.txt
   ```
7. Rename file `.env.template` to `.env` and specify your received token and key in it
   ```
   BOT_TOKEN = "Your token from @BotFather"
   KINOPOISK_API_KEY = "Your API key from https://kinopoisk.dev"
   ```
8. Change git remote url to avoid accidental pushes to base project
   ```
   git remote set-url python_basic_diploma https://github.com/github_username_new/repo_name_new.git
   ```
9. To launch the bot, run the following command
   ```
   python main.py
   ```
   
### Usage

List of available bot commands:
- `/start` - start interacting with the bot
- `/help` - show available commands
- `/hello_world` - test command for educational process
- `/stop_search` - stop the movie search process
- `/history` - show the history of the search results for a specific date
- `/movie_search` - movie search by name
- `/movie_by_rating` - movie search by rating
- `/low_budget_movie` - movie search by low budget parameter
- `/high_budget_movie` - movie search by high budget parameter