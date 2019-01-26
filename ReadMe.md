# Written By Chris Doherty

## This application will send a Facebook message

The idea behind this program is to automatically send a Facebook message to a user. All the messages are in a text file which the program will select one message (one line) from the file and send it to the user of your choice.

## How to use
1. Clone this repo
2. Rename the "sample_data" folder to "data"
3. Edit the creds.config file in the data folder with your Facebook account information

   NOTE: Do not leave any space between the colon and your information
  Enter the username of the person you intend to send the messages to 
  To find their username look them up on Facebook and it should be the text directly after facebook.com/\<username>

4. Edit the messages you want to send in the messages.txt file 

   The program will randomly choose one of these messages. It will not go in order

5. After you are done editing the messages.txt file copy its contents to the messages.bak file

   The .bak file will be used when all the messages in the messages.txt file are gone to populate the .txt file again

6. To compile the program into an exe you will need pyinstaller
7. Using your terminal (PowerShell, cmd) browse to the folder containing your files
8. Use pip to install pyinstaller (pip install pyinstaller)
9. run pyinstaller to create your exe (pyinstaller --onefile send-facebook-message-no-prompt.py)
10. We need to include the data folder so look at the sample-send-facebook-message-no-prompt.spec and add  
    
    Tree('data', prefix='data'),

    in the same location
11. Re-build your exe (pyinstaller send-facebook-message-no-prompt.spec)
12. Look in the dist folder to find your .exe