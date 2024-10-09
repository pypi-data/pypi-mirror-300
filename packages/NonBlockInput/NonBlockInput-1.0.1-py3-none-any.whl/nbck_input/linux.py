import select
import tty
import sys
import atexit

from .base import BaseInput
from .keys import get_ansi_value, match_ansi

if sys.platform == "linux":
    # 此模块引入会改变标准输入的设置，如果出现输入相关异常，请检查是否此模块导致
    setting = [*tty.tcgetattr(sys.stdin.fileno())]
    tty.setcbreak(sys.stdin.fileno(), tty.TCSADRAIN)  # 注意，此处是Linux的终端设置，如果传入是自定义的文件描述符，例如PIPE.stdin，则可能会存在异常

    def restore():
        tty.tcsetattr(sys.stdin.fileno(), tty.TCSADRAIN, setting)

    # 此处已注册退出时恢复标准输入的设置
    atexit.register(restore)


class LinuxInput(BaseInput):
    def read_byte(self, echo: bool = True, ansi: bool = True) -> bytes:
        ready, _, _ = select.select([self.stdin], [], [], 0.001)
        if ready:
            b = self.stdin.buffer.read(1)
            if b in [b"\x1b"]:
                _1 = self.stdin.buffer.read(1)
                b = b + _1
                if _1 in [b"[", b"O"]: # 识别预期内的CSI指令
                    for i in range(3):
                        b = b + self.stdin.buffer.read(1)
                        if not isinstance(match_ansi(b), list):
                            break
            if ansi:
                b = get_ansi_value(b)
            if echo:
                self.stdout.buffer.write(b)
                self.stdout.buffer.flush()
            return b
        else:
            return b""
