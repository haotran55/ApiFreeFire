import telebot
import subprocess
import sys
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
admin_diggory = "ad_an_danhso5" 
name_bot = "TranHao"
ADMIN_ID = '7658079324'
zalo = "0585019743"
web = "https://dichvukey.site/"
facebook = "no"
bot = telebot.TeleBot(os.environ.get('token')) 
print(os.environ.get('token'))  # Kiểm tra token có tồn tại không
print("Bot đã được khởi động thành công")
users_keys = {}
key = ""
user_cooldown = {}
last_usage = {} 
share_log = []
auto_spam_active = False
last_sms_time = {}
global_lock = Lock()
allowed_users = []
processes = []
ADMIN_ID =  7845889525 #nhớ thay id nhé nếu k thay k duyệt dc vip đâu v.L..ong.a
allowed_group_id = -1002311654677
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

@bot.message_handler(commands=['muavip'])
def muavip(message):
    user = message.from_user

    if message.chat.type != "private":
        bot.send_message(message.chat.id, "Vui lòng nhắn riêng với bot để thực hiện lệnh này.\nBảng giá: 1 ngày VIP = 1,000 VND, tối đa 100 ngày = 100,000 VND.")
        return

    cooldown = check_command_cooldown(user.id, '/muavip', 5)  
    if cooldown:
        bot.send_message(message.chat.id, f"Vui lòng chờ {cooldown} giây trước khi thực hiện lại lệnh này.")
        return

    try:
        so_tien = int(message.text.split()[1])

        if so_tien < 5000 or so_tien > 100000 or so_tien % 1000 != 0:
            bot.send_message(message.chat.id, "Số tiền không hợp lệ. Mỗi 1,000 VND tương ứng với 1 ngày VIP. Vui lòng nhập số tiền từ 5,000 đến 100,000 VND.")
            return

        full_name = user.first_name if user.first_name else "user"
        letters = ''.join(random.choices(string.ascii_uppercase, k=5))
        digits = ''.join(random.choices(string.digits, k=7))
        random_str = letters + digits
        noidung = f"{full_name} {random_str}"

        message_text = (f"STK: `0123456890`\n"
                        f"Ngân hàng: `MBBANK`\n"
                        f"Chủ tài khoản: `TRAN NHAT HAO`\n\n"
                        f"Vui lòng nạp {so_tien} VNĐ theo đúng nội dung\n"
                        f"Nội Dung: `{noidung}`\n"
                        f"Sau khi nạp hãy nhấn Xác Nhận\n")

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Xác Nhận ✅", callback_data=f"vip:confirm_{so_tien}_{noidung}_{user.id}"))
        markup.add(types.InlineKeyboardButton("Huỷ Bỏ ❌", callback_data=f"vip:cancel_{user.id}"))

        bot.send_message(message.chat.id, message_text, reply_markup=markup, parse_mode='Markdown')

    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Vui lòng nhập số tiền cần nạp | Ví dụ: /muavip 100000")
####zalo 0789041631..
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = call.data
    args = data.split("_")

    if args[0] == "vip:confirm":
        so_tien, noidung, user_id = args[1:]
        admin_message = (f"Người mua VIP: {call.from_user.first_name} (ID: {user_id})\n"
                         f"Số tiền: {so_tien} VNĐ\n"
                         f"Nội dung: {noidung}\n"
                         f"Thời gian nạp: {datetime.datetime.now(vietnam_tz).strftime('%H:%M:%S %d-%m-%Y')}")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Duyệt ✅", callback_data=f"vip:approve_{user_id}_{so_tien}"))
        markup.add(types.InlineKeyboardButton("Từ Chối ❌", callback_data=f"vip:deny_{user_id}_{so_tien}"))

        bot.send_message(chat_id=8167596347, text=admin_message, reply_markup=markup)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"Yêu cầu mua VIP đã được gửi đến quản trị viên 📤\nSố tiền: {so_tien} VNĐ\nNội dung: {noidung}\nNgày tạo đơn: {datetime.datetime.now(vietnam_tz).strftime('%H:%M:%S %d-%m-%Y')}")

    elif args[0] == "vip:cancel":
        user_id = args[1]
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Bạn đã huỷ bỏ yêu cầu mua VIP.")
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    elif args[0] == "vip:approve":
        user_id, so_tien = args[1:]
        so_ngay_vip = int(so_tien) // 1000
        so_ngay_vip = min(so_ngay_vip, 100)  
        expiration_time = datetime.datetime.now() + datetime.timedelta(days=so_ngay_vip)

        connection = sqlite3.connect('user_data.db')
        save_user_to_database(connection, int(user_id), expiration_time)
        connection.close()

        allowed_users.append(int(user_id))

        bot.send_message(chat_id=user_id, text=f"Chúc mừng! Bạn đã trở thành VIP trong {so_ngay_vip} ngày đến {expiration_time.strftime('%Y-%m-%d %H:%M:%S')}.")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Đã duyệt yêu cầu VIP của ID {user_id}.")
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    elif args[0] == "vip:deny":
        user_id, so_tien = args[1:]
        bot.send_message(chat_id=user_id, text="Yêu cầu VIP của bạn đã bị từ chối.")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Đã từ chối yêu cầu VIP của ID {user_id}.")
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

load_users_from_database()


def fetch_data(user_id):
    try:
        url = f'https://api.ffcommunity.site/info.php?uid={user_id}'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

@bot.message_handler(commands=['ff'])
def handle_command(message):
    parts = message.text.split()
    if len(parts) != 2:
        bot.reply_to(message, "<blockquote>Sử dụng: /ff ID\nVí dụ: /ff 1733997441</blockquote>", parse_mode="HTML")
        return
    
    command, user_id = parts
    if not user_id.isdigit():
        bot.reply_to(message, "<blockquote>ID không hợp lệ. Vui lòng nhập ID số.</blockquote>", parse_mode="HTML")
        return

    try:
        data = fetch_data(user_id)
        if data is None:
            bot.reply_to(message, "<blockquote>❌ Server API đang bảo trì hoặc quá tải. Vui lòng thử lại sau.</blockquote>", parse_mode="HTML")
            return
            
        basic_info = data
        clan_info = data.get('Guild Information', {})
        leader_info = data.get('Guild Leader Information', {})
        avatar_url = basic_info.get('AccountAvatarId', 'Không có')

        def get_value(key, data_dict):
            return data_dict.get(key, "Không có thông tin")

        info_text = f"""
<blockquote>
<b>Thông tin cơ bản:</b>
Avatar: <a href="{avatar_url}">Nhấn để xem</a>
Nickname: {get_value('AccountName', basic_info)}
Cấp độ: {get_value('AccountLevel', basic_info)}
Khu vực: {get_value('AccountRegion', basic_info)}
Xếp hạng Sinh Tồn: {get_value('BrRank', basic_info)}
Tổng Sao Tử Chiến: {get_value('CsRank', basic_info)}
Số lượt thích: {get_value('AccountLikes', basic_info)}
Lần đăng nhập gần nhất: {get_value('AccountLastLogin (GMT 0530)', basic_info)}
Ngôn ngữ: {get_value('AccountLanguage', basic_info)}
Tiểu sử game: {get_value('AccountSignature', basic_info)}

<b>Thông tin quân đoàn:</b>
Tên quân đoàn: {get_value('GuildName', clan_info)}
Cấp độ quân đoàn: {get_value('GuildLevel', clan_info)}
Sức chứa: {get_value('GuildCapacity', clan_info)}
Số thành viên hiện tại: {get_value('GuildMember', clan_info)}
Chủ quân đoàn: {get_value('LeaderName', leader_info)}
Cấp độ chủ quân đoàn: {get_value('LeaderLevel', leader_info)}
</blockquote>
"""

        bot.reply_to(message, info_text, parse_mode='HTML')

    except Exception as e:
        bot.reply_to(message, "<blockquote>Đã xảy ra lỗi</blockquote>", parse_mode="HTML")


@bot.message_handler(commands=['start'])
def send_help(message):
    bot.reply_to(message, """<blockquote>
╔══════════════════╗  
     📌         *DANH SÁCH LỆNH*  
╚══════════════════╝  
 _____________________________________
| /ff : check acc xem thông tin 
| /tv : chuyển đổi ngôn ngữ 
| /like : buff like
| /getkey : lấy key 
| /key : nhập key
| /uptime : xem video gai xinh
| /spam : spam số điện thoại
|—————————————————
                     Lệnh Admin
|____________________________
| /muavip
|____________________________
</blockquote>""", parse_mode="HTML")

API_BASE_URL = "https://freefire-virusteam.vercel.app"

def get_vip_key():
    try:
        response = requests.get("https://dichvukey.site/keyvip.txt", timeout=5)
        response.raise_for_status()
        return response.text.strip()
    except requests.exceptions.RequestException:
        return "default-key"  

VIP_KEY = get_vip_key()

region_translation = {
    "VN": "Việt Nam", "ID": "Indonesia", "TH": "Thái Lan",
    "SG": "Singapore", "TW": "Đài Loan", "EU": "Châu Âu",
    "US": "Hoa Kỳ", "BR": "Brazil", "MX": "Mexico",
    "IN": "Ấn Độ", "KR": "Hàn Quốc", "PK": "Pakistan",
    "BD": "Bangladesh", "RU": "Nga", "MENA": "Trung Đông & Bắc Phi",
    "LA": "Châu Mỹ Latinh"
}

def call_api(endpoint, params=None):
    url = f"{API_BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return {"status": "error", "message": "Sever quá tải hoặc lỗi kết nối"}

def check_user_permission(message):
    user_id = message.from_user.id
    today_day = datetime.date.today().day
    key_path = f"./user/{today_day}/{user_id}.txt"

    return user_id in allowed_users or os.path.exists(key_path)

def handle_api_error(message, error_message):
    bot.reply_to(message, f"<blockquote>❌ {error_message}</blockquote>", parse_mode="HTML")
####zalo 0789041631
### /like

@bot.message_handler(commands=['spam'])
def spam_vip_handler(message):
    user_id = message.from_user.id
    
    if user_id not in allowed_users:
        bot.reply_to(message, '⚠️ *Bạn chưa có quyền sử dụng lệnh này!* ⚠️\n💰 Hãy mua VIP để sử dụng\nNhắn /muavip riêng với bot @spamsmsvlong_bot.', parse_mode='Markdown')
        return
    params = message.text.split()[1:]
    if len(params) != 2:
        bot.reply_to(message, "❌ *Sai cú pháp!*\n\n✅ Đúng: `/spamvip số_điện_thoại số_lần`", parse_mode='Markdown')
        return

    sdt, count = params

    if not count.isdigit() or int(count) <= 0:
        bot.reply_to(message, "⚠️ *Số lần spam không hợp lệ!*\n🔢 Vui lòng nhập một số dương.", parse_mode='Markdown')
        return

    count = int(count)

    if count > 50:
        bot.reply_to(message, "⚠️ *Giới hạn spam!*\n⏳ Tối đa là 50 lần mỗi lệnh.", parse_mode='Markdown')
        return

    if sdt in blacklist:
        bot.reply_to(message, f"🚫 *Số điện thoại {sdt} đã bị cấm spam!* 🚫", parse_mode='Markdown')
        return

    sdt_request = f"84{sdt[1:]}" if sdt.startswith("0") else sdt
    current_time = time.time()
    if user_id in last_usage:
        elapsed_time = current_time - last_usage[user_id]
        if elapsed_time < 100:
            remaining_time = 100 - elapsed_time
            bot.reply_to(message, f"⏳ *Hãy chờ {remaining_time:.1f} giây trước khi dùng lại!*", parse_mode='Markdown')
            return

    last_usage[user_id] = current_time

    message_content = f"""
🎯 *Spam Thành Công!* 🎯
📌 Người dùng: @{message.from_user.username}
📲 Số điện thoại: `{sdt}`
🔢 Số lần spam: `{count}`
⚠️ Lưu ý: Spam 50 lần mất khoảng 15 phút để hoàn tất.
💎 Gói VIP giúp bạn spam hiệu quả hơn!
    """

    script_filename = "dec.py"

    try:
        if not os.path.isfile(script_filename):
            bot.reply_to(message, "Lỗi!", parse_mode='Markdown')
            return
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            with open(script_filename, 'r', encoding='utf-8') as file:
                temp_file.write(file.read().encode('utf-8'))
            temp_file_path = temp_file.name

        subprocess.Popen(["python", temp_file_path, sdt, str(count)])

        bot.send_message(message.chat.id, message_content, parse_mode='Markdown')

        requests.get(f'https://dichvukey.site/apivl/call1.php?sdt={sdt_request}')

    except Exception as e:
        print(f'Lỗi')


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
        video_link = video_data.get('url', '')  # Lấy đường dẫn video từ trường 'url'
        
        # Kiểm tra nếu có https
        if video_link and (video_link.startswith('http://')or video_link.startswith('https://')):
            video_link = video_link.strip()  # Loại bỏ khoảng trắng thừa ở đầu và cuối
        else:
            video_link = 'Không thể lấy video'

    except ValueError:
        video_link = 'Không thể lấy video'

    # Tạo và gửi tin nhắn
    bot.send_message(message.chat.id, 
                     f"📊 ⏳ Bot đã hoạt động: {uptime_formatted}\n"
                     f"🎮 FPS trung bình: {fps} FPS\n"
                     "Không thể lấy thông tin cấu hình.\n"
                     f"🎥 Video giải trí cho ae FA vibu đây! 😏\n{video_link}")
                     


    API_LIKE_URL = "https://dichvukey.site/addlike.php?uid={}"  # API tăng like UID FF

def add_like(uid):
    url = API_LIKE_URL.format(uid)
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == 400:
            return f"❌ Lỗi từ API: {data.get('message', 'Không thể tăng like')}"
        
        return f"✅ Đã gửi yêu cầu tăng like cho UID {uid}!"
    except requests.exceptions.RequestException as e:
        return f"❌ Lỗi kết nối API: {str(e)}"
    except Exception as e:
        return f"❌ Lỗi không xác định: {str(e)}"

        reply_text = (
            f"\n👤 Tên: {data.get('username', 'Không xác định')}\n"
            f"🆔 UID: {data.get('uid', 'Không xác định')}\n"
            f"❤️ Like hiện tại: {data.get('current_likes', 'N/A')}\n"
            f"👍 Like đã thêm: {data.get('added_likes', 'N/A')}\n"
            f"📅 Ngày hết hạn: {data.get('expiry_date', 'N/A')}"
        )
        return reply_text
    return "Lỗi không xác định."

@bot.message_handler(commands=['like'])
def like_command(message):
    try:
        uid = message.text.split()[1]
        if not uid.isdigit():
            bot.reply_to(message, "⚠ UID phải là số!")
            return
        bot.reply_to(message, "👍 Đang tăng like cho UID...")
        result = add_like(uid)
        bot.reply_to(message, result)
    except IndexError:
        bot.reply_to(message, "⚠ Vui lòng nhập UID sau lệnh /like")
    except Exception as e:
        bot.reply_to(message, f"❌ Lỗi: {str(e)}")

@bot.message_handler(commands=['getkey'])
def startkey(message):
    user_id = message.from_user.id
    today_day = datetime.date.today().day
    key = "HaoEsport" + str(user_id * today_day - 2007)

    api_token = '67c1fe72a448b83a9c7e7340'
    key_url = f"https://dichvukey.site/key.html?key={key}"

    try:
        response = requests.get(f'https://link4m.co/api-shorten/v2?api={api_token}&url={key_url}')
        response.raise_for_status()
        url_data = response.json()
        print(key)

        if 'shortenedUrl' in url_data:
            url_key = url_data['shortenedUrl']
            text = (f'Link Lấy Key Ngày {TimeStamp()} LÀ: {url_key}\n'
                    'KHI LẤY KEY XONG, DÙNG LỆNH /key HaoEsport ĐỂ TIẾP TỤC Hoặc /muavip đỡ vượt tốn thời gian nhé')
            bot.reply_to(message, text)
        else:
            bot.reply_to(message, 'Lỗi.')
    except requests.RequestException:
        bot.reply_to(message, 'Lỗi.')

@bot.message_handler(commands=['key'])
def key(message):
    if len(message.text.split()) != 2:
        bot.reply_to(message, 'Key Đã Vượt Là? đã vượt thì nhập /key chưa vượt thì /muavip nhé')
        return

    user_id = message.from_user.id
    key = message.text.split()[1]
    today_day = datetime.date.today().day
    expected_key = "HaoEsport" + str(user_id * today_day - 2007)  # Đảm bảo công thức khớp với công thức tạo key

    if key == expected_key:
        text_message = f'<blockquote>[ KEY HỢP LỆ ] NGƯỜI DÙNG CÓ ID: [ {user_id} ] ĐƯỢC PHÉP ĐƯỢC SỬ DỤNG CÁC LỆNH TRONG [/start]</blockquote>'
        video_url = 'https://v16m-default.akamaized.net/8c4208955e22e46d82f245894d6d3e31/67e53e48/video/tos/alisg/tos-alisg-pve-0037c001/okvpfADKBSYBbFRXn1fOjQQEgIDrBxoEIrn0Eq/?a=0&bti=OUBzOTg7QGo6OjZA'  # Đổi URL đến video của bạn
        bot.send_video(message.chat.id, video_url, caption=text_message, parse_mode='HTML')
        
        user_path = f'./user/{today_day}'
        os.makedirs(user_path, exist_ok=True)
        with open(f'{user_path}/{user_id}.txt', "w") as fi:
            fi.write("")
    else:
        bot.reply_to(message, 'KEY KHÔNG HỢP LỆ.')

@bot.message_handler(commands=['tv'])
def tieng_viet(message):
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton("Tiếng Việt 🇻🇳", url='https://t.me/setlanguage/vi')
    keyboard.add(url_button)
    bot.send_message(chat_id, '<blockquote>Click vào nút "<b>Tiếng Việt</b>" để đổi ngôn ngữ sang Tiếng Việt 🇻🇳</blockquote>', reply_markup=keyboard, parse_mode='HTML')
######


if __name__ == "__main__":
    bot_active = True
    bot.polling()  #
