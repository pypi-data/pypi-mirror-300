import msvcrt

from .base import BaseInput
from .keys import get_ansi_value


class Win32Input(BaseInput):
    def read_byte(self, echo: bool = True, ansi: bool = True) -> bytes:
        if msvcrt.kbhit():
            b = msvcrt.getch()
            if b in [b"\xe0", b"\x00"]:  # 识别预期内的按键操作
                b = b + self.read_byte(echo=False, ansi=False)
            if ansi:
                b = get_ansi_value(b)
            if echo:
                self.stdout.buffer.write(b)
                self.stdout.buffer.flush()
            return b
        else:
            return b""
