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
import logging
import tempfile
import random
from gtts import gTTS
import re
import string
import os
import io
import base64
import hashlib
from flask import Flask, request
from telebot.types import Message
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
name_bot = "SPAM PRO BOT"
ADMIN_ID = '7658079324'
facebook = "no"
users_keys = {}
key = ""
blacklist = set()# hoặc set(), hoặc list chứa sẵn các số
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


start_time = time.time()



@bot.message_handler(commands=['bot','start'])
def send_help(message):
    bot.reply_to(message, """<blockquote>
┌───⭓ Trần Hào
➤ /spam : Spam FREE
➤ /tv : Tiếng việt cho telegram
➤ /id : Lấy id bản thân
➤ /checkban : Kiểm tra tk có khoá không
➤ /searchff : Tìm tk ff bằng tên
└───Tiện Ích Khác
➤ /ff : check info
➤ /uptime : Xem Thời gian bot hoạt động
➤ /voice : Chuyển văn bản thành giọng nói 
➤ /hoi : hỏi gamini 
└───Contact
➤ /admin : Liên Hệ admin
➤ /themvip : Thêm Vip
└───
</blockquote>""", parse_mode="HTML")
### /like

VIP_FILE = "vip_users.txt"

def is_user_vip(user_id):
    if not os.path.exists(VIP_FILE):
        return False
    with open(VIP_FILE, "r") as f:
        return str(user_id) in f.read()

def save_vip_user(user_id):
    with open(VIP_FILE, "a") as f:
        f.write(f"{user_id}\n")



ADMIN_ID = 7658079324  # thay bằng ID Telegram của bạn

@bot.message_handler(commands=['themvip'])
def themvip(message: Message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "🚫 Bạn không có quyền sử dụng lệnh này.")
        return

    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        bot.reply_to(message, "❓ Dùng đúng cú pháp: /themvip <user_id>")
        return

    user_id_to_add = int(parts[1])
    save_vip_user(user_id_to_add)
    bot.reply_to(message, f"✅ Đã thêm ID {user_id_to_add} vào danh sách VIP.")


import requests

def fetch_data(user_id):
    url = f'https://scromnyimodz-444.vercel.app/api/player-info?id={user_id}'
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

@bot.message_handler(commands=['ff'])
def handle_command(message):
    parts = message.text.split()
    if len(parts) != 2:
        bot.reply_to(message, "<blockquote>❌ Sai cú pháp!\nVí dụ: /ff 12345678</blockquote>", parse_mode="HTML")
        return

    _, user_id = parts

    try:
        data = fetch_data(user_id)
        if not data or data.get('status') != 'success':
            bot.reply_to(message, "<blockquote>❌ Không tìm thấy người chơi hoặc server quá tải!</blockquote>", parse_mode="HTML")
            return

        basic = data['data'].get('basic_info', {})
        clan = data['data'].get('clan', {})
        leader = clan.get('leader', {})

        def g(key, dic): return dic.get(key, 'Không có')

        info = f"""
<blockquote>
<b>📌 Thông tin tài khoản:</b>
Tên: {g('name', basic)}
ID: {g('id', basic)}
Cấp độ: {g('level', basic)}
Booyah Pass: {g('booyah_pass_level', basic)}
Lượt thích: {g('likes', basic)}
Máy chủ: {g('server', basic)}
Tiểu sử: {g('bio', basic)}
Ngày tạo: {g('account_created', basic)}

<b>👥 Thông tin quân đoàn:</b>
Tên: {g('name', clan)}
Cấp độ: {g('level', clan)}
Thành viên: {g('members_count', clan)}

<b>👑 Chủ quân đoàn:</b>
Tên: {g('name', leader)}
Cấp độ: {g('level', leader)}
Lượt thích: {g('likes', leader)}
Ngày tạo: {g('account_created', leader)}
</blockquote>
"""
        bot.reply_to(message, info.strip(), parse_mode="HTML")

    except Exception as e:
        bot.reply_to(message, "<blockquote>⚠️ Đã xảy ra lỗi khi xử lý yêu cầu.</blockquote>", parse_mode="HTML")
        print(e)




start_time = time.time()

# Biến để tính toán FPS
last_time = time.time()
frame_count = 0
fps = 0
# Hàm xử lý lệnh '/like'
import threading

# Hàm animation loading
def animate_loading(chat_id, message_id, stop_event):
    frames = ["⏳", "⌛"]
    max_cycles = 2
    delay = 0.7
    total_frames = len(frames) * max_cycles
    i = 0
    while not stop_event.is_set() and i < total_frames:
        try:
            bot.edit_message_text(frames[i % len(frames)], chat_id, message_id)
            i += 1
        except:
            pass
        time.sleep(delay)

@bot.message_handler(commands=['uptime'])
def uptime(message):
    global last_time, frame_count, fps
    
    # Tính uptime
    uptime_seconds = int(time.time() - start_time)
    uptime_formatted = str(timedelta(seconds=uptime_seconds))
    
    # Tính FPS
    current_time = time.time()
    frame_count += 1
    if current_time - last_time >= 1:
        fps = frame_count
        frame_count = 0
        last_time = current_time

    # Gửi thông báo uptime
    bot.send_message(message.chat.id, 
        f"📊 ⏳ Bot đã hoạt động: {uptime_formatted}\n"
        f"🎮 FPS trung bình: {fps} FPS\n"
        "Không thể lấy thông tin cấu hình.\n"
        "🎥 Video giải trí cho ae FA vibu đây!")

    # Gửi tin nhắn initial loading
    loading_msg = bot.send_message(message.chat.id, "⏳")

    # Tạo sự kiện dừng animation
    stop_event = threading.Event()

    # Bắt đầu animation trong thread riêng
    animation_thread = threading.Thread(
        target=animate_loading,
        args=(message.chat.id, loading_msg.message_id, stop_event)
    )
    animation_thread.start()

    # Lấy video từ API
    video_url = "https://api.ffcommunity.site/randomvideo.php"
    try:
        video_response = requests.get(video_url)
        video_data = video_response.json()
        video_url = video_data.get('url', None)
    except (ValueError, requests.RequestException):
        video_url = None

    # Gửi video nếu có
    if video_url:
        try:
            bot.send_video(message.chat.id, video_url)
        except Exception as e:
            bot.send_message(message.chat.id, f"Không gửi được video: {e}")

    # Dừng animation và xoá tin nhắn loading
    stop_event.set()
    try:
        bot.delete_message(message.chat.id, loading_msg.message_id)
    except:
        pass





 
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




def format_timestamp(timestamp):
    try:
        if not timestamp:
            return "Không rõ"
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%H:%M:%S %d-%m-%Y")
    except:
        return "Không xác định"

def escape_html(text):
    """
    Escape các ký tự đặc biệt để tránh lỗi khi dùng HTML parse mode.
    """
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

@bot.message_handler(commands=['searchff'])
def search_ff(message):
    try:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            bot.reply_to(message, "❗ Vui lòng nhập tên cần tìm. Ví dụ: /searchff Scromnyi")
            return

        username = args[1].strip()
        api_url = f"https://ariflexlabs-search-api.vercel.app/search?name={username}"
        response = requests.get(api_url)

        if response.status_code != 200:
            bot.reply_to(message, f"⚠️ Lỗi từ máy chủ API: {response.status_code}")
            return

        try:
            regions = response.json()
        except ValueError:
            bot.reply_to(message, "⚠️ Không thể phân tích dữ liệu từ API.")
            return

        all_players = []
        for region_data in regions:
            players = region_data.get("result", {}).get("player", [])
            for player in players:
                all_players.append({
                    "nickname": player.get("nickname", "?"),
                    "accountId": player.get("accountId", "?"),
                    "level": player.get("level", "?"),
                    "region": player.get("region", "?"),
                    "lastLogin": format_timestamp(player.get("lastLogin", 0))
                })

        if not all_players:
            bot.reply_to(message, f"❌ Không tìm thấy kết quả cho <code>{escape_html(username)}</code>.", parse_mode="HTML")
            return

        max_results = 10
        reply_text = f"🔎 <b>Kết quả tìm kiếm cho</b> <code>{escape_html(username)}</code>:\n\n"
        for i, player in enumerate(all_players[:max_results], 1):
            reply_text += (
                f"<blockquote>\n"
                f"<b>{i}. {escape_html(player['nickname'])}</b>\n"
                f"🆔 UID: <code>{escape_html(player['accountId'])}</code>\n"
                f"🎮 Level: {player['level']} | 🌍 Region: {escape_html(player['region'])}\n"
                f"⏰ Đăng nhập cuối: {escape_html(player['lastLogin'])}\n"
                f"</blockquote>\n"
            )

        if len(all_players) > max_results:
            reply_text += f"📌 Hiển thị {max_results}/{len(all_players)} kết quả đầu tiên."

        bot.reply_to(message, reply_text, parse_mode="HTML")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Đã xảy ra lỗi:\n<code>{escape_html(str(e))}</code>", parse_mode="HTML")

ADMINS = [7658079324]  # Thay bằng user_id admin của bạn
GROUP_CHAT_IDS = [-1002639856138]  # Thay bằng chat_id nhóm

@bot.message_handler(commands=['thongbao'])
def thongbao_to_groups(message):
    if message.chat.type != 'private':
        bot.reply_to(message, "⚠️ Vui lòng dùng lệnh này trong chat riêng với bot.")
        return

    if message.from_user.id not in ADMINS:
        bot.reply_to(message, "🚫 Bạn không có quyền dùng lệnh này.")
        return

    try:
        announcement = message.text.split(' ', 1)[1]
    except IndexError:
        bot.reply_to(message, "❗ Vui lòng nhập nội dung: /announce <nội dung>")
        return

    success = 0
    for chat_id in GROUP_CHAT_IDS:
        try:
            bot.send_message(chat_id, f"📢 <b>Thông báo từ Admin</b>:\n\n{announcement}", parse_mode='HTML')
            success += 1
        except Exception as e:
            print(f"Lỗi gửi nhóm {chat_id}: {e}")

    bot.reply_to(message, f"✅ Đã gửi thông báo đến {success} nhóm.")




@bot.message_handler(commands=['checkban'])
def check_ban(message):
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "❗ Vui lòng nhập ID. Ví dụ: /checkban 8324665667")
            return

        user_id = args[1]
        api_url = f"https://wlx-scorpion.vercel.app/Checkban?key=Scromnyi&id={user_id}"
        response = requests.get(api_url)
        data = response.json()

        if data.get("is_banned") == True:
            reply_text = (
                f"🚫 **ID `{user_id}` đã bị BAN**\n"
                f"📆 Thời hạn ban: {data.get('ban_period', 'Không rõ')} ngày"
            )
        else:
            reply_text = (
                f"✅ **ID `{user_id}` không bị ban**\n"
                f"📄 Trạng thái: {data.get('status', 'Không xác định')}"
            )

        bot.reply_to(message, reply_text, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Đã xảy ra lỗi:\n`{e}`", parse_mode="Markdown")


@bot.message_handler(commands=['hoi'])
def handle_hoi(message):
    text = message.text[len('/hoi '):].strip()
    

    # Nếu hợp lệ, cho spam
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


   
import threading

@bot.message_handler(commands=['spam'])
def supersms(message):
    user_id = message.from_user.id
    current_time = time.time()

    if user_id in user_last_command_time:
        elapsed_time = current_time - user_last_command_time[user_id]
        if elapsed_time < 100:
            remaining_time = 100 - elapsed_time
            bot.reply_to(message, f"Vui lòng đợi {remaining_time:.1f} giây trước khi sử dụng lệnh lại.")
            return

    params = message.text.split()[1:]
    if len(params) != 2:
        bot.reply_to(message, "/spam sdt số_lần (tối đa 1000)")
        return

    sdt, count = params

    if not count.isdigit():
        bot.reply_to(message, "Số lần spam không hợp lệ. Vui lòng chỉ nhập số.")
        return

    count = int(count)

    if count > 1000:
        bot.reply_to(message, "/spam sdt số_lần tối đa là 1000")
        return

    if sdt in blacklist:
        bot.reply_to(message, f"Số điện thoại {sdt} đã bị cấm spam.")
        return

    sdt_request = f"84{sdt[1:]}" if sdt.startswith("0") else sdt

    # Gửi loading ban đầu
    loading_msg = bot.send_message(message.chat.id, "⏳")

    # Tạo hiệu ứng loading động với 2 biểu tượng
    loading_symbols = ["⏳", "⌛"]
    stop_loading = threading.Event()

    def animate_loading():
        i = 0
        while not stop_loading.is_set():
            try:
                bot.edit_message_text(
                    loading_symbols[i % 2],
                    message.chat.id,
                    loading_msg.message_id
                )
                i += 1
                time.sleep(0.5)
            except:
                break

    loading_thread = threading.Thread(target=animate_loading)
    loading_thread.start()

    diggory_chat3 = f'''┌──⭓ Bot Hào Vip 😘
│ 🚀 Attack Sent Successfully
│ 💳 Plan Vip: Min 1 | Max 1000
│ 📞 Phone: {sdt}
│ ⚔️ Attack By: @{message.from_user.username or "None"}
│ 🔗 Api: 1x (MAX)
│ ⏳ Delay: 20s
│ 📎 Vòng Lặp: {count}
└────────────⭓'''

    script_filename = "dec.py"

    try:
        if not os.path.isfile(script_filename):
            stop_loading.set()
            bot.edit_message_text("Không tìm thấy file.", message.chat.id, loading_msg.message_id)
            return

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            with open(script_filename, 'r', encoding='utf-8') as file:
                temp_file.write(file.read().encode('utf-8'))
            temp_file_path = temp_file.name

        subprocess.Popen(["python", temp_file_path, sdt, str(count)])
        requests.get(f'https://dichvukey.site/apivl/call1.php?sdt={sdt_request}')
        user_last_command_time[user_id] = time.time()

        stop_loading.set()
        bot.edit_message_text(
            f'<blockquote>{diggory_chat3}</blockquote>',
            message.chat.id,
            loading_msg.message_id,
            parse_mode='HTML'
        )

    except Exception as e:
        stop_loading.set()
        bot.edit_message_text("Đã xảy ra lỗi trong quá trình xử lý.", message.chat.id, loading_msg.message_id)
        print(f'Lỗi: {e}')






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
    
