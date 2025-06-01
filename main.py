import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from dog.dog_fact import get_dog_fact
from dog.dog_photo import get_dog_photo
from game.hangman import start_hangman, guess_hangman
from game.tic_tac_toe import start_tic_tac_toe, play_tic_tac_toe

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
member_role = 'Member'


### EVENTS ###

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_member_join(member):
    await member.send(f'Welcome to the server {member.name}! Type !command_list for a list of commands.')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "marco!" in message.content.lower():
        await message.channel.send('Polo!')

    await bot.process_commands(message)


### COMMANDS ###

@bot.command()
async def command_list(ctx):
    await ctx.send(
        '''List of commands:
        1) !ping -> Pings the bot.
        2) !hello -> Says hello.
        3) !assign -> Assigns the Member role.
        4) !unassign -> Removes the Member role.
        5) !secret -> Secret command for the Member role.
        6) !dog_fact -> Returns a random dog fact.
        7) !dog_photo -> Returns a random dog photo.
        8) !tic_tac_toe_start <X|O> -> Starts a new game of Tic Tac Toe. Select X or O as your marker.
        9) !tic_tac_toe_play <row> <column> -> Places a mark at the specified row and column.
        10) !hangman_start -> Starts a new game of Hangman.
        11) !hangman_guess <letter|word> -> To guess a letter or the entire word.'''
    )


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.mention}!')


@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=member_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f'{ctx.author.mention} has been assigned the Member role!')
    else:
        await ctx.send('Role does not exist!')


@bot.command()
async def unassign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=member_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f'{ctx.author.mention} has the Member role removed!')


@bot.command()
@commands.has_role(member_role)
async def secret(ctx):
    await ctx.send('Welcome to the club!')


@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f'{ctx.author.mention}, you do not have permission to use this command!')


@bot.command()
async def dog_fact(ctx):
    fact = get_dog_fact()
    await ctx.send(fact)


@bot.command()
async def dog_photo(ctx):
    photo = get_dog_photo()
    await ctx.send(photo)


@bot.command()
async def tic_tac_toe_start(ctx, player_mark):
    game_event = start_tic_tac_toe(ctx.author.id, player_mark)
    await display_game_event(ctx, game_event)


@tic_tac_toe_start.error
async def tic_tac_toe_start_error(ctx, _):
    await ctx.send(
        'Please add X or O to the command to specify your marker. Example: !tic_tac_toe_start X or !tic_tac_toe_start O.')


@bot.command()
async def tic_tac_toe_play(ctx, row, column):
    game_event = play_tic_tac_toe(ctx.author.id, int(row), int(column))
    await display_game_event(ctx, game_event)


@tic_tac_toe_play.error
async def tic_tac_toe_play_error(ctx, _):
    await ctx.send(
        'Please add your row and column numbers. Example: !tic_tac_toe_play 0 2. They can range from 0 to 2.')


@bot.command()
async def hangman_start(ctx):
    game_event = start_hangman(ctx.author.id)
    await display_game_event(ctx, game_event)


@bot.command()
async def hangman_guess(ctx, guess):
    game_event = guess_hangman(ctx.author.id, guess)
    await display_game_event(ctx, game_event)


@hangman_guess.error
async def hangman_guess_error(ctx, _):
    await ctx.send('Please add a letter or a word. Example: !hangman_guess e or !hangman_guess test')


async def display_game_event(ctx, game_event):
    if game_event.message(): await ctx.send(game_event.message())
    if game_event.board(): await ctx.send("```" + game_event.board() + "```")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)
