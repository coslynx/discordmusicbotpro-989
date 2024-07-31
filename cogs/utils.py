import discord

def format_message(message, title=None, color=None):
    """Formats a message for display in Discord.

    Args:
        message (str): The message to be formatted.
        title (str, optional): The title of the message. Defaults to None.
        color (discord.Color, optional): The color of the message embed. Defaults to None.

    Returns:
        discord.Embed: The formatted message embed.
    """
    embed = discord.Embed(description=message)
    if title:
        embed.title = title
    if color:
        embed.color = color
    return embed

def get_user_info(user):
    """Retrieves user information from Discord.

    Args:
        user (discord.User or discord.Member): The Discord user or member.

    Returns:
        dict: A dictionary containing user information.
    """
    return {
        "name": user.name,
        "id": user.id,
        "avatar_url": user.avatar.url if user.avatar else None,
        "discriminator": user.discriminator,
    }

def handle_error(ctx, error):
    """Handles errors gracefully and provides informative messages.

    Args:
        ctx (discord.ext.commands.Context): The command context.
        error (Exception): The error that occurred.
    """
    print(f"Error occurred: {error}")
    if isinstance(error, discord.ext.commands.CommandNotFound):
        await ctx.send(f"Command not found: `{ctx.invoked_with}`")
    elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument: `{error.param.name}`")
    elif isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(f"Missing permissions: {error.missing_permissions}")
    else:
        await ctx.send(f"An error occurred. Please try again later.")