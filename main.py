import threading

import discordBot
import telegramBot


def main():
    discord_thread = threading.Thread(target=discordBot.init)
    telegram_thread = threading.Thread(target=telegramBot.main)

    discord_thread.start()
    telegram_thread.start()

    discord_thread.join()
    telegram_thread.join()


if __name__ == '__main__':
    main()
