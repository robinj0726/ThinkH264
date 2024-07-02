class Macroblock:
    def __init__(self, parent_slice, idx, pskip = False):
        self._idx = idx
        self._slice = parent_slice
        self._bits = parent_slice._bits

        self.macroblock_layer()     
    
    def macroblock_layer(self):
        self.mb_type_int = self._bits.ue()

    def MbPartPredMode(self, mb_type_int, n = 0):
        if mb_type_int == 0:
            return "Intra4x4"
        elif mb_type_int >= 1 and mb_type_int <= 24:
            self.Intra16x16PredMode = (mb_type_int - 1) % 4
            self.CodedBlockPatternChroma = ((mb_type_int - 1) // 4) % 3
            self.CodedBlockPatternLuma = (mb_type_int // 13) * 15
            return "Intra16x16"
        elif (mb_type_int, n) in [(0,0), (1,0), (2,0), (5,0), (1,1), (2,1)]:
            self.NumMbPart = [1,2,2,4,4,1][mb_type_int]
            self.MbPartWidth = [16,16,8,8,8,16][mb_type_int]
            self.MbPartHeight = [16,8,16,8,8,16][mb_type_int]
            return "Pred_L0"
        else:
            raise NameError("Unknown MbPartPredMode")

