# call api 通信
class DestType:
    UNITY = "unity"
    WEB_IDE = "web_ide"

# 键盘按键
class KeyboardType:
    SHIFT_LEFT = "ShiftLeft"
    SHIFT_RIGHT = "ShiftRight"
    Control_Left = "ControlLeft"
    Control_Right = "ControlRight"
    SPACE = "Space"
    Arrow_Up = "ArrowUp"
    Arrow_Down = "ArrowDown"
    Arrow_Left = "ArrowLeft"
    Arrow_Right = "ArrowRight"
    A = "KeyA"
    B = "KeyB"
    C = "KeyC"
    D = "KeyD"
    E = "KeyE"
    F = "KeyF"
    G = "KeyG"
    H = "KeyH"
    I = "KeyI"
    J = "KeyJ"
    K = "KeyK"
    L = "KeyL"
    M = "KeyM"
    N = "KeyN"
    O = "KeyO"
    P = "KeyP"
    Q = "KeyQ"
    R = "KeyR"
    S = "KeyS"
    T = "KeyT"
    U = "KeyU"
    V = "KeyV"
    W = "KeyW"
    X = "KeyX"
    Y = "KeyY"
    Z = "KeyZ"
    DIGIT_0 = "Digit0"
    DIGIT_1 = "Digit1"
    DIGIT_2 = "Digit2"
    DIGIT_3 = "Digit3"
    DIGIT_4 = "Digit4"
    DIGIT_5 = "Digit5"
    DIGIT_6 = "Digit6"
    DIGIT_7 = "Digit7"
    DIGIT_8 = "Digit8"
    DIGIT_9 = "Digit9"
    NUM_0 = "Num 0"
    NUM_1 = "Num 1"
    NUM_2 = "Num 2"
    NUM_3 = "Num 3"
    NUM_4 = "Num 4"
    NUM_5 = "Num 5"
    NUM_6 = "Num 6"
    NUM_7 = "Num 7"
    NUM_8 = "Num 8"
    NUM_9 = "Num 9"

# 按键动作
class KeyActiveType:
    KEY_DOWN = "key_down"
    KEY_UP = "key_up"

# 鼠标按键
class MouseKeyType:
    LEFT = 0
    RIGHT = 1
    MIDDLE = 2

# 挂点
class HangPointType:
    BOTTOM: 1
    CAMERA: 2
    LEFT_FRONT_WHEEL: 3
    RIGHT_FRONT_WHEEL: 4
    LEFT_HAND: 10
    RIGHT_HAND: 11
    ITEM_HANGING_POINT: 100
    CAMERA_FOLLOW_POINT: 1000
    TOP: 2000




# 角色动作
class Actions:

    PICK = "Pick"
    PLACE: "Place"
    LAUGH: "Laugh"
    HAPPY: "Happy"
    THINK: "Think"
    CONFUSE: "Confuse"
    SAD: "Sad"
    TALK: "Talk"
    GREET: "Greet"
    NO: "No"
    YES: "Yes"
    LOOKAROUND: "LookAround"
    APOLOGIZE: "Apologize"
    APPLAUD: "Applaud"
    BOW: "Bow"
    ANGRY: "Angry"
    FAINT: "Faint"
    ARMRESET: "ArmReset"
    DOWNPICK: "DownPick"
    UPPICK: "UpPick"
    REPAIR: "Repair"
    STANDGUARD: "StandGuard"


# 三维坐标值
class Axis:
    X = "X"
    Y = "Y"
    Z = "Z"


# 坐标类型 本地坐标或世界坐标
class AxisType:
    LOCAL: "local"
    WORLD: "world"


# 说话语气
class Tone:
    ANGRY: "angry"
    EXPRESSION: "expression"
    SADNESS: "sadness"
    SHY: "shy"
    SURPRISE: "surprise"


# 音量大小
class Volume:
    LARGE: "large"
    MEDIUM: "medium"
    SMALL: "small"


# 立绘对话选项
class OptionName:
    OPTION01: "opt_1"
    OPTION02: "opt_2"
    OPTION03: "opt_3"


# 提示面板展示内容
class ResultType:
    SUCCESS: "success"
    FAIL: "fail"
    START: "start"


# Toast提示位置
class ToastPosition:
    TOP: "top"
    BOTTOM: "bottom"
    MIDDLE: "middle"


# Toast提示状态
class ToastState:
    DYNAMIC: "dynamic"
    STATIC: "static"


# 手势方向
class Direction:
    LEFT: "left"
    RIGHT: "right"
    UP: "up"
    DOWN: "down"


# 滤镜类型
class FilterStyle:
    FOG: "fog"


# 对象的动作
class ActionType:
    ENTER: "enter"
    LEAVE: "leave"
