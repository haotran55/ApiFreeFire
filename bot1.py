import telebot
import subprocess
import sys
import json
from requests import post, Session
import time
import datetime
import threading
from urllib.parse import urlparse
import psutil
import tempfile
import random
from gtts import gTTS
import re
import string
import os
from flask import Flask, request
from threading import Lock
import requests
import sqlite3
from telebot import types
from time import strftime
import queue
import pytz
from datetime import timedelta
from keep_alive import keep_alive
keep_alive()
BOT_TOKEN = os.environ.get('BOT_TOKEN')  # <- thêm dòng này
bot = telebot.TeleBot(BOT_TOKEN)         # <- bot dùng biến này

print(BOT_TOKEN)  # Kiểm tra token có tồn tại không
print("Bot đã được khởi động thành công")
admin_diggory = "HaoEsport" 
name_bot = "Trần Hào"
ADMIN_ID = '7912024917'
zalo = "0585019743"
web = "https://dichvukey.site/"
facebook = "no"
users_keys = {}
key = ""
user_cooldown = {}
active_processes = {}
last_usage = {} 
share_log = []
auto_spam_active = False
last_sms_time = {}
global_lock = Lock()
allowed_users = []
processes = []
admin_mode = False
ADMIN_ID = 7658079324 #nhớ thay id nhé nếu k thay k duyệt dc vip đâu v.L..ong.a
allowed_group_id = -1002639856138
connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()
last_command_time = {}

last_command_timegg = 0



def check_command_cooldown(user_id, command, cooldown):
    current_time = time.time()
    
    if user_id in last_command_time and current_time - last_command_time[user_id].get(command, 0) < cooldown:
        remaining_time = int(cooldown - (current_time - last_command_time[user_id].get(command, 0)))
        return remaining_time
    else:
        last_command_time.setdefault(user_id, {})[command] = current_time
        return None

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        expiration_time TEXT
    )
''')
connection.commit()

def TimeStamp():
  now = str(datetime.date.today())
  return now

#vLong zz#v
def load_users_from_database():
  cursor.execute('SELECT user_id, expiration_time FROM users')
  rows = cursor.fetchall()
  for row in rows:
    user_id = row[0]
    expiration_time = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
    if expiration_time > datetime.datetime.now():
      allowed_users.append(user_id)


def save_user_to_database(connection, user_id, expiration_time):
  cursor = connection.cursor()
  cursor.execute(
    '''
        INSERT OR REPLACE INTO users (user_id, expiration_time)
        VALUES (?, ?)
    ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
  connection.commit()
###

vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')


###
#zalo ...07890416.31

####
start_time = time.time()



video_url = 'https://v16m-default.akamaized.net/b7650db4ac7f717b7be6bd6a04777a0d/66a418a5/video/tos/useast2a/tos-useast2a-ve-0068-euttp/o4QTIgGIrNbkAPGKKLKteXyLedLE7IEgeSzeE2/?a=0&bti=OTg7QGo5QHM6OjZALTAzYCMvcCMxNDNg&ch=0&cr=0&dr=0&lr=all&cd=0%7C0%7C0%7C0&cv=1&br=2576&bt=1288&cs=0&ds=6&ft=XE5bCqT0majPD12cy-773wUOx5EcMeF~O5&mime_type=video_mp4&qs=0&rc=Mzk1OzY7PGdpZjxkOTQ3M0Bpajh1O2w5cmlzbzMzZjgzM0AuNWJgLi02NjMxLzBgXjUyYSNzNmptMmRjazFgLS1kL2Nzcw%3D%3D&vvpl=1&l=202407261543513F37EAD38E23B6263167&btag=e00088000'
@bot.message_handler(commands=['add', 'adduser'])
def add_user(message):
    admin_id = message.from_user.id
    if admin_id != ADMIN_ID:
        bot.reply_to(message, 'Bạn Không Phải admin')
        return

    if len(message.text.split()) == 1:
        bot.reply_to(message, 'VUI LÒNG NHẬP ID NGƯỜI DÙNG VÀ SỐ NGÀY')
        return
    if len(message.text.split()) == 2:
        bot.reply_to(message, 'HÃY NHẬP SỐ NGÀY')
        return
    user_id = int(message.text.split()[1])
    allowed_users.append(user_id)
    days = int(message.text.split()[2])
    expiration_time = datetime.datetime.now() + datetime.timedelta(days)
    connection = sqlite3.connect('user_data.db')
    save_user_to_database(connection, user_id, expiration_time)
    connection.close()

    caption_text = (f'<blockquote>NGƯỜI DÙNG CÓ ID {user_id}\nĐÃ ĐƯỢC THÊM VÀO DANH SÁCH VIP\nTHỜI GIAN: {days} DAY\nLỆNH CÓ THỂ SỬ DỤNG CÁC LỆNH TRONG [/start]</blockquote>')
    bot.send_video(
        message.chat.id,
        video_url,
        caption=caption_text, parse_mode='HTML')

load_users_from_database()

def is_key_approved(chat_id, key):
    if chat_id in users_keys:
        user_key, timestamp = users_keys[chat_id]
        if user_key == key:
            current_time = datetime.datetime.now()
            if current_time - timestamp <= datetime.timedelta(hours=2):
                return True
            else:
                del users_keys[chat_id]
    return False



VERIFIED_FILE = "verified_users.txt"

# 🕒 Hàm tạo timestamp
def TimeStamp():
    return datetime.datetime.now().strftime("%d/%m/%Y")

# ✅ Kiểm tra user đã vượt key chưa
def is_user_verified(user_id):
    if not os.path.exists(VERIFIED_FILE):
        return False
    with open(VERIFIED_FILE, "r") as f:
        return str(user_id) in f.read()

# 💾 Ghi user vào file sau khi xác thực thành công
def save_verified_user(user_id):
    with open(VERIFIED_FILE, "a") as f:
        f.write(f"{user_id}\n")

# 📩 /getkey – Gửi link lấy key
@bot.message_handler(commands=['getkey'])
def startkey(message: Message):
    user_id = message.from_user.id

    if is_user_verified(user_id):
        bot.reply_to(message, "✅ Bạn đã vượt key rồi, không cần lấy lại nữa.")
        return

    today_day = datetime.date.today().day
    key = "haoesport" + str(user_id * today_day - 2007)

    api_token = '67c1fe72a448b83a9c7e7340'  # Bạn nên ẩn token nếu đưa lên GitHub
    key_url = f"https://haoesportst.blogspot.com/2025/04/blog-post.html?key={key}"

    try:
        response = requests.get(f'https://link4m.co/api-shorten/v2?api={api_token}&url={key_url}')
        response.raise_for_status()
        url_data = response.json()

        if 'shortenedUrl' in url_data:
            url_key = url_data['shortenedUrl']
            text = (f'🔑 Link lấy Key ngày {TimeStamp()} là:\n{url_key}\n\n'
                    '✅ Sau khi lấy key, nhập /key <key của bạn> để xác thực.\n'
                    '👉 Hoặc nhập /muavip nếu không muốn vượt key mỗi ngày.')
            bot.reply_to(message, text)
        else:
            bot.reply_to(message, '⚠️ Lỗi: Không rút gọn được link.')
    except requests.RequestException:
        bot.reply_to(message, '⚠️ Lỗi khi kết nối đến hệ thống rút gọn.')

# ✅ /key – Kiểm tra key người dùng nhập vào
@bot.message_handler(commands=['key'])
def key(message: Message):
    if len(message.text.split()) != 2:
        bot.reply_to(message, '❓ Nhập sai cú pháp! Vui lòng dùng: /key <key của bạn>')
        return

    user_id = message.from_user.id
    key_input = message.text.split()[1]
    today_day = datetime.date.today().day
    expected_key = "haoesport" + str(user_id * today_day - 2007)

    if key_input == expected_key:
        if not is_user_verified(user_id):
            save_verified_user(user_id)

        text_message = f'<blockquote>[ ✅ KEY HỢP LỆ ]\nID Người dùng: <b>{user_id}</b>\nĐã được phép sử dụng các lệnh trong /bot</blockquote>'
        video_url = 'https://v16m-default.tiktokcdn.com/0acc3d8de1dfd9654aa08021bba9a94f/67f4edda/video/tos/useast2a/tos-useast2a-ve-0068c003/oc1EA6nAeRTT8X3eRkbEGMU0EwMaeeRpADFM4g/?a=0&bti=OTg7QGo5QHM6OjZALTAzYCMvcCMxNDNg&ch=0&cr=0&dr=0&er=0&lr=all&net=0&cd=0%7C0%7C0%7C0&cv=1&br=4244&bt=2122&cs=0&ds=6&ft=EeF4ntZWD03Q12NvrxloeIxRSfYFpq_45SY&mime_type=video_mp4&qs=0&rc=aDppaTdkODRpZzc3NmczNkBpam08amY6ZjhpbTMzNzczM0A1LmBeYl9eXzIxMmBiLjYtYSMubzYucjQwY3FgLS1kMTZzcw%3D%3D&vvpl=1&l=20250408113503D5D8A4FD124771691A53&btag=e000b8000'  # Thay link video bạn muốn

        bot.send_video(message.chat.id, video_url, caption=text_message, parse_mode='HTML')
    else:
        bot.reply_to(message, '❌ KEY KHÔNG HỢP LỆ. Hãy kiểm tra lại.')


@bot.message_handler(commands=['bot','start'])
def send_help(message):
    bot.reply_to(message, """<blockquote>
┌───⭓ Trần Hào
➤ /spam : Spam FREE
➤ /spamvip : Spam Vip
➤ /stop : Dừng Spam SĐT
➤ /tv : Tiếng việt cho telegram
➤ /id : Lấy id bản thân
└───Tiện Ích Khác
➤ /like : Buff Like FF
➤ /voice : Chuyển văn bản thành giọng nói 
➤ /hoi : hỏi gamini 
➤ /tiktokinfo : xem thông tin tiktok
└───Contact
➤ /admin : Liên Hệ admin
└───
</blockquote>""", parse_mode="HTML")
### /like
API_BASE_URL = "https://dichvukey.site/freefire/like.php?key=vLong161656"

def call_api(uid):
    url = f"{API_BASE_URL}&uid={uid}"
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return {"status": "error", "message": "Server đang bị admin Tắt"}

@bot.message_handler(commands=['like'])
def like_handler(message):
    args = message.text.split()

    if len(args) != 2:
        bot.reply_to(message, "<blockquote>🔹 Cách dùng: /like [UID]</blockquote>", parse_mode="HTML")
        return

    uid = args[1]

    # Gửi thông báo "loading"
    loading_msg = bot.reply_to(message, "<i>⏳ Đang tiến hành buff like...</i>", parse_mode="HTML")

    data = call_api(uid)

    if data.get("status") == "error":
        bot.edit_message_text(
            f"<blockquote>❌ {data['message']}</blockquote>",
            chat_id=loading_msg.chat.id,
            message_id=loading_msg.message_id,
            parse_mode="HTML"
        )
        return

    reply_text = (
        f"<blockquote>\n"
        f"🎯 <b>Kết quả buff like:</b>\n"
        f"👤 <b>Tên:</b> {data.get('username', 'Tạm Thời Lỗi')}\n"
        f"🆔 <b>UID:</b> {data.get('uid', 'Không xác định')}\n"
        f"👍 <b>Like trước:</b> {data.get('likes_before', 'Tạm Thời Lỗi')}\n"
        f"✅ <b>Like sau:</b> {data.get('likes_after', 'Tạm Thời Lỗi')}\n"
        f"➕ <b>Tổng cộng:</b> {data.get('likes_given', 'Tạm Thời Lỗi')} like\n"
        f"</blockquote>"
    )

    bot.edit_message_text(
        reply_text,
        chat_id=loading_msg.chat.id,
        message_id=loading_msg.message_id,
        parse_mode="HTML"
    )

@bot.message_handler(commands=['voice'])
def text_to_voice(message):
    text = message.text[7:].strip()  
    if not text:
        bot.reply_to(message, 'Nhập nội dung đi VD : /voice Tôi là bot')
        return

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            tts = gTTS(text, lang='vi')
            tts.save(temp_file.name)
            temp_file_path = temp_file.name  
       
        with open(temp_file_path, 'rb') as f:
            bot.send_voice(message.chat.id, f, reply_to_message_id=message.message_id)
    
    except Exception as e:
        bot.reply_to(message, f'Đã xảy ra lỗi: {e}')
    
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)




@bot.message_handler(commands=['hoi'])
def handle_hoi(message):
    text = message.text[len('/hoi '):].strip()
    
    if text:
        url = f"https://dichvukey.site/apishare/hoi.php?text={text}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            reply = data.get("message", "Không có phản hồi.")
        else:
            reply = "Lỗi."
    else:
        reply = "Lệnh Ví Dụ : /hoi xin chào."
    bot.reply_to(message, reply)

@bot.message_handler(commands=['time'])
def handle_time(message):
    uptime_seconds = int(time.time() - start_time)
    
    uptime_minutes, uptime_seconds = divmod(uptime_seconds, 60)
    bot.reply_to(message, f'Bot đã hoạt động được: {uptime_minutes} phút, {uptime_seconds} giây')



@bot.message_handler(commands=['id', 'ID'])
def handle_id_command(message):
    if message.reply_to_message:  
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
        bot.reply_to(message, f"ID của {first_name} là: `{user_id}`", parse_mode='Markdown')
    elif len(message.text.split()) == 1:
        if message.chat.type in ["group", "supergroup"]:
            chat_id = message.chat.id
            chat_title = message.chat.title
            bot.reply_to(message, f"ID của nhóm này là: `{chat_id}`\nTên nhóm: {chat_title}", parse_mode='Markdown')
        else:
            user_id = message.from_user.id
            first_name = message.from_user.first_name
            bot.reply_to(message, f"ID của bạn là: `{user_id}`\nTên: {first_name}", parse_mode='Markdown')


   
def detect_carrier(phone_number: str) -> str:
    phone_number = phone_number.strip().replace("+84", "0")
    prefixes = {
        "Viettel": ["086", "096", "097", "098", "032", "033", "034", "035", "036", "037", "038", "039"],
        "Mobifone": ["089", "090", "093", "070", "076", "077", "078", "079"],
        "Vinaphone": ["088", "091", "094", "081", "082", "083", "084", "085"],
        "Vietnamobile": ["092", "056", "058"],
        "Gmobile": ["099", "059"],
    }

    for name, prefix_list in prefixes.items():
        if any(phone_number.startswith(p) for p in prefix_list):
            return name
    return "Không xác định"


@bot.message_handler(commands=['spam'])
def spam(message):
    user_id = message.from_user.id
    current_time = time.time()
    
    if not bot_active:
        msg = bot.reply_to(message, 'Bot hiện đang tắt.')
        time.sleep(10)
        try:
            bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Error deleting message: {e}")
        return

    if admin_mode and user_id not in admins:
        msg = bot.reply_to(message, 'có lẽ admin đang fix gì đó hãy đợi xíu')
        time.sleep(10)
        try:
            bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Error deleting message: {e}")
        return

    if user_id in last_usage and current_time - last_usage[user_id] < 10:
        warn_msg = bot.reply_to(message, f"⏳ Vui lòng đợi {10 - (current_time - last_usage[user_id]):.1f} giây trước khi dùng lại.")
        time.sleep(10)
        try:
            bot.delete_message(chat_id=message.chat.id, message_id=warn_msg.message_id)
        except:
            pass
        return

    # Phân tích cú pháp
    params = message.text.split()[1:]
    if len(params) != 2:
        msg = bot.reply_to(message, "/spam sdt số_lần như này cơ mà")
        time.sleep(10)
        bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
        return

    sdt, count = params
    carrier = detect_carrier(sdt)

    if not count.isdigit():
        msg = bot.reply_to(message, "Số lần spam không hợp lệ. Vui lòng chỉ nhập số.")
        time.sleep(10)
        bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
        return

    count = int(count)

    if count > 25:
        msg = bot.reply_to(message, "/spam sdt số_lần tối đa là 25 - đợi 10 giây sử dụng lại.")
        time.sleep(10)
        bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
        return

    if sdt in blacklist:
        msg = bot.reply_to(message, f"Số điện thoại {sdt} đã bị cấm spam.")
        time.sleep(10)
        bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
        return

    sdt_request = f"84{sdt[1:]}" if sdt.startswith("0") else sdt

    username = message.from_user.username if message.from_user.username else "Không có username"
    diggory_chat3 = f'''┌──────⭓ {name_bot}
➤ Sᴘᴀᴍ : Thành Công 
➤ Số Lần Sᴘᴀᴍ : {count}
➤ Đang Tấn Công : {sdt}
➤ Dừng Sᴘᴀᴍ [/stop {sdt}]
➤ Nhà Mạng : {carrier}
➤ Vùng : Việt Nam
➤ Người Dùng : @{username}
➤ ⵊD Người Dùng : {user_id}
└─────────────
'''

    script_filename = "dec.py"
    try:
        if not os.path.isfile(script_filename):
            bot.reply_to(message, "Không tìm thấy file script.")
            return

        with open(script_filename, 'r', encoding='utf-8') as file:
            script_content = file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(script_content.encode('utf-8'))
            temp_file_path = temp_file.name

        # Chạy script spam
        process = subprocess.Popen(["python", temp_file_path, sdt, str(count)])
        active_processes[sdt] = process
        # Gửi kết quả spam
        sent_msg = bot.send_message(
            message.chat.id,
            f'<blockquote>{diggory_chat3}</blockquote>\n<blockquote>GÓI NGƯỜI DÙNG: FREE</blockquote>',
            parse_mode='HTML'
        )

        threading.Thread(
        target=lambda: (
        time.sleep(0),
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    )
).start()

        last_usage[user_id] = current_time

    except FileNotFoundError:
        bot.reply_to(message, "Không tìm thấy file.")
    except Exception as e:
        bot.reply_to(message, f"Lỗi xảy ra: {str(e)}")


blacklist = ["112", "113", "114", "115", "116", "117", "118", "119", "0", "1", "2", "3", "4"]


@bot.message_handler(commands=['spamvip'])
def spam(message):
    user_id = message.from_user.id
    current_time = time.time()
    
    if not bot_active:
        msg = bot.reply_to(message, 'Bot hiện đang tắt.')
        time.sleep(10)
        try:
            bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Error deleting message: {e}")
        return

    if admin_mode and user_id not in admins:
        msg = bot.reply_to(message, 'có lẽ admin đang fix gì đó hãy đợi xíu')
        time.sleep(10)
        try:
            bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Error deleting message: {e}")
        return

    if user_id in last_usage and current_time - last_usage[user_id] < 10:
        warn_msg = bot.reply_to(message, f"⏳ Vui lòng đợi {100 - (current_time - last_usage[user_id]):.1f} giây trước khi dùng lại.")
        time.sleep(10)
        try:
            bot.delete_message(chat_id=message.chat.id, message_id=warn_msg.message_id)
        except:
            pass
        return

    # Phân tích cú pháp
    params = message.text.split()[1:]
    if len(params) != 2:
        msg = bot.reply_to(message, "/spamvip sdt số_lần")
        time.sleep(10)
        bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
        return

    sdt, count = params
    carrier = detect_carrier(sdt)

    if not count.isdigit():
        msg = bot.reply_to(message, "Số lần spam không hợp lệ. Vui lòng chỉ nhập số.")
        time.sleep(10)
        bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
        return

    count = int(count)

    if count > 100:
        msg = bot.reply_to(message, "/spamvip sdt số_lần tối đa là 100 - đợi 100 giây sử dụng lại.")
        time.sleep(10)
        bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
        return

    if sdt in blacklist:
        msg = bot.reply_to(message, f"Số điện thoại {sdt} đã bị cấm spam.")
        time.sleep(10)
        bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
        return

    sdt_request = f"84{sdt[1:]}" if sdt.startswith("0") else sdt

    username = message.from_user.username if message.from_user.username else "Không có username"
    first_name = message.from_user.first_name
    diggory_chat3 = f'''┌──────⭓ {name_bot}
┌───⭓
» {first_name} | @{username}
» ID [{user_id}]
└───⧕

┌───⭓
» Server: Spam SMS VIP
» Đang Tiến Hành Spam: [ {sdt} ]
» Nhà Mạng: [ {carrier} ]
» Vòng Lặp Spam: {count}
» Dừng Spam [/stop {sdt}]
└───⧕
'''

    script_filename = "dec.py"
    try:
        if not os.path.isfile(script_filename):
            bot.reply_to(message, "Không tìm thấy file script.")
            return

        with open(script_filename, 'r', encoding='utf-8') as file:
            script_content = file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(script_content.encode('utf-8'))
            temp_file_path = temp_file.name

        # Chạy script spam
        process = subprocess.Popen(["python", temp_file_path, sdt, str(count)])
        active_processes[sdt] = process
        # Gửi kết quả spam
        sent_msg = bot.send_message(
            message.chat.id,
            f'<blockquote>{diggory_chat3}</blockquote>\n<blockquote>GÓI NGƯỜI DÙNG: VIP</blockquote>',
            parse_mode='HTML'
        )

        threading.Thread(
        target=lambda: (
        time.sleep(0),
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    )
).start()

        last_usage[user_id] = current_time

    except FileNotFoundError:
        bot.reply_to(message, "Không tìm thấy file.")
    except Exception as e:
        bot.reply_to(message, f"Lỗi xảy ra: {str(e)}")


blacklist = ["112", "113", "114", "115", "116", "117", "118", "119", "0", "1", "2", "3", "4"]



@bot.message_handler(commands=['stop'])
def stop_spam(message):
    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "Dùng đúng cú pháp: /stop 098xxxxxxx")
        return

    sdt = args[1]
    process = active_processes.get(sdt)

    if process:
        process.terminate()  # Dừng tiến trình
        del active_processes[sdt]  # Xóa khỏi danh sách
        bot.reply_to(message, f"⛔️ Đã dừng spam số {sdt}")
    else:
        bot.reply_to(message, f"Không tìm thấy tiến trình spam với số {sdt}. Có thể đã hoàn thành hoặc sai số.")




@bot.message_handler(commands=['tiktokinfo'])
def get_tiktok_info(message):
    chat_id = message.chat.id
    args = message.text.split()

    if len(args) < 2:
        bot.send_message(chat_id, "⚠️ Vui lòng nhập tên người dùng TikTok!\nVí dụ: /tiktokinfo ho.esports", parse_mode="Markdown")
        return

    username = args[1]
    api_url = f"https://api.sumiproject.net/tiktok?info={username}"

    try:
        response = requests.get(api_url)
        data = response.json()

        if data['code'] != 0 or 'data' not in data:
            bot.send_message(chat_id, "❌ Không tìm thấy tài khoản TikTok!", parse_mode="Markdown")
            return

        user = data['data']['user']
        stats = data['data']['stats']

        profile_message = f"""
======[ 𝙏𝙄𝙆𝙏𝙊𝙆 𝙄𝙉𝙁𝙊 ]======  

👤 Tên hiển thị: {user['nickname']}  
🆔 Username: @{user['uniqueId']}  
🔗 Profile: [Xem trên TikTok](https://www.tiktok.com/@{user['uniqueId']})  

📊 Thống kê:  
├ 👥 Người theo dõi: {stats['followerCount']}  
├ 👤 Đang theo dõi: {stats['followingCount']}  
├ ❤️ Tổng lượt thích: {stats['heartCount']}  
├ 🎥 Số video: {stats['videoCount']}  

🔗 Mạng xã hội khác:  
{f"▶️ [YouTube](https://www.youtube.com/channel/{user['youtube_channel_id']})" if user.get('youtube_channel_id') else "🚫 Không có YouTube"}  
{f"📌 Bio: {user['signature']}" if user.get('signature') else "🚫 Không có mô tả"}  
        """

        bot.send_photo(chat_id, user['avatarLarger'], caption=profile_message, parse_mode="Markdown")

    except Exception as error:
        bot.send_message(chat_id, "⚠️ Lỗi khi lấy thông tin tài khoản TikTok!", parse_mode="Markdown")
        print(error)

@bot.message_handler(commands=['tv'])
def tieng_viet(message):
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton("Tiếng Việt 🇻🇳", url='https://t.me/setlanguage/vi')
    keyboard.add(url_button)
    bot.send_message(chat_id, '<blockquote>Click vào nút "<b>Tiếng Việt</b>" để đổi ngôn ngữ sang Tiếng Việt 🇻🇳</blockquote>', reply_markup=keyboard, parse_mode='HTML')
######

# Hàm gọi API T
def react_to_message(chat_id, message_id, emoji="❤️"):
    url = f"https://api.telegram.org/bot{os.environ.get('BOT_TOKEN')}/setMessageReaction"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "reaction": [{"type": "emoji", "emoji": emoji}],
        "is_big": True
    }
    requests.post(url, json=payload)

import random

# Danh sách emoji tuỳ thích
emojis = ["❤️", "😂", "🔥", "🤔", "👍", "😍", "😎", "💯", "👏", "😢", "😡"]

@bot.message_handler(func=lambda message: True)
def auto_like(message):
    emoji = random.choice(emojis)  # Lấy emoji ngẫu nhiên
    react_to_message(message.chat.id, message.message_id, emoji=emoji)




if __name__ == "__main__":
    bot_active = True
    bot.polling()  #
