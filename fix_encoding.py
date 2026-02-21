# fix_encoding.py
import os
import subprocess
import sys

# Устанавливаем переменные окружения для кодировки
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

# Запускаем миграцию
result = subprocess.run(
    [sys.executable, "manage.py", "migrate"], capture_output=True, text=True
)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)
