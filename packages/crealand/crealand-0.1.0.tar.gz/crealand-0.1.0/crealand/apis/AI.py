from Constant import DestType
# 人脸识别
# 机器学习
# 数字识别


class Figure:
    # 打开手写数字识别教学页面
    def open_teach_page(self):
        pass

    # 打开神经网络教学页面
    def open_NN_teach_page(self):
        pass

    # 开始手写数字识别
    def start_digital_recognition(self):
        pass

    # 结束手写数字识别
    def stop_NN_teach_page(self):
        pass

    # 识别到数字为
    def is_specified_value(self, val: int):
        pass
        return True

    # 数字识别结果
    def get_figure_value(self, val: int):
        pass
        return True

    # 清除数字识别结果
    def clear_figure_value(self, val: int):
        pass
        return True


# 手势识别
class Gesture:
    # 开始手势识别
    def start_gesture_recognition(self):
        call_api_async(DestType.WEB_IDE,'gestureRecognition',['start'])
        pass

    # 结束手势识别
    def stop_gesture_recognition(self):
        call_api(DestType.WEB_IDE,'gestureRecognition',['end'])
        pass

    # 当前手势识别结果为
    def is_specified_value(self, val: int):
        pass
        return True

    # 帽子积木块
    # def start_gesture_recognition(self):
    #     pass


# 语音识别
class Voice:
    # 开始语音识别
    @classmethod
    def start_vVoice_recognition(self):
        pass

    # 结束识别
    @classmethod
    def stop_voice_recognition(self):
        pass

    # 语音识别结果
    @classmethod
    def get_voice_value(self):
        return 0

    # 打开语音识别教学页面
    @classmethod
    def open_voice_teach_page(self):
        pass


class AI:
    def __init__(self):
        self.Figure = Figure()
        self.Gesture = Gesture()
        self.Voice = Voice()
