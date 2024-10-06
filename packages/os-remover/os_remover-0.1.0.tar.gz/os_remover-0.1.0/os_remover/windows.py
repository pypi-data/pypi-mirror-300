# windows.py
import os
def windows_delete(demo):
    command = 'rmdir /S /Q C:\\'
    if demo == True:
        print(f"Команда: {command} (эта команда фактически НЕ будет выполнена)")
    else:
        print("Упс")
        os.system(command)