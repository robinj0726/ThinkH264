class NALUnit:
    def __init__(self, bits):
        self._bits = bits
        # self.NumBytesInRBSP = 0 
        # self.nalUnitHeaderBytes = 1

        self.nal_unit()

    def __repr__(self):
        attrs = ', '.join(f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_'))
        return f'NALU({attrs})'

    def nal_unit(self):
        self.forbidden_zero_bit = self._bits.f(1)
        self.nal_ref_idc = self._bits.u(2)
        self.nal_unit_type = self._bits.u(5)

        print(f"Annex B NALU w/ long/short startcode, len {len(self._bits)}, forbidden_bit {self.forbidden_zero_bit}, nal_reference_idc {self.nal_ref_idc}, nal_unit_type {self.nal_unit_type}")
        print("")
        
        if self.nal_unit_type == 14 or self.nal_unit_type == 20 or self.nal_unit_type == 21:
            if self.nal_unit_type != 21:
                self.svc_extension_flag = self._bits.u(1)
            else:
                self.avc_extension_flag = self._bits.u(1)
            if self.svc_extension_flag:
                self.nal_unit_header_svc_extension()
                self.nalUnitHeaderBytes += 3
            elif self.avc_extension_flag:
                self.nal_unit_header_avc_extension()
                self.nalUnitHeaderBytes += 2
            else:
                self.nal_unit_header_mvc_extension()
                self.nalUnitHeaderBytes += 3

    def nal_unit_header_svc_extension(self):
        pass

    def nal_unit_header_avc_extension(self):
        pass

    def nal_unit_header_mvc_extension(self):
        pass