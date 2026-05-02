# 🤖 Telegram Request Bot (FSM Architecture)

A professional, asynchronous Telegram bot designed to collect and manage user requests. Built with a focus on **Finite State Machine (FSM)** logic to ensure a seamless and error-free user experience.

## 🚀 Key Features
* **Structured Data Collection:** Uses a state-based flow (Name → Request → Confirmation) to prevent user confusion.
* **Automated Routing:** Instantly forwards verified requests to a private Admin ID and a dedicated Telegram channel.
* **Smart State Management:** Users can cancel, restart, or loop through multiple requests within a single session without breaking the bot.
* **Security First:** Sensitive credentials (API Tokens, IDs) are securely managed via environment variables.

## 🛠 Tech Stack
* **Language:** Python 3.10+
* **Framework:** `python-telegram-bot` (v20+, Asyncio)
* **Configuration:** `python-dotenv`

## ⚙️ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
2. Configure Environment
Create a .env file from the provided .env.example template and add your bot token:

Plaintext
BOT_TOKEN=your_token_here
ADMIN_ID=your_id_here
CHANNEL_ID=@your_channel_here
3. Launch the Bot
python bot.py
Developed by [TimTech-dev]
