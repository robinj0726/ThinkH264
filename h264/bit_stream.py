from .nal_unit import NALUnit

class BitStream:
    def __init__(self, bits):
        self._bs = bits[24:]
        self.convertPayloadToRBSP()

    def __repr__(self):
        return f'BitStream(data:<{self._bs}>)'
        
    def u(self,n):
        return self._bs.read(n).uint

    def f(self,n):
        return self.u(n)

    def ue(self):
        return self._bs.read('ue')
    
    def se(self):
        return self._bs.read('se')

    def byte_aligned(self):
        return self._bs.pos % 8 == 0

    def more_data(self):
        return self._bs.pos < self._bs.length

    def more_rbsp_data(self):
        if not self.more_data():
            return False
        i = self._bs.length - 1
        while i >= 0:
            if self._bs[i] == True:
                if self._bs.pos == i:
                    return False
                else:
                    return True
            i -= 1

    # perform anti-emulation prevention
    def convertPayloadToRBSP(self):
        self._bs.replace('0x000003', '0x0000', bytealigned=True)

    
