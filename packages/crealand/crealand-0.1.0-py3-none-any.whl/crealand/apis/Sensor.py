from Constant import DestType


# 超声波传感器

class Ultrasonic:

    _sensors = {}
     
    #添加一个超声波 并设置绑定对象及挂点
    def add_sensor(self, name: str, id: int, point: int):
        self._sensors[name] = (id, point)

    def get_sensor(self, name: str)->Dict[str, int]:
        return self._sensors[name]
    
    # 获取距离
    async def get_obstacle_distance(self, sensor: List[int]):
        length=await call_api(DestType.UNITY,'sensor.rayRanging',[sensor[0], sensor[1]])
        return length


class Auditory:

    # 获取声音强度
    def get_decibel_value(self):
        return 0

    # 开始分贝识别
    def start_decibel_recognition(self):
        return 0

    # 结束分贝识别
    def stop_decibel_recognition(self):
        return 0

    # 判断声音强度
    def check_decibel_value(self, operators: str, decibel: float):
        return 0


class Visual:
    _sensors = {}

    def __init__(self):
        self.set_sensor = set_sensor_impl
        self.get_sensor = get_sensor_impl

    # 将传感器绑定到对象的挂点
    def set_sensor_impl(self, name: str, id: int, point: int):
        self._sensors[name] = (id, point)
        pass

    # 获取传感器信息
    def get_sensor_impl(self, name: str):
        return self._sensors[name]

    # 获取传感器画面
    def open_visual_sensor(self, is_open: bool=True, sensor_info: List[int]):
        if is_open:
            func_name = 'sensor.openVirsual'
        else:
            func_name = 'sensor.closeVirsual'
        call_api(DestType.UNITY,func_name,[sensor_info[0], sensor_info[1]])
        pass

    # 获取传感器信息
    def get_sensor(self, name: str):
        return self.get_sensor_impl(name)


class Temperature:

    _sensors = {}

    def __init__(self,name,id):
        self.data={name:name,id:id}
        self.set_sensor = set_sensor_impl
        self.get_sensor = get_sensor_impl

    # 将传感器绑定到对象的挂点
    def set_sensor_impl(self, name: str, id: int, point: int):
        self._sensors[name] = (id, point)
        call_api(DestType.UNITY,'sensor.attachTemperature',[id])
        pass
    
    # 获取传感器信息
    def get_sensor_impl(self, name: str):
        return self._sensors[name]
    
    # 设置判定区域温度

    def set_temperature(self, area_id: int, temp_val: float):
        call_api(DestType.UNITY,'sensor.setTemperature',[area_id,temp_val])
        pass

    # 持续检测判定区域温度

    def continuously_monitor_temperature(self, area: int):
        pass

    # 获取温度值

    def get_temperature_value(self, id: int, point: int):
        call_api(DestType.UNITY,'sensor.getTemperature',[id,point])
        return 10


class Humidity:

    _sensors = {}

    def __init__(self):
        self.set_sensor = set_sensor_impl
        self.get_sensor = get_sensor_impl

    # 将传感器绑定到对象的挂点
    def set_sensor_impl(self, name: str, id: int, point: int):
        self._sensors[name] = (id, point)
        pass
    
    # 获取传感器信息
    def get_sensor_impl(self, name: str):
        return self._sensors[name]

    # 设置判定区域湿度

    def set_humidity(self, area_id: int, humidity_val: float):
        call_api(DestType.UNITY,'sensor.setHumidity',[area_id,humidity_val])
        pass

    # 持续检测判定区域湿度

    def continuously_monitor_humidity(self, area: int):
        pass

    # 获取湿度值

    def get_humidity_value(self, humidity_sensor: List[int]):
        call_api(DestType.UNITY,'sensor.getHumidity',[humidity_sensor[0],humidity_sensor[1]])
        return 10

    # 判断湿度值

    def check_humidity_value(self, sensor_info: dict, operators: str, humidity_val: float):
        return 10


class Gravity:

    _sensors = {}

    def __init__(self):
        self.set_sensor = set_sensor_impl
        self.get_sensor = get_sensor_impl

    # 将传感器绑定到对象的挂点
    def set_sensor_impl(self, name: str, id: int):
        self._sensors[name] = id
        call_api(DestType.UNITY,'sensor.attachGravity',[id])
        pass
    
    # 获取传感器信息
    def get_sensor_impl(self, name: str):
        return self._sensors[name]

    # 设置对象重力

    def set_gravity(self, sensor_name: str, val: float):
        sensor_info = self._sensors[sensor_name]
        call_api(DestType.UNITY,'sensor.setGravity',[sensor_info[0],val])
        pass

    # 获取重力值

    def get_gravity_value(self, sensor_info: dict):
        call_api(DestType.UNITY,'sensor.getGravity',[sensor_info[0]])
        return 10


class Sensor:
    def __init__(self):
        self.Ultrasonic = Ultrasonic()
        self.Auditory = Auditory()
        self.Visual = Visual()
        self.Temperature = Temperature()
        self.Humidity = Humidity()
        self.Gravity = Gravity()


Sensor = Sensor()
