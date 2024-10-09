import sys


if sys.platform == "win32":
    from .win32 import Win32Input as TermInput
else:
    from .linux import LinuxInput as TermInput

from .prompts import Prompt


def read_line(timeout: float = 0, time_seq: float = 0.001, echo: bool = True, pre_func: callable = None) -> str:
    """
    ### 函数功能: 
        读取用户输入直至获取到换行符，使用示例：
        ```python
        # 读取用户输入
        user_input = read_line()
        print("用户输入：", user_input)
        # 读取用户输入，并设置超时时间为5秒
        user_input = read_line(timeout=5)
        print("用户输入：", user_input)
        # 读取用户输入，外部条件满足时结束阻塞
        sign = [False]
        def pre_func():
            return sign[0]
        user_input = read_line(pre_func=pre_func) # 阻塞时若sign[0]被设置为True，则结束阻塞
        ```

    ### Args:
        - timeout (float, optional): 允许设置超时时间，若为0则不超时. Defaults to 0.
        - time_seq (float, optional): 检测通道写入间隔，值越小用户输入越流畅. Defaults to 0.001.
        - echo (bool, optional): 是否回显. Defaults to True.
        - pre_func (callable, optional): 用于中途结束阻塞的函数. Defaults to None.

    ### Returns:
        - str: 获取到的用户输入内容，不包含换行符
    """
    return TermInput().read_line(timeout=timeout, time_seq=time_seq, echo=echo, pre_func=pre_func)


def read_char(timeout: float = 0, time_seq: float = 0.001, echo: bool = True, pre_func: callable = None) -> str:
    """
    ### 函数功能: 
        读取用户单个字符输入，类似keyboard获取按键，使用示例：
        ```python
        # 读取用户输入
        user_input = read_char()
        print("用户输入：", user_input)
        # 读取用户输入，并设置超时时间为5秒
        user_input = read_char(timeout=5)
        print("用户输入：", user_input)
        # 读取用户输入，外部条件满足时结束阻塞
        sign = [False]
        def pre_func():
            return sign[0]
        user_input = read_char(pre_func=pre_func) # 阻塞时若sign[0]被设置为True，则结束阻塞
        ```

    ### Args:
        - timeout (float, optional): 允许设置超时时间，若为0则不超时. Defaults to 0.
        - time_seq (float, optional): 检测通道写入间隔，值越小用户输入越流畅. Defaults to 0.001.
        - echo (bool, optional): 是否回显. Defaults to True.
        - pre_func (callable, optional): 用于中途结束阻塞的函数. Defaults to None.

    ### Returns:
        - str: 获取到的用户输入字符
    """
    return TermInput().read_char(timeout=timeout, time_seq=time_seq, echo=echo, pre_func=pre_func)