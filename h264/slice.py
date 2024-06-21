class Slice:
    slice_types = {0:"P",1:"B",2:"I",3:"SP",4:"SI",5:"P",6:"B",7:"I",8:"SP",9:"SI"}

    def __init__(self, bits, sps, ppss, params):
        self._bits = bits
        self._sps = sps
        self._pps_list = ppss
        self._params = params

    def __repr__(self):
        attrs = ', '.join(f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_'))
        return f'PPS({attrs})'

    def slice_header(self):
        self.IdrPicFlag = 1 if self._params["nal_unit_type"] == 5 else 0

        self.first_mb_in_slice = self._bits.ue()
        self.slice_type_int = self._bits.ue()
        self.pic_parameter_set_id = self._bits.ue()
        if self._sps.separate_colour_plane_flag == 1:
            self.colour_plane_id = self._bits.u(2)
        self.frame_num = self._bits.u(self._sps.log2_max_frame_num_minus4 + 4)
        if not self._sps.frame_mbs_only_flag:
            self.field_pic_flag = self._bits.u(1)
            if self.field_pic_flag:
                self.bottom_field_flag = self._bits.u(1)
        else:
            self.field_pic_flag = 0
        if self.IdrPicFlag :
            self.idr_pic_id = self._bits.ue()
