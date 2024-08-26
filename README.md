# dani

Your mechanic under the hood. A Discord utility and helper.

This Discord bot provides commands to manage channel names within your server, specifically for adding and removing emoji prefixes based on category names.

## Features

- `/chan paint`: Adds emoji prefixes to channel names based on their category's emoji.
- `/chan strip`: Removes emoji prefixes from all channel names.

## Requirements

- Python 3.8 or higher
- discord.py library
- A Discord Bot Token

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/discord-channel-manager-bot.git
   cd discord-channel-manager-bot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your Discord Bot Token:
   ```
   DISCORD_TOKEN=your_bot_token_here
   GUILD_ID=your_guild_id_here
   ```

## Usage

1. Start the bot:
   ```
   python main.py
   ```

2. In your Discord server, use the following commands:
   - `/chan paint`: Add emoji prefixes to channel names
   - `/chan strip`: Remove emoji prefixes from channel names

## Project Structure

```
discord-bot/
│
├── main.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
│
├── cogs/
│   ├── __init__.py
│   └── channel_management.py
│
└── utils/
    ├── __init__.py
    ├── emoji_helpers.py
    └── command_sync.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This bot is not affiliated with Discord Inc. Use it at your own risk.

## Support

If you encounter any problems or have any questions, please open an issue in this repository.