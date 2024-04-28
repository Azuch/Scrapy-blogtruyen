import telepot
import psutil
import time

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual Telegram bot token
bot = telepot.Bot('YOUR_TELEGRAM_BOT_TOKEN')

def check_process(pid):
    for proc in psutil.process_iter(['pid', 'cmdline']):
        if proc.info['pid'] == pid:
            return True, proc.info['cmdline']
    return False, None

def send_message(chat_id, message):
    bot.sendMessage(chat_id, message)

def monitor_process(chat_id, pid, command):
    while True:
        done, _ = check_process(pid)
        if not done:
            send_message(chat_id, f"The process {pid} with command '{command}' is done")
            break
        time.sleep(5)  # Check every 5 seconds

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        command = msg['text']
        if command.isdigit():
            pid = int(command)
            exists, command = check_process(pid)
            if exists:
                send_message(chat_id, f"Process {pid} with command '{command}' is running")
                monitor_process(chat_id, pid, command)
            else:
                send_message(chat_id, f"No process found with PID {pid}")

bot.message_loop(handle)

# Keep the program running
while True:
    time.sleep(10)
