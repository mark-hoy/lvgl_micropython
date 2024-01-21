import time
from micropython import const  # NOQA

import lvgl as lv  # NOQA
import lcd_bus  # NOQA
import display_driver_framework


_SWRST = const(0x0100)
_DISPOFF = const(0x2800)
_DISPON = const(0x2900)

_CASET = const(0x2A00)
_PASET = const(0x2B00)
_RAMWR = const(0x2C00)

_MAD_H_FLIP = const(0x02)
_MAD_V_FLIP = const(0x01)
_MADCTL = const(0x3600)

STATE_HIGH = display_driver_framework.STATE_HIGH
STATE_LOW = display_driver_framework.STATE_LOW
STATE_PWM = display_driver_framework.STATE_PWM

BYTE_ORDER_RGB = display_driver_framework.BYTE_ORDER_RGB
BYTE_ORDER_BGR = display_driver_framework.BYTE_ORDER_BGR


class RM68120(display_driver_framework.DisplayDriver):
    _INVOFF = 0x2000
    _INVON = 0x2100

    def _set_memory_location(self, x1, y1, x2, y2):
        # Column addresses
        param_buf = self._param_buf

        param_buf[0] = (x1 >> 8) & 0xFF
        param_buf[1] = x1 & 0xFF
        param_buf[2] = (x2 >> 8) & 0xFF
        param_buf[3] = x2 & 0xFF

        self._data_bus.tx_param(_CASET, self._param_mv[:4])

        # Page addresses
        param_buf[0] = (y1 >> 8) & 0xFF
        param_buf[1] = y1 & 0xFF
        param_buf[2] = (y2 >> 8) & 0xFF
        param_buf[3] = y2 & 0xFF

        self._data_bus.tx_param(_PASET, self._param_mv[:4])

        return _RAMWR

    def init(self):
        self.set_params(0xF000, bytearray([0x55]))
        self.set_params(0xF001, bytearray([0xAA]))
        self.set_params(0xF002, bytearray([0x52]))
        self.set_params(0xF003, bytearray([0x08]))
        self.set_params(0xF004, bytearray([0x01]))
        self.set_params(0xF004)

        self.set_params(0xD400, bytearray([0x00]))
        self.set_params(0xD401, bytearray([0x00]))
        self.set_params(0xD402, bytearray([0x1b]))
        self.set_params(0xD403, bytearray([0x44]))
        self.set_params(0xD404, bytearray([0x62]))
        self.set_params(0xD405, bytearray([0x00]))
        self.set_params(0xD406, bytearray([0x7b]))
        self.set_params(0xD407, bytearray([0xa1]))
        self.set_params(0xD408, bytearray([0xc0]))
        self.set_params(0xD409, bytearray([0xee]))
        self.set_params(0xD40A, bytearray([0x55]))
        self.set_params(0xD40B, bytearray([0x10]))
        self.set_params(0xD40C, bytearray([0x2c]))
        self.set_params(0xD40D, bytearray([0x43]))
        self.set_params(0xD40E, bytearray([0x57]))
        self.set_params(0xD40F, bytearray([0x55]))
        self.set_params(0xD410, bytearray([0x68]))
        self.set_params(0xD411, bytearray([0x78]))
        self.set_params(0xD412, bytearray([0x87]))
        self.set_params(0xD413, bytearray([0x94]))
        self.set_params(0xD414, bytearray([0x55]))
        self.set_params(0xD415, bytearray([0xa0]))
        self.set_params(0xD416, bytearray([0xac]))
        self.set_params(0xD417, bytearray([0xb6]))
        self.set_params(0xD418, bytearray([0xc1]))
        self.set_params(0xD419, bytearray([0x55]))
        self.set_params(0xD41A, bytearray([0xcb]))
        self.set_params(0xD41B, bytearray([0xcd]))
        self.set_params(0xD41C, bytearray([0xd6]))
        self.set_params(0xD41D, bytearray([0xdf]))
        self.set_params(0xD41E, bytearray([0x95]))
        self.set_params(0xD41F, bytearray([0xe8]))
        self.set_params(0xD420, bytearray([0xf1]))
        self.set_params(0xD421, bytearray([0xfa]))
        self.set_params(0xD422, bytearray([0x02]))
        self.set_params(0xD423, bytearray([0xaa]))
        self.set_params(0xD424, bytearray([0x0b]))
        self.set_params(0xD425, bytearray([0x13]))
        self.set_params(0xD426, bytearray([0x1d]))
        self.set_params(0xD427, bytearray([0x26]))
        self.set_params(0xD428, bytearray([0xaa]))
        self.set_params(0xD429, bytearray([0x30]))
        self.set_params(0xD42A, bytearray([0x3c]))
        self.set_params(0xD42B, bytearray([0x4A]))
        self.set_params(0xD42C, bytearray([0x63]))
        self.set_params(0xD42D, bytearray([0xea]))
        self.set_params(0xD42E, bytearray([0x79]))
        self.set_params(0xD42F, bytearray([0xa6]))
        self.set_params(0xD430, bytearray([0xd0]))
        self.set_params(0xD431, bytearray([0x20]))
        self.set_params(0xD432, bytearray([0x0f]))
        self.set_params(0xD433, bytearray([0x8e]))
        self.set_params(0xD434, bytearray([0xff]))

        self.set_params(0xD500, bytearray([0x00]))
        self.set_params(0xD501, bytearray([0x00]))
        self.set_params(0xD502, bytearray([0x1b]))
        self.set_params(0xD503, bytearray([0x44]))
        self.set_params(0xD504, bytearray([0x62]))
        self.set_params(0xD505, bytearray([0x00]))
        self.set_params(0xD506, bytearray([0x7b]))
        self.set_params(0xD507, bytearray([0xa1]))
        self.set_params(0xD508, bytearray([0xc0]))
        self.set_params(0xD509, bytearray([0xee]))
        self.set_params(0xD50A, bytearray([0x55]))
        self.set_params(0xD50B, bytearray([0x10]))
        self.set_params(0xD50C, bytearray([0x2c]))
        self.set_params(0xD50D, bytearray([0x43]))
        self.set_params(0xD50E, bytearray([0x57]))
        self.set_params(0xD50F, bytearray([0x55]))
        self.set_params(0xD510, bytearray([0x68]))
        self.set_params(0xD511, bytearray([0x78]))
        self.set_params(0xD512, bytearray([0x87]))
        self.set_params(0xD513, bytearray([0x94]))
        self.set_params(0xD514, bytearray([0x55]))
        self.set_params(0xD515, bytearray([0xa0]))
        self.set_params(0xD516, bytearray([0xac]))
        self.set_params(0xD517, bytearray([0xb6]))
        self.set_params(0xD518, bytearray([0xc1]))
        self.set_params(0xD519, bytearray([0x55]))
        self.set_params(0xD51A, bytearray([0xcb]))
        self.set_params(0xD51B, bytearray([0xcd]))
        self.set_params(0xD51C, bytearray([0xd6]))
        self.set_params(0xD51D, bytearray([0xdf]))
        self.set_params(0xD51E, bytearray([0x95]))
        self.set_params(0xD51F, bytearray([0xe8]))
        self.set_params(0xD520, bytearray([0xf1]))
        self.set_params(0xD521, bytearray([0xfa]))
        self.set_params(0xD522, bytearray([0x02]))
        self.set_params(0xD523, bytearray([0xaa]))
        self.set_params(0xD524, bytearray([0x0b]))
        self.set_params(0xD525, bytearray([0x13]))
        self.set_params(0xD526, bytearray([0x1d]))
        self.set_params(0xD527, bytearray([0x26]))
        self.set_params(0xD528, bytearray([0xaa]))
        self.set_params(0xD529, bytearray([0x30]))
        self.set_params(0xD52A, bytearray([0x3c]))
        self.set_params(0xD52B, bytearray([0x4a]))
        self.set_params(0xD52C, bytearray([0x63]))
        self.set_params(0xD52D, bytearray([0xea]))
        self.set_params(0xD52E, bytearray([0x79]))
        self.set_params(0xD52F, bytearray([0xa6]))
        self.set_params(0xD530, bytearray([0xd0]))
        self.set_params(0xD531, bytearray([0x20]))
        self.set_params(0xD532, bytearray([0x0f]))
        self.set_params(0xD533, bytearray([0x8e]))
        self.set_params(0xD534, bytearray([0xff]))

        self.set_params(0xD600, bytearray([0x00]))
        self.set_params(0xD601, bytearray([0x00]))
        self.set_params(0xD602, bytearray([0x1b]))
        self.set_params(0xD603, bytearray([0x44]))
        self.set_params(0xD604, bytearray([0x62]))
        self.set_params(0xD605, bytearray([0x00]))
        self.set_params(0xD606, bytearray([0x7b]))
        self.set_params(0xD607, bytearray([0xa1]))
        self.set_params(0xD608, bytearray([0xc0]))
        self.set_params(0xD609, bytearray([0xee]))
        self.set_params(0xD60A, bytearray([0x55]))
        self.set_params(0xD60B, bytearray([0x10]))
        self.set_params(0xD60C, bytearray([0x2c]))
        self.set_params(0xD60D, bytearray([0x43]))
        self.set_params(0xD60E, bytearray([0x57]))
        self.set_params(0xD60F, bytearray([0x55]))
        self.set_params(0xD610, bytearray([0x68]))
        self.set_params(0xD611, bytearray([0x78]))
        self.set_params(0xD612, bytearray([0x87]))
        self.set_params(0xD613, bytearray([0x94]))
        self.set_params(0xD614, bytearray([0x55]))
        self.set_params(0xD615, bytearray([0xa0]))
        self.set_params(0xD616, bytearray([0xac]))
        self.set_params(0xD617, bytearray([0xb6]))
        self.set_params(0xD618, bytearray([0xc1]))
        self.set_params(0xD619, bytearray([0x55]))
        self.set_params(0xD61A, bytearray([0xcb]))
        self.set_params(0xD61B, bytearray([0xcd]))
        self.set_params(0xD61C, bytearray([0xd6]))
        self.set_params(0xD61D, bytearray([0xdf]))
        self.set_params(0xD61E, bytearray([0x95]))
        self.set_params(0xD61F, bytearray([0xe8]))
        self.set_params(0xD620, bytearray([0xf1]))
        self.set_params(0xD621, bytearray([0xfa]))
        self.set_params(0xD622, bytearray([0x02]))
        self.set_params(0xD623, bytearray([0xaa]))
        self.set_params(0xD624, bytearray([0x0b]))
        self.set_params(0xD625, bytearray([0x13]))
        self.set_params(0xD626, bytearray([0x1d]))
        self.set_params(0xD627, bytearray([0x26]))
        self.set_params(0xD628, bytearray([0xaa]))
        self.set_params(0xD629, bytearray([0x30]))
        self.set_params(0xD62A, bytearray([0x3c]))
        self.set_params(0xD62B, bytearray([0x4A]))
        self.set_params(0xD62C, bytearray([0x63]))
        self.set_params(0xD62D, bytearray([0xea]))
        self.set_params(0xD62E, bytearray([0x79]))
        self.set_params(0xD62F, bytearray([0xa6]))
        self.set_params(0xD630, bytearray([0xd0]))
        self.set_params(0xD631, bytearray([0x20]))
        self.set_params(0xD632, bytearray([0x0f]))
        self.set_params(0xD633, bytearray([0x8e]))
        self.set_params(0xD634, bytearray([0xff]))

        self.set_params(0xB000, bytearray([0x05]))
        self.set_params(0xB001, bytearray([0x05]))
        self.set_params(0xB002, bytearray([0x05]))

        self.set_params(0xB100, bytearray([0x05]))
        self.set_params(0xB101, bytearray([0x05]))
        self.set_params(0xB102, bytearray([0x05]))

        self.set_params(0xB600, bytearray([0x34]))
        self.set_params(0xB601, bytearray([0x34]))
        self.set_params(0xB603, bytearray([0x34]))

        self.set_params(0xB700, bytearray([0x24]))
        self.set_params(0xB701, bytearray([0x24]))
        self.set_params(0xB702, bytearray([0x24]))

        self.set_params(0xB800, bytearray([0x24]))
        self.set_params(0xB801, bytearray([0x24]))
        self.set_params(0xB802, bytearray([0x24]))

        self.set_params(0xBA00, bytearray([0x14]))
        self.set_params(0xBA01, bytearray([0x14]))
        self.set_params(0xBA02, bytearray([0x14]))

        self.set_params(0xB900, bytearray([0x24]))
        self.set_params(0xB901, bytearray([0x24]))
        self.set_params(0xB902, bytearray([0x24]))

        self.set_params(0xBc00, bytearray([0x00]))
        self.set_params(0xBc01, bytearray([0xa0]))  # vgmp=5.0
        self.set_params(0xBc02, bytearray([0x00]))
        self.set_params(0xBd00, bytearray([0x00]))
        self.set_params(0xBd01, bytearray([0xa0]))  # vgmn=5.0
        self.set_params(0xBd02, bytearray([0x00]))

        self.set_params(0xBe01, bytearray([0x3d]))  # 3

        self.set_params(0xF000, bytearray([0x55]))
        self.set_params(0xF001, bytearray([0xAA]))
        self.set_params(0xF002, bytearray([0x52]))
        self.set_params(0xF003, bytearray([0x08]))
        self.set_params(0xF004, bytearray([0x00]))

        self.set_params(0xB400, bytearray([0x10]))

        self.set_params(0xBC00, bytearray([0x05]))
        self.set_params(0xBC01, bytearray([0x05]))
        self.set_params(0xBC02, bytearray([0x05]))

        self.set_params(0xB700, bytearray([0x22]))  # GATE EQ CONTROL
        self.set_params(0xB701, bytearray([0x22]))  # GATE EQ CONTROL
        self.set_params(0xC80B, bytearray([0x2A]))  # DISPLAY TIMING CONTROL
        self.set_params(0xC80C, bytearray([0x2A]))  # DISPLAY TIMING CONTROL
        self.set_params(0xC80F, bytearray([0x2A]))  # DISPLAY TIMING CONTROL
        self.set_params(0xC810, bytearray([0x2A]))  # DISPLAY TIMING CONTROL

        self.set_params(0xd000, bytearray([0x01]))

        self.set_params(0xb300, bytearray([0x10]))

        self.set_params(0xBd02, bytearray([0x07]))

        self.set_params(0xBe02, bytearray([0x07]))

        self.set_params(0xBf02, bytearray([0x07]))

        self.set_params(0xF000, bytearray([0x55]))
        self.set_params(0xF001, bytearray([0xAA]))
        self.set_params(0xF002, bytearray([0x52]))
        self.set_params(0xF003, bytearray([0x08]))
        self.set_params(0xF004, bytearray([0x02]))

        self.set_params(0xc301, bytearray([0xa9]))

        self.set_params(0xfe01, bytearray([0x94]))

        self.set_params(0xf600, bytearray([0x60]))

        self.set_params(0x3500, bytearray([0x00]))
        self.set_params(0xFFFF, bytearray([0xFF]))

        time.sleep_ms(100)  # NOQA
        self.set_params(0x1100)

        time.sleep_ms(100)  # NOQA
        self.set_params(0x2900)

        self.set_params(0x3A00, bytearray([0x00, 0x55]))
        self.set_params(_MADCTL, bytearray([0x00, self._color_byte_order]))

    def set_rotation(self, value):
        rot0 = lv.DISPLAY_ROTATION._0  # NOQA
        rot90 = lv.DISPLAY_ROTATION._90  # NOQA
        rot180 = lv.DISPLAY_ROTATION._180  # NOQA
        rot270 = lv.DISPLAY_ROTATION._270  # NOQA

        if (
            (
                self._rotation in (rot0, rot180) and
                value in (rot90, rot270)
            ) or (
                self._rotation in (rot90, rot270) and
                value in (rot0, rot180)
            )
        ):
            width = self._disp_drv.get_horizontal_resolution()
            height = self._disp_drv.get_vertical_resolution()
            self._disp_drv.set_resolution(height, width)

            self._offset_x, self._offset_y = self._offset_y, self._offset_x

        self._rotation = value

        if self._initilized:
            param_buf = bytearray([
                0x00,
                self._madctl(
                    self._color_byte_order,
                    ~value,
                    display_driver_framework._ORIENTATION_TABLE  # NOQA
                )
            ])
            self._data_bus.tx_param(_MADCTL, param_buf)
