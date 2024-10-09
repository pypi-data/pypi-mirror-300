import crealand.utils.utils as utils
from crealand.utils.utils import call_api_async, call_api


class Dialogue:

    # 立绘对话 初始化
    @staticmethod
    def init(self):
        pass

    # 立绘对话 说
    @staticmethod
    def speak(self, role: str, text: str, url: str):
        pass

    # 立绘对话 说-音量
    @staticmethod
    def speak_describe(self, role: str, mood: str, volume: str, text: str, url: str):
        pass

    # 立绘对话 设置选项
    @staticmethod
    def set_options(self, opt: str, content: str):
        pass

    # 立绘对话 判断选项
    @staticmethod
    def check_options(self, opt: str):
        pass
        return True

    # 立绘对话 显示
    @staticmethod
    def set_options_show(self, show: bool):
        pass


class HelpPane:
    # 帮助面板 初始化
    @staticmethod
    def init(self):
        pass

    # 帮助面板 设置标题
    @staticmethod
    def set_title(self, title: str, url: str):
        pass

    # 帮助面板 显示
    @staticmethod
    def show(self, show: bool):
        pass


class TaskPane:

    # 任务面板 设置标题
    @staticmethod
    def set_task_title(self, title: str, name: str):
        pass

    # 任务面板 设置任务项
    @staticmethod
    def set_task_item(self, task: str, opt: str, schedule: int, total: int):
        pass

    # 任务面板 显示
    @staticmethod
    def set_task_show(self, show: bool):
        pass


class Speak:
    # 说
    @staticmethod
    def text(self, runtime_id: int, content: str, time: int):
        call_api_async(
            "unity",
            "actor.speak",
            [runtime_id, content, time],
        )

    # 说-img
    @staticmethod
    def speak_image(self, runtime_id: int, url: str, time: int):
        call_api_async(
            WEB_IDE,
            "actor.speakImage",
            [runtime_id, content, time],
        )

    # 提示面板显示
    @staticmethod
    def set_tip_show(self, show: bool):
        pass

    # 提示面板显示
    @staticmethod
    def set_toast(self, position: str, action: str, content: str):
        pass

