import io
import json
import time
import math
import random
import psutil
import shutil
import asyncio
import discord
import platform
import threading
import urllib.parse
from io import BytesIO
from discord import app_commands
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from discord import Button, ButtonStyle, InteractionType
import discord
from discord.ext import commands, tasks
import random
import asyncio
from datetime import timedelta, datetime, timezone
import re
import json
import os
from colorama import init, Fore
import time
import yt_dlp
import sqlite3
from discord import Interaction, app_commands
import requests
import string

# TOKEN CSGZ: MTI2Njk4MTY4NjYzODQxNTkxMg.G_sPha.3N1PCxs0yBC6dVYUUpde-Q30Zf4SZ8t1NN0RQQ
# TOKEN STORE: MTI1MTc2NzU3NTUyNDgwNjcwNg.Gnpq-U.tN32vR7gllONCL9UIv3bpwJls9f4XdSTWTnbfg

TOKEN = 'MTI1MTc2NzU3NTUyNDgwNjcwNg.Gnpq-U.tN32vR7gllONCL9UIv3bpwJls9f4XdSTWTnbfg'
BOT_MASTER = ['595870690498838558','485646161261101066','1048949206125125742']

intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.guilds = True
intents.message_content = True
intents = discord.Intents.all()


red = "\033[91m"
yellow = "\033[93m"
green = "\033[92m"
blue = "\033[94m"
pretty = "\033[95m"
magenta = "\033[35m"
lightblue = "\033[36m"
cyan = "\033[96m"
gray = "\033[37m"
reset = "\033[0m"
pink = "\033[95m"
dark_green = "\033[92m"
yellow_bg = "\033[43m"
clear_line = "\033[K"




def reloadconfig():
    with open('config.json', 'r', encoding='utf-8-sig') as file:
        data = json.load(file)
    return data
@tasks.loop(seconds=15)
async def change_activity():
    activities = [
        discord.Activity(type=discord.ActivityType.watching, name="CHEAP NITRO | Hazel Store"),
        discord.Activity(type=discord.ActivityType.watching, name="FAST | Hazel Store"),
        discord.Activity(type=discord.ActivityType.watching, name="LEGIT SERVICE | Hazel Store"),
    ]
    
    for activity in activities:
        await bot.change_presence(activity=activity)
        await asyncio.sleep(5)

worktime = time.time()


def paymentcode():
    characters = string.ascii_uppercase + string.digits
    payment_code = ''.join(random.choices(characters, k=6))
    return payment_code

class Paginator:
    def __init__(self, ctx, pages):
        self.ctx = ctx
        self.pages = pages
        self.current_page = 0
        self.message = None
        self.emojis = ["⛔", "✅"]

    async def start(self):
        self.message = await self.ctx.send(embed=self.pages[self.current_page], ephemeral=True)
        for emoji in self.emojis:
            await self.message.add_reaction(emoji)
        bot.loop.create_task(self.wait_for_reactions())

    async def wait_for_reactions(self):
        while True:
            def check(reaction, user):
                return user == self.ctx.author and reaction.message.id == self.message.id and str(reaction.emoji) in self.emojis

            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await self.message.clear_reactions()
                break
            else:
                await self.message.remove_reaction(reaction.emoji, user)
                if str(reaction.emoji) == "⛔":
                    self.current_page = (self.current_page - 1) % len(self.pages)
                elif str(reaction.emoji) == "✅":
                    self.current_page = (self.current_page + 1) % len(self.pages)
                await self.message.edit(embed=self.pages[self.current_page])



init(autoreset=True)

with open('config.json', 'r') as file:
    config = json.load(file)


FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}
YDL_OPTIONS = {'format': 'bestaudio', 'cookies': 'www.youtube.com_cookies.txt', 'noplaylist': True, 'quiet': True}
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config['prefixstore'], intents=intents, help_command=None, case_insensitive=True)
tree = bot.tree

class MusicPlayer:
    def __init__(self):
        self.queue = []
        self.is_looping = False
        self.current_song = None

music_player = MusicPlayer()

logchannel = reloadconfig()['logchannel']
ttchannel = reloadconfig()['ttchannel']

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        current_time = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
        print(f"{Fore.LIGHTYELLOW_EX}{current_time} |{Fore.LIGHTRED_EX} Đã có lỗi xảy ra {Fore.LIGHTMAGENTA_EX}| Nội dung lỗi : {error}")
    else:
        current_time = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
        print(f"{Fore.LIGHTYELLOW_EX}{current_time} |{Fore.LIGHTRED_EX} Đã có lỗi xảy ra {Fore.LIGHTMAGENTA_EX}| Nội dung lỗi : {error}")


###############################################################################################################
def load_json(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            json.dump({'members': [], 'guilds': []}, file)
    with open(filename, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {'members': [], 'guilds': []}

def save_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
        

banned = load_json('banned.json')

def convert_time_to_seconds(time_str):
    total_seconds = 0

    time_elements = re.findall(r'(\d+)([smhdwSMHDW]?)', time_str)

    for value, unit in time_elements:
        value = int(value)
        if unit in ['m', 'M']:
            total_seconds += value * 60
        elif unit in ['h', 'H']:
            total_seconds += value * 3600
        elif unit in ['d', 'D']:
            total_seconds += value * 86400
        elif unit in ['w', 'W']:
            total_seconds += value * 604800
        else:
            total_seconds += value

    if total_seconds > 2 * 604800:
        total_seconds = 2 * 604800

    return total_seconds

# Kiểm tra kênh voice và gửi tin nhắn
async def is_in_voice_channel(ctx, user, giveaway_message):
    if user.voice and user.voice.channel:
        return True
    else:
        try:
            await user.send(f"**Không thể tham gia giveaway**\n**Lí do: Đây là GA treo voice,vui lòng vào kênh voice để tham gia**\n**Giveaway yêu cầu treo voice:** https://discord.com/channels/{ctx.guild.id}/{giveaway_message.channel.id}/{giveaway_message.id}")
        except discord.Forbidden:
            pass
        return False
    
# Kiểm tra bot master

def is_bot_master(ctx):
    return ctx.author.id == 595870690498838558, 1017063185859231845, 912166134982275113, 485646161261101066

# Sự kiện kiểm tra phản ứng
@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    message = reaction.message
    guild = message.guild

    # Kiểm tra nếu user hoặc guild bị cấm
    if str(user.id) in banned['members'] or str(guild.id) in banned['guilds']:
        await reaction.remove(user)
        embed = discord.Embed(title="Bạn đã bị cấm tham gia các giveaway", color=0xff0000)
        embed.description = ("Bạn đã nhận lệnh cấm sử dụng bot Giveaway này, "
                             "vui lòng liên hệ Staff của [Hazel Store](https://discord.gg/hazelstore) để biết thêm chi tiết")
        embed.set_footer(text=f"Thời gian: {datetime.now().strftime('%H:%M:%S - %d/%m/%Y')} | Hazel Store")
        try:
            await user.send(embed=embed)
        except discord.Forbidden:
            pass
        return

    # Kiểm tra nếu phản ứng là cho giveaway yêu cầu treo voice
    for embed in message.embeds:
        if embed.description and "Yêu cầu treo voice" in embed.description:
            if not await is_in_voice_channel(message.channel, user, message):
                await reaction.remove(user)
            return

        




########################################################################################################################

# Bật bot

@bot.event
async def on_ready():
    current_time = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
    print(f'{Fore.LIGHTYELLOW_EX}{current_time} |{Fore.BLUE} Bot đã sẵn sàng. Đăng nhập với tên: {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="Hazel Store"))
    nigga = bot.get_channel(1307708725502541905)
    embed = discord.Embed(title="Bot đã được khởi động lại",description=f"**<t:{math.floor(time.time())}:R>**")
    await nigga.send(embed=embed)
    await bot.tree.sync()
    change_activity.start()

########################################################################################################################
@bot.command(name="checkticket")
@commands.has_role("Legit Seller")
async def concacccccc(ctx, target_id: int, ticket_id: int):
    await ctx.message.delete()
    target_info = await bot.fetch_user(target_id)
    await target_info.send(f'<@{target_id}> oiii, check ticket mua hàng <#{ticket_id}> đi bạn oiiii')
    

# Bot stock
@bot.command()
@commands.has_role("Legit Seller")
async def stock(ctx):
    await ctx.message.delete()

    embed = discord.Embed(
        	title="Hazel Store",
        	description="<:new:1239064757453983865> Thông báo hàng!! \n\n <:boost:1236133359290290226> Nitro Boost 1 tháng login 85k\n<:boost:1236133359290290226> Nitro Boost 1 năm login 820k\n\n<:boost:1236133359290290226> Nitro Trial 3 tháng 50k ( mua từ 2 acc trở lên thì 1 acc 30k từ đó tính tới )\n\n<:butsv:1278620350019797037> 14 Boost Server 3 tháng 200k\n<:butsv:1278620350019797037> 14 Boost Server 1 tháng 100k\n\n<:Discord:1236134366233628732> Decor discord thì tạo ticket nhennn\n\n<:Spotify:1236133935898169404> Spotify 1 tháng 35k ( Cấp acc )\n<:Spotify:1236133935898169404> Spotify 1 tháng 50k ( Up  chính chủ )\n\n<:Netflix:1236134072389075016> Netflix 1 tháng 70k\n\n~~<:youtube:1236133480342224956> Acc Youtube 1 tháng 35k~~\n\n<:visa:1298041529071571025> Thanh toán hộ sử dụng visa/mastercard phí rẻ ib nhen\n\n<:canva:1298042222746406922> Canva 1 năm 200k\n\n\n\n",
        	color=discord.Color.from_rgb(247, 57, 24)
    )
    
    embed.add_field(name="", value="",inline=False)
    embed.add_field(name="", value="",inline=False)
    embed.add_field(name="Seller luôn luôn có giá riêng khi thu và chỉ chấp nhận thu sll ( trên 5 )", value="", inline=False)


    embed.set_footer(text="Hazel Store")
    
    embed.set_image(url="")
    
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1251767575524806706/a_5792a01d18171b9765984811fbf2b6d3.gif?size=4096")
    
    await ctx.send("# Stock Hôm Nay <@&1238133106389680178>\n# <:haz1:1291658759030181919><:haz2:1291658781838540821><:haz3:1291658797776896070><:haz4:1291658813648277514><:haz5:1291658830178156606>\n**Bên dưới đây vẫn còn những mặt hàng mình chưa để nhưng vẫn bán nha**", embed=embed)
    server_name = ctx.guild.name
    server_id = ctx.guild.id
    user_name = ctx.author.name
    user_id = ctx.author.id
    display_name = ctx.author.display_name
    current_time = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
    console_output = (
        f"{Fore.LIGHTYELLOW_EX}=============================================================================================================================================================== \n"
        f"{Fore.LIGHTCYAN_EX}Thời gian      :{Fore.LIGHTMAGENTA_EX} {current_time} \n"
        f"{Fore.LIGHTCYAN_EX}Server         :{Fore.LIGHTMAGENTA_EX} {server_name}{Fore.LIGHTCYAN_EX} - ID Server :{Fore.LIGHTMAGENTA_EX} {server_id} \n"
        f"{Fore.LIGHTCYAN_EX}Tên người dùng :{Fore.LIGHTMAGENTA_EX} {user_name} {Fore.LIGHTCYAN_EX}- ID người dùng :{Fore.LIGHTMAGENTA_EX} {user_id} {Fore.LIGHTCYAN_EX}| Role trong server :{Fore.LIGHTMAGENTA_EX} {display_name} \n"
        f"{Fore.LIGHTYELLOW_EX}=============================================================================================================================================================== \n"
    )
    print(console_output)

########################################################################################################################

# Bot stk
@bot.command()
@commands.has_role("bot")
async def bank(ctx, hang: str, gia: int):
    await ctx.message.delete()
    embed = discord.Embed(
        title="Thanh toán",
        description="Thông tin thanh toán",
        color=discord.Color.from_rgb(247, 57, 24)
    )
    price = f"{int(gia):,}".replace(",", ".")
    tong = f"{int(price)*1000:,}".replace(",", ".")
    taoqrtech = config['taoqrtech']
    acceptcode = paymentcode()
    transfermessage = config["transfermessage"].replace(f"%random%", acceptcode)

    embed.add_field(name="Techcombank", value="```19038504541019```", inline=False)
    embed.add_field(name="Chủ tài khoản", value="```THACH GIA BAO```", inline=False)
    embed.add_field(name="Nội dung", value=f'```{transfermessage}```', inline=False)
    embed.add_field(name="Giá", value=f'```{tong} VND```', inline=False)
    url = f"https://img.vietqr.io/image/TCB-{taoqrtech['sotaikhoan']}-compact.png?amount={int(price)*1000}&addInfo={urllib.parse.quote(transfermessage)}&accountName={urllib.parse.quote(taoqrtech['chutaikhoan'])}"
    embed.set_footer(text="Hazel Store")

    embed.set_image(url=url)

    await ctx.send("# Không ghi nội dung thì phải gửi bill!",embed=embed)
    current_time = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
    user_name = ctx.author.name
    user_id = ctx.author.id
    server_name = ctx.guild.name
    server_id = ctx.guild.id
    console_output = (
        f"{Fore.LIGHTRED_EX}Có người vừa tạo bill: \n"
        f"{Fore.LIGHTYELLOW_EX}=============================================================================================================================================================== \n"
        f"{Fore.LIGHTCYAN_EX}Tên người dùng :{Fore.LIGHTMAGENTA_EX} {user_name} {Fore.LIGHTCYAN_EX}- ID người dùng :{Fore.LIGHTMAGENTA_EX} {user_id} {Fore.LIGHTCYAN_EX} \n"
        f"{Fore.LIGHTCYAN_EX}Nơi tạo        :{Fore.LIGHTMAGENTA_EX} {server_name} - ID Server :{Fore.LIGHTMAGENTA_EX} {server_id} \n"
        f"{Fore.LIGHTCYAN_EX}Thời gian      :{Fore.LIGHTMAGENTA_EX} {current_time} \n"
        f"{Fore.LIGHTCYAN_EX}Hàng           :{Fore.LIGHTMAGENTA_EX} {hang} \n"
        f"{Fore.LIGHTCYAN_EX}Giá            :{Fore.LIGHTMAGENTA_EX} {tong} VND \n"
        f"{Fore.LIGHTCYAN_EX}Ngân hàng nhận :{Fore.LIGHTMAGENTA_EX} {taoqrtech['nganhang']} \n"
        f"{Fore.LIGHTCYAN_EX}Stk nhận       :{Fore.LIGHTMAGENTA_EX} {taoqrtech['sotaikhoan']} - Tên tk :{Fore.LIGHTMAGENTA_EX} {taoqrtech['chutaikhoan']} \n"
        f"{Fore.LIGHTYELLOW_EX}=============================================================================================================================================================== \n"
    )
    print(console_output)

@bot.command()
@commands.has_role("reseller")
async def mb(ctx,hang: str, gia: int):
    await ctx.message.delete()
    embed = discord.Embed(
        title="Thanh toán",
        description="Thông tin thanh toán",
        color=discord.Color.from_rgb(247, 57, 24)
    )
    price = f"{int(gia):,}".replace(",", ".")
    tong = f"{int(price)*1000:,}".replace(",", ".")
    taoqr = config['taoqr']
    acceptcode = paymentcode()
    transfermessage = config["transfermessage"].replace(f"%random%", acceptcode)

    embed.add_field(name="MB Bank", value=f"```{taoqr['sotaikhoan']}```", inline=False)
    embed.add_field(name="Chủ tài khoản", value="```THACH GIA BAO```", inline=False)
    embed.add_field(name="Nội dung", value=f'```{transfermessage}```', inline=False)
    embed.add_field(name="Giá", value=f'```{tong} VND```', inline=False)
    url = f"https://img.vietqr.io/image/mb-{taoqr['sotaikhoan']}-compact.png?amount={int(price)*1000}&addInfo={urllib.parse.quote(transfermessage)}&accountName={urllib.parse.quote(taoqr['chutaikhoan'])}"
    embed.set_footer(text="Hazel Store")
    embed.set_image(url=url)
    tao = ctx.author.id
    svv = ctx.guild.name
    hahaha = await ctx.send(f"# Không ghi nội dung thì phải gửi bill!!",embed=embed)
    log_embed = discord.Embed(color=discord.Color.from_rgb(135, 206, 235), title='Chuyển khoản MB',description=f'**Người tạo: <@{tao}>**\n**{svv}**\n**Giá tiền: {gia}.OOO VND**\n**Hàng: {hang}**\n**Nội dung bank: {transfermessage}**\n**<t:{math.floor(time.time())}:f>**')
    await bot.get_channel(logchannel).send(embed = log_embed)
    await ctx.send("Sau khi chuyển khoản xong thì dùng lệnh /thongtin để điền thông tin nếu bạn mua nitro nhé!")

    current_time = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
    user_name = ctx.author.name
    user_id = ctx.author.id
    server_name = ctx.guild.name
    server_id = ctx.guild.id
    console_output = (
        f"{Fore.LIGHTRED_EX}Có người vừa tạo bill: \n"
        f"{Fore.LIGHTYELLOW_EX}=============================================================================================================================================================== \n"
        f"{Fore.LIGHTCYAN_EX}Tên người dùng :{Fore.LIGHTMAGENTA_EX} {user_name} {Fore.LIGHTCYAN_EX}- ID người dùng :{Fore.LIGHTMAGENTA_EX} {user_id} {Fore.LIGHTCYAN_EX} \n"
        f"{Fore.LIGHTCYAN_EX}Nơi tạo        :{Fore.LIGHTMAGENTA_EX} {server_name} - ID Server :{Fore.LIGHTMAGENTA_EX} {server_id} \n"
        f"{Fore.LIGHTCYAN_EX}Thời gian      :{Fore.LIGHTMAGENTA_EX} {current_time} \n"
        f"{Fore.LIGHTCYAN_EX}Hàng           :{Fore.LIGHTMAGENTA_EX} {hang} \n"
        f"{Fore.LIGHTCYAN_EX}Giá            :{Fore.LIGHTMAGENTA_EX} {tong} VND \n"
        f"{Fore.LIGHTCYAN_EX}Ngân hàng nhận :{Fore.LIGHTMAGENTA_EX} {taoqr['nganhang']} \n"
        f"{Fore.LIGHTCYAN_EX}Stk nhận       :{Fore.LIGHTMAGENTA_EX} {taoqr['sotaikhoan']} - Tên tk :{Fore.LIGHTMAGENTA_EX} {taoqr['chutaikhoan']} \n"
        f"{Fore.LIGHTYELLOW_EX}=============================================================================================================================================================== \n"
    )
    print(console_output)

########################################################################################################################

#Bot nhạc dùng lệnh play,pause,skip
@bot.command()
async def play(ctx, *, search):
    voice_channel = ctx.author.voice.channel if ctx.author.voice else None

    if not voice_channel:
        return await ctx.reply("Bạn cần ở trong một kênh thoại!")

    if ctx.voice_client:
        if ctx.voice_client.channel != voice_channel:
            non_bot_members = [member for member in ctx.voice_client.channel.members if not member.bot]
            if len(non_bot_members) == 0:
                await ctx.voice_client.disconnect()
                await voice_channel.connect()
            else:
                return await ctx.reply("Bot đang kết nối với kênh khác.")
    else:
        await voice_channel.connect()

    async with ctx.typing():
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(f"ytsearch:{search}", download=False)
            if 'entries' in info:
                info = info['entries'][0]
            url = info['url']
            title = info['title']
            duration = info['duration']
            thumbnail = info['thumbnail']
            item = (url, title, duration, thumbnail)
            music_player.queue.append(item)
            music_player.current_song = item
            embed = discord.Embed(title="Đã thêm vào hàng đợi", description=f"**{title}**", color=discord.Color.green())
            embed.add_field(name="Thời lượng", value=f"{duration // 60}:{duration % 60:02d}", inline=True)
            embed.add_field(name="Hàng đợi", value=len(music_player.queue), inline=True)
            embed.set_thumbnail(url=thumbnail)
            await ctx.send(embed=embed)
            server_name = ctx.guild.name
            server_id = ctx.guild.id
            user_name = ctx.author.name
            user_id = ctx.author.id
            display_name = ctx.author.display_name
            current_time = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
            console_output = (
        f"{Fore.LIGHTYELLOW_EX}=============================================================================================================================================================== \n"
        f"{Fore.LIGHTCYAN_EX}Thời gian      :{Fore.LIGHTMAGENTA_EX} {current_time} \n"
        f"{Fore.LIGHTCYAN_EX}Bài hát        :{Fore.LIGHTMAGENTA_EX} {title} \n"
        f"{Fore.LIGHTCYAN_EX}Thời lượng     :{Fore.LIGHTMAGENTA_EX} {duration // 60}:{duration % 60:02d} \n"
        f"{Fore.LIGHTCYAN_EX}Server         :{Fore.LIGHTMAGENTA_EX} {server_name}{Fore.LIGHTCYAN_EX} - ID Server :{Fore.LIGHTMAGENTA_EX} {server_id} \n"
        f"{Fore.LIGHTCYAN_EX}Tên người dùng :{Fore.LIGHTMAGENTA_EX} {user_name} {Fore.LIGHTCYAN_EX}- ID người dùng :{Fore.LIGHTMAGENTA_EX} {user_id} {Fore.LIGHTCYAN_EX}| Role trong server :{Fore.LIGHTMAGENTA_EX} {display_name} \n"
        f"{Fore.LIGHTYELLOW_EX}=============================================================================================================================================================== \n"
    )
            print(console_output)

    if not ctx.voice_client.is_playing():
        await play_next(ctx)

async def play_next(ctx):
    if ctx.voice_client is None or not ctx.voice_client.is_connected():
        await ctx.send("Bot không còn kết nối với kênh thoại.")
        return

    if music_player.queue:
        item = music_player.queue.pop(0)
        if len(item) == 4:
            url, title, _, _ = item
            source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
            ctx.voice_client.play(source, after=lambda _: bot.loop.create_task(play_next(ctx)))
            await ctx.send(embed = discord.Embed(title="Đang phát", description=f"**{title}**", color=discord.Color.green()))
        else:
            await ctx.send("Lỗi: Định dạng item trong hàng đợi không đúng.")
    else:
        if music_player.is_looping and music_player.current_song:
            music_player.queue.append(music_player.current_song)
            await play_next(ctx)
        else:
            await ctx.send(embed=discord.Embed(title="Hàng đợi trống", description="", color=discord.Color.blue()))

@bot.command()
async def skip(ctx):
    if ctx.voice_client:
        if ctx.voice_client.is_playing():
            if ctx.author.voice and ctx.author.voice.channel == ctx.voice_client.channel:
                ctx.voice_client.stop()
                await ctx.reply(embed=discord.Embed(title="Đã bỏ qua bài hát", description="", color=discord.Color.green()))
            else:
                await ctx.reply("Bạn cần ở trong cùng một kênh thoại với bot để sử dụng lệnh này.")
        else:
            await ctx.reply("Bot không đang phát bất cứ thứ gì.")
    else:
        await ctx.reply("Bot không kết nối với bất kỳ kênh thoại nào.")

@bot.command()
async def pause(ctx):
    if ctx.voice_client:
        if ctx.voice_client.is_playing():
            if ctx.author.voice and ctx.author.voice.channel == ctx.voice_client.channel:
                ctx.voice_client.pause()
                await ctx.reply(embed=discord.Embed(title="Đã tạm dừng", description="", color=discord.Color.red()))
            else:
                await ctx.reply("Bạn cần ở trong cùng một kênh thoại với bot để sử dụng lệnh này.")
        else:
            await ctx.reply("Bot không đang phát bất cứ thứ gì.")
    else:
        await ctx.reply("Bot không kết nối với bất kỳ kênh thoại nào.")

@bot.command()
async def resume(ctx):
    if ctx.voice_client:
        if ctx.voice_client.is_paused():
            if ctx.author.voice and ctx.author.voice.channel == ctx.voice_client.channel:
                ctx.voice_client.resume()
                await ctx.reply(embed=discord.Embed(title="Đã tiếp tục", description="", color=discord.Color.green()))
            else:
                await ctx.reply("Bạn cần ở trong cùng một kênh thoại với bot để sử dụng lệnh này.")
        else:
            await ctx.reply("Bot không đang tạm dừng hoặc không phát bất cứ thứ gì.")
    else:
        await ctx.reply("Bot không kết nối với bất kỳ kênh thoại nào.")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        if ctx.author.voice and ctx.author.voice.channel == ctx.voice_client.channel:
            music_player.queue.clear()
            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
            await ctx.reply(embed=discord.Embed(title="Dừng phát", description="", color=discord.Color.red()))
        else:
            await ctx.reply("Bạn cần ở trong cùng một kênh thoại với bot để sử dụng lệnh này.")
    else:
        await ctx.reply("Bot không kết nối với bất kỳ kênh thoại nào.")

@bot.command()
async def loop(ctx):
    music_player.is_looping = not music_player.is_looping
    status = "Bật" if music_player.is_looping else "Tắt"
    await ctx.reply(embed=discord.Embed(title=f"Chế độ lặp lại: {status}", description="", color=discord.Color.green()))

@tasks.loop(minutes=3)
async def check_voice_channels():
    for vc in bot.voice_clients:
        if vc.channel:
            if len(vc.channel.members) == 1:
                await vc.disconnect()
                music_player.queue.clear()
                await bot.get_channel(vc.channel.id).send(embed=discord.Embed(title="Ngắt kết nối", description="Không có người dùng trong kênh thoại. Hàng đợi đã được xóa.", color=discord.Color.red()))

########################################################################################################
@bot.command()
async def p(ctx, *, search):
    voice_channel = ctx.author.voice.channel if ctx.author.voice else None

    if not voice_channel:
        return await ctx.reply("Bạn cần ở trong một kênh thoại!")

    if ctx.voice_client:
        if ctx.voice_client.channel != voice_channel:
            non_bot_members = [member for member in ctx.voice_client.channel.members if not member.bot]
            if len(non_bot_members) == 0:
                await ctx.voice_client.disconnect()
                await voice_channel.connect()
            else:
                return await ctx.reply("Bot đang kết nối với kênh khác.")
    else:
        await voice_channel.connect()

    async with ctx.typing():
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(f"ytsearch:{search}", download=False)
            if 'entries' in info:
                info = info['entries'][0]
            url = info['url']
            title = info['title']
            duration = info['duration']
            thumbnail = info['thumbnail']
            item = (url, title, duration, thumbnail)
            music_player.queue.append(item)
            music_player.current_song = item
            embed = discord.Embed(title="Đã thêm vào hàng đợi", description=f"**{title}**", color=discord.Color.green())
            embed.add_field(name="Thời lượng", value=f"{duration // 60}:{duration % 60:02d}", inline=True)
            embed.add_field(name="Hàng đợi", value=len(music_player.queue), inline=True)
            embed.set_thumbnail(url=thumbnail)
            await ctx.send(embed=embed)
            server_name = ctx.guild.name
            server_id = ctx.guild.id
            user_name = ctx.author.name
            user_id = ctx.author.id
            display_name = ctx.author.display_name
            current_time = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
            console_output = (
        f"{Fore.LIGHTYELLOW_EX}=============================================================================================================================================================== \n"
        f"{Fore.LIGHTCYAN_EX}Thời gian      :{Fore.LIGHTMAGENTA_EX} {current_time} \n"
        f"{Fore.LIGHTCYAN_EX}Bài hát        :{Fore.LIGHTMAGENTA_EX} {title} \n"
        f"{Fore.LIGHTCYAN_EX}Thời lượng     :{Fore.LIGHTMAGENTA_EX} {duration // 60}:{duration % 60:02d} \n"
        f"{Fore.LIGHTCYAN_EX}Server         :{Fore.LIGHTMAGENTA_EX} {server_name}{Fore.LIGHTCYAN_EX} - ID Server :{Fore.LIGHTMAGENTA_EX} {server_id} \n"
        f"{Fore.LIGHTCYAN_EX}Tên người dùng :{Fore.LIGHTMAGENTA_EX} {user_name} {Fore.LIGHTCYAN_EX}- ID người dùng :{Fore.LIGHTMAGENTA_EX} {user_id} {Fore.LIGHTCYAN_EX}| Role trong server :{Fore.LIGHTMAGENTA_EX} {display_name} \n"
        f"{Fore.LIGHTYELLOW_EX}=============================================================================================================================================================== \n"
    )
            print(console_output)

    if not ctx.voice_client.is_playing():
        await play_next(ctx)




@bot.command()
async def s(ctx):
    if ctx.voice_client:
        if ctx.voice_client.is_playing():
            if ctx.author.voice and ctx.author.voice.channel == ctx.voice_client.channel:
                ctx.voice_client.stop()
                await ctx.reply(embed=discord.Embed(title="Đã bỏ qua bài hát", description="", color=discord.Color.green()))
            else:
                await ctx.reply("Bạn cần ở trong cùng một kênh thoại với bot để sử dụng lệnh này.")
        else:
            await ctx.reply("Bot không đang phát bất cứ thứ gì.")
    else:
        await ctx.reply("Bot không kết nối với bất kỳ kênh thoại nào.")
########################################################################################################################


@bot.command(alias = ["join"])
async def join(ctx):
    if (ctx.author.voice): 
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("Bot đã vào room.")
    else: 
        await ctx.send("Bạn phải trong 1 room nào đó mới có thể sử dụng lệnh này.")

@bot.command(alias = ["leave"])
async def leave(ctx): 
    if (ctx.voice_client): 
        await ctx.guild.voice_client.disconnect() 
        await ctx.send("Bot đã out.")

    else: 
        await ctx.send("Bot đang không ở trong room.")
########################################################################################################################



@bot.command()
@commands.has_role("bot")
async def yumi(ctx, hang: str, gia: int):
    await ctx.message.delete()
    embed = discord.Embed(
        title="Thanh toán",
        description="Thông tin thanh toán",
        color=discord.Color.from_rgb(247, 57, 24)
    )
    price = f"{int(gia):,}".replace(",", ".")
    tong = f"{int(price)*1000:,}".replace(",", ".")
    taoqrmbyumi = config['taoqrmbyumi']
    acceptcode = paymentcode()
    transfermessage = config["transfermessage"].replace(f"%random%", acceptcode)

    embed.add_field(name="MB Bank", value="```0388943002```", inline=False)
    embed.add_field(name="Chủ tài khoản", value="```HUYNH THANH MY HANH```", inline=False)
    embed.add_field(name="Nội dung", value=f'```{transfermessage}```', inline=False)
    embed.add_field(name="Giá", value=f'```{tong} VND```', inline=False)
    url = f"https://img.vietqr.io/image/mb-{taoqrmbyumi['sotaikhoan']}-compact.png?amount={int(price)*1000}&addInfo={urllib.parse.quote(transfermessage)}&accountName={urllib.parse.quote(taoqrmbyumi['chutaikhoan'])}"

    embed.set_footer(text="Hazel Store")

    embed.set_image(url=url)

    await ctx.send("# Không ghi nội dung thì phải gửi bill!",embed=embed)

    current_time = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
    user_name = ctx.author.name
    user_id = ctx.author.id
    console_output = (
        f"{Fore.LIGHTRED_EX}Có người vừa tạo bill: \n"
        f"{Fore.LIGHTYELLOW_EX}=============================================================================================================================================================== \n"
        f"{Fore.LIGHTCYAN_EX}Tên người dùng :{Fore.LIGHTMAGENTA_EX} {user_name} {Fore.LIGHTCYAN_EX}- ID người dùng :{Fore.LIGHTMAGENTA_EX} {user_id} {Fore.LIGHTCYAN_EX} \n"
        f"{Fore.LIGHTCYAN_EX}Thời gian      :{Fore.LIGHTMAGENTA_EX} {current_time} \n"
        f"{Fore.LIGHTCYAN_EX}Hàng           :{Fore.LIGHTMAGENTA_EX} {hang} \n"
        f"{Fore.LIGHTCYAN_EX}Giá            :{Fore.LIGHTMAGENTA_EX} {tong} VND \n"
        f"{Fore.LIGHTCYAN_EX}Ngân hàng nhận :{Fore.LIGHTMAGENTA_EX} {taoqrmbyumi['nganhang']} \n"
        f"{Fore.LIGHTCYAN_EX}Stk nhận       :{Fore.LIGHTMAGENTA_EX} {taoqrmbyumi['sotaikhoan']} - Tên tk :{Fore.LIGHTMAGENTA_EX} {taoqrmbyumi['chutaikhoan']} \n"
        f"{Fore.LIGHTYELLOW_EX}=============================================================================================================================================================== \n"
    )
    print(console_output)

########################################################################################################################


@bot.command(name='help')
@commands.has_role("bot")
async def help_nigga(ctx):
    await ctx.message.delete()

    pages = [
        discord.Embed(title="Các lệnh của Bot nhạc Hazel Store", description="**Lưu ý khi dùng bot**\n`prefix: đéo có prefix`\n> Bot sử dụng youtube và không dùng được playlist ạ\n**- play <Bài hát>: Mở nhạc**\n**- skip: Qua bài**\n**- stop: Dừng bài hát**\n**- pause: Tạm dừng**\n**- resume: Tiếp tục phát**\n**- join: Cho bot vào room**\n**- leave: Cho bot ra khỏi room**"),
        discord.Embed(title="Các lệnh của Bot Hazel Store dành cho staff", description="**Lưu ý khi dùng bot\n> Số tiền phải dưới 1000 có nghĩa là đéo có món nào 1tr đó**\n`prefix: đéo có prefix`\n\n**- bank <Tên hàng> <Số tiền>**\n**- mb <Tên hàng> <Số tiền>**\n**- yumi <Tên hàng> <Số tiền>**\n**- stock**\n**- !order <@Khách hàng> (Riêng lệnh này thì là !order)**\n**- nitro <loại> <id> <link>**\n**- acc <loại> <id> <tk> <mk>**\n"),
        discord.Embed(title="Thông tin Bot Hazel Store", description="## **Developer** \n- **[za pao](https://www.facebook.com/thachgiabao210)**\n\n## **Contributor**\n[**Mời bot vào server**](https://discord.gg/hazelstore)"),
    ]

    paginator = Paginator(ctx, pages)
    await paginator.start()

########################################################################################################################

@bot.command(name = "<1251767575524806706>")
@commands.has_role("bot")
async def testt(ctx):
    await ctx.message.delete()

    embed = discord.Embed(title="Các lệnh của Bot nhạc Hazel Store", description="**Lưu ý khi dùng bot**\n`prefix: đéo có prefix`\n> Bot sử dụng youtube và không dùng được playlist ạ\n**- play <Bài hát>: Mở nhạc**\n**- skip: Qua bài**\n**- stop: Dừng bài hát**\n**- pause: Tạm dừng**\n**- resume: Tiếp tục phát**\n**- join: Cho bot vào room**\n**- leave: Cho bot ra khỏi room**")

    await ctx.send(embed=embed)





########################################################################################################################

@bot.command()
@commands.has_role("bot")
async def e(ctx, thangngu: str):
    await ctx.message.delete()
    await ctx.send(f'ê {thangngu}')




########################################################################################################################

@bot.command()
@commands.has_role("bot")
async def tos(ctx):
    await ctx.message.delete()

    pages = [
        discord.Embed(title="TOS - Term Of Service", description="\n\n> Luôn luôn tuân theo Discord TOS\n[Đọc tại đây](https://discord.com/tos)\n"),
        discord.Embed(title="Cảm ơn bạn đã chấp nhận luật mua hàng", description="\n# Đọc kĩ lại tại [**đây**](https://discord.com/channels/1220320347316948992/1235583420768325722/1235586848911528017) =)))))))))))"),
        discord.Embed(title="Cặc", description="cút")
    ]

    paginator = Paginator(ctx, pages)
    await paginator.start()




########################################################################################################################


@bot.command()
@commands.has_role("-`ღ´- ˚ •。✰ Staff ✰  ｡• ˚ -`ღ´-")
async def ping(ctx, id: str):
    await ctx.message.delete()
    await ctx.send(f'# <a:gz_chucmung:1278942262780235901> Fls ga + Minigame <a:gz_chucmung:1278942262780235901> Nhá <@&{id}>')


@bot.command()
@commands.has_role("-`ღ´- ˚ •。✰ Staff ✰  ｡• ˚ -`ღ´-")
async def givefls(ctx):
    await ctx.message.delete()
    await ctx.send("# <:gz_chamthan:1276887538618990715>  Gửi ảnh + cmt số lần trúng tại: https://discord.com/channels/1221739755138453525/1253630340602396672")


@bot.command()
@commands.has_role("-`ღ´- ˚ •。✰ Staff ✰  ｡• ˚ -`ღ´-")
async def phi(ctx):
    await ctx.message.delete()
    await ctx.send("# <:gz_n1:1284529120729890897> Giá Trị Giveaway <:gz_n1:1284529120729890897>\n<:gz_cat14:1284526283111534674> Giveaway kéo member.\n<a:gz_mui_ten_hong:1284526189482082344> Giá trị 1,000,000 <:cowoncy:1284526152161034351>\n<:gz_cat14:1284526283111534674> Giveaway kéo vote.\n<a:gz_mui_ten_hong:1284526189482082344> Giá trị ≥ 600,000 <:cowoncy:1284526152161034351>\n<:gz_cat14:1284526283111534674> Giveaway PR sản phẩm, quảng cáo, mạng xã hội ngoài phạm vi Discord.\n<a:gz_mui_ten_hong:1284526189482082344> Giá trị ≥ 800,000 <:cowoncy:1284526152161034351>\n<:gz_cat14:1284526283111534674> Giveaway Vui Vẻ, Chat CMSN,..\n<a:gz_mui_ten_hong:1284526189482082344> Giá trị ≥ 200,000  <:cowoncy:1284526152161034351>\n<:gz_cat14:1284526283111534674> Giveaway từ <@408785106942164992>  như pray/ curse…. \n<a:gz_mui_ten_hong:1284526189482082344> Giá trị ≥ 300,000  <:cowoncy:1284526152161034351>\n<a:gz_tim1:1284527630795935805>  ・┈ ・ ・┈ ・ ・┈ ・ ・┈・ <a:gz_tim1:1284527630795935805> \n# <a:gz_trai_tim:1284526223036518450> Phí Tạo Giveaway\n<a:gz_bluestar:1284527973592203334>  2 giờ = 200,000 <:cowoncy:1284526152161034351>\n<a:gz_bluestar:1284527973592203334>  5 giờ = 500,000 <:cowoncy:1284526152161034351>\n<a:gz_bluestar:1284527973592203334>  12 giờ = 800,000 <:cowoncy:1284526152161034351>\n<a:gz_bluestar:1284527973592203334>  1 ngày = 1,200,000 <:cowoncy:1284526152161034351>\n<a:gz_bluestar:1284527973592203334>  2 ngày = 2,000,000 <:cowoncy:1284526152161034351>\n<a:gz_bluestar:1284527973592203334>  3 ngày = 3,000,000 <:cowoncy:1284526152161034351>\n<a:gz_tim1:1284527630795935805>  ・┈ ・ ・┈ ・ ・┈ ・ ・┈・ <a:gz_tim1:1284527630795935805>\nhttps://discord.com/channels/1221739755138453525/1225002716095451196")


@bot.command()
@commands.has_role("OWNER")
async def lt(ctx, mem: str):
    await ctx.message.delete()
    await ctx.send(f'# <a:gz_chucmung:1278942262780235901> Chúc mừng <a:gz_chucmung:1278942262780235901> {mem} đã trở thành Lễ tân của sv CSGZ')


@bot.command()
@commands.has_role("OWNER")
async def mod(ctx, mem: str):
    await ctx.message.delete()
    await ctx.send(f'# <a:gz_chucmung:1278942262780235901> Chúc mừng <a:gz_chucmung:1278942262780235901> {mem} đã trở thành Moderator của sv CSGZ')


@bot.command()
@commands.has_role("OWNER")
@commands.has_role("con cặc")
async def sp(ctx, mem: str):
    await ctx.message.delete()
    await ctx.send(f'# <a:gz_chucmung:1278942262780235901> Chúc mừng <a:gz_chucmung:1278942262780235901> {mem} đã trở thành Supporter của sv CSGZ')

########################################################################################################################




@bot.command(name='acc')
@commands.has_role("Legit Seller")
async def trahangacc(ctx, ten, target_id: int, tk, mk):
    await ctx.message.delete()
    target_info = await bot.fetch_user(target_id)
    await target_info.send(f'# Cảm ơn bạn đã ủng hộ ạaaa\n\n> Tài khoản: {tk}\n> Pass: {mk}')
    await ctx.send(f'<@{target_id}> Bạn oi có gì vouch cho mình với ạaa')
    current_time = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
    console_output = (
        f"{Fore.LIGHTRED_EX}Vừa trả hàng bên dưới \n"
        f"{Fore.LIGHTYELLOW_EX}=============================================================================================================================================================== \n"
        f"{Fore.LIGHTCYAN_EX}ID khách       :{Fore.LIGHTMAGENTA_EX} {target_id} \n"
        f"{Fore.LIGHTCYAN_EX}Tên hàng       :{Fore.LIGHTMAGENTA_EX} {ten} \n"
        f"{Fore.LIGHTCYAN_EX}Tài khoản      :{Fore.LIGHTMAGENTA_EX} {tk} \n"
        f"{Fore.LIGHTCYAN_EX}Pass           :{Fore.LIGHTMAGENTA_EX} {mk} \n"
        f"{Fore.LIGHTCYAN_EX}Thời gian trả  :{Fore.LIGHTMAGENTA_EX} {current_time} \n"
        f"{Fore.LIGHTYELLOW_EX}=============================================================================================================================================================== \n"
    )
    print(console_output)




###############################################################################
# VOUCH BOT

@bot.command(name="+vouch")
async def hsuadhuiuid(interaction: discord.Interaction, *, msg: str = None):
    if int(interaction.channel.id) == int(config['vouchchannel']):
        if msg:
            with open('vouches.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()  
                vouchcounter = len(lines)
                uservouchcounter = 0
                for line in lines:
                    if f'{interaction.author.id}' in line:
                        uservouchcounter += 1
            message = config['message'].replace('(usermention)',f'{interaction.author.mention}').replace('(vouchcounter)', f'{vouchcounter + 1}')
            botmessage = await interaction.send (message, mention_author=False)
            try:
                avatar_url = interaction.author.avatar.url
            except: avatar_url = None
            with open('vouches.txt', 'a', encoding='utf-8') as f:
                f.write(f'{interaction.author.id}|{interaction.author.display_name}|{avatar_url}|{botmessage.id}|{interaction.message.id}|{msg}\n')
        else:
            await interaction.reply(f"{interaction.author.mention} Bạn cần cung cấp thông tin!", delete_after=10)
            await asyncio.sleep(10)
            await interaction.message.delete()
    else:
        await interaction.reply(f"{interaction.author.mention} Bạn chỉ có thể sử dụng lệnh ở <#{config['vouchchannel']}>!", delete_after=10)
        await asyncio.sleep(10)
        await interaction.message.delete()



@bot.command(name="+rep")
async def rep(interaction: discord.Interaction, *, msg: str = None):
    if int(interaction.channel.id) == int(config['vouchchannel']):
        if msg:
            with open('vouches.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()  
                vouchcounter = len(lines)
                uservouchcounter = 0
                for line in lines:
                    if f'{interaction.author.id}' in line:
                        uservouchcounter += 1
            message = config['message'].replace('(usermention)',f'{interaction.author.mention}').replace('(vouchcounter)', f'{vouchcounter + 1}')
            botmessage = await interaction.send (message, mention_author=False)
            try:
                avatar_url = interaction.author.avatar.url
            except: avatar_url = None
            with open('vouches.txt', 'a', encoding='utf-8') as f:
                f.write(f'{interaction.author.id}|{interaction.author.display_name}|{avatar_url}|{botmessage.id}|{interaction.message.id}|{msg}\n')
        else:
            await interaction.reply(f"{interaction.author.mention} Bạn cần cung cấp thông tin!", delete_after=10)
            await asyncio.sleep(10)
            await interaction.message.delete()
    else:
        await interaction.reply(f"{interaction.author.mention} Bạn chỉ có thể sử dụng lệnh ở <#{config['vouchchannel']}>!", delete_after=10)
        await asyncio.sleep(10)
        await interaction.message.delete()

@bot.command(name="+remove")
async def remove(interaction: discord.Interaction, messageid: int = None):
    if interaction.channel.permissions_for(interaction.author).manage_messages:
        if messageid:
            vouches = []
            with open('vouches.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()  
                for line in lines:
                    if f'{messageid}' in line:
                        try:
                            message = await interaction.channel.fetch_message(messageid)
                            await message.delete()
                        except discord.NotFound:
                            pass
                        try:
                            message = await interaction.channel.fetch_message(line.split('|')[3])
                            await message.delete()
                        except discord.NotFound:
                            pass
                        continue
                    vouches.append(line)
                with open('vouches.txt', 'w', encoding='utf-8') as f:
                    f.writelines(vouches)
            await interaction.reply(f"{interaction.author.mention} Removed vouch {messageid}!", delete_after=10)
            await asyncio.sleep(10)
            await interaction.message.delete()                
        else:
            await interaction.reply(f"{interaction.author.mention} Vui lòng nhập message_id!", delete_after=10)
            await asyncio.sleep(10)
            await interaction.message.delete()
    else:
        await interaction.reply(f"{interaction.author.mention} Bạn không có quyền sử dụng lệnh!", delete_after=10)
        await asyncio.sleep(10)
        await interaction.message.delete()

@bot.command(name="+backup")
async def backup(interaction: discord.Interaction, webhook: str = None):
    if interaction.guild:
        member = interaction.guild.get_member(interaction.author.id)
        if member.guild_permissions.administrator:
            if webhook:
                response = requests.get(webhook)
                if response.status_code == 200:
                    print('backup...')
                    with open('vouches.txt', 'r', encoding='utf-8') as f:
                        lines = f.readlines()  
                        for line in lines:
                            backup = line.split("|")
                            username = backup[1]
                            avatar_url = backup[2]
                            content = config['backupmessage'].replace('(message)', f'{backup[5]}')
                            if avatar_url == 'None':
                                data = {
                                    'username': username,
                                    'avatar_url': 'https://cdn.discordapp.com/embed/avatars/0.png',
                                    'content': content
                                }
                            else:
                                data = {
                                    'username': username,
                                    'avatar_url': avatar_url,
                                    'content': content
                                }
                            try:
                                response = requests.post(webhook, headers={'Content-Type': 'application/json'}, data=json.dumps(data))
                            except: None
                        print('successfully!')
                        await interaction.reply(f"{interaction.author.mention} Done!", delete_after=10)
                        await asyncio.sleep(10)
                        await interaction.message.delete()
                else:
                    await interaction.reply(f"{interaction.author.mention} Webhook không hợp lệ!", delete_after=10)
                    await asyncio.sleep(10)
                    await interaction.message.delete()
            else:
                await interaction.reply(f"{interaction.author.mention} Vui lòng nhập webhookurl!", delete_after=10)
                await asyncio.sleep(10)
                await interaction.message.delete()
        else:
            await interaction.reply(f"{interaction.author.mention} Bạn không có quyền sử dụng lệnh!", delete_after=10)
            await asyncio.sleep(10)
            await interaction.message.delete()
    else:
        await interaction.reply("Lệnh này chỉ có thể sử dụng trong server!", delete_after=10)
        await asyncio.sleep(10)
        await interaction.message.delete()

@bot.command()
async def addar(ctx, *, trigger_and_response: str):
    # Split the trigger and response using a comma (",")
    trigger, response = map(str.strip, trigger_and_response.split(','))

    with open('auto_responses.json', 'r') as file:
        data = json.load(file)

    data[trigger] = response

    with open('auto_responses.json', 'w') as file:
        json.dump(data, file, indent=4)

    await ctx.send(f'**AUTO-RESPONSE ADDED.. !** **{trigger}** - **{response}**')



@bot.command()
async def removear(ctx, trigger: str):
    with open('auto_responses.json', 'r') as file:
        data = json.load(file)

    if trigger in data:
        del data[trigger]

        with open('auto_responses.json', 'w') as file:
            json.dump(data, file, indent=4)

        await ctx.send(f'**AUTO-RESPONSE REMOVED** **{trigger}**')
    else:
        await ctx.send(f'**AUTO-RESPONSE NOT FOUND** **{trigger}**')







#########################################################################################################################################


@bot.command()
@commands.has_role("Legit Seller")
async def baohanh(ctx):
    await ctx.message.delete()

    embed = discord.Embed(
        title="Hazel Store",
        description="# Chính sách bảo hành!!!",
        color=discord.Color.from_rgb(247, 57, 24)
    )
    
    embed.add_field(name="", value="",inline=False)
    embed.add_field(name="", value="",inline=False)
    embed.add_field(name="Bảo hành", value="- Để được hỗ trợ bảo hành hãy tạo ticket và trình bày vấn đề, nên nhớ **ĐỪNG PING 1 AI**\n- Tất cả đều được bảo hành trong thời gian sử dụng\n- Để nhận được bảo hành cần cung cấp đủ thông tin đã mua hàng\n- Không bảo hành cho những trường hợp share acc, đổi thông tin khi mình chưa cho phép và bán lại acc khi chưa thông báo bạn là seller\n- Chỉ hoàn tiền trong trường hợp đã hết hàng tồn\n- Đừng hối bảo hành vì nếu bạn bị thì người khác cũng vậy thôi\n- Seller khi thu về cần bảo hành phải ib riêng không tạo ticket\n", inline=False)
    embed.add_field(name="Lưu ý vui lòng đọc kĩ để tránh hiểu nhầm 2 bên", value="", inline=False)
    embed.add_field(name="Mình có thể thay đổi luật này bất cứ lúc nào", value="", inline=False)


    embed.set_footer(text="Hazel Store")
    
    embed.set_image(url="")
    
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1251767575524806706/a_5792a01d18171b9765984811fbf2b6d3.gif?size=4096")
    
    await ctx.send("# <:haz1:1291658759030181919><:haz2:1291658781838540821><:haz3:1291658797776896070><:haz4:1291658813648277514><:haz5:1291658830178156606>\n", embed=embed)
    server_name = ctx.guild.name
    server_id = ctx.guild.id
    user_name = ctx.author.name
    user_id = ctx.author.id
    display_name = ctx.author.display_name
    current_time = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
    console_output = (
        f"{Fore.LIGHTYELLOW_EX}=============================================================================================================================================================== \n"
        f"{Fore.LIGHTCYAN_EX}Thời gian      :{Fore.LIGHTMAGENTA_EX} {current_time} \n"
        f"{Fore.LIGHTCYAN_EX}Server         :{Fore.LIGHTMAGENTA_EX} {server_name}{Fore.LIGHTCYAN_EX} - ID Server :{Fore.LIGHTMAGENTA_EX} {server_id} \n"
        f"{Fore.LIGHTCYAN_EX}Tên người dùng :{Fore.LIGHTMAGENTA_EX} {user_name} {Fore.LIGHTCYAN_EX}- ID người dùng :{Fore.LIGHTMAGENTA_EX} {user_id} {Fore.LIGHTCYAN_EX}| Role trong server :{Fore.LIGHTMAGENTA_EX} {display_name} \n"
        f"{Fore.LIGHTYELLOW_EX}=============================================================================================================================================================== \n"
    )
    print(console_output)
##########################################################################################################################################

@bot.command(name="!latency")
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))

@bot.command(name="!gach")
async def hahahahah(ctx):
    await ctx.message.delete()
    await ctx.send("-------------------------------------------")

##########################################################################################################################################

    
###########################################################################################################################################
class Select(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='NICHO BOOST', emoji='a:NITRO:1255338967021260860', description='Nitro Boost hàng login'),
            discord.SelectOption(label='NICHO BASIC', emoji='a:basic:1255339140627693660', description='Nitro Basic hàng login'),
            discord.SelectOption(label='NICHO TRIAL', emoji='a:NITRO:1255338967021260860', description='Nitro trial giá rẻ'),
            discord.SelectOption(label='BOOST SERVER', emoji='a:butsv:1278620350019797037', description='BOOST SERVER'),
            discord.SelectOption(label='SPOTIFY', emoji='a:Spotify:1236133935898169404', description='Spotify giá rẻ đâyyy'),
            discord.SelectOption(label='THẺ', emoji='a:visa:1298041529071571025', description='Dịch vụ thuê thẻ'),

        ]

        super().__init__(placeholder="Ấn ở đây để chọn!",max_values=1,min_values=1,options=options)
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        config = reloadconfig()
        if self.values[0] == 'NICHO BOOST': 
            embed = discord.Embed(title='NICHO', description=f"", color=0xd4b4f4)
            embed.add_field(name="NICHO BOOST", value=f"> NICHO LOGIN — 1 THÁNG : **85.OOO VND**\n> NICHO LOGIN — 1 NĂM : **820.000 VND**", inline=False)
            await interaction.followup.send(embed=embed, ephemeral=True)

        elif self.values[0] == 'NICHO BASIC':
            embed = discord.Embed(title='NICHO', description=f"", color=0xd4b4f4)
            embed.add_field(name="NICHO BASIC", value=f"> NICHO LOGIN — 1 THÁNG : **35.OOO VND**\n> NICHO LOGIN — 1 NĂM : **35O.OOO VND**", inline=False)
            await interaction.followup.send(embed=embed, ephemeral=True)

        elif self.values[0] == 'NICHO TRIAL':
            embed = discord.Embed(title='NICHO', description=f"", color=0xd4b4f4)
            embed.add_field(name="NICHO TRIAL", value=f"> NICHO TRIAL — 3 THÁNG : **50.OOO VND**\n> NITRO TRIAL — 1 THÁNG: **25.OOO VND**", inline=False)
            await interaction.followup.send(embed=embed, ephemeral=True)
        elif self.values[0] == 'BOOST SERVER':
            embed = discord.Embed(title='BOOST SERVER', description=f"", color=0xd4b4f4)
            embed.add_field(name="BOOST SERVER", value=f"> 14 BOOST SERVER — 3 THÁNG : **200.OOO VND**\n> 14 BOOST SERVER — 1 THÁNG: **65.OOO VND**", inline=False)
            await interaction.followup.send(embed=embed, ephemeral=True)
        elif self.values[0] == 'SPOTIFY':
            embed = discord.Embed(title='SPOTIFY', description=f"", color=0xd4b4f4)
            embed.add_field(name="SPOTIFY", value=f"> SPOTIFY 1 THÁNG DẠNG CẤP ACC : **35.OOO VND**\n> SPOTIFY 1 THÁNG DẠNG CHÍNH CHỦ : **50.OOO VND**", inline=False)
            await interaction.followup.send(embed=embed, ephemeral=True)
        elif self.values[0] == 'THẺ':
            embed = discord.Embed(title='VISA / MASTERCARD', description=f"", color=0xd4b4f4)
            embed.add_field(name="VISA / MASTERCARD", value=f"> THUÊ THẺ 1 THÁNG : 40.OOO VND ( THẺ THỔ NHĨ KỲ, FREE NẾU THUÊ THẺ VÀ NẠP TIỀN VÀO THẺ ĐỂ DÙNG )", inline=False)
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.followup.send("Có lỗi khi xử lý yêu cầu của bạn. Vui lòng thử lại sau!", ephemeral=True)
class SelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Select())
@bot.tree.command(name="banggia", description="Xem bảng giá!")
async def banggia(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    embedtitle = reloadconfig()['embedtitle']
    embed = discord.Embed(title=embedtitle, description=f"Chọn ở dưới xem chi tiết sản phẩm", color=0xd4b4f4)
    await interaction.followup.send(embed=embed, view=SelectView(), ephemeral=True)
    
    
    
    
@bot.command(name="!thanhtoan")
@commands.has_role("Legit Seller")
async def log(ctx,khach: int,hang: str,* ,args):
    await ctx.message.delete()
    await bot.get_channel(logchannel).send(embed=discord.Embed(color=discord.Color.from_rgb(135, 206, 235), title='Bank',description=f'**User: <@{khach}>\nGiá tiền: {args}.OOO VND\nHàng: {hang}\n<t:{math.floor(time.time())}:R>**'))
    
    
@bot.command()
@commands.has_role("bot")
async def ltcprice(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/litecoin'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        await ctx.send(f"**THE CURRENT PRICE OF LITECOIN IN MARKET IS :** `{price:.2f}`")
    else:
        await ctx.send("**FAILED TO FETCH**")
        
        
        
@bot.command()
@commands.has_role("bot")
async def usdt(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/tether'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['vnd']
        await ctx.send(f"**THE CURRENT PRICE OF USDT IN MARKET IS :** `{price:.2f}`")
    else:
        await ctx.send("**FAILED TO FETCH**")
        
        
@bot.command()
@commands.has_role("Legit Seller")
async def mybal(ctx):
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/ltc1qhkmt57nawemc5s6aae8frjpvv7caepgckptzdq/balance')

    if response.status_code == 200:
        data = response.json()
        balance = data['balance'] / 10**8
        total_balance = data['total_received'] / 10**8
        unconfirmed_balance = data['unconfirmed_balance'] / 10**8
    else:
        await ctx.send("- `FAILED`")
        return

    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')

    if cg_response.status_code == 200:
        usd_price = cg_response.json()['litecoin']['usd']
    else:
        await ctx.send("- `FAILED`")
        return

    usd_balance = balance * usd_price
    usd_total_balance = total_balance * usd_price
    usd_unconfirmed_balance = unconfirmed_balance * usd_price

    message = f"**CURRENT LTC BALANCE** : `{usd_balance:.2f}$ USD`\n"
    message += f"**TOTAL LTC RECEIVED** : `{usd_total_balance:.2f}$ USD`\n"
    message += f"**UNCONFIRMED LTC** : `{usd_unconfirmed_balance:.2f}$ USD`\n\n"

    await ctx.send(message)

############################################################################################################################################
class ttcuakhach(discord.ui.Modal, title=reloadconfig()['embedtitle']):
    def __init__(self):
        super().__init__(title=reloadconfig()['embedtitle'])
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.long,
            label="Email hoặc Sdt",
            required=True,
            placeholder="Điền đi"
        ))
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.long,
            label="Mật khẩu",
            required=True,
            placeholder="Điền đi"
        ))
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.long,
            label="Mã backup (Nếu có)",
            required=False,
            placeholder="Điền 3 mã không xuống dòng và nếu không có thì đừng điền gì cả"
        ))
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        config = reloadconfig()
        user = interaction.user
        tt1 = self.children[0].value
        tt2 = self.children[1].value
        tt3 = self.children[2].value
        if tt3:
        	await bot.get_channel(1311663512019537971).send(embed=discord.Embed(color=discord.Color.from_rgb(135, 206, 235), title='Thông tin khách',description=f'**User: {user.name} - <@{user.id}>\n\nEmail / Sdt: ```{tt1}```\nPass: ```{tt2}```\nMã: ```{tt3}```\n<t:{math.floor(time.time())}:f>**'))
        else:
            await bot.get_channel(1311663512019537971).send(embed=discord.Embed(color=discord.Color.from_rgb(135, 206, 235), title='Thông tin khách',description=f'**User: {user.name} - <@{user.id}>\n\nEmail / Sdt: ```{tt1}```\nPass: ```{tt2}```\n<t:{math.floor(time.time())}:f>**'))
            
class billmb(discord.ui.Modal, title="Tạo bill"):
    def __init__(self):
        super().__init__(title=reloadconfig()['embedtitle'])
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.long,
            label="Tên hàng",
            required=True,
            placeholder="Mua gì ghi đó"
        ))
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.long,
            label="Giá",
            required=True,
            placeholder="VD: 85"
        ))
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.long,
            label="ID Khách",
            required=True,
            placeholder="Điền id"
        ))
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.long,
            label="Ghi chú",
            required=False,
            placeholder="Có thể ghi số tháng khách mua vào đây"
        ))
        
        
        
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        config = reloadconfig()
        user = interaction.user
        tt1 = self.children[0].value
        tt2 = self.children[1].value
        idkhach = self.children[2].value
        note = self.children[3].value
        price = f"{int(tt2):,}".replace(",", ".")
        tong = f"{int(price)*1000:,}".replace(",", ".")
        acceptcode = paymentcode()
        transfermessage = config["transfermessage"].replace(f"%random%", acceptcode)
        embed = discord.Embed(title="",description="",color=discord.Color.from_rgb(247, 57, 24))
        embed.set_image(url=f"https://img.vietqr.io/image/mb-560799999-compact.png?amount={int(price)*1000}&addInfo={transfermessage}&accountName=THACH%20GIA%20BAO")
        await interaction.followup.send("# Dùng lệnh /thongtin để thêm thông tin acc nếu mua nitro nhoé\nCheck đúng chủ là THACH GIA BAO thì mới chuyển nha",embed=embed)
        if note:
            log_embed = discord.Embed(color=discord.Color.from_rgb(135, 206, 235), title='Chuyển khoản MB',description=f'**Người tạo: <@{user.id}>**\n**Khách hàng: <@{idkhach}>**\n**Hazel’s Merchandise 💲 || Limited Stock**\n**Giá tiền: {tong} VND**\n**Hàng: {tt1}**\n**Nội dung bank: {transfermessage}**\n**Ghi chú**: ```{note}```\n**<t:{math.floor(time.time())}:f>**')
        else:
            log_embed = discord.Embed(color=discord.Color.from_rgb(135, 206, 235), title='Chuyển khoản MB',description=f'**Người tạo: <@{user.id}>**\n**Khách hàng: <@{idkhach}>**\n**Hazel’s Merchandise 💲 || Limited Stock**\n**Giá tiền: {tong} VND**\n**Hàng: {tt1}**\n**Nội dung bank: {transfermessage}**\n**<t:{math.floor(time.time())}:f>**')
        await bot.get_channel(logchannel).send(embed = log_embed)
    
    
@bot.tree.command(name="thongtin", description="Điền thông tin để mua nitro")
async def thongtin(interaction : discord.Interaction):
    await interaction.response.send_modal(ttcuakhach())
    await interaction.followup.send("Đã cập nhật thông tin của bạn lên server",ephemeral=True)
    
@bot.tree.command(name="taobill", description="Tạo bill")
async def taobill(interaction: discord.Interaction):
    try:
        user = interaction.user
        role = discord.utils.get(bot.get_guild(1295202254759919687).roles, id=1295203177792016437)
        member_has_role = []
        for guild in bot.guilds:
            member = guild.get_member(user.id)
            if member and role in member.roles:
                member_has_role.append(guild.name)
    except Exception as e:
        print(e)
        await interaction.followup.send("Có lỗi khi xử lý yêu cầu của bạn. Vui lòng thử lại sau!", ephemeral=True)
        return

    if not member_has_role:
        await interaction.followup.send("Bạn không có quyền sử dụng lệnh!", ephemeral=True)
        return
    await interaction.response.send_modal(billmb())

    
    
class tuthanhtoan(discord.ui.Modal, title="Lên đơn order nitro đợi chủ shop on là done"):
    def __init__(self):
        super().__init__(title=reloadconfig()['embedtitle'])
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.long,
            label="Email hoặc Sdt",
            required=True,
            placeholder="Nhập đi"
        ))
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.long,
            label="Mật khẩu",
            required=True,
            placeholder="Nhập đi nè"
        ))
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.long,
            label="Giá",
            required=True,
            placeholder="Đừng có thêm chữ k mà phải ghi như vầy: 85, mua trên 2 cái thì 80k 1 tháng nha còn 1 năm thì 820k"
        ))
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.long,
            label="Mã backup 8 số (Nếu có thì ghi)",
            required=False,
            placeholder="Ghi theo hàng ngang và ghi 3 mã"
        ))
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.long,
            label="Ghi chú",
            required=False,
            placeholder="Mua nhiêu tháng ghi vô để biết"
        ))
        
        
        
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        config = reloadconfig()
        user = interaction.user
        taikhoan = self.children[0].value
        matkhau = self.children[1].value
        gia = self.children[2].value
        backup = self.children[3].value
        note = self.children[4].value
        acceptcode = paymentcode()
        transfermessage = config["transfermessage"].replace(f"%random%", acceptcode)
        price = f"{int(gia):,}".replace(",", ".")
        tong = f"{int(price)*1000:,}".replace(",", ".")
        embed = discord.Embed(title="",description="",color=discord.Color.from_rgb(247, 57, 24))
        embed.set_image(url=f"https://img.vietqr.io/image/mb-560799999-compact.png?amount={int(price)*1000}&addInfo={transfermessage}&accountName=THACH%20GIA%20BAO")
        await interaction.followup.send("Check đúng chủ là THACH GIA BAO thì mới chuyển nha\nBấm nút dưới xong nhớ đọc nha",embed=embed, ephemeral=True)
        if note:
            log_embed = discord.Embed(color=discord.Color.from_rgb(135, 206, 235), title='Chuyển khoản MB (Khách dùng lệnh /order)',description=f'**Khách: <@{user.id}>**\n**Hazel’s Merchandise 💲 || Limited Stock**\n**Giá tiền: {tong} VND**\n**Nội dung bank: {transfermessage}**\n**Ghi chú**: ```{note}```\n**<t:{math.floor(time.time())}:f>**')
        else:
            log_embed = discord.Embed(color=discord.Color.from_rgb(135, 206, 235), title='Chuyển khoản MB (Khách dùng lệnh /order)',description=f'**Khách: <@{user.id}>**\n**Hazel’s Merchandise 💲 || Limited Stock**\n**Giá tiền: {tong} VND**\n**Nội dung bank: {transfermessage}**\n**<t:{math.floor(time.time())}:f>**')
        await bot.get_channel(logchannel).send(embed = log_embed)
        if backup:
            await bot.get_channel(ttchannel).send(embed=discord.Embed(color=discord.Color.from_rgb(135, 206, 235), title='Thông tin khách dùng lệnh /order',description=f'**User: {user.name} - <@{user.id}>\n\nEmail / Sdt: ```{taikhoan}```\nPass: ```{matkhau}```\nMã: ```{backup}```\nMã giao dịch (Check đúng mới tiếp tục làm):```{transfermessage}```\n<t:{math.floor(time.time())}:f>**'))
        else:
            await bot.get_channel(ttchannel).send(embed=discord.Embed(color=discord.Color.from_rgb(135, 206, 235), title='Thông tin khách dùng lệnh /order',description=f'**User: {user.name} - <@{user.id}>\n\nEmail / Sdt: ```{taikhoan}```\nPass: ```{matkhau}```\nMã giao dịch (Check đúng mới tiếp tục làm):```{transfermessage}```\n<t:{math.floor(time.time())}:f>**'))    
    

@bot.tree.command(name="order", description="Tự lên đơn dành cho nitro")
async def ccccccc(interaction: discord.Interaction):
    await interaction.response.send_modal(tuthanhtoan())
    await interaction.followup.send("Cảm ơn bạn đã giúp tui nhẹ bớt việc huhu",ephemeral=True)
    
class concacbutton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Order", style=discord.ButtonStyle.green, emoji="🩷")
    async def button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(tuthanhtoan())


class confirmbutton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Bấm vào nếu đã chuyển khoản", style=discord.ButtonStyle.green,emoji="✅")
    async def button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Cảm ơn bạn đã ủng hộ tớ ạaaa!!! Nếu như đây là lần đầu tiên mua nitro login thì bạn nhớ để ý thông báo nhé tớ sẽ cần bạn check gmail để xác nhận đó ạ",ephemeral=True)


    
    
@bot.command(name="!order")
async def order(ctx: commands.Context):
    await ctx.message.delete()
    if not ctx.author.guild_permissions.manage_messages:
        embed = discord.Embed(title=reloadconfig()['embedtitle'], description="Bạn không có quyền sử dụng lệnh!", color=0xFF0000)
        await ctx.send(embed=embed)
        return
    embed = discord.Embed(title=reloadconfig()['embedtitle'], description="— Dành cho ai ngại mà giàu\n**BẤM NÚT DƯỚI ĐÂY ĐỂ ORDER NITRO**", color=0xd4b4f4)
    await ctx.send(embed=embed, view=concacbutton())
    

bot.run(config['tokenstore'])