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
| /gg : tìm ảnh 
| /tv : chuyển đổi ngôn ngữ 
| /like : buff like
| /getkey : lấy key 
| /key : nhập key
| /uptime : xem video gai xinh
| /spam : spam số điện thoại
|—————————————————
                     Lệnh Admin
|____________________________
| /off : tắt bot
| /on : bật bot
| /themvip
| /rs : khởi động lại bot
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
    if user_id in last_usage and current_time - last_usage[user_id] < 100:
        bot.reply_to(message, f"Vui lòng đợi {100 - (current_time - last_usage[user_id]):.1f} giây trước khi sử dụng lệnh lại.")
        return

    last_usage[user_id] = current_time

    # Phân tích cú pháp lệnh
    params = message.text.split()[1:]
    if len(params) != 2:
        bot.reply_to(message, "/spam sdt số_lần như này cơ mà - vì lý do server treo bot hơi cùi nên đợi 100giây nữa dùng lại nhé")
        return

    sdt, count = params

    if not count.isdigit():
        bot.reply_to(message, "Số lần spam không hợp lệ. Vui lòng chỉ nhập số.")
        return

    count = int(count)

    if count > 20:
        bot.reply_to(message, "/spam sdt số_lần tối đa là 20 - đợi 100giây sử dụng lại.")
        return

    if sdt in blacklist:
        bot.reply_to(message, f"Số điện thoại {sdt} đã bị cấm spam.")
        return

    diggory_chat3 = f'''
┌──────⭓ {name_bot}
│ Spam: Thành Công 
│ Số Lần Spam Free: {count}
│ Đang Tấn Công : {sdt}
│ Spam 5 Lần Tầm 1-2p mới xong 
│ Hạn Chế Spam Nhé !  
└─────────────
    '''

    script_filename = "dec.py"  # Tên file Python trong cùng thư mục
    try:
        # Kiểm tra xem file có tồn tại không
        if not os.path.isfile(script_filename):
            bot.reply_to(message, "Không tìm thấy file script. Vui lòng kiểm tra lại.")
            return

        # Đọc nội dung file với mã hóa utf-8
        with open(script_filename, 'r', encoding='utf-8') as file:
            script_content = file.read()

        # Tạo file tạm thời
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(script_content.encode('utf-8'))
            temp_file_path = temp_file.name

        # Chạy file tạm thời
        process = subprocess.Popen(["python", temp_file_path, sdt, str(count)])
        bot.send_message(message.chat.id, diggory_chat3)
    except FileNotFoundError:
        bot.reply_to(message, "Không tìm thấy file.")
    except Exception as e:
        bot.reply_to(message, f"Lỗi xảy ra: {str(e)}")



blacklist = ["112", "113", "114", "115", "116", "117", "118", "119", "0", "1", "2", "3", "4"]

 
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
        if video_link and video_link.startswith('https://'):
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

#gg
API_URL = "https://dichvukey.site/apivl/gg.php?gg="
@bot.message_handler(commands=['gg'])
def search_google_image(message):
    command_parts = message.text.split(maxsplit=1)
    
    if len(command_parts) == 2:
        query = command_parts[1].strip()
        api_request_url = API_URL + requests.utils.quote(query)
        
        try:
            response = requests.get(api_request_url)
            response_data = response.json()
            
            if "image_url" in response_data and "caption" in response_data:
                image_url = response_data["image_url"]
                caption = response_data["caption"]
                
                bot.send_photo(message.chat.id, photo=image_url, caption=caption, parse_mode="Markdown")
            else:
                bot.reply_to(message, "không tìm thấy hình ảnh nào.")
        except Exception as e:
            bot.reply_to(message, "Lỗi khi tìm kiếm hình ảnh.")
            print(f"Lỗi")
    else:
        bot.reply_to(message, "/gg siêu nhân")
### tiep theo codeby HàoEsports

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
