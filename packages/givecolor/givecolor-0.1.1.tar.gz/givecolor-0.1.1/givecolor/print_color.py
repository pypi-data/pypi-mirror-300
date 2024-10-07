from enum import Enum
import builtins
import re

class Color(Enum):
    """Lista de colores con sus respectivas secuencias de escape ANSI"""
    DEFAULT = '\033[0m'  # Resetear al color original
    BLACK  = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    def __str__(self):
        return self.value

# Guardar la referencia original de la función print
class Colored():
    def __init__(self) -> None:
        self.original_print = builtins.print
        builtins.print = self.color_print
        

    # Crear una nueva función que envuelve a print con soporte de color
    def color_print(self,
                    *values: object,
                    color: str = Color.DEFAULT,
                    sep: str = ' ',
                    end: str = '\n',
                    **kwargs) -> None:
        """Establece un color predetermina en el texto del print"""
        if type(color) is Color:
            color = str(color)

        if not re.fullmatch(r'\033\[[0-9]+m', color):
            self.original_print('Esto no es una cadena valida')
            color = Color.DEFAULT
            
        if color == Color.DEFAULT:
            self.original_print(*values, sep=sep, end=end, **kwargs)
        else:
            self.original_print(color, end='')
            self.original_print(*values, sep=sep, end='', **kwargs)
            self.original_print(Color.DEFAULT)



