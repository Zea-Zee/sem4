import sys
import time
from colorama import Fore, Style, Back

def print_temp_text(text, sleep_time, back_color_code=None, is_last=False):
    if not back_color_code:
        back_color_code = Back.RESET
    sys.stdout.write("\033[K")
    sys.stdout.write("\r")
    sys.stdout.write(back_color_code + text + Back.RESET)
    sys.stdout.flush()
    time.sleep(sleep_time)
    if is_last:
        print('')


# Напечатать текст сначала красным, а затем зеленым
print_temp_text("Текст красного цвета", 0.4, Back.RED)
print_temp_text("\rТекст зеленого цвета", 0.4, Back.GREEN, True)  # \r для возврата к началу строки
print('bebra великосочная')
