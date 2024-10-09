import time
import asyncio


class TimeoutIter:
    def __init__(self, timeout: float = 0, time_seq: float = 0.001, pre_func=None) -> None:
        """
        ### Class:
            用于创建一个延时迭代器，初始化时记录当前时间，每次迭代检查是否超时，超时则结束迭代过程，否则延时time_seq时间后进入下一轮循环；
            使用方法:
            ```
            # 每隔1s执行一轮循环，直至运行时间超过10s，每次循环中打印一次当前运行时间
            for i in TimeoutIter(10, time_seq=1):
                print(i)
            ```

        ### Args:
            - timeout (int, optional): 超时时间. Defaults to 0.
            - time_seq (float, optional): 每次循环的延时时间. Defaults to 0.001.
            - pre_func (fuction, optional): 提前中止循环的判断函数. Defaults to None.
        """
        self.timeout = timeout
        self.time_seq = time_seq
        self.start_time = time.time()
        self.pre_func = pre_func if pre_func else lambda: True

    def __iter__(self):
        return self

    def __aiter__(self):
        return self

    def __next__(self):
        now_time = time.time()
        _time = now_time - self.start_time
        if self.pre_func() and (_time < self.timeout or self.timeout == 0):
            if self.time_seq:
                time.sleep(self.time_seq)
            return time.time() - self.start_time
        else:
            raise StopIteration

    async def __anext__(self):
        now_time = time.time()
        _time = now_time - self.start_time
        if self.pre_func() and (_time < self.timeout or self.timeout == 0):
            if self.time_seq:
                await asyncio.sleep(self.time_seq)
            return time.time() - self.start_time
        else:
            raise StopIteration