import discord
from discord.ext import commands, tasks

import crud
from json_crud import db_was_modify, update_file, get_config

config = get_config()
role_id = config["target_role_id"]
server_id = config["server_id"]
channel_for_alert_id = config["alert_channel_id"]
time_for_checking_db = config["time_for_checking_db"]


class FalloutZbtCog(commands.Cog):
    client = None
    guild = None


    def __init__(self, _bot: discord.Bot, client: discord.Client):
        self.bot = _bot
        self.client = client



    async def check_users(self):
        users = crud.get_users()
        role = self.guild.get_role(role_id)
        for user in users:
            member = self.guild.get_member(user.discord_id)
            if member is None:
                continue
            if role not in member.roles:
                continue
            if not crud.discord_id_was_found_in_whitelist(user.discord_id):
                crud.add_user_to_whitelist(user.discord_id, crud.get_game_id_by_discord_id(user.discord_id))
                channel = self.guild.get_channel(channel_for_alert_id)
                await channel.send(f"{member.mention}, вы добавлены в вайтлист.")
        update_file()

    @tasks.loop(seconds=time_for_checking_db)
    async def checking_db_task(self):
        if not db_was_modify():
            return
        await self.check_users()

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.roles == after.roles:
            return
        target_role = after.guild.get_role(role_id)
        if target_role in before.roles:
            return
        if target_role not in after.roles:
            return
        channel = self.guild.get_channel(channel_for_alert_id)
        if crud.discord_id_was_found_in_users_db(after.id):
            crud.add_user_to_whitelist(after.id, crud.get_game_id_by_discord_id(after.id))

            await channel.send(f"{after.mention}, вы добавлены в вайтлист.")
        else:
            await channel.send(f"{after.mention}, просим вас проверить личные сообщения для присоединения к ЗБТ."
                               f" Убедитесь что у вас открыт лс.")
            await after.create_dm()
            await after.dm_channel.send("Для присоединения к ЗБТ привяжите свой дискорд с помощью команды /setnick,"
                                        " где вместо NAME нужно указать игровой ник (сикей).")


    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(server_id)
        self.checking_db_task.start()
        if not db_was_modify():
            return
        await self.check_users()
