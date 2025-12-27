import io
import json
import time
import math
import random
import string
import psutil
import shutil
import asyncio
import qrcode
import discord
import requests
import platform
import threading
import urllib.parse
from ping3 import ping
from io import BytesIO
from bs4 import BeautifulSoup
from discord import app_commands
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from discord import Button, ButtonStyle, InteractionType
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import requests
import threading
import time
import tls_client
import json
from datetime import datetime, timedelta

#############################
import re
import os
import sys
import aiohttp
import httpx
import typing
#############################

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.tree.sync()
    change_activity.start()

@tasks.loop(seconds=15)
async def change_activity():
    activities = [
        discord.Activity(type=discord.ActivityType.watching, name="/muahang | Hazel Store"),
        discord.Activity(type=discord.ActivityType.watching, name="/banggia | Hazel Store"),
        discord.Activity(type=discord.ActivityType.watching, name="/masanpham | Hazel Store"),
    ]
    
    for activity in activities:
        await bot.change_presence(activity=activity)
        await asyncio.sleep(5)


def reloadconfig():
    with open('config.json', 'r', encoding='utf-8-sig') as file:
        data = json.load(file)
    return data

worktime = time.time()
logchannel = reloadconfig()['logchannel']
role_id = reloadconfig()['role_id']

def paymentcode():
    characters = string.ascii_uppercase + string.digits
    payment_code = ''.join(random.choices(characters, k=6))
    return payment_code

def logmessage(message):
    embed = discord.Embed(
    color=discord.Color.from_rgb(247, 57, 24),
    description=f"<t:{math.floor(time.time())}:R>",
    ).set_author(name=message)
    return embed

class payment(discord.ui.Modal, title=reloadconfig()['embedtitle']):
    def __init__(self):
        super().__init__(title=reloadconfig()['embedtitle'])
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.short,
            label="Mã sản phẩm",
            required=True,
            placeholder="Sử dụng lệnh /masanpham để xem mã sản phẩm"
        ))
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.short,
            label="Số lượng",
            max_length=3,
            min_length=1,
            required=True,
            placeholder="Nhập số lượng"
        ))
        self.add_item(discord.ui.TextInput(
            style=discord.TextStyle.long,
            label="Ghi chú",
            required=True,
            placeholder="Ghi cái đéo gì cũng được"
        ))

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        config = reloadconfig()
        user = interaction.user
        codevalue = self.children[0].value
        soluongvalue = self.children[1].value
        description = self.children[2].value

        try:
            soluongvalue = int(soluongvalue)
        except Exception as e:
            await interaction.followup.send("Số lượng không hợp lệ vui lòng thử lại!", ephemeral=True)
            await bot.get_channel(logchannel).send(embed=logmessage(f'User: {user.name} ({user.id})\nSố lượng không hợp lệ!\nInput: {soluongvalue}'))    
            return

        if int(soluongvalue) == 0:
            await interaction.followup.send("Số lượng tối thiểu là 1!", ephemeral=True)
            return
        try:
            stocks = config["stocks"]
            
            if codevalue not in stocks:
                await interaction.followup.send("Mã mặt hàng không tồn tại!", ephemeral=True)
                await bot.get_channel(logchannel).send(embed=logmessage(f'User: {user.name} ({user.id})\nMã mặt hàng không tồn tại!\nInput: {codevalue}'))  
            elif int(soluongvalue) > stocks[codevalue]["limit"]:
                await interaction.followup.send(f"Bạn chỉ có thể mua tối đa {stocks[codevalue]['limit']} sản phẩm!", ephemeral=True)
                await bot.get_channel(logchannel).send(embed=logmessage(f'User: {user.name} ({user.id})\nMua quá số lượng cho phép!\nInput: {soluongvalue}'))
            else:
                if stocks[codevalue]["deliverytype"] == 2:
                    amountstock = 0
                else:
                    amountstock = len(open(stocks[codevalue]['file'], "r").readlines())
                if int(soluongvalue) > amountstock and stocks[codevalue]["deliverytype"] != 2:      
                    await interaction.followup.send("Số lượng yêu cầu lớn hơn số lượng sản phẩm có sẵn! (hết hàng)", ephemeral=True)
                    await bot.get_channel(logchannel).send(embed=logmessage(f'User: {user.name} ({user.id})\nSố lượng yêu cầu lớn hơn số lượng sản phẩm có sẵn!\nCode: {codevalue}\nInput: {soluongvalue}'))
                    return
                embedtitle = config['embedtitle']
                code = codevalue
                amount = soluongvalue
                deliverytype = stocks[code]["deliverytype"]
                name = stocks[code]["name"]
                price = stocks[code]["price"]
                if deliverytype == 1:
                    delivery = stocks[code]["file"]
                    with open(delivery, "r") as file:
                        lines = [line.strip() for line in file]
                    amount = min(int(amount), len(lines))
                    indices = random.sample(range(len(lines)), int(amount))
                    products = [lines[i] for i in indices]
                    remaining_lines = [line for i, line in enumerate(lines) if i not in indices]
                    with open(delivery, "w") as file:
                        if remaining_lines:
                            file.write("\n".join(remaining_lines) + "\n")
                        else:
                            file.write("")

                taoqr = config['taoqr']
                acceptcode = paymentcode()
                transfermessage = config["transfermessage"].replace(f"%random%", acceptcode)
                pricee = f"{int(price):,}".replace(",", ".")
                tong = f"{int(price)*int(amount):,}".replace(",", ".")
                embed = discord.Embed(title=embedtitle, description="", color=0x87CEEB)
                embed.add_field(name="Thông tin sản phẩm", value=f"Tên mặt hàng: {name}\nMã sản phẩm: {code}\nSố tiền: {pricee}đ/1\nSố lượng: {amount}", inline=False)
                embed.add_field(name=f"<:mb:1239064157991600190> {taoqr['nganhang']}", value=f"```{taoqr['sotaikhoan']}```", inline=False)
                embed.add_field(name=f"<:mb:1239064157991600190> Chủ Tài Khoản", value=f"```{taoqr['chutaikhoan']}```", inline=False)
                embed.add_field(name=f"💵 Số Tiền", value=f"```{tong}đ```", inline=False)
                embed.add_field(name=f"🏦 Nội Dung", value=f"```{transfermessage}```", inline=False)
                url = f"https://img.vietqr.io/image/mb-{taoqr['sotaikhoan']}-compact.png?amount={int(price)*int(amount)}&addInfo={urllib.parse.quote(transfermessage)}&accountName={urllib.parse.quote(taoqr['chutaikhoan'])}"
                embed.set_image(url=url)
                embed.set_footer(text="ⓘ Đơn hàng sẽ bị hủy sau 10p nếu không thanh toán!")
                await interaction.followup.send(embed=embed, ephemeral=True)
                await bot.get_channel(logchannel).send(embed=discord.Embed(color=discord.Color.from_rgb(135, 206, 235), title='Bank',description=f'**User: {user.name} ({user.id})\nCreated Purchase {name} - x{amount} - {transfermessage}\n<t:{math.floor(time.time())}:R>**'))

                notpaid = True
                timeout = time.time() + 10*60
                while notpaid and time.time() < timeout:
                    await asyncio.sleep(1)
                    response = requests.get('http://127.0.0.1:8888/mbapiserver')
                    if response.status_code == 200:
                        try:
                            lsgd = response.json()['transactionHistoryList']
                            if lsgd is not None:
                                for gd in lsgd:
                                    if transfermessage.lower() in gd['addDescription'].replace(" ", "").lower() and gd['creditAmount'] == str(int(price)*int(amount)):
                                        notpaid = False
                                        ticket = None
                                        embed = discord.Embed(title=embedtitle, description=f"**Mã sản phẩm: {code}**", color=0x00FF00)
                                        embed.add_field(name="Đơn hàng của bạn", value=f"```Tên mặt hàng: {name} - x{amount}```", inline=False)
                                        embed.add_field(name="Trạng thái", value=f"```Thanh toán thành công```", inline=False)
                                        log_embed = discord.Embed(color=discord.Color.from_rgb(0, 255, 0),title='Bank',description=f"**Người mua: {user.name} ({user.id})\Trạng thái: Đã thanh toán món {name} - x{amount} - {transfermessage}\n<t:{math.floor(time.time())}:R>**")
                                        guild = bot.get_guild(config['serverid'])
                                        if deliverytype == 1:
                                            for i, item in enumerate(products, start=1):
                                                embed.add_field(name=f"Sản phẩm {i}", value=f"```{item}```", inline=False)
                                                log_embed.add_field(name=f"Sản phẩm {i}", value=f"```{item}```", inline=False)
                                            await user.send(embed=embed)
                                        else:
                                            await user.send(embed=embed)
                                            category_id = config['delivery']['category']
                                            category = discord.utils.get(guild.categories, id=category_id)
                                            channelname = config['delivery']['channelname'].replace("%username%", user.name)
                                            overwrites = {
                                                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                                                user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True)
                                            }

                                            ticket = await guild.create_text_channel(name=channelname, category=category, overwrites=overwrites)

                                        if description:
                                            log_embed.add_field(name=f"Thông tin", value=f"```{description}```", inline=False)
                                        await asyncio.sleep(1)
                                        if ticket:
                                            embed = discord.Embed(title=embedtitle, description=f"— Cảm ơn bạn đã mua hàng!\n— Vui lòng đợi trong vòng 15 phút nhé, nếu hết 15 phút không ai trả lời thì bạn có thể xin hoàn tiền\nTên hàng: {name} - {amount} cái", color=0xd4b4f4)
                                            embed.set_image(url='https://cdn.discordapp.com/avatars/1251767575524806706/a_5792a01d18171b9765984811fbf2b6d3.gif?size=4096')
                                            await ticket.send("<@595870690498838558> / <@485646161261101066>",embed=embed)
                                            await user.send(f'Vào đây để nhận hàng: {ticket.mention}\nNếu gặp vấn đề vui lòng đề cập vấn để trong ticket!')
                                        await asyncio.sleep(1)
                                        await user.add_roles(discord.utils.get(guild.roles, id=role_id))
                                        await bot.get_channel(logchannel).send(embed=log_embed)
                        except: None
                    else:
                        print(f"Request failed with status code {response.status_code}")
                if notpaid and time.time() > timeout:
                    if deliverytype == 1:
                        with open(delivery, "a") as file:
                            file.write("\n".join(products) + "\n")
                    embed = discord.Embed(title=embedtitle, description=f"**Mã sản phẩm: {code}**", color=0xFF0000)
                    embed.add_field(name="Đơn hàng của bạn", value=f"```Tên mặt hàng: {name} - x{amount}```", inline=False)
                    embed.add_field(name="Trạng thái", value=f"```Quá hạn thanh toán!```", inline=False)
                    await user.send(embed=embed)  
                    await bot.get_channel(logchannel).send(embed=logmessage(f'User: {user.name} ({user.id})\nQuá hạn thanh toán!'))       
        except Exception as e:
            print(e)
            await interaction.followup.send(f"Lỗi: {e}!", ephemeral=True)
            await bot.get_channel(logchannel).send(embed=logmessage(f'{user} Lỗi: {e}!'))
            if deliverytype == 1 and products:
                with open(delivery, "a") as file:
                    file.write("\n".join(products) + "\n")

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.followup.send("Có lỗi khi xử lý yêu cầu của bạn. Vui lòng thử lại sau.", ephemeral=True)
        await bot.get_channel(logchannel).send(embed=logmessage(f'{interaction.user} encountered an error: {error}'))

class autobuybutton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Mua hàng", style=discord.ButtonStyle.green, emoji="🛒")
    async def button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(payment())

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
            embed.add_field(name="NICHO BOOST", value=f"> NICHO LOGIN — 1 THÁNG : **85.OOO VND**\n> NICHO LOGIN — 1 NĂM : **800.000 VND**", inline=False)
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


class baohanh(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='NICHO BOOST', emoji='a:NITRO:1255338967021260860', description='Chế độ bảo hành nitro boost hàng login'),
            discord.SelectOption(label='NICHO BASIC', emoji='a:basic:1255339140627693660', description='Chế độ bảo hành nitro basic hàng login'),
            discord.SelectOption(label='NICHO TRIAL', emoji='a:NITRO:1255338967021260860', description='Chế độ bảo hành nitro trial'),
        ]

        super().__init__(placeholder="Ấn ở đây để chọn!",max_values=1,min_values=1,options=options)
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        config = reloadconfig()
        if self.values[0] == 'NICHO BOOST': 
            embed = discord.Embed(title='NICHO', description=f"", color=0xd4b4f4)
            embed.add_field(name="NICHO BOOST", value=f"> NICHO LOGIN — 1 THÁNG : **85.OOO VND**\n> NICHO LOGIN — 1 NĂM : **800.000 VND**", inline=False)
            await interaction.followup.send(embed=embed, ephemeral=True)

        elif self.values[0] == 'NICHO BASIC':
            embed = discord.Embed(title='NICHO', description=f"", color=0xd4b4f4)
            embed.add_field(name="NICHO BASIC", value=f"> NICHO LOGIN — 1 THÁNG : **35.OOO VND**\n> NICHO LOGIN — 1 NĂM : **35O.OOO VND**", inline=False)
            await interaction.followup.send(embed=embed, ephemeral=True)

        elif self.values[0] == 'NICHO TRIAL':
            embed = discord.Embed(title='NICHO', description=f"", color=0xd4b4f4)
            embed.add_field(name="NICHO TRIAL", value=f"> NICHO TRIAL — 3 THÁNG : **50.OOO VND**\n> NITRO TRIAL — 1 THÁNG: **25.OOO VND**", inline=False)
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.followup.send("Có lỗi khi xử lý yêu cầu của bạn. Vui lòng thử lại sau!", ephemeral=True)



class SelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Select())


class Baohanh(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(baohanh())

@bot.command()
async def autobuy(ctx: commands.Context):
    await ctx.message.delete()
    if not ctx.author.guild_permissions.manage_messages:
        embed = discord.Embed(title=reloadconfig()['embedtitle'], description="Bạn không có quyền sử dụng lệnh!", color=0xFF0000)
        await ctx.send(embed=embed)
        return
    embed = discord.Embed(title=reloadconfig()['embedtitle'], description="— Sử dụng lệnh `/banggia` để xem thông tin sản phẩm\n— Sử dụng lệnh `/masanpham` để xem mã sản phẩm\n**BẤM NÚT DƯỚI ĐÂY ĐỂ MUA HÀNG**", color=0xd4b4f4)
    await ctx.send(embed=embed, view=autobuybutton())

@bot.command()
@commands.has_permissions(administrator=True)
async def close(ctx: commands.Context):
    await ctx.message.delete()
    config=reloadconfig()
    if ctx.channel.category_id != config["delivery"]["category"]:
        await ctx.send(f'Bạn không thể sử dụng lệnh ở đây!')
        return
    guild = bot.get_guild(config['serverid'])
    original_name = ctx.channel.name
    closed_category = guild.get_channel(config["closedticket"])
    await ctx.channel.edit(
        category=closed_category,
        name=f"closed-{original_name}",
        sync_permissions=True
    )
    await ctx.send(f'Đóng ticket của khách {original_name}, người đóng {ctx.author.mention}!')
    await ctx.send(f'Cảm ơn bạn đã mua hàng nếu có gì cần hỏi thì đừng ngần ngại trao đổi riêng với mình nhé')


@bot.command()
async def testaddrole(ctx: commands.Context):
    user = ctx.author
    config = reloadconfig()
    guild = bot.get_guild(config['serverid'])
    await user.add_roles(discord.utils.get(guild.roles, id=role_id))

@bot.tree.command(name="muahang", description="Mua hàng!")
async def muahang(interaction : discord.Interaction):
    await interaction.response.send_modal(payment())

@bot.tree.command(name="banggia", description="Xem bảng giá!")
async def banggia(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    try:
        user = interaction.user
        role = discord.utils.get(bot.get_guild(1220320347316948992).roles, id=1221800767288250449)
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
    embedtitle = reloadconfig()['embedtitle']
    embed = discord.Embed(title=embedtitle, description=f"Chọn ở dưới xem chi tiết sản phẩm", color=0xd4b4f4)
    await interaction.followup.send(embed=embed, view=SelectView(), ephemeral=True)

@bot.tree.command(name="baohanh", description="Xem chế độ bảo hành")
async def baohanhh(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    embedtitle = reloadconfig()['embedtitle']
    embed = discord.Embed(title=embedtitle, description=f"Chọn loại sản phẩm bạn mua để xem chế độ bảo hành của sản phẩm", color=0xd4b4f4)
    await interaction.followup.send(embed=embed, view=SelectView(), ephemeral=True)

@bot.tree.command(name="masanpham", description="Xem mã sản phẩm!")
async def masanpham(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    embedtitle = reloadconfig()['embedtitle']
    embed = discord.Embed(title=f"{embedtitle}", description="", color=0xd4b4f4)
    embed.add_field(name="NICHO BOOST", value=f"nitroboost1thang\nnitroboost1nam", inline=False)
    embed.add_field(name="NICHO BASIC", value=f"nitrobasic1thang\nnitrobasic1nam", inline=False)
    embed.add_field(name="NICHO TRIAL", value=f"nitrotrial1m\nnitrotrial3m", inline=False)

    await interaction.followup.send(embed=embed, ephemeral=True)

@bot.tree.command(name="dashboard", description="Xem thông tin!")
async def dashboard(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    try:
        user = interaction.user
        role = discord.utils.get(bot.get_guild(1220320347316948992).roles, id=1221800767288250449)
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

    embedtitle = reloadconfig()['embedtitle']

    elapsed_time_seconds = time.time() - worktime
    if elapsed_time_seconds >= 3600:
        elapsed_time = elapsed_time_seconds / 3600
        unit = "hours"
    elif elapsed_time_seconds >= 60:
        elapsed_time = elapsed_time_seconds / 60
        unit = "minutes"
    else:
        elapsed_time = elapsed_time_seconds
        unit = "seconds"
    
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    total_ram = memory_info.total / (1024 ** 3)
    used_ram = memory_info.used / (1024 ** 3)
    
    total_disk, used_disk, free_disk = shutil.disk_usage("/")
    total_disk_gb = total_disk / (1024 ** 3)
    used_disk_gb = used_disk / (1024 ** 3)
    
    system = platform.system()
    release = platform.release()
    uptime_seconds = time.time() - psutil.boot_time()
    if uptime_seconds >= 3600:
        uptime = uptime_seconds / 3600
        uptime_unit = "hours"
    elif uptime_seconds >= 60:
        uptime = uptime_seconds / 60
        uptime_unit = "minutes"
    else:
        uptime = uptime_seconds
        uptime_unit = "seconds"
    
    ping_ms = ping('discord.com', timeout=2) * 1000

    embed = discord.Embed(
        title=embedtitle, 
        description=(
            f"CPU Usage: {cpu_usage:.2f}%\n"
            f"Used RAM: {used_ram:.2f} GB / Total RAM: {total_ram:.2f} GB\n"
            f"Used Disk: {used_disk_gb:.2f} GB / Total Disk: {total_disk_gb:.2f} GB\n"
            f"OS: {system} {release}\n"
            f"Uptime: {uptime:.2f} {uptime_unit}\n"
            f"Ping: {ping_ms:.2f} ms\n"
            f"Worktime: {elapsed_time:.2f} {unit}"
        ), 
        color=0xFF0000
    )
    await interaction.followup.send(embed=embed, ephemeral=True)




##################################################################################################################################################################################

token = reloadconfig()['token']
bot.run(token)