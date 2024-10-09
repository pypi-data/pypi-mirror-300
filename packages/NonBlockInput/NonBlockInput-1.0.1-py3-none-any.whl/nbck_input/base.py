import sys
from typing import Union, TextIO, List
from abc import abstractmethod

import pyte

from .utils import TimeoutIter
from .keys import Enter, Home, End, Left, Right, Backspace


class VT:
    def __init__(self, columns: int = 200, lines: int = 2) -> None:
        self.screen = pyte.Screen(columns, lines)
        self.steam = pyte.ByteStream(self.screen)
        self.feed(b'\x1b[2J') # 重置所有键，避免被历史记录影响

    def feed(self, b: bytes) -> None:
        self.steam.feed(b)
        Home.ansi = self.home  # 为实现Home键功能，每次输入后都要更新Home键指令
        End.ansi = self.end  # 以下同理
        Left.ansi = self.left
        Right.ansi = self.right
        Backspace.ansi = self.backspace

    @property
    def display(self) -> List[str]:
        return self.screen.display

    @property
    def home(self) -> str:
        """ANSI指令: 光标移动到行首"""
        return f"\x1b[{self.screen.cursor.x}D".encode("utf-8") if self.screen.cursor.x > 0 else b""

    @property
    def end(self) -> str:
        """ANSI指令: 光标移动到行尾"""
        _ = len(self.screen.display[self.screen.cursor.y].rstrip()) - self.screen.cursor.x
        return f"\x1b[{_}C".encode("utf-8") if _ > 0 else b""
    
    @property
    def left(self) -> str:
        """ANSI指令: 光标左移一个字符"""
        return b"\x1b[D" if self.screen.cursor.x > 0 else b""
    
    @property
    def right(self) -> str:
        """ANSI指令: 光标右移一个字符"""
        _ = len(self.screen.display[self.screen.cursor.y].rstrip()) - self.screen.cursor.x
        return b"\x1b[C" if _ > 0 else b""
    
    @property
    def backspace(self) -> str:
        """ANSI指令: 清除左侧一个字符，同时光标左移"""
        return b"\x1b[D\x1b[P" if self.screen.cursor.x > 0 else b""


class BaseInput:
    """读取用户输入的基类，通过read_byte、is_enter实现跨平台特性"""

    def __init__(self, stdin: TextIO = None, stdout: TextIO = None) -> None:
        self.stdin = stdin if stdin else sys.stdin
        self.stdout = stdout if stdout else sys.stdout

    @abstractmethod
    def read_byte(echo: bool = True) -> bytes:
        """用于获取单个字符"""
        pass

    def is_enter(self, b: Union[bytes, int]) -> bool:
        """用于判断是否为回车键字符"""
        b = b if isinstance(b, bytes) else bytes([b])
        return b == Enter.ansi

    def read_input(self, timeout: float = 0, time_seq: float = 0.001, echo: bool = True, pre_func: callable = None) -> str:
        """
        ### 函数功能:
            读取用户输入，并返回bytes类型数据，注意：不支持中文输入！

        ### Args:
            - timeout (float, optional): 超时时间，为0则不超时. Defaults to 0.
            - time_seq (float, optional): 轮询buffer间隔. Defaults to 0.1.
            - pre_func (callable, optional): 退出条件. Defaults to None.

        ### Returns:
            - bytes: _description_
        """
        pre_func = pre_func if pre_func and callable(pre_func) else None  # callable 判断前移，减少不必要的判断
        vt = VT()
        self.clear_buffer()
        for _ in TimeoutIter(timeout=timeout, time_seq=time_seq):
            data = self.read_byte(echo=echo)
            if data:
                vt.feed(data)
            if pre_func and pre_func(data):  # 退出阻塞条件
                break
        return vt.display[0].strip()

    def read_line(self, timeout: float = 0, time_seq: float = 0.001, echo: bool = True, pre_func: callable = None) -> str:
        """读取用户输入，直到按下回车键"""
        pre_func = pre_func if pre_func and callable(pre_func) else None

        def func(x: bytes) -> bool:
            # 判定条件: 按下回车
            return self.is_enter(x) or (pre_func(x) if pre_func else False)  # 判断额外条件，退出阻塞

        data = self.read_input(timeout=timeout, time_seq=time_seq, echo=echo, pre_func=func)
        return data

    def read_char(self, timeout: float = 0, time_seq: float = 0.001, echo: bool = True, pre_func: callable = None) -> str:
        """读取用户单个字符输入，不需要按下回车"""
        pre_func = pre_func if pre_func and callable(pre_func) else None

        def func(x: bytes) -> bool:
            # 判定条件: 获取到任意输入
            return x or (pre_func(x) if pre_func else False)  # 判断额外条件，退出阻塞

        return self.read_input(timeout=timeout, time_seq=time_seq, echo=echo, pre_func=func)

    def clear_buffer(self, echo: bool = False) -> None:
        """清空缓冲区"""
        while self.read_byte(echo=echo):
            pass