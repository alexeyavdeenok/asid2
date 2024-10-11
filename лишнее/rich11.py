from rich.console import Console
from rich.text import Text

console = Console()

# Создаем текст с цветами
text = Text("Это пример строки с подстрокой")
text.stylize("bold red", 4, 11)  # Красный жирный текст для диапазона [4:11]
text.stylize("bold yellow", 9, 26)  # Желтый жирный текст для диапазона [17:26]

# Выводим текст в консоль
console.print(text)
