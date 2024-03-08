import disnake
from disnake.ext import commands
from disnake import TextInputStyle
from disnake import Embed
from disnake.ext import tasks
import re

def is_valid_nickname(nickname: str) -> bool:
    if len(nickname) < 3 or len(nickname) > 16:
        return False


    # Проверка, что имя пользователя не содержит запрещённых слов
    forbidden_words = ["admin", "root", "moderator", "support", "help"]
    if nickname.lower() in forbidden_words:
        return False
    return True

def is_valid_rp_name(rp_name: str) -> bool:

    return True



class RegistrationModal(disnake.ui.Modal):
    def __init__(self, arg):
        self.arg = arg  # arg - это аргумент, который передается в конструкторе класса RecruitementSelect

        components = [
            disnake.ui.TextInput(
                label="Введите ваш ник в игре",
                placeholder="Например: OnlyFansVitalya",
                custom_id="nick",  # Изменено
                style=TextInputStyle.short,
                max_length=25,
            ),
            disnake.ui.TextInput(
                label="Введите ваше РП имя",
                placeholder="Например: Лева Иксбокс",
                custom_id="rp_nick",  # Изменено
                style=TextInputStyle.short,
                max_length=25,
            ),
            disnake.ui.TextInput(
                label="Ваш возраст в реалии",
                required=False,
                placeholder="По желанию",
                custom_id="age",  # Изменено
                style=TextInputStyle.short,
                max_length=2,
            ),
            disnake.ui.TextInput(
                label="Сколько вайпов играете",
                placeholder="По желанию",
                required=False,
                custom_id="count_wipe",  # Изменено
                style=TextInputStyle.short,
                max_length=2,
            ),
        ]
        title = "Создание паспорта"
        super().__init__(title=title, components=components, custom_id="registrationModal")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        nick = interaction.text_values["nick"]
        rp_nick = interaction.text_values["rp_nick"]
        age = interaction.text_values["age"]
        count_wipe = interaction.text_values["count_wipe"]
        # Проверка данных
        if not is_valid_nickname(nick):
            await interaction.response.send_message("Неверный формат никнейма, пожалуйста, попробуйте ещё раз.",
                                                    ephemeral=True)
            return
        if not is_valid_rp_name(rp_nick):
            await interaction.response.send_message("Неверный формат РП-имени, пожалуйста, попробуйте ещё раз.",
                                                    ephemeral=True)
            return



        await interaction.user.edit(nick=nick)

        embed = disnake.Embed(color=0x2F3136, title="Регистрация выполнена!")
        embed.description = f"{interaction.author.mention}, Благодарим вас за **регистрацию**! " \
                            f"Все **каналы** уже должны быть доступны, " \
                            f"Приятной игры в нашем **городе**"

        embed.set_thumbnail(url=interaction.author.display_avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)
        channel = interaction.guild.get_channel(1102940176482840630)  # Вставить ID канала куда будут отправляться заявки

        username = interaction.user.display_name
        embed = Embed(title=f"Паспорт игрока: {username}",
                      description=f"Ник в игре: **{nick}**\nРп имя: *{rp_nick}*\nВозраст: {age}\nКол-во вайпов: {count_wipe}\nПрофессия: *{self.arg}*",
                      color=0x008AFF)
        # Получаем ссылку на аватар пользователя

        embed.set_thumbnail(url=interaction.author.display_avatar.url)

        # Отправляем Embed-сообщение в указанный канал
        await channel.send(embed=embed)

        role = None  # Переменная для хранения роли, которую нужно выдать
        if self.arg == "строитель":
            role = interaction.guild.get_role(1078273484280574012)
        elif self.arg == "шахтер":
            role = interaction.guild.get_role(1078033428177490052)
        elif self.arg == "архитектор":
            role = interaction.guild.get_role(1078275904662405152)
        elif self.arg == "секретарь":
            role = interaction.guild.get_role(1078278123256287254)
        elif self.arg == "разнорабочий":
            role = interaction.guild.get_role(1144951487504592897)
        elif self.arg == "военнослужащий":
            role = interaction.guild.get_role(1145645634175635516)
        elif self.arg == "гость":
            role = interaction.guild.get_role(1213589719242248192)

        main_role = interaction.guild.get_role(1016763331505295462)
        if role != interaction.guild.get_role(1213589719242248192):
            await interaction.user.add_roles(main_role)
            await interaction.user.add_roles(role)
        else:
            await interaction.user.add_roles(role)

class RegistraionSelect(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label="🏗️ Строитель", value="строитель", description="Строит здания по чертежам"),
            disnake.SelectOption(label="⛏️ Шахтёр", value="шахтёр", description="Добывает руду для строительства"),
            disnake.SelectOption(label="📐 Архитектор", value="архитектор", description="Создает чертежи зданий(Необходимо пройти тест)"),
            disnake.SelectOption(label="📝 Рекрутёр", value="рекрутёр", description="Добавляет и заселяет новых граждан."),
            disnake.SelectOption(label="🔧 Разнорабочий", value="разнорабочий", description="Работает везде"),
            disnake.SelectOption(label="💂🏻‍♀️ Военнослужащий", value="военнослужащий", description="В военное время занимается обороной города, в невоенное разнорабочий"),
            disnake.SelectOption(label="👨‍💼 Гость", value="гость", description="Вы из другого города? Хотите поговорить? Это ваша роль!"),
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
            await interaction.response.send_modal(RegistrationModal(interaction.values[0]))


class RegistrationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistents_views_added = False

    async def registration(self):
        channel_id = 1103700455059640440
        channel = self.bot.get_channel(channel_id)
        view = disnake.ui.View(timeout=None)  # Изменено
        view.add_item(RegistraionSelect())

        embed = disnake.Embed(color=0x008AFF)
        embed.set_author(name="Добро пожаловать!")
        embed.description = "Для вступления в ряды граждан нашего **города** и получения доступа ко всем **каналам**, \nвам необходимо пройти короткую **регистрацию** \n" \
                            "Ниже вы можете выбрать желаемую профессию, нажав на кнопку роли в меню выбора, ее всегда можно будет изменить. Почитать о профессиях можно в канале #📋профессии \n" \
                            "**(не забывайте скроллить, у нас много профессий)**.\n\n" \
                            "**Внимание! Если вы столкнулись с ошибкой, напишите в лс администратору сервера** \n" \
                            "🏗️ - Строитель\n" \
                            "⛏️ - Шахтёр\n" \
                            "📐 - Архитектор\n" \
                            "📝 - Рекрутёр\n" \
                            "🔧 - Разнорабочий\n" \
                            "💂🏻‍♀️ - Военнослужащий\n" \
                            "👨‍💼 - Гость\n"
        embed.set_image(url="https://i.postimg.cc/7hzQDtr1/rabstol-net-flags-57.jpg")

        await channel.send(embed=embed)
        await channel.send('Выберите желаемую профессию:', view=view)

    @commands.Cog.listener()
    async def on_connect(self):
        if self.persistents_views_added:
            return

        view = disnake.ui.View(timeout=None)
        view.add_item(RegistraionSelect())
        self.bot.add_view(view, message_id=1145409322269032448)

    async def clear_chat(self, channel):
        await channel.purge(limit=100)  # Очистка чата (вы можете установить другой лимит сообщений)

    @commands.Cog.listener()
    async def on_ready(self):
        channel_id = 1103700455059640440
        channel = self.bot.get_channel(channel_id)

        if channel is None:
            print(f"Канал с ID {channel_id} не найден.")
            return

        # Очистка чата и отправка select menu
        await self.clear_chat(channel)
        await self.registration()
    @tasks.loop(minutes=60)
    async def message_refresh(self):
        print("Очистка чата и отправка сообщения...")
        channel_id = 1103700455059640440
        channel = self.bot.get_channel(channel_id)

        if channel is None:
            print(f"Канал с ID {channel_id} не найден.")
            return

        # Очистка чата и отправка select menu
        await self.clear_chat(channel)
        await self.registration()

    @message_refresh.before_loop
    async def before_message_refresh(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(RegistrationCog(bot))
