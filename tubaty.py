
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
path_in_use=False
commands = [
BotCommand("start","welcome message"),
BotCommand("help","help message"),
BotCommand("download","downloads a youtube video from url")
]
text_msg={
    "welcome":u"\nأهلاً ({name}) ✋"
    "\n\nهذا البوت يعمل على سورس tubaty 🤖"
    "\n\n  اكتب /download لتحميل فيديو من اليوتيوب",
    "url":"ارسل رابط الفيديو",
    "download_start":"جاي تنزيل {video} الرجاء الانتظار ⏳ ...",
    "download_end":"تم التنزيل بنجاح !",
    "sending":"جاري الارسال  ⏳ ...",
    "done":"{video}",
    "retry":"خطأ : لا يوجد رابط كهذا الرجاء اعادة المحاولة"
}


for i in range(5):
    try:
        TOKEN=input("\n\033[0;33m[TOKEN]\033[0;37m  enter your telebot token : ")
        bot = TeleBot(TOKEN)
        bot.set_my_commands(commands)
        print("\nyour bot has been \033[0;32mactivated\033[0;37m !")
        break
    except:
        print("\n\033[0;31m[Error]\033[0;37m your telebot token is not valid please try another one !")
        continue



@bot.message_handler(commands=["start","help"])
def on_start(msg):
    """
    handles [start,help] commands
    -
    sends a welcome msg with user's name
    """
    chat_id = msg.chat.id
    first_name = msg.from_user.first_name
    bot.send_message(chat_id,text_msg["welcome"].format(name=first_name))

@bot.message_handler(commands=["download"])
def on_download(msg):
    """
    handles the download command
    -
    prompt user to send url then
    activates the download function
    """
    chat_id = msg.chat.id
    url_request =bot.send_message(chat_id,text_msg["url"])
    clean() # cleans only if path not in use
    bot.register_next_step_handler(url_request,validate_url)
def validate_url(urlmsg):
    """
    get valid youtube url
    _
    prompt user to enter url and check if its valid
    """
    url=urlmsg.text
    chat_id = urlmsg.chat.id
    
    try:
        YouTube(url)
    except:
        url_request=bot.send_message(chat_id,text_msg["retry"])
        return bot.register_next_step_handler(url_request,validate_url)
    
    return download(urlmsg)

def download(urlmsg):
    """
    download and send video
    -
    takes the url from user then sends a video downloaded from youtube
    """
    global path_in_use
    path_in_use = True
    chat_id = urlmsg.chat.id
    tube = YouTube(urlmsg.text)
    #TODO check if video already on telegram db
    new_message=bot.send_message(chat_id,text_msg["download_start"].format(video=tube.title))
    message_id=new_message.message_id
    if os.path.exists(DOWNLOAD_PATH):
        pass
    else:
        os.mkdir("downloads")
    tube.streams.filter(progressive=True, file_extension="mp4")
    pathtosaved=tube.streams.get_highest_resolution().download(DOWNLOAD_PATH)
    bot.edit_message_text(text_msg["download_end"],chat_id,message_id)
    media=open(pathtosaved,'rb') #rb for read binary
    bot.edit_message_text(text_msg["sending"],chat_id,message_id)
    bot.send_video(chat_id, video=media, supports_streaming=True)
    bot.edit_message_text(text_msg["done"].format(video=tube.title),chat_id,message_id)
    path_in_use = False
    return 

def clean():
    """
    cleaning
    -
    removes every file in the download directory to free up  space
    """
    global path_in_use
    if path_in_use:
        pass
    else:
        files=os.listdir(DOWNLOAD_PATH)
        for file in files:
            os.remove(DOWNLOAD_PATH+file)

print("""
your bot is running with \033[0;35mtubaty\033[0;37m source ...
""")
bot.infinity_polling()