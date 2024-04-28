import discord
from discord.ext import commands
from discord import app_commands
import Token
import numpy as np
import typing
import asyncio
from difflib import *

from keep_alive import *

keep_alive()

bot = commands.Bot(command_prefix="?", intents= discord.Intents.all())

@bot.event
async def on_ready():
    print("Im jbc bot")
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)

@bot.tree.command(name="addstock", description = "Add stock for an item")
@app_commands.describe(item = "Name of item", amount = "Amount of stock to add")
async def addstock(interaction : discord.Interaction, item : str, amount : str):

    stock = np.load("stock.npy", allow_pickle=True).item()
    admins = np.load("admin.npy", allow_pickle=True).item()
    if int(interaction.user.id) not in list(admins.keys()):
        await interaction.response.send_message("You are not a bot admin", ephemeral=True)
        return
    
    if item in list(stock.keys()):
        stock[item] += int(amount)
        np.save('stock.npy',stock)

        embed=discord.Embed(description=f'Changed the stock of {item} to {stock[item]} by adding {amount}', color=0x00ff00)
        await interaction.response.send_message(embed=embed)

        user = await bot.fetch_user(745583659389681675)

        await user.send(file = discord.File('stock.npy'))

        m = ''
        keys = list(stock.keys())
        for key in keys:
            if key in ["M12", "RTX", "Yellow5"]:
                m += f'\n**{key} :** {stock[key]}\n'
            else:
                m += f'\n**{key} :** {stock[key]}'
        embed=discord.Embed(title="**New stock:**",description=m, color=0x00ff00)

        user = await bot.fetch_user(442959580570451969)
        await user.send(embed=embed)

    else:
        embed=discord.Embed(description=f'No item named {item}', color=0xff0000) 
        await interaction.response.send_message(embed=embed)
    

@addstock.autocomplete('item')
async def addstock_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> typing.List[app_commands.Choice[str]]:
    stock = np.load("stock.npy", allow_pickle=True).item()
    fruits = list(stock.keys())
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ]

@bot.tree.command(name="removestock", description = "Remove stock for an item")
@app_commands.describe(item = "Name of item", amount = "Amount of stock to remove")
async def removestock(interaction : discord.Interaction, item : str, amount : str):

    stock = np.load("stock.npy", allow_pickle=True).item()
    admins = np.load("admin.npy", allow_pickle=True).item()
    if int(interaction.user.id) not in list(admins.keys()):
        await interaction.response.send_message("You are not a bot admin", ephemeral=True)
        return

    if item in list(stock.keys()):
        if int(amount) <= stock[item]:
            stock[item] -= int(amount)
            np.save('stock.npy',stock)

            embed=discord.Embed(description=f'Changed the stock of {item} to {stock[item]} by removing {amount}', color=0x00ff00)
            await interaction.response.send_message(embed=embed)

            user = await bot.fetch_user(745583659389681675)

            await user.send(file = discord.File('stock.npy'))

            m = ''
            keys = list(stock.keys())
            for key in keys:
                if key in ["M12", "RTX", "Yellow5"]:
                    m += f'\n**{key} :** {stock[key]}\n'
                else:
                    m += f'\n**{key} :** {stock[key]}'
            embed=discord.Embed(title="**New stock:**",description=m, color=0x00ff00)

            user = await bot.fetch_user(442959580570451969)
            await user.send(embed=embed)
        else:
            embed=discord.Embed(description=f'Current stock of {item} is only {stock[item]}', color=0xff0000) 
            await interaction.response.send_message(embed=embed)
    else:
        embed=discord.Embed(description=f'No item named {item}', color=0xff0000) 
        await interaction.response.send_message(embed=embed)

@removestock.autocomplete('item')
async def removestock_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> typing.List[app_commands.Choice[str]]:
    stock = np.load("stock.npy", allow_pickle=True).item()
    fruits = list(stock.keys())
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ]

@bot.tree.command(name="additem", description = "Add an item")
@app_commands.describe(item = "Name of item", amount = "Amount of stock to add")
async def additem(interaction : discord.Interaction, item : str, amount : str):

    stock = np.load("stock.npy", allow_pickle=True).item()
    admins = np.load("admin.npy", allow_pickle=True).item()
    if int(interaction.user.id) not in list(admins.keys()):
        await interaction.response.send_message("You are not a bot admin", ephemeral=True)
        return
    
    if item not in list(stock.keys()):
        stock[item] = int(amount)
        np.save('stock.npy',stock)
        embed=discord.Embed(description=f'Added {item} with stock {stock[item]}', color=0x00ff00)
        await interaction.response.send_message(embed=embed)

    else:
        embed=discord.Embed(description=f'Already an item named {item}', color=0xff0000) 
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="removeitem", description = "Remove an item")
@app_commands.describe(item = "Name of item")
async def removeitem(interaction : discord.Interaction, item : str):

    stock = np.load("stock.npy", allow_pickle=True).item()
    admins = np.load("admin.npy", allow_pickle=True).item()
    if int(interaction.user.id) not in list(admins.keys()):
        await interaction.response.send_message("You are not a bot admin", ephemeral=True)
        return
    
    if item in list(stock.keys()):
        del stock[item]
        np.save('stock.npy',stock)
        embed=discord.Embed(description=f'Deleted {item}', color=0x00ff00)
        await interaction.response.send_message(embed=embed)

    else:
        embed=discord.Embed(description=f'No item named {item}', color=0xff0000) 
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="addadmin", description = "Add admins to change stock")
@app_commands.describe(user_id = "ID of user to add as admin")
async def addadmin(interaction : discord.Interaction, user_id : str):
    dev_id = ['745583659389681675', '442959580570451969']
    if str(interaction.user.id) not in dev_id:
        await interaction.response.send_message("This command is only for owner", ephemeral=True)
        return
    admins = np.load("admin.npy", allow_pickle=True).item()
    if int(user_id) in list(admins.keys()):
        embed=discord.Embed(title="**Error:**",description="User is already an admin", color=0xff0000)
        await interaction.response.send_message(embed=embed)
    else:
        try:
            admins[int(user_id)] = 1
            user = await bot.fetch_user(int(user_id))
            np.save("admin.npy", admins)

            embed=discord.Embed(description=f"Made {user} an admin", color=0x00ff00)
            await interaction.response.send_message(embed=embed)

            user = await bot.fetch_user(745583659389681675)

            await user.send(file = discord.File('admin.npy'))
        except:
            embed=discord.Embed(title="**Error:**",description="No user with that ID", color=0xff0000)
            await interaction.response.send_message(embed=embed)
    
@bot.tree.command(name="removeadmin", description = "Remove admins to change stock")
@app_commands.describe(user_id = "ID of user to remove as admin")
async def addadmin(interaction : discord.Interaction, user_id : str):
    dev_id = ['745583659389681675', '442959580570451969']
    if str(interaction.user.id) not in dev_id:
        await interaction.response.send_message("This command is only for owner", ephemeral=True)
        return
    admins = np.load("admin.npy", allow_pickle=True).item()
    if int(user_id) not in list(admins.keys()):
        embed=discord.Embed(title="**Error:**",description="User is already not an admin", color=0xff0000)
        await interaction.response.send_message(embed=embed)
    else:
        try:
            del admins[int(user_id)]
            user = await bot.fetch_user(int(user_id))
            np.save("admin.npy", admins)

            embed=discord.Embed(description=f"Removed {user} as an admin", color=0x00ff00)
            await interaction.response.send_message(embed=embed)

            user = await bot.fetch_user(745583659389681675)

            await user.send(file = discord.File('admin.npy'))
        except:
            embed=discord.Embed(title="**Error:**",description="No user with that ID", color=0xff0000)
            await interaction.response.send_message(embed=embed)

@bot.tree.command(name="addsupport", description = "Add support to view stock")
@app_commands.describe(user_id = "ID of user to add as support")
async def addsupport(interaction : discord.Interaction, user_id : str):
    dev_id = ['745583659389681675', '442959580570451969']
    if str(interaction.user.id) not in dev_id:
        await interaction.response.send_message("This command is only for owner", ephemeral=True)
        return
    support = np.load("support.npy", allow_pickle=True).item()
    if int(user_id) in support:
        embed=discord.Embed(title="**Error:**",description="User is already in support", color=0xff0000)
        await interaction.response.send_message(embed=embed)
    else:
        try:
            support[int(user_id)] = 1
            user = await bot.fetch_user(int(user_id))
            np.save("support.npy", support)

            embed=discord.Embed(description=f"Added {user} to support", color=0x00ff00)
            await interaction.response.send_message(embed=embed)

            user = await bot.fetch_user(745583659389681675)

            await user.send(file = discord.File('support.npy'))
        except:
            embed=discord.Embed(title="**Error:**",description="No user with that ID", color=0xff0000)
            await interaction.response.send_message(embed=embed)


@bot.tree.command(name="removesupport", description = "Remove support to view stock")
@app_commands.describe(user_id = "ID of user to remove as support")
async def addsupport(interaction : discord.Interaction, user_id : str):
    dev_id = ['745583659389681675', '442959580570451969']
    if str(interaction.user.id) not in dev_id:
        await interaction.response.send_message("This command is only for owner", ephemeral=True)
        return
    support = np.load("support.npy", allow_pickle=True).item()
    if int(user_id) not in support:
        embed=discord.Embed(title="**Error:**",description="User is already not in support", color=0xff0000)
        await interaction.response.send_message(embed=embed)
    else:
        try:
            del support[int(user_id)]
            user = await bot.fetch_user(int(user_id))
            np.save("support.npy", support)

            embed=discord.Embed(description=f"Removed {user} from support", color=0x00ff00)
            await interaction.response.send_message(embed=embed)

            user = await bot.fetch_user(745583659389681675)

            await user.send(file = discord.File('support.npy'))
        except:
            embed=discord.Embed(title="**Error:**",description="No user with that ID", color=0xff0000)
            await interaction.response.send_message(embed=embed)


@bot.tree.command(name="stock", description = "View stock of an item")
@app_commands.describe(item = "Item to view stock of")
async def stock(interaction : discord.Interaction, item : typing.Optional[str]):
    support = np.load("support.npy", allow_pickle=True).item()
    admin = np.load("admin.npy", allow_pickle=True).item()
    stock = np.load("stock.npy", allow_pickle=True).item()

    if int(interaction.user.id) not in list(support.keys()):
        if int(interaction.user.id) not in list(admin.keys()):
            await interaction.response.send_message("You do not have permissions to do this", ephemeral=True)
            return
    if item != None:
        if item in list(stock.keys()):
            m = f'\n**{item} :** {stock[item]}'
        else:
            embed=discord.Embed(title="**Error:**",description=f"No item named {item}", color=0xff0000)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
    else:
        m = ''
        keys = list(stock.keys())
        for key in keys:
            if key in ["M12", "RTX", "Yellow5"]:
                m += f'\n**{key} :** {stock[key]}\n'
            else:
                m += f'\n**{key} :** {stock[key]}'
    embed=discord.Embed(title="**Available stock:**",description=m, color=0x00ff00)
    await interaction.response.send_message(embed=embed, ephemeral=True)
        


@stock.autocomplete('item')
async def stock_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> typing.List[app_commands.Choice[str]]:
    stock = np.load("stock.npy", allow_pickle=True).item()
    fruits = list(stock.keys())
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ]

@bot.tree.command(name="exchange", description = "View exchange rate")
async def exchange(interaction : discord.Interaction):

    support = np.load("support.npy", allow_pickle=True).item()
    admin = np.load("admin.npy", allow_pickle=True).item()

    if int(interaction.user.id) not in list(support.keys()):
        if int(interaction.user.id) not in list(admin.keys()):
            await interaction.response.send_message("You do not have permissions to do this", ephemeral=True)
            return

    embed=discord.Embed(title="**Exchange rate:**",description="1 USD = 0.79 gpb = 0.93 Euro", color=0x00ff00)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="calculate", description = "Calculate price in different currency")
@app_commands.describe(price = "Input price in USD", second_currency = "Currency to convert into")
async def calculate(interaction : discord.Interaction, price : str, second_currency : typing.Literal['gpb','euro']):
    support = np.load("support.npy", allow_pickle=True).item()
    admin = np.load("admin.npy", allow_pickle=True).item()

    if int(interaction.user.id) not in list(support.keys()):
        if int(interaction.user.id) not in list(admin.keys()):
            await interaction.response.send_message("You do not have permissions to do this", ephemeral=True)
            return

    price = float(price)
    if second_currency == "gpb":
        price = price * 0.79
    else:
        price = price * 0.93
    embed=discord.Embed(description=f"Price in {second_currency} = {price}", color=0x00ff00)
    await interaction.response.send_message(embed=embed)

bot.run(Token.Token)