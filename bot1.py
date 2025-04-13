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
➤ /like : buff like
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


def fetch_data(user_id):
    url = f'https://scromnyimodz-444.vercel.app/api/player-info?id={user_id}'
    response = requests.get(url)
    return response.json()

def safe_get(d, key, default="N/A"):
    return d.get(key, default) if isinstance(d, dict) else default

#pet
@bot.message_handler(commands=['ff'])
def handle_ff(message):
    parts = message.text.split()
    if len(parts) != 2:
        bot.reply_to(message, "<i>⚠️ Dùng đúng cú pháp:</i>\n<code>/ff 12345678</code>", parse_mode="HTML")
        return

    user_id = parts[1]

    try:
        data = fetch_data(user_id)
        if not data or data.get("status") != "success":
            bot.reply_to(message, "❌ <i>Không tìm thấy người chơi hoặc API lỗi.</i>", parse_mode="HTML")
            return

        d = data.get("data", {})
        basic = d.get("basic_info", {})
        clan = d.get("clan", {})
        leader = clan.get("leader", {})
        pet = d.get("animal", {}).get("name", "Không có")

        from html import escape

        def safe(val):
            return escape(str(val)) if val else "Không có"

        info = f"""
<blockquote>
👤 <b>{safe(basic.get('name'))}</b> | 🆔 <code>{basic.get('id', 'N/A')}</code>
⭐ Cấp: <b>{basic.get('level', 'N/A')}</b> | ❤️ Like: {basic.get('likes', 'N/A')}
🌍 Server: <code>{safe(basic.get('server'))}</code>
📅 Tạo: {basic.get('account_created', 'N/A')}
🎫 Booyah Pass: {basic.get('booyah_pass_level', 'N/A')}
📝 Bio: <i>{safe(basic.get('bio'))}</i>
🐾 Pet: <i>{safe(pet)}</i>

<b>─── Quân Đoàn ───</b>
🛡️ {safe(clan.get('name'))} (Lv. {clan.get('level', 'N/A')})
👥 Thành viên: {clan.get('members_count', 'N/A')}
👑 Chủ: {safe(leader.get('name'))} (Lv. {leader.get('level', 'N/A')})
</blockquote>
"""

        bot.send_message(message.chat.id, info, parse_mode="HTML")


    except Exception as e:
        print("Lỗi:", e)
        bot.reply_to(message, "⚠️ <i>Đã xảy ra lỗi khi xử lý yêu cầu.</i>", parse_mode="HTML")




GROUP_CHAT_IDS = [-1002639856138, 1002282514761]


# Hàm xử lý lệnh '/like'
@bot.message_handler(commands=['like'])
def like_handler(message):
    if message.chat.id not in GROUP_CHAT_IDS:
        bot.reply_to(message, "⚠️ Lệnh này chỉ sử dụng được trong nhóm đã được cấp quyền.")
        return
    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "<blockquote>❗ Vui lòng nhập đúng cú pháp: /like 1733997441</blockquote>", parse_mode="HTML")
        return

    uid = args[1]
    data = call_api(uid)

    if "message" in data:
        msg_content = data["message"]
        if isinstance(msg_content, str):
            reply_text = f"<blockquote>⚠️ {msg_content}</blockquote>"
        elif isinstance(msg_content, dict):
            reply_text = (
                f"<blockquote>\n"
                f"🎯 <b>Kết quả buff like:</b><br>"
                f"👤 <b>Tên:</b> {msg_content.get('Name', 'Không xác định')}<br>"
                f"🆔 <b>UID:</b> {msg_content.get('UID', uid)}<br>"
                f"🌎 <b>Khu vực:</b> {msg_content.get('Region', 'Không xác định')}<br>"
                f"📊 <b>Level:</b> {msg_content.get('Level', 'Không xác định')}<br>"
                f"👍 <b>Like trước:</b> {msg_content.get('Likes Before', 'Không xác định')}<br>"
                f"✅ <b>Like sau:</b> {msg_content.get('Likes After', 'Không xác định')}<br>"
                f"➕ <b>Tổng cộng:</b> {msg_content.get('Likes Added', 'Không xác định')} like<br>"
                f"</blockquote>"
            )
        else:
            reply_text = "<blockquote>Dữ liệu trả về không đúng định dạng.</blockquote>"

        bot.reply_to(message, reply_text, parse_mode="HTML")
    else:
        handle_api_error(message, "API không trả về kết quả hợp lệ.")

start_time = time.time()

# Biến để tính toán FPS
last_time = time.time()
frame_count = 0
fps = 0

# Lệnh /uptime
@bot.message_handler(commands=['uptime'])
def uptime(message):
    global last_time, frame_count, fps
    
    # Tính toán thời gian hoạt động
    uptime_seconds = int(time.time() - start_time)
    uptime_formatted = str(timedelta(seconds=uptime_seconds))
    
    # Cập nhật FPS mỗi khi lệnh được xử lý
    current_time = time.time()
    frame_count += 1
    if current_time - last_time >= 1:  # Tính FPS mỗi giây
        fps = frame_count
        frame_count = 0
        last_time = current_time
    
    # Gửi video từ API
    video_url = "https://api.ffcommunity.site/randomvideo.php"
    video_response = requests.get(video_url)
    
    # Phân tích dữ liệu JSON và lấy đường dẫn video (chú ý đến phần https)
    try:
        video_data = video_response.json()  # Phân tích JSON
        video_url = video_data.get('url', '')  # Lấy đường dẫn video từ trường 'url'

    except ValueError:
        video_link = 'Không thể lấy video'

    # Tạo và gửi tin nhắn
    # Tạo và gửi tin nhắn
    bot.send_message(message.chat.id, 
                 f"📊 ⏳ Bot đã hoạt động: {uptime_formatted}\n"
                 f"🎮 FPS trung bình: {fps} FPS\n"
                 "Không thể lấy thông tin cấu hình.\n"
                 f"🎥 Video giải trí cho ae FA vibu đây! 😏\n{video_url}")





 
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


def animate_loading(chat_id, message_id, stop_event):
    dots = ""
    while not stop_event.is_set():
        dots += "."
        if len(dots) > 3:
            dots = ""
        try:
            bot.edit_message_text(f"⏳ Đang xử lý{dots}", chat_id, message_id)
        except:
            pass
        time.sleep(0.5)
        
    
from datetime import datetime
      
@bot.message_handler(commands=['spam'])
def spam(message):
    user_id = message.from_user.id
    current_time = time.time()

    if user_id in last_usage and current_time - last_usage[user_id] < 10:
        bot.reply_to(message, f"⏳ Vui lòng đợi {10 - (current_time - last_usage[user_id]):.1f} giây trước khi dùng lại.")
        return

    params = message.text.split()[1:]
    if len(params) != 2:
        warn = bot.reply_to(message, "/spam sdt số_lần như này cơ mà")
        time.sleep(5)
        try:
            bot.delete_message(message.chat.id, warn.message_id)
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
        return

    sdt, count = params
    carrier = detect_carrier(sdt)

    try:
        count = int(count)
        if count < 1 or count > 500:
            raise ValueError
    except ValueError:
        bot.reply_to(message, "Số lần spam không hợp lệ. Chỉ chấp nhận từ 1 đến 500.")
        return

    if sdt in blacklist:
        bot.reply_to(message, f"Số điện thoại {sdt} đã bị cấm spam.")
        return

    sdt_request = f"84{sdt[1:]}" if sdt.startswith("0") else sdt
    username = message.from_user.username if message.from_user.username else "Không có username"

    script_filename = "dec.py"
    try:
        if not os.path.isfile(script_filename):
            bot.reply_to(message, "Không tìm thấy file script.")
            return

        loading_msg = bot.send_message(message.chat.id, "⏳ Đang xử lý...")
        stop_loading = threading.Event()
        loading_thread = threading.Thread(
            target=animate_loading,
            args=(message.chat.id, loading_msg.message_id, stop_loading),
            daemon=True
        )
        loading_thread.start()

        with open(script_filename, 'r', encoding='utf-8') as file:
            script_content = file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(script_content.encode('utf-8'))
            temp_file_path = temp_file.name

        process = subprocess.Popen(["python", temp_file_path, sdt, str(count)])
        active_processes[sdt] = process

        stop_loading.set()
        bot.delete_message(chat_id=message.chat.id, message_id=loading_msg.message_id)

        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        masked_sdt = sdt[:3] + "***" + sdt[-3:]

        spam_msg = f"""
<pre>======[ 𝙎𝙋𝘼𝙈 𝙋𝙍𝙊 ]======</pre>

<b>🕵️‍♂️ Số điện thoại mục tiêu:</b>
  ├─> {masked_sdt}
  ├─────────────⭔
<b>⏳ Thời gian tấn công:</b>
  ├─> {now}
  ├─────────────⭔
<b>🌐 SEVER 1</b>
  ├─────────────⭔
<b>💥 Thời gian chờ (Cooldown):</b>
  ├─> 120 giây
  ├─────────────⭔
<b>🔁 Số lần tấn công lặp lại:</b>
  ├─> {count} lần
  ├─────────────⭔
"""
        bot.send_message(
            chat_id=message.chat.id,
            text=spam_msg,
            parse_mode="HTML"
        )

        last_usage[user_id] = current_time

    except FileNotFoundError:
        bot.reply_to(message, "Không tìm thấy file.")
    except Exception as e:
        bot.reply_to(message, f"Lỗi xảy ra: {str(e)}")



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
    
