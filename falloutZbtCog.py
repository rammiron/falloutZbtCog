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

    def __init__(self, _bot: discord.Bot):
        self.bot = _bot

    async def try_send_message(self, private_message, public_message, member: discord.Member):

        try:
            await member.create_dm()
            await member.dm_channel.send(private_message)
        except:
            channel = self.guild.get_channel(channel_for_alert_id)
            await channel.send(public_message)

    async def check_whitelist_users(self):
        users = crud.get_users_from_whitelist()
        role = self.guild.get_role(role_id)
        for user in users:
            member = self.guild.get_member(user.user_id)
            if member is None:
                crud.delete_user_from_whitelist(user.user_id)
                continue
            if role not in member.roles:
                crud.delete_user_from_whitelist(user.user_id)
                continue

    async def check_users(self):
        users = crud.get_users()
        role = self.guild.get_role(role_id)
        for user in users:
            member = self.guild.get_member(user.discord_id)
            if member is None:
                if crud.user_id_was_found_in_whitelist(user.user_id):
                    crud.delete_user_from_whitelist(user.user_id)
                continue
            if role not in member.roles:
                if crud.user_id_was_found_in_whitelist(user.user_id):
                    crud.delete_user_from_whitelist(user.user_id)
                continue
            if not crud.user_id_was_found_in_whitelist(user.user_id):
                crud.add_user_to_whitelist(user.user_id)
                try:
                    channel = await member.create_dm()
                    await channel.send(f"{member.mention}, вы добавлены в вайтлист.")
                except:
                    channel = self.guild.get_channel(channel_for_alert_id)
                    await channel.send(f"{member.mention}, вы добавлены в вайтлист.")
        update_file()

    async def check_role(self):
        role = self.guild.get_role(role_id)
        members_with_role = role.members
        for member in members_with_role:
            if crud.user_id_was_found_in_whitelist(crud.get_game_id_by_discord_id(member.id)):
                continue

            if crud.discord_id_was_found_in_users_db(member.id):
                crud.add_user_to_whitelist(crud.get_game_id_by_discord_id(member.id))
                await self.try_send_message("Вы добавлены в вайтлист фоллаута.",
                                            f"{member.mention}, вы добавлены в вайтлист.",
                                            member)
                continue
            await self.try_send_message("Для присоединения к ЗБТ привяжите свой дискорд с помощью команды /setnick,"
                                        " где вместо NAME нужно указать игровой ник (сикей).",
                                        f"{member.mention}, "
                                        f"для присоединения к ЗБТ привяжите свой дискорд с помощью команды /setnick,"
                                        " где вместо NAME нужно указать игровой ник (сикей).", member)

    @tasks.loop(seconds=time_for_checking_db)
    async def checking_db_task(self):
        if not db_was_modify():
            return
        await self.check_users()

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if crud.user_id_was_found_in_whitelist(crud.get_game_id_by_discord_id(member.id)):
            crud.delete_user_from_whitelist(crud.get_game_id_by_discord_id(member.id))

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):

        if before.roles == after.roles:
            return
        target_role = after.guild.get_role(role_id)
        if target_role in before.roles:
            if target_role not in after.roles:
                if crud.user_id_was_found_in_whitelist(crud.get_game_id_by_discord_id(after.id)):
                    crud.delete_user_from_whitelist(crud.get_game_id_by_discord_id(after.id))
            return
        if crud.user_id_was_found_in_whitelist(crud.get_game_id_by_discord_id(after.id)):
            return
        if crud.discord_id_was_found_in_users_db(after.id):
            crud.add_user_to_whitelist(crud.get_game_id_by_discord_id(after.id))

            await self.try_send_message("Вы добавлены в вайтлист фоллаута.",
                                        f"{after.mention}, вы добавлены в вайтлист.",
                                        after)
            return
        await self.try_send_message("Для присоединения к ЗБТ привяжите свой дискорд с помощью команды /setnick,"
                                    " где вместо NAME нужно указать игровой ник (сикей).",
                                    f"{after.mention}, похоже у вас закрыт лс,"
                                    f"для присоединения к ЗБТ привяжите свой дискорд с помощью команды /setnick,"
                                    " где вместо NAME нужно указать игровой ник (сикей).", after)

    @commands.Cog.listener()
    async def on_ready(self):
        print("работает, алилуя")
        Base.metadata.create_all(engine)
        self.guild = self.bot.get_guild(server_id)
        self.checking_db_task.start()
        await self.check_whitelist_users()
        await self.check_role()
        if not db_was_modify():
            return
        await self.check_users()
