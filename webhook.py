from discord_webhook import DiscordWebhook, DiscordEmbed
import sys
import os


def tail(filename, no_of_lines=1):
    lines_to_return = ''

    file = open(filename,'r')
    lines = file.readlines()
    last_lines = lines[-no_of_lines:]
    for line in last_lines:
        lines_to_return = lines_to_return + line
    file.close()

    return lines_to_return


DISCORD_WEBHOOK_URL = os.environ['DISCORD_WEBHOOK_URL']
DISCORD_USER_ID = os.environ['DISCORD_USER_ID']

def lookup_code(code):
    codes = {
        'stop': 'has been stopped',
        'restart': 'has been restarted',
        'start': 'has been started'
    }

    try:
        return codes[code]
    except:
        return None


def lookup_application_logs(application):
    applications = {
        'Server': '/var/log/syslog',
        # 'Server': 'test.txt',
        'Kafka Apache Consumer': '/home/kafka/kafka/logs/server.log'
        # 'Kafka Apache Consumer': 'test.txt'
    }

    try:
        return applications[application]
    except:
        return False


def format_message(application, action):
    return "<@{}> {} {}".format(DISCORD_USER_ID, application, action)


def send_webhook_message(application, action):

    message_to_send = format_message(application, action)
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=message_to_send)

    application_logs = lookup_application_logs(application)
    syslogs = lookup_application_logs('Server')

    if application_logs is not False:
        with open(application_logs, "rb+") as f:
            filename = application + '.txt'
            webhook.add_file(file=f.read(), filename=filename)

    if syslogs is not False:
        with open(syslogs, "rb+") as f:
            filename = syslogs + '.txt'
            webhook.add_file(file=f.read(), filename=filename)

    webhook.execute()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        application = sys.argv[1]
        code = sys.argv[2]

        action = lookup_code(code)
        if action is None:
            exit()

        send_webhook_message(application, action)


    # send_webhook_message('Kafka Apache Consumer', 'Start')