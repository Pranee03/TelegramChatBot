# GenieBot: Your Open-Source AI Assistant

GenieBot is a Telegram bot that uses AI to provide conversational responses. It's designed to be a free and open-source alternative for users who want an AI assistant without relying on proprietary services.

## Features

* Text-based conversations: GenieBot can engage in text-based conversations with users on Telegram.
* AI-powered responses: GenieBot uses a language model to generate its responses.
* Open-source: The code for GenieBot is freely available, allowing anyone to use, modify, and contribute to the project.

## How It Works

GenieBot uses the following technologies:

* Telegram Bot API: To communicate with users on Telegram.
* Hugging Face Transformers: To generate conversational responses using a pre-trained language model.
* Python: The bot is written in Python.

When a user sends a message to GenieBot on Telegram:

1.  The message is received by the Telegram Bot API.
2.  The message is forwarded to the GenieBot application (running on a server).
3.  GenieBot uses the Hugging Face Transformers library to generate a response.
4.  The response is sent back to the user via the Telegram Bot API.

## Setup

### Prerequisites

* A Telegram account.
* Python 3.7 or later.
* pip (Python's package installer).

### Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/your-username/geniebot.git](https://www.google.com/search?q=https://github.com/your-username/geniebot.git) # Replace with the actual repo URL
    cd geniebot
    ```
2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate # On macOS/Linux
    venv\\Scripts\\activate # On Windows
    ```
3.  **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

    (You'll need to create a requirements.txt file with the dependencies. I can help with this.)
4.  **Get a Telegram Bot Token:**

    * Talk to BotFather on Telegram to create a new bot and obtain an API token.
5.  **Set the Telegram Bot Token as an environment variable:**

    * On Linux/macOS:

        ```bash
        export TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN" # Replace with your token
        ```
    * On Windows:

        ```bash
        setx TELEGRAM_BOT_TOKEN "YOUR_TELEGRAM_BOT_TOKEN" # Replace with your token
        ```

        (You might need to restart your command prompt.)
6.  **Run the bot:**

    ```bash
    python bot.py
    ```

## Usage

1.  Start a chat with GenieBot on Telegram.
2.  Send the `/start` command to receive a greeting.
3.  Type any text message to have a conversation with the bot.

## Disclaimer

GenieBot is powered by a language model, which generates responses based on patterns learned from a large amount of data. This means that:

* Responses may sometimes be inaccurate, untruthful, or inappropriate.
* The bot does not have genuine understanding or beliefs.
* The bot's responses should not be taken as factual or professional advice.
* Users should exercise caution and critical thinking when interacting with the bot.

## Contributing

Contributions are welcome! Please refer to the [Contributing Guidelines](CONTRIBUTING.md) for information on how to contribute to GenieBot.

## License

GenieBot is licensed under the [MIT License](LICENSE).
