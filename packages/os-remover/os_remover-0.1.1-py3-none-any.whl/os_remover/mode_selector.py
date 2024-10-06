# mode_selector.py
import questionary

def choose_mode():
    os_choice = questionary.select(
        "Выберите режим работы:",
        choices=[
            "Опасный 💀💀💀",
            "Безопасный 😇😇😇"
        ]
    ).ask()

    if os_choice == "Опасный 💀💀💀":
        return 0
    elif os_choice == "Безопасный 😇😇😇":
        return 1
    else:
        print("Неверный выбор.")
        return None
