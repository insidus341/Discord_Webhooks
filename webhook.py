from discord_webhook import DiscordWebhook, DiscordEmbed
import sys

###########################################################
# https://github.com/insidus341/Discord_Webhooks
###########################################################

# When running this file you need to include two additional parameter
# Example: python3 webhook.py <applcation> <code>

# If <application> exists in the the APPLICATIONS dictionary, the logs can be included in the Webhook call
# <code> has to match a specific code, such as 'start', 'stop' and 'restart'

###########################################################
#### START OF CONFIGUABLES ####
###########################################################

# This is the URL of your server/channel
DISCORD_WEBHOOK_URL = 'https://...'

# Your USER ID. Can be 'Everyone'
DISCORD_USER_ID = '12345...'

# Shall we attach the logs? (configurable in APPLICATIONS)
ATTACH_LOGS = True

# Shall we embed 10 lines of the logs?
EMBED_LOGS = True

# The list of applications and their logs which you want to include
APPLICATIONS = {
    'Server': '/var/log/syslog',
    'Apache2': '/var/log/apache2/access.log'
}

# A list of service codes
CODES = {
    'stop': 'has been stopped',
    'restart': 'has been restarted',
    'start': 'has been started'
 }


###########################################################
#### END OF CONFIGUABLES ####
###########################################################


# Returns the last x number of lines from a file
def tail(filename, no_of_lines=1):
    lines_to_return = ''

    file = open(filename,'r')
    lines = file.readlines()
    last_lines = lines[-no_of_lines:]
    for line in last_lines:
        lines_to_return = lines_to_return + line
    file.close()

    return lines_to_return


def lookup_code(code):
    try:
        return CODES[code]
    except:
        return False


def lookup_application_logs(application):
    try:
        return APPLICATIONS[application]
    except:
        return False


# Format the message our Webhook sends
def format_message(application, action):
    return "<@{}> {} {}".format(DISCORD_USER_ID, application, action)


def send_webhook_message(application, action):
    message_to_send = format_message(application, action)
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=message_to_send)

    if ATTACH_LOGS:
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

    if EMBED_LOGS:
        application_logs = lookup_application_logs(application)
        syslogs = lookup_application_logs('Server')

        if application_logs is not False:
            embed = DiscordEmbed(title=application, description=tail(application_logs, 10))
            webhook.add_embed(embed)

        if syslogs is not False:
            embed = DiscordEmbed(title='/var/log/syslog', description=tail(syslogs, 10))
            webhook.add_embed(embed)

    webhook.execute()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        application = sys.argv[1]
        code = sys.argv[2]

        action = lookup_code(code)
        if action is False:
            exit()

        send_webhook_message(application, action)