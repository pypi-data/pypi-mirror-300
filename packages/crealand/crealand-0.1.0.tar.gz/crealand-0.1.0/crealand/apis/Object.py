import crealand.utils.utils as utils
from crealand.utils.utils import call_api, call_api_async


# 信息
class Info:

    # 别名对象id
    @staticmethod
    def get_alias_id(self, nickname: str = "别名1"):
        result = call_api("unity", "alias.getByAlias", [nickname])
        return result

    # 获取configID的对象id
    @staticmethod
    def get_object_id(self, runtime_id) -> int:
        result = call_api("unity", "actor.getConfigID", [runtime_id])
        return result

    # 获取对象的空间坐标
    @staticmethod
    def get_object_coordinates(self, runtime_id: int) -> list[float]:
        result = call_api("unity", "actor.getCoordinate", [runtime_id])
        return result

    # 获取判定区域中的对象id
    @staticmethod
    def get_id_in_area(self, area_id: int, config_ids: list[str]) -> list[int]:
        result = call_api(
            "unity", "editableTrigger.getContentRuntimeIds", [area_id, config_ids]
        )
        return result

    # 获取空间坐标某个轴的值
    @staticmethod
    def get_spatial_coordinates(self, coordinate: list[float], axis: str) -> float:
        AXIS = {"X": 0, "Y": 1, "Z": 2}
        return coordinate[AXIS[axis]]

    # 获取对象的运动方向向量
    @staticmethod
    def get_motion_vector(self, runtime_id: int) -> list[float]:
        result = call_api("unity", "character.getMoveDirection", [runtime_id])
        return result


class Camera:
    @classmethod
    def get_default_id(self):
        return call_api_async("unity", "camera.getDefaultID")

    # 获取空间坐标
    @classmethod
    def get_object_coordinates(self, runtime_id: int) -> list[float]:
        result = call_api("unity", "actor.getCoordinate", [runtime_id])
        return result

    # 相机移动
    @classmethod
    def move_to(self, time: float, coordinate: list[float], block: bool):
        new_time = utils.value_range(time, 0)
        call_api_async(
            "unity",
            "camera.moveTo",
            [self.get_default_id(), new_time, coordinate, block],
        )

    # 调整FOV
    @classmethod
    def adjust_FOV(self, time: float, fov: float):
        new_time = utils.value_range(time, 0)

        new_fov = utils.value_range(fov, 60, 120)
        call_api_async(
            "unity", "camera.adjustFOV", [self.get_default_id(), new_time, new_fov]
        )

    # 相机锁定朝向并移动
    @classmethod
    def move_while_looking(
        self,
        coordinate_1: list[float],
        time: float,
        coordinate_2: list[float],
        block: bool,
    ):
        new_time = utils.value_range(time, 0)
        call_api_async(
            "unity",
            "camera.moveWhileLooking",
            [self.get_default_id(), new_time, coordinate_2, coordinate_1, block],
        )

    # 获取相机坐标
    @classmethod
    def get_camera_coordinate(self) -> list[float]:
        call_api_async(
            "unity",
            "camera.moveWhileLooking",
            [
                self.get_object_coordinates(get_default_id()),
            ],
        )

    # 相机朝向
    @classmethod
    def look_at(self, coordinate: list[float]):
        call_api_async(
            "unity",
            "camera.lookAt",
            [
                self.get_object_coordinates(get_default_id()),
            ],
        )

    # 相机跟随
    @classmethod
    def follow_target(self, runtime_id: int, distance: float, is_rotate: bool):
        call_api_async(
            "unity",
            "camera.followTarget",
            [self.get_default_id(), runtime_id, distance, is_rotate],
        )

    # 相机结束跟随
    @classmethod
    def end_follow_target(self):
        call_api_async(
            "unity",
            "camera.stopFollowing",
            [
                self.get_default_id(),
            ],
        )

    # 相机跟随
    @classmethod
    def filters(self, filter_name: str, state: bool):
        CAMERA_EFFECTS = {"fog": 1}
        STATES = {"start": True, "stop": False}
        call_api_async(
            "unity",
            "camera.openEffect",
            [self.get_default_id(), CAMERA_EFFECTS[filter_name], STATES[state]],
        )


class Motion:
    # 创建对象
    @classmethod
    def create_object_coordinate(self, config_id: str, coordinate: list[float]):
        result = call_api_async(
            "unity",
            "actor.createObject",
            [config_id, coordinate],
        )

    # 移动
    @staticmethod
    def move_to(self, runtime_id: int, coordinate: list[float]):
        call_api_async(
            "unity",
            "actor.setObjectPosition",
            [
                runtime_id,
                coordinate,
            ],
        )

    # 朝向
    @staticmethod
    def face_towards(self, runtime_id: int, coordinate: list[float]):
        call_api_async(
            "unity",
            "actor.setObjectTowardPosition",
            [
                runtime_id,
                coordinate,
            ],
        )

    # 前进
    @staticmethod
    def move_forward(self, runtime_id: int, speed: float, distance: float, block: bool):
        new_speed = utils.value_range(speed, 1, 5)
        call_api_async(
            "unity",
            "actor.moveForwardByDistance",
            [
                runtime_id,
                speed,
                distance,
                block,
            ],
        )

    # 对象旋转
    @staticmethod
    def rotate(self, runtime_id: int, time: float, degree: float, block: bool):
        new_time = utils.value_range(time, 0)
        call_api_async(
            "unity",
            "actor.rotateUpAxisByAngle",
            [
                runtime_id,
                time,
                degree,
                block,
            ],
        )

    # 云台旋转
    @staticmethod
    def ptz(self, runtime_id: int, degree: float):
        call_api_async(
            "unity",
            "actor.rotateUpAxisByAngle",
            [
                runtime_id,
                degree,
            ],
        )

    # 播放动作
    @staticmethod
    def action(self, runtime_id: int, active: str, block: bool):
        call_api_async(
            "unity",
            "actor.playAnimation",
            [runtime_id, active, block],
        )

    # # 将对象吸附到挂点
    # @staticmethod
    # def attach_to_anchor_point(self, adsorbed_id: int, adsorb_id: int, point: int):
    #     call_api_async("unity",
    #         "actor.bindAnchor",
    #         [runtime_id, attachment_id_1, runtime_id_2, attachment_id_2],
    #     )

    # 绑定挂点
    @staticmethod
    def bind_to_object_point(
        self,
        runtime_id_1: int,
        attachment_id_1: str,
        runtime_id_2: int,
        attachment_id_2: str,
    ):
        call_api_async(
            "unity",
            "actor.bindAnchor",
            [runtime_id, attachment_id_1, runtime_id_2, attachment_id_2],
        )

    # 解除绑定
    @staticmethod
    def detach(self, runtime_id: int):
        call_api_async(
            "unity",
            "actor.detach",
            [
                runtime_id,
            ],
        )

    # 向画面空间前进
    @staticmethod
    def move_towards_screen_space(
        self, runtime_id: int, speed: float, direction: list[float]
    ):
        new_speed = utils.value_range(speed, 1, 5)
        call_api_async(
            "unity",
            "actor.moveByVelocity",
            [
                runtime_id,
                2,
                new_speed,
                direction,
            ],
        )

    # 旋转运动方向向量
    @staticmethod
    def rotate_to_direction(
        self, runtime_id: int, angle: float, direction: list[float]
    ):
        call_api_async(
            "unity",
            "actor.rotateUpAxisByDirection",
            [runtime_id, angle, direction, False],
        )

    # 停止运动
    @staticmethod
    def stop_move(self, runtime_id: int):
        call_api_async(
            "unity",
            "character.stop",
            [runtime_id],
        )

    # 设置别名
    @classmethod
    def create_object(self, coordinate: list[float], config_id: int, nickname: str):
        call_api_async(
            "unity",
            "alias.setAlias",
            [
                nickname,
                self.create_object_coordinate(config_id, coordinate),
            ],
        )

    # 销毁对象
    @staticmethod
    def destroy(self, runtime_id: int):
        call_api_async(
            "unity",
            "alias.destoryObject",
            [
                runtime_id,
            ],
        )

    # 上升
    @staticmethod
    def rise(self, runtime_id: int, speed: float, height: float, block: bool):
        new_speed = utils.value_range(speed, 1, 5)
        call_api_async(
            "unity",
            "alias.moveUpByDistance",
            [runtime_id, height, new_speed, block],
        )

    # 获取离自身距离的坐标
    @staticmethod
    def get_object_local_position(
        self, runtime_id: int, coordinate: list[float], distance: float
    ):
        result = call_api_async(
            "unity",
            "alias.getObjectLocalPosition",
            [runtime_id, coordinate, distance],
        )
        return result

    # 移动到指定坐标
    @staticmethod
    def move_by_point(
        self, runtime_id: int, time: float, coordinate: list[float], block: bool
    ):
        new_time = utils.value_range(time, 0)
        call_api_async(
            "unity",
            "alias.moveByPoint",
            [runtime_id, new_time, coordinate, block],
        )

    # 绕坐标轴旋转
    @staticmethod
    def rotate_by_origin_and_axis(
        self,
        runtime_id: int,
        time: float,
        point_1: str,
        coordinate_1: list[float],
        point_2: str,
        coordinate_2: list[float],
        angle: float,
        block: bool,
    ):
        new_time = utils.value_range(time, 0)
        call_api_async(
            "unity",
            "alias.rotateByOringinAndAxis",
            [
                runtime_id,
                coordinate_1,
                point_1,
                coordinate_2,
                point_2,
                angle,
                new_time,
                block,
            ],
        )


class Property:
    # 新增自定义属性
    @staticmethod
    def add_attr(self, runtime_id: int, attr_name: str, attr_value: str):
        call_api(
            "unity",
            "actor.addCustomProp",
            [runtime_id, attr_name, attr_value],
        )

    # 删除自定义属性
    @staticmethod
    def del_attr(self, runtime_id: int, attr_name: str):
        call_api(
            "unity",
            "actor.delCustomProp",
            [runtime_id, attr_name],
        )

    # 修改自定义属性
    @staticmethod
    def set_attr(self, runtime_id: int, attr_name: str, attr_value: str):
        call_api(
            "unity",
            "actor.setCustomProp",
            [runtime_id, attr_name, attr_value],
        )

    # 获取自定义属性的值
    @staticmethod
    def get_value(self, runtime_id: int, attr_name: str):
        call_api(
            "unity",
            "actor.getCustomProp",
            [runtime_id, attr_name],
        )

    # 获取自定义属性组中某一项的值
    @staticmethod
    def get_value_by_Idx(self, runtime_id: int, index: int):
        call_api(
            "unity",
            "actor.getCustomPropValueByIdx",
            [runtime_id, index],
        )

    # 获取自定义属性组中某一项的名称
    @staticmethod
    def get_key_by_Idx(self, runtime_id: int, index: int):
        call_api(
            "unity",
            "actor.getCustomPropKeyByIdx",
            [runtime_id, index],
        )


class Show:
    # 3d文本
    # @staticmethod def set_3D_text_status_rgb(self, runtime_id: int, color: str, size: int, text: str):
    #
    #     if color[0] == '#':
    #         color = webcolors.hex_to_rgb(color)
    #         color = webcolors.name_to_hex(color)
    #     else:
    #         color = webcolors.name_to_hex(color)
    #         color = webcolors.hex_to_rgb(color)
    #
    #     print(webcolors.hex_to_name("#daa520"), color[0], {'R': color[0], 'G': color[1], 'B': color[2]})

    # 3d文本-RGB
    @staticmethod
    def set_3D_text_status_rgb(
        self, runtime_id: int, rgb: list[int], size: int, text: str
    ):
        call_api(
            "unity",
            "actor.set3DTextStatus",
            [runtime_id, rgb, size, text],
        )


class Object:
    @classmethod
    def __init__(self):
        self.Info = Info()
        self.Camera = Camera()
        self.Motion = Motion()
        self.Property = Property()
        self.Show = Show()


Object = Object()

print(utils.value_range(-20, 1, 5))
