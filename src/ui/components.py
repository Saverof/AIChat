# Импорт необходимых библиотек и модулей
import flet as ft  # Фреймворк для создания пользовательского интерфейса
from ui.styles import AppStyles  # Импорт стилей приложения
import asyncio  # Библиотека для асинхронного программирования


class MessageBubble(ft.Container):
    """
    Компонент "пузырька" сообщения в чате.

    Наследуется от ft.Container для создания стилизованного контейнера сообщения.
    Отображает сообщения пользователя и AI с разными стилями и позиционированием.

    Args:
        message (str): Текст сообщения для отображения
        is_user (bool): Флаг, указывающий, является ли это сообщением пользователя
    """

    def __init__(self, message: str, is_user: bool):
        # Инициализация родительского класса Container
        super().__init__()

        # Настройка отступов внутри пузырька
        self.padding = 10

        # Настройка скругления углов пузырька
        self.border_radius = 10

        # Установка цвета фона в зависимости от отправителя:
        # - Синий для сообщений пользователя
        # - Серый для сообщений AI
        self.bgcolor = ft.Colors.BLUE_700 if is_user else ft.Colors.GREY_700

        # Установка выравнивания пузырька:
        # - Справа для сообщений пользователя
        # - Слева для сообщений AI
        self.alignment = (
            ft.alignment.center_right if is_user else ft.alignment.center_left
        )

        # Настройка внешних отступов для создания эффекта диалога:
        # - Отступ слева для сообщений пользователя
        # - Отступ справа для сообщений AI
        # - Небольшие отступы сверху и снизу для разделения сообщений
        self.margin = ft.margin.only(
            left=50 if is_user else 0,  # Отступ слева
            right=0 if is_user else 50,  # Отступ справа
            top=5,  # Отступ сверху
            bottom=5,  # Отступ снизу
        )

        # Создание содержимого пузырька
        self.content = ft.Column(
            controls=[
                # Текст сообщения с настройками отображения
                ft.Text(
                    value=message,  # Текст сообщения
                    color=ft.Colors.WHITE,  # Белый цвет текста
                    size=16,  # Размер шрифта
                    selectable=True,  # Возможность выделения текста
                    weight=ft.FontWeight.W_400,  # Нормальная толщина шрифта
                )
            ],
            tight=True,  # Плотное расположение элементов в колонке
        )


class ModelSelector(ft.Dropdown):
    """
    Выпадающий список для выбора AI модели с функцией поиска.

    Наследуется от ft.Dropdown для создания кастомного выпадающего списка
    с дополнительным полем поиска для фильтрации моделей.

    Args:
        models (list): Список доступных моделей в формате:
                      [{"id": "model-id", "name": "Model Name"}, ...]
    """

    def __init__(self, models: list):
        # Инициализация родительского класса Dropdown
        super().__init__()

        # Применение стилей из конфигурации к компоненту
        for key, value in AppStyles.MODEL_DROPDOWN.items():
            setattr(self, key, value)

        # Настройка внешнего вида выпадающего списка
        self.label = None  # Убираем текстовую метку
        self.hint_text = "Выбор модели"  # Текст-подсказка

        # Создание списка опций из предоставленных моделей
        self.options = [
            ft.dropdown.Option(
                key=model["id"],  # ID модели как ключ
                text=model["name"],  # Название модели как отображаемый текст
            )
            for model in models
        ]

        # Сохранение полного списка опций для фильтрации
        self.all_options = self.options.copy()

        # Установка начального значения (первая модель из списка)
        self.value = models[0]["id"] if models else None

        # Создание поля поиска для фильтрации моделей
        self.search_field = ft.TextField(
            on_change=self.filter_options,  # Функция обработки изменений
            hint_text="Поиск модели",  # Текст-подсказка в поле поиска
            **AppStyles.MODEL_SEARCH_FIELD,  # Применение стилей из конфигурации
        )

    def filter_options(self, e):
        """
        Фильтрация списка моделей на основе введенного текста поиска.

        Args:
            e: Событие изменения текста в поле поиска
        """
        # Получение текста поиска в нижнем регистре
        search_text = self.search_field.value.lower() if self.search_field.value else ""

        # Если поле поиска пустое - показываем все модели
        if not search_text:
            self.options = self.all_options
        else:
            # Фильтрация моделей по тексту поиска
            # Ищем совпадения в названии или ID модели
            self.options = [
                opt
                for opt in self.all_options
                if search_text in opt.text.lower() or search_text in opt.key.lower()
            ]

        # Обновление интерфейса для отображения отфильтрованного списка
        e.page.update()


class AuthScreen(ft.Column):
    """
    Экран аутентификации для ввода API ключа и PIN-кода.

    Обеспечивает:
    - Ввод API ключа OpenRouter при первом входе
    - Ввод PIN-кода при последующих входах
    - Сброс API ключа при необходимости

    Args:
        on_auth_success: Функция обратного вызова при успешной аутентификации
        cache: Экземпляр класса ChatCache для хранения данных аутентификации
        api_client: Экземпляр класса OpenRouterClient для проверки API ключа
    """

    def __init__(self, on_auth_success, cache, api_client):
        super().__init__()

        # Сохранение параметров
        self.on_auth_success = on_auth_success
        self.cache = cache
        self.api_client = api_client

        # Применение стилей
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 20
        self.expand = True

        # Получение сохраненных данных аутентификации
        self.api_key, self.pin = self.cache.get_auth_data()

        # Создание контролов
        self.controls = []

        # Определение режима отображения (PIN или API ключ)
        if self.pin:
            self.show_pin_screen()
        else:
            self.show_api_key_screen()

    def show_pin_screen(self):
        """Отображение экрана ввода PIN-кода"""
        self.controls.clear()

        # Заголовок
        self.controls.append(
            ft.Text(
                "Введите PIN-код для входа",
                size=24,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            )
        )

        # Поле ввода PIN
        self.pin_input = ft.TextField(
            label="PIN-код",
            password=True,
            width=200,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        self.controls.append(self.pin_input)

        # Кнопка входа
        self.controls.append(
            ft.ElevatedButton(text="Войти", width=200, on_click=self.verify_pin)
        )

        # Кнопка сброса ключа
        self.controls.append(
            ft.TextButton(text="Сбросить ключ API", on_click=self.reset_api_key)
        )

        # Обновление интерфейса только если компонент уже добавлен на страницу
        if hasattr(self, "page") and self.page:
            self.update()

    def show_api_key_screen(self):
        """Отображение экрана ввода API ключа"""
        self.controls.clear()

        # Заголовок
        self.controls.append(
            ft.Text(
                "Введите ключ OpenRouter API",
                size=24,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            )
        )

        # Описание
        self.controls.append(
            ft.Text(
                "Ключ будет проверен на валидность и баланс",
                size=16,
                text_align=ft.TextAlign.CENTER,
            )
        )

        # Поле ввода API ключа
        self.api_key_input = ft.TextField(
            label="API ключ", width=400, password=True, can_reveal_password=True
        )
        self.controls.append(self.api_key_input)

        # Кнопка проверки ключа
        self.controls.append(
            ft.ElevatedButton(
                text="Проверить и сохранить", width=200, on_click=self.verify_api_key
            )
        )

        # Обновление интерфейса только если компонент уже добавлен на страницу
        if hasattr(self, "page") and self.page:
            self.update()

    def show_error(self, page, message):
        """Отображение сообщения об ошибке"""
        snack = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.RED_500),
            bgcolor=ft.Colors.GREY_900,
            duration=5000,
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()

    def verify_pin(self, e):
        """Проверка введенного PIN-кода"""
        entered_pin = self.pin_input.value

        if not entered_pin:
            self.show_error(e.page, "PIN-код не может быть пустым")
            return

        # Проверка PIN-кода
        if entered_pin == self.pin:
            # Установка API ключа в клиент
            self.api_client.api_key = self.api_key
            # Вызов функции успешной аутентификации
            self.on_auth_success()
        else:
            self.show_error(e.page, "Неверный PIN-код")
            self.pin_input.value = ""
            e.page.update()

    def verify_api_key(self, e):
        """Проверка введенного API ключа"""
        api_key = self.api_key_input.value

        if not api_key:
            self.show_error(e.page, "API ключ не может быть пустым")
            return

        # Отображение индикатора загрузки
        loading = ft.ProgressRing()
        self.controls.append(loading)
        if hasattr(self, "page") and self.page:
            self.update()

        try:
            # Временная установка API ключа для проверки
            self.api_client.api_key = api_key
            self.api_client.headers["Authorization"] = f"Bearer {api_key}"

            # Проверка баланса
            balance = self.api_client.get_balance()

            # Удаление индикатора загрузки
            if loading in self.controls:
                self.controls.remove(loading)
                if hasattr(self, "page") and self.page:
                    self.update()

            if balance == "Ошибка":
                self.show_error(e.page, "Неверный API ключ или ошибка сервера")
                return

            # Генерация 4-значного PIN-кода
            import random

            pin = "".join([str(random.randint(0, 9)) for _ in range(4)])

            # Сохранение API ключа и PIN-кода
            self.cache.save_auth_data(api_key, pin)

            # Отображение диалога с PIN-кодом
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("PIN-код создан"),
                content=ft.Column(
                    [
                        ft.Text("Ваш PIN-код для входа:"),
                        ft.Text(
                            pin,
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            "Запомните этот код! Он потребуется при следующем входе."
                        ),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                actions=[
                    ft.TextButton(
                        "Продолжить",
                        on_click=lambda x: self.close_dialog_and_proceed(x, dialog),
                    )
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

            e.page.overlay.append(dialog)
            dialog.open = True
            e.page.update()

        except Exception as ex:
            # Удаление индикатора загрузки
            if loading in self.controls:
                self.controls.remove(loading)
            self.show_error(e.page, f"Ошибка: {str(ex)}")
            if hasattr(self, "page") and self.page:
                self.update()

    def close_dialog_and_proceed(self, e, dialog):
        """Закрытие диалога и переход к основному интерфейсу"""
        dialog.open = False
        e.page.update()

        if dialog in e.page.overlay:
            e.page.overlay.remove(dialog)

        # Вызов функции успешной аутентификации
        self.on_auth_success()

    def reset_api_key(self, e):
        """Сброс API ключа и PIN-кода"""
        # Создание диалога подтверждения
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Подтверждение сброса"),
            content=ft.Text(
                "Вы уверены, что хотите сбросить ключ API? Потребуется ввести новый ключ."
            ),
            actions=[
                ft.TextButton(
                    "Отмена", on_click=lambda x: self.close_dialog(x, dialog)
                ),
                ft.TextButton(
                    "Сбросить", on_click=lambda x: self.confirm_reset(x, dialog)
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        e.page.overlay.append(dialog)
        dialog.open = True
        e.page.update()

    def close_dialog(self, e, dialog):
        """Закрытие диалога"""
        dialog.open = False
        e.page.update()

        if dialog in e.page.overlay:
            e.page.overlay.remove(dialog)

    def confirm_reset(self, e, dialog):
        """Подтверждение сброса API ключа"""
        # Закрытие диалога
        self.close_dialog(e, dialog)

        # Сброс данных аутентификации
        self.cache.reset_auth_data()

        # Переход к экрану ввода API ключа
        self.show_api_key_screen()
        e.page.update()
