import discord
from discord.ext import commands

import config
from cogs.music import MusicCog

# Set intents for the bot
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

# Create the bot instance
bot = commands.Bot(command_prefix='/', intents=intents)

# Load the Music cog
bot.add_cog(MusicCog(bot))

# Run the bot
if __name__ == '__main__':
    bot.run(config.BOT_TOKEN)