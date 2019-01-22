import os
import random
import sys

from fbchat import Client
from fbchat.models import *

# File Names in the data folder. they will be joined with the resource_path function
messages_file_name = "messages.txt"
messages_backup_file_name = "messages.bak"
credentials_file_name = "creds.config"
data_dir = "data"


# Used to ensure we have the correct path after building exe
def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)

    return os.path.join(relative)


# Variables for file references
messages_file = resource_path(os.path.join(data_dir, messages_file_name))
messages_backup_file = resource_path(os.path.join(data_dir, messages_backup_file_name))
credentials_file = resource_path(os.path.join(data_dir, credentials_file_name))


# Creates the client connection
# Returns the connection to pass into the send_message and the username we want to send to
def create_client():
    credentials = {}
    with open(credentials_file) as f:
        for line in f:
            (key, val) = line.split(':')
            credentials[key] = val

    client_connection = Client(credentials['email'], credentials['password'])

    return client_connection, credentials['user_name']


# finds the user id numbers based on the username we want to send to
def getuserid(client_connection, username):
    # `searchForUsers` searches for the user and gives us a list of the results,
    # and then we just take the first one, aka. the most likely one:
    user = client_connection.searchForUsers(username)[0]

    return user.uid


# function pulls a message from the messages.txt file and returns it to be sent
def find_a_Message():
    all_messages = []

    # Read in all lines from the file storing as list
    try:
        # Open the message.txt file and read in all the content
        with open(messages_file, "r", encoding="utf8") as f:
            all_messages = f.readlines()
        f.close()

        # Find the number of messages that were read in
        len_of_list = len(all_messages)

        # If there are no messages read in from messages.txt then copy all
        # the messages from the backup file to the messages.txt file
        # This ensures we use all the messages only once then will reuse messages
        # should be long enough period to forget we already sent that message
        if len_of_list == 0:
            with open(messages_backup_file, "r", encoding="utf8") as f:
                all_messages = f.readlines()
                f.close()
                len_of_list = len(all_messages)
            fw = open(messages_file, "w", encoding="utf8")
            for x in range(len_of_list):
                fw.write(all_messages[x])
            fw.close()

        # generate random number to use as index for message to select
        # this ensures we do not go in order
        message_index_to_send = random.randint(0, (len_of_list - 1))

        # Open messages.txt to write back all messages we didn't use
        fw = open(messages_file, "w", encoding="utf8")
        for x in range(len_of_list):
            # will not write the message at the random index to ensure we only send it once
            if x != message_index_to_send:
                fw.write(all_messages[x])
        fw.close()

        # select the message based on the random index we will send
        message_to_send = all_messages[message_index_to_send]

        # Return the message string
        return message_to_send

    # If there are no more messages to send
    except:
        print("Error Finding message or copying from backup")
        sys.exit(-1)


# this will send the message to the user we wanted
def send_message(client_connection, cust_message, thread_id):
    # Thread type is use to ensure the client knows it is a user we are sending to not a group
    thread_type = ThreadType.USER

    # Will send a message to the thread
    try:
        output = client_connection.send(Message(text=cust_message), thread_id=thread_id, thread_type=thread_type)
        return output

    # likely error is fb locked the account due to suspicious activity
    except Exception as error:
        print("Failed Sending Message: " + str(error))
        sys.exit(-1)


def main():
    # S1: Fina a message from the messages.txt file we will send to the desired user
    message = find_a_Message()

    # Step 2: create a connection to facebook and save return to variables
    client_connection, user_name = create_client()

    # Step 3: get the user ID from user name
    uid = getuserid(client_connection, user_name)

    # Step 4: send the message from the file to the user
    send_message(client_connection, message, uid)


# Calls the main function
main()
