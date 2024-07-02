class NALUnit:
    def __init__(self, bits):
        self._bits = bits

        self.nal_unit()

    def __repr__(self):
        attrs = ', '.join(f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_'))
        return f'NALU({attrs})'

    # perform anti-emulation prevention
    def nal_to_rbsp(self):
        self._bits.replace('0x000003', '0x0000', bytealigned=True)

    def nal_unit(self):
        self.forbidden_zero_bit = self._bits.f(1)
        self.nal_ref_idc = self._bits.u(2)
        self.nal_unit_type = self._bits.u(5)

        self.nal_to_rbsp()        
