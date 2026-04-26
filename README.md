# Aprobator 🤖

> Your AI-powered university survival bot for Telegram.

Aprobator helps university students manage their academic life directly from Telegram — calculate the grades you need to pass, run Pomodoro sessions, and more.

---

## Features

- `/aprobar <current_grade> <percentage_completed>` — calculates the exact grade you need on your final exam to pass
- `/ayuda` — shows the full command menu
- More features coming soon (Pomodoro timer, grade tracker, AI-powered notes summarizer)

## Getting Started

### Prerequisites

- Python 3.10+
- A Telegram account
- A bot token from [@BotFather](https://t.me/BotFather)

### Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/aprobator.git
cd aprobator
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root folder and add your bot token

```
TELEGRAM_TOKEN=your_token_here
```

4. Run the bot

```bash
python bot.py
```

## Usage

Open Telegram, search for `@AprobatorBot` and send `/start`.

**Example:**
If you scored a 4.5 on a midterm worth 40% of your final grade, send:
```
/aprobar 4.5 40
```
Aprobator will tell you exactly what you need on the final to pass.

## Project Structure

```
aprobator/
├── bot.py          # Main bot logic
├── .env            # Your secret token (never commit this)
├── .gitignore
├── requirements.txt
└── README.md
```

## Roadmap

- [x] Grade calculator
- [ ] Pomodoro timer
- [ ] Exam reminder system
- [ ] AI-powered notes summarizer (Claude API)
- [ ] Premium tier

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

## License

[MIT](LICENSE)

---

Built by a student, for students.