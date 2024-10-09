CUT_LINE = "=" * 50


# TODO checkbox 类型还没有实现
class Prompt:
    @staticmethod
    def input_box(prompt: str) -> str:
        return "\r\n".join([CUT_LINE, prompt])

    @staticmethod
    def selector(prompt: str, options: list) -> str:
        return "\r\n".join(
            [
                CUT_LINE,
                prompt,
                "\r\n".join([f"{i+1}. {option}" for i, option in enumerate(options)]),
                CUT_LINE,
                "请选择: ",
            ]
        )

    @staticmethod
    def confirm(prompt: str) -> str:
        return "\r\n".join([CUT_LINE, prompt, CUT_LINE, "请确认: (y/n)"])

    @staticmethod
    def msgbox(prompt: str) -> str:
        return "\r\n".join([CUT_LINE, prompt, CUT_LINE, "请按任意键继续..."])
