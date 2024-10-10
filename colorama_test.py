from colorama import init, Fore, Style, Back

# Инициализация colorama
init(autoreset=True)

indices = [0, 3, 4, 5, 6, 20]
text = 'ahsdfhasdskjffhasdsfhahalsd'
print_text = ''
for i in range(len(text)):
    if i in indices:
        print_text += Fore.RED + text[i] + Style.RESET_ALL
    else:
        print_text += text[i]
print(print_text)