from typing import Union, Callable, List

from dataclasses import dataclass


all_keys = []


class KeyBase:
    keys: List[bytes]
    ansi: Union[bytes, Callable] = b""

    def __init__(self, keys: List[bytes], ansi: Union[bytes, Callable] = b""):
        self.keys = keys
        self.ansi = ansi
        all_keys.append(self)


@dataclass
class InsertMode:
    insert: bool = True

    def reverse(self):
        self.insert = not self.insert
        return b""


insert_mode = InsertMode(insert=True)

F1 = KeyBase(keys=[b"\x1bOP", b"\x00;"])
F2 = KeyBase(keys=[b"\x1bOQ", b"\x00<"])
F3 = KeyBase(keys=[b"\x1bOR", b"\x00="])
F4 = KeyBase(keys=[b"\x1bOS", b"\x00>"])
F5 = KeyBase(keys=[b"\x1b[15~", b"\x00?"])
F6 = KeyBase(keys=[b"\x1b[17~", b"\x00@"])
F7 = KeyBase(keys=[b"\x1b[18~", b"\x00A"])
F8 = KeyBase(keys=[b"\x1b[19~", b"\x00B"])
F9 = KeyBase(keys=[b"\x1b[20~", b"\x00C"])
F10 = KeyBase(keys=[b"\x1b[21~", b"\x00D"])
F12 = KeyBase(keys=[b"\x1b[24~", b"\xe0\x86"])
Insert = KeyBase(keys=[b"\x1b[2~", b"\xe0R", b"\x00R"], ansi=lambda: insert_mode.reverse())
Delete = KeyBase(keys=[b"\x1b[3~", b"\xe0S", b"\x00s"], ansi=b"\x1b[P")
Home = KeyBase(keys=[b"\x1b[H", b"\xe0G", b"\x00G"], ansi=b"\r")
End = KeyBase(keys=[b"\x1b[F", b"\xe0O", b"\x00O"])
PageUp = KeyBase(keys=[b"\x1b[5~", b"\xe0I", b"\x00I"])
PageDown = KeyBase(keys=[b"\x1b[6~", b"\xe0Q", b"\x00Q"])
Up = KeyBase(keys=[b"\x1b[A", b"\xe0H", b"\x00H"])
Down = KeyBase(keys=[b"\x1b[B", b"\xe0P", b"\x00P"])
Left = KeyBase(keys=[b"\x1b[D", b"\xe0K", b"\x00K"], ansi=b"\x1b[D")
Right = KeyBase(keys=[b"\x1b[C", b"\xe0M", b"\x00M"], ansi=b"\x1b[C")
Backspace = KeyBase(keys=[b"\x7f", b"\x08"], ansi=b"\x1b[D\x1b[P")
Enter = KeyBase(keys=[b"\r", b"\n"], ansi=b"\r")


def match_key(byte_sequence: bytes) -> Union[KeyBase, None]:
    if not byte_sequence:
        return
    for key in all_keys:
        if byte_sequence in key.keys:
            return key


def match_ansi(byte_sequence: bytes) -> Union[bytes, List[bytes], None]:
    if not byte_sequence:
        return
    
    result = []
    for i in all_keys:
        for j in i.keys:
            if j.startswith(byte_sequence):
                if i == byte_sequence:
                    return i
                result.append(i)
    return result if result else None


def get_ansi_value(byte_sequence: bytes) -> Union[bytes, None]:
    key = match_key(byte_sequence)
    if key is not None:
        if callable(key.ansi):
            return key.ansi()
        else:
            return key.ansi
    elif insert_mode.insert:
        return b"\x1b[@" + byte_sequence
    return byte_sequence
