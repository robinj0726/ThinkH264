from enum import Enum

class MBModeTypes(Enum):
    PSKIP        =  0,
    BSKIP_DIRECT =  0,
    P16x16       =  1,
    P16x8        =  2,
    P8x16        =  3,
    SMB8x8       =  4,
    SMB8x4       =  5,
    SMB4x8       =  6,
    SMB4x4       =  7,
    P8x8         =  8,
    I4MB         =  9,
    I16MB        = 10,
    IBLOCK       = 11,
    SI4MB        = 12,
    I8MB         = 13,
    IPCM         = 14,
    MAXMODE      = 15

    
class Macroblock:
    def __init__(self, parent_slice, idx, pskip = False):
        self._idx = idx
        self._slice = parent_slice
        self._bits = parent_slice._bits

        self.macroblock_layer()     
    
    def macroblock_layer(self):
        self.mb_type = self.slice.bits.ue()
        if self.mb_type == MBModeTypes.IPCM:
            pass
        elif self.mb_type == MBModeTypes.I4MB:
            self.read_intra4x4_macroblock_cavlc()
        else:
            self.read_intra_macroblock()


    def read_intra4x4_macroblock_cavlc(self):
        self.read_ipred_modes()
        

    def read_intra_macroblock(self):
        pass

    def MbPartPredMode(self, mb_type, n = 0):
        if mb_type == 0:
            return "Intra4x4"
        elif mb_type >= 1 and mb_type <= 24:
            self.Intra16x16PredMode = (mb_type - 1) % 4
            self.CodedBlockPatternChroma = ((mb_type - 1) // 4) % 3
            self.CodedBlockPatternLuma = (mb_type // 13) * 15
            return "Intra16x16"
        elif (mb_type, n) in [(0,0), (1,0), (2,0), (5,0), (1,1), (2,1)]:
            self.NumMbPart = [1,2,2,4,4,1][mb_type]
            self.MbPartWidth = [16,16,8,8,8,16][mb_type]
            self.MbPartHeight = [16,8,16,8,8,16][mb_type]
            return "Pred_L0"
        else:
            raise NameError("Unknown MbPartPredMode")

