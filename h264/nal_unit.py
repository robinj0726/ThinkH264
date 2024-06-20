from .sps import SPS

class NALUnit:
    def __init__(self, bitstream):
        self._bs = bitstream

        self.nal_unit()

    def __repr__(self):
        attrs = ', '.join(f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_'))
        return f'NALU({attrs})'

    def nal_unit(self):
        self.forbidden_zero_bit = self._bs.f(1)
        self.nal_ref_idc = self._bs.u(2)
        self.nal_unit_type = self._bs.u(5)

        if self.nal_unit_type == 14 or self.nal_unit_type == 20 or self.nal_unit_type == 21:
            if self.nal_unit_type != 21:
                self.svc_extension_flag = self._bs.u(1)
            else:
                self.avc_3d_extension_flag = self._bs.u(1)
        
        if self.nal_unit_type == 7: # SPS
            self._bs.sps = SPS(self._bs)