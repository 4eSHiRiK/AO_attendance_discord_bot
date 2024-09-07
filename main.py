from discord import app_commands
import discord

from src.interfaces.services.players_battle_service import PlayersBattleServiceABC
from src.services.players_battle_service import PlayersBattleService
from src.repository.sqla.db import database
from src.core.settings import bot_token


MY_GUILD = discord.Object(id=1253968970923507754)  # replace with your guild id


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")


@client.event
async def on_disconnect():
    await database.engine.dispose()


@client.tree.command(name="find")
async def get_user(interaction: discord.Interaction, name: str):
    print(f"Start to check user")
    service: PlayersBattleServiceABC = PlayersBattleService()
    player_battle = await service.get_player_battle(name)
    if player_battle:
        await interaction.response.send_message(
            f"User found: {player_battle.nickname}, \n Guild: {player_battle.guildname}, \n Alliance: {player_battle.alliancename}"
        )
    else:
        await interaction.response.send_message("User not found")


@client.tree.command(name="attendance")
@app_commands.describe(
    name="Write the nickname",
    days="Write the numbers of days",
)
async def get_attendance(interaction: discord.Interaction, name: str, days: int):
    service: PlayersBattleServiceABC = PlayersBattleService()
    player_battle = await service.get_player_battle(name)
    if not player_battle:
        await interaction.response.send_message(f"User not found")
    else:
        player_attendance = await service.get_player_attendance(name, days)

        await interaction.response.send_message(
            f"User: {name} has: {player_attendance.battle_count} attendances ({player_attendance.percent_of_max}%)\n"
            f"K/D: {player_attendance.kd}"
        )


@client.tree.command(name="gkick")
@app_commands.describe(
    days="Write the numbers of days",
    activity_threshold="Write inactive period",
    percentage_threshold="Percentage threshold",
)
async def need_kick(
    interaction: discord.Interaction,
    days: int,
    activity_threshold: int,
    percentage_threshold: int | None,
):
    service: PlayersBattleServiceABC = PlayersBattleService()
    player_list = await service.need_g_kick(
        days, activity_threshold, percentage_threshold
    )
    player_info = [
        f"**{player.nickname}** (last active: {player.last_activity.strftime('%Y-%m-%d')}, battles: {player.battle_count})"
        for player in player_list
    ]
    message = "Go kick the following inactive players:\n"
    max_length = 2000  # Максимальная длина сообщения в Discord
    current_message = message
    first_message_sent = False

    for player in player_info:
        if len(current_message) + len(player) + 1 > max_length:
            if not first_message_sent:
                await interaction.response.send_message(current_message)
                first_message_sent = True
            else:
                await interaction.followup.send(current_message)
            current_message = player + "\n"
        else:
            current_message += player + "\n"

    if current_message.strip():
        if not first_message_sent:
            await interaction.response.send_message(current_message)
        else:
            await interaction.followup.send(current_message)


if __name__ == "__main__":
    client.run(bot_token)
