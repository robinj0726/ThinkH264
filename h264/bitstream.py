from .nalunit import NALUnit

class H264BitStream:
    def __init__(self, bits):
        self._bits = bits[24:]

        # function delegation
        self.replace = self._bits.replace

    @property
    def pos(self):
        return self._bits.pos
    
    def __repr__(self):
        return f'BitStream(data="{self._bits}")'
        
    def u(self,n):
        return self._bits.read(n).uint

    def f(self,n):
        return self.u(n)

    def ue(self):
        return self._bits.read('ue')
    
    def se(self):
        return self._bits.read('se')

    def byte_aligned(self):
        return self._bits.pos % 8 == 0

    def more_data(self):
        return self._bits.pos < self._bits.length

    def more_rbsp_data(self):
        if not self.more_data():
            return False
        i = self._bits.length - 1
        while i >= 0:
            if self._bits[i] == True:
                if self._bits.pos == i:
                    return False
                else:
                    return True
            i -= 1
    

    
