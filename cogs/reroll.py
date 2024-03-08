import disnake
from disnake.ext import commands

class ReRollSelect(disnake.ui.Select):
    def __init__(self):

        options = [
            disnake.SelectOption(label="🏗️ Строитель", value="строитель", description="Строит здания по чертежам"),
            disnake.SelectOption(label="⛏️ Шахтёр", value="шахтёр", description="Добывает руду для строительства"),
            disnake.SelectOption(label="📐 Архитектор", value="архитектор", description="Создает чертежи зданий(Необходимо пройти тест)"),
            disnake.SelectOption(label="📝 Рекрутёр", value="рекрутёр", description="Добавляет и заселяет новых граждан"),
            disnake.SelectOption(label="🔧 Разнорабочий", value="разнорабочий", description="Работает везде"),
            disnake.SelectOption(label="💂🏻‍♀️ Военнослужащий", value="военнослужащий", description="В военное время занимается обороной города, в невоенное разнорабочий"),
        ]
        super().__init__(
            placeholder="Выберите желаемую роль",
            options=options,
            min_values=0,
            max_values=1,
            custom_id="registration"
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        if not interaction.values:
            await interaction.response.defer()
        else:
            await interaction.response.defer()
            chosen_role_str = interaction.values[0]

            # Словарь соответствия названий ролей и их ID
            roles = {
                "строитель": 1078273484280574012,
                "шахтёр": 1078033428177490052,
                "архитектор": 1078275904662405152,
                "рекрутёр": 1078278123256287254,
                "разнорабочий": 1144951487504592897,
                "военнослужащий": 1145645634175635516
            }

            guild_roles = interaction.guild.roles
            user_roles = interaction.user.roles

            # Удалить старую роль
            for role_id in roles.values():
                role = interaction.guild.get_role(role_id)
                if role in user_roles:
                    await interaction.user.remove_roles(role)

            # Добавить новую роль
            new_role = interaction.guild.get_role(roles[chosen_role_str])
            await interaction.user.add_roles(new_role)
            await interaction.followup.send(f"Ваша профессия изменена на: {chosen_role_str}", ephemeral=True)




class ReRoll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def reroll(self):
        channel_id = 1145652227927703562
        channel = self.bot.get_channel(channel_id)
        view = disnake.ui.View()
        view.add_item(ReRollSelect())

        embed = disnake.Embed(color=0x008AFF)
        embed.set_author(name="Здесь вы можете изменить свою профессию!")
        embed.description = "" \
                            "🏗️ - Строитель\n" \
                            "⛏️ - Шахтёр\n" \
                            "📐 - Архитектор\n" \
                            "📝 - Рекрутёр\n" \
                            "🔧 - Разнорабочий\n" \
                            "💂🏻‍♀️ - Военнослужащий\n"
        embed.set_image(url="https://i.postimg.cc/7hzQDtr1/rabstol-net-flags-57.jpg")

        await channel.send(embed=embed)
        await channel.send('Выберите желаемую профессию:', view=view)

    @commands.Cog.listener()
    async def on_ready(self):
        channel_id = 1145652227927703562
        channel = self.bot.get_channel(channel_id)

        if channel is None:
            print(f"Канал с ID {channel_id} не найден.")
            return

        # Очистка чата
        await channel.purge(limit=100)

        # Отправка сообщения
        await self.reroll()

def setup(bot):
    bot.add_cog(ReRoll(bot))