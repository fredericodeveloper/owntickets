import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import db
import lang
import sys
import utils

# If env file exists
if os.path.isfile('.env'):
    # Loads variables from the .env environment file into os.environ
    load_dotenv()

if os.getenv('BOT_TOKEN') is None:
    print("Please set the BOT_TOKEN enviroment variable.")
    sys.exit(1)

# Initialize database
db.init_db()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='ticket!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

class TicketChannelButtons(discord.ui.View):
    def __init__(self, language: str):
        super().__init__(timeout=None)
        self.language = language

        # Create the button dynamically using lang and add it to the view
        button = discord.ui.Button(
            label=lang.get_content(self.language, "ticketchannel_closebtn_label"),
            style=discord.ButtonStyle.red,
            custom_id="close_ticket"
        )
        button.callback = self.close_ticket  # Attach the callback
        self.add_item(button)

    async def close_ticket(self, interaction: discord.Interaction):
        channel = interaction.channel
        if channel is None:
            return

        guild = interaction.guild
        if guild is None:
            return

        if 'ticketmanager' not in [role.name for role in interaction.user.roles]: # pyright: ignore
            await interaction.response.send_message(lang.get_content(self.language, "no_permission"), ephemeral=True)
            return

        if not guild.me.guild_permissions.manage_channels:
            await interaction.response.send_message(lang.get_content(self.language, "bot_no_permission"), ephemeral=True)
            return

        await channel.delete() # pyright: ignore

class TicketButton(discord.ui.View):
    def __init__(self, language: str):
        super().__init__(timeout=None)
        self.language = language

        # Create the button dynamically using lang and add it to the view
        button = discord.ui.Button(
            label=lang.get_content(self.language, "ticket_open_btnlabel"),
            style=discord.ButtonStyle.green,
            custom_id="open_ticket"
        )
        button.callback = self.open_ticket  # Attach the callback
        self.add_item(button)

    async def open_ticket(self, interaction: discord.Interaction):
        guild = interaction.guild
        if guild is None:
            return

        existing_channel = discord.utils.get(guild.text_channels, name=f'ticket-{interaction.user.name.replace(" ", "-")}')
        if existing_channel:
            await interaction.response.send_message(
                lang.get_content(self.language, "ticket_exists_message"),
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            lang.get_content(self.language, "ticket_open_message"),
            ephemeral=True
        )

        # Create a private channel for the user who opened the ticket

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(send_messages=True, read_messages=True)
        }
        role = discord.utils.get(guild.roles, name="ticketmanager")
        if role is not None:
            for member in guild.members:
                if role in member.roles:
                    overwrites[member] = discord.PermissionOverwrite(send_messages=True, read_messages=True)

        private_channel = await guild.create_text_channel(f'ticket-{interaction.user.name.replace(" ", "-")}', overwrites=overwrites)

        # Send a message to the new ticket channel
        await private_channel.send(view=TicketChannelButtons(language=self.language))

@bot.command()
async def init(ctx, language: str):
    if not lang.is_valid(language):
        await ctx.send(lang.get_content("en", "init_fail_invalid_lang"))
        return

    channel_id = ctx.channel.id
    server_id = ctx.guild.id

    user = ctx.author
    if not user.guild_permissions.administrator:
        await ctx.send(lang.get_content(language, "no_permission"))
        return

    if utils.set_initialized(server_id, channel_id, language):
        embed = discord.Embed(title=lang.get_content(language, "ticket_open_title"), description=lang.get_content(language, "ticket_open_description"), colour=discord.Colour(0x3e038c))
        message = await ctx.send(embed=embed, view=TicketButton(language=language))
        # Set the message id
        message_id = message.id
        utils.set_ticket_message_id(server_id, message_id)
    else:
        await ctx.send(lang.get_content(language, "init_fail_already_initialized"))

    role = discord.utils.get(ctx.guild.roles, name="ticketmanager")
    if role is None:
        await ctx.guild.create_role(name="ticketmanager", permissions=discord.Permissions(send_messages=False), reason="Role required for ticket system")

@bot.command()
async def reset(ctx):
    server_id = ctx.guild.id

    language = utils.get_language(server_id)

    user = ctx.author
    if not user.guild_permissions.administrator:
        await ctx.send(lang.get_content("en", "no_permission"))
        return

    try:
        channel_id, message_id = utils.get_ticket_channel_message_info(server_id)
        if channel_id == None or message_id == None:
            await ctx.send(lang.get_content(language, "reset_not_initialized"))

        channel = bot.get_channel(int(str(channel_id)))
        if isinstance(channel, discord.TextChannel):
            message_to_delete = await channel.fetch_message(int(str(message_id)))
            await message_to_delete.delete()
        else:
            await ctx.send(lang.get_content(language, "reset_not_initialized"))
    except:
        pass

    if utils.unset_initialized(server_id):
        await ctx.send(lang.get_content(language, "reset_success"))
    else:
        await ctx.send(lang.get_content(language, "reset_not_initialized"))



# Run the bot using the BOT_TOKEN loaded
if __name__ == '__main__':
    token_value = None
    if 'BOT_TOKEN' in os.environ:
        token_value = os.environ['BOT_TOKEN']
    if token_value is not None:
        bot.run(token_value)
