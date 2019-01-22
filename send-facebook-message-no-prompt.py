"""

pyinstaller --onefile --add-data "messages.txt;messages.txt" --add-data "messages.bak;messages.bak" --add-data "creds.config;creds.config" fbchat_send_message.py
Gives me the error no messages in file

"""
import os
import random
import sys
from fbchat import Client
from fbchat.models import *

messages_file_name = "messages.txt"
messages_backup_file_name = "messages.bak"
credentials_file_name = "creds.config"
data_dir = "data"


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)

    return os.path.join(relative)


messages_file = resource_path(os.path.join(data_dir, messages_file_name))
messages_backup_file = resource_path(os.path.join(data_dir, messages_backup_file_name))
credentials_file = resource_path(os.path.join(data_dir, credentials_file_name))


def create_client():
    credentials = {}
    with open(credentials_file) as f:
        for line in f:
            (key, val) = line.split(':')
            credentials[key] = val

    client_connection = Client(credentials['email'], credentials['password'])

    return client_connection, credentials['user_name']


def getuserid(client_connection, username):
    # `searchForUsers` searches for the user and gives us a list of the results,
    # and then we just take the first one, aka. the most likely one:
    user = client_connection.searchForUsers(username)[0]

    return user.uid


def find_a_Message():
    all_messages = []

    # Read in all lines from the file storing as list
    try:
        with open(messages_file, "r", encoding="utf8") as f:
            all_messages = f.readlines()
        f.close()

        len_of_list = len(all_messages)

        # If there are no messages copy all from backup file
        if len_of_list == 0:
            with open(messages_backup_file, "r", encoding="utf8") as f:
                all_messages = f.readlines()
                f.close()
                len_of_list = len(all_messages)
            fw = open(messages_file, "w", encoding="utf8")
            for x in range(len_of_list):
                fw.write(all_messages[x])
            fw.close()

        # generate random number to use as index for message
        message_index_to_send = random.randint(0, (len_of_list - 1))

        # Open messages.text to write back all messages we didn't use
        fw = open(messages_file, "w", encoding="utf8")
        for x in range(len_of_list):
            if x != message_index_to_send:
                fw.write(all_messages[x])
        fw.close()

        message_to_send = all_messages[message_index_to_send]

        return message_to_send

    # If there are no more messages to send
    except:
        print("Error Finding message or copying from backup")
        sys.exit(-1)


def send_message(client_connection, cust_message, thread_id):
    thread_type = ThreadType.USER
    # Will send a message to the thread
    try:
        output = client_connection.send(Message(text=cust_message), thread_id=thread_id, thread_type=thread_type)
        return output
    except Exception as error:
        print("Failed Sending Message: " + str(error))
        sys.exit(-1)


def main():
    # S3: compose message - moved to top so we do not have to keep trying if there
    # are no more messages
    message = find_a_Message()

    # step 1: login
    client_connection, user_name = create_client()

    # s2: get user ID from user name
    uid = getuserid(client_connection, user_name)

    # s4: send message
    send_message(client_connection, message, uid)


main()
