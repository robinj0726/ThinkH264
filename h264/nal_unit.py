class NALUnit:
    def __init__(self, bitstream):
        self._bs = bitstream
        self.forbidden_zero_bit = self._bs.f(1)
        self.nal_ref_idc = self._bs.u(2)
        self.nal_unit_type = self._bs.u(5)

    def __repr__(self):
        attrs = ', '.join(f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_'))
        return f'NALU({attrs})'
