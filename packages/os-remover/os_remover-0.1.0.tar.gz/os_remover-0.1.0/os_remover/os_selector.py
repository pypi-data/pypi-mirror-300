# os_selector.py
import questionary

def choose_os():
    os_choice = questionary.select(
        "Выберите операционную систему:",
        choices=[
            "Windows",
            "Linux",
            "macOS"
        ]
    ).ask()

    if os_choice == "Windows":
        return "windows"
    elif os_choice == "Linux":
        return "linux"
    elif os_choice == "macOS":
        return "macos"
    else:
        print("Неверный выбор.")
        return None
