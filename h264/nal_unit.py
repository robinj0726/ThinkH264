from .sps import SPS
from .pps import PPS

class NALUnit:
    def __init__(self, bits, params):
        self._bits = bits
        self._params = params

        self.nal_unit()

    def __repr__(self):
        attrs = ', '.join(f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_'))
        return f'NALU({attrs})'

    def nal_unit(self):
        if self._params["nal_unit_type"] == 14 or self._params["nal_unit_type"] == 20 or self._params["nal_unit_type"] == 21:
            if self._params["nal_unit_type"] != 21:
                self.svc_extension_flag = self._bits.u(1)
            else:
                self.avc_3d_extension_flag = self._bits.u(1)
        
