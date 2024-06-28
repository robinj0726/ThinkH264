class Macroblock:
    def __init__(self, parent_slice, idx, pskip = False):
        self._idx = idx
        self._slice = parent_slice

        self.macroblock_layer()     
    
    def macroblock_layer(self):
        pass
