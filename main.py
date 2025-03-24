import threading

import discordBot
import telegramBot


def main():
    discord_thread = threading.Thread(target=discordBot.init)
    discord_thread.start()
    telegramBot.main()
    discord_thread.join()


if __name__ == '__main__':
    main()
