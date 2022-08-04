#? terminal coloring
# BOLD = '\033[1m'
# U = '\033[4m'
# BL='\033[0;30m'        # Black
# R='\033[0;31m'          # Red
# G='\033[0;32m'        # Green
# Y='\033[0;33m'       # Yellow
# B='\033[0;34m'         # Blue
# P='\033[0;35m'       # Purple
# C='\033[0;36m'         # Cyan
# W='\033[0;37m'        # White

print("""\33[32m\033[0;32m
                                                                              
\033[0;34mali@Github: https://github.com/morethancoder\033[0;32m                     
                                                                          
MMMMMMMM               MMMMMMMMTTTTTTTTTTTTTTTTTTTTTTT       CCCCCCCCCCCCC
M:::::::M             M:::::::MT:::::::::::::::::::::T    CCC::::::::::::C
M::::::::M           M::::::::MT:::::::::::::::::::::T  CC:::::::::::::::C
M:::::::::M         M:::::::::MT:::::TT:::::::TT:::::T C:::::CCCCCCCC::::C
M::::::::::M       M::::::::::MTTTTTT  T:::::T  TTTTTTC:::::C       CCCCCC
M:::::::::::M     M:::::::::::M        T:::::T       C:::::C              
M:::::::M::::M   M::::M:::::::M        T:::::T       C:::::C              
M::::::M M::::M M::::M M::::::M        T:::::T       C:::::C                   
M::::::M  M::::M::::M  M::::::M        T:::::T       C:::::C                  
M::::::M   M:::::::M   M::::::M        T:::::T       C:::::C              
M::::::M    M:::::M    M::::::M        T:::::T       C:::::C              
M::::::M     MMMMM     M::::::M        T:::::T        C:::::C       CCCCCC
M::::::M               M::::::M      TT:::::::TT       C:::::CCCCCCCC::::C
M::::::M               M::::::M      T:::::::::T        CC:::::::::::::::C
M::::::M               M::::::M      T:::::::::T          CCC::::::::::::C
MMMMMMMM               MMMMMMMM      TTTTTTTTTTT             CCCCCCCCCCCCC

\33[37m\033[0;37m""")
# imports
import os
from time import sleep
# first thing first check install packages
try:
    from pytube import YouTube
    from telebot import TeleBot
    from telebot.types import BotCommand
except ImportError as e:
    print(f"\n\033[0;31mImportError : {e}\033[0;37m")
    print("""
    please install required libraries to start the script
    you can find more details on \033[0;36m./README.md\033[0;37m file
    """)
    exit()

# variables
DOWNLOAD_PATH="./downloads/"
listening=False
commands = [
BotCommand("start","welcome message"),
BotCommand("help","help message"),
BotCommand("download","downloads a youtube video from url")
]
text_msg={
    "welcome":u"\nأهلاً ({name}) ✋"
    "\nهذا البوت يعمل على سورس tubaty 🤖"
    "\n\n  اكتب /download لتحميل فيديو من اليوتيوب",
    "url":"ارسل رابط الفيديو",
    "download_start":"جاي تنزيل الفيديو الرجاء الانتظار ...",
    "download_end":"تم تنزيل الفيديو بنجاح !"
}


for i in range(5):
    try:
        TOKEN=input("\n\033[0;33m[TOKEN]\033[0;37m  enter your telebot token : ")
        bot = TeleBot(TOKEN)
        bot.set_my_commands(commands)
        break
    except:
        print("\n\033[0;31m[Error]\033[0;37m your telebot token is not valid please try another one !")
        continue

print("\nyour bot has been \033[0;32mactivated\033[0;37m !")

@bot.message_handler(commands=["start","help"])
def on_start(msg):
    chat_id = msg.chat.id
    first_name = msg.from_user.first_name
    bot.send_message(chat_id,text_msg["welcome"].format(name=first_name))

@bot.message_handler(commands=["download"])
def on_download(msg):
    chat_id = msg.chat.id
    url_request =bot.send_message(chat_id,text_msg["url"])
    bot.register_next_step_handler(url_request,download)
def download(urlmsg):
    url=urlmsg.text
    chat_id = urlmsg.chat.id
    new_message=bot.send_message(chat_id,text_msg["download_start"])
    message_id=new_message.message_id
    if os.path.exists(DOWNLOAD_PATH):
        pass
    else:
        os.mkdir("downloads")
    tube=YouTube(url)
    tube.streams.filter(progressive=True, file_extension="mp4")
    tube.streams.get_highest_resolution().download(DOWNLOAD_PATH)
    bot.edit_message_text(text_msg["download_end"],chat_id,message_id)
    media=open(DOWNLOAD_PATH)
    #TODO we are stuck here how to send the video
    bot.send_video(chat_id,media)
    

print("""
your bot is running with \033[0;35mtubaty\033[0;37m source ...
""")
bot.infinity_polling()