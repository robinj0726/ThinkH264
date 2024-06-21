class PPS:
    def __init__(self, bitstream):
        self._bs = bitstream

        self.pic_parameter_set_rbsp()

    def pic_parameter_set_rbsp(self):
        self.pic_parameter_set_id = self._bs.ue()
        self.seq_parameter_set_id = self._bs.ue()
        self.entropy_coding_mode_flag = self._bs.u(1)
        self.bottom_field_pic_order_in_frame_present_flag = self._bs.u(1)
        self.num_slice_groups_minus1 = self._bs.ue()
        if self.num_slice_groups_minus1 > 0 :
            self.slice_group_map_type = self._bs.ue()
            if self.slice_group_map_type == 0 :
                self.run_length_minus1 = []
                for i in range(self.num_slice_groups_minus1+1):
                    self.run_length_minus1.append(self._bs.ue())
            elif self.slice_group_map_type == 2 :
                self.top_left = []
                self.bottom_right = []
                for i in range(self.num_slice_groups_minus1):
                    self.top_left.append(self._bs.ue())
                    self.bottom_right.append(self._bs.ue())
            elif self.slice_group_map_type == 3 or \
                 self.slice_group_map_type == 4 or \
                 self.slice_group_map_type == 5 :
                self.slice_group_change_direction_flag = self._bs.u(1)
                self.slice_group_change_rate_minus1 = self._bs.ue()
            elif self.slice_group_map_type == 6 :
                self.pic_size_in_map_units_minus1 = self._bs.ue()
                self.slice_group_id = []
                from math import ceil, log2
                for i in range(self.pic_size_in_map_units_minus1+1):
                    tmp = self._bs.u(ceil(log2(self.num_slice_groups_minus1+1)))
                    self.slice_group_id.append(tmp)
        self.num_ref_idx_l0_default_active_minus1 = self._bs.ue()
        self.num_ref_idx_l1_default_active_minus1 = self._bs.ue()
        self.weighted_pred_flag = self._bs.u(1)
        self.weighted_bipred_idc = self._bs.u(2)
        self.pic_init_qp_minus26 = self._bs.se()
        self.pic_init_qs_minus26 = self._bs.se()
        self.chroma_qp_index_offset = self._bs.se()
        self.deblocking_filter_control_present_flag = self._bs.u(1)
        self.constrained_intra_pred_flag = self._bs.u(1)
        self.redundant_pic_cnt_present_flag = self._bs.u(1)

        if self._bs.more_rbsp_data() :
            self.transform_8x8_mode_flag = self._bs.u(1)
            self.pic_scaling_matrix_present_flag = self._bs.u(1)
            if self.pic_scaling_matrix_present_flag > 0 :
                upper = (2 if self.chroma_format_idc != 3 else 6) * self.transform_8x8_mode_flag
                self.pic_scaling_list_present_flag = []
                for i in range(upper) :
                    elem = self._bs.u(1)
                    self.pic_scaling_list_present_flag.append(elem)
                    if elem > 0:
                        raise NameError("scaling_list not impl")
                        if i < 6 :
                            pass
                            #scaling_list( ScalingList4x4[ i ], 16, UseDefaultScalingMatrix4x4Flag[ i ] )
                        else:
                            pass
                            #scaling_list( ScalingList8x8[ i − 6 ], 64, UseDefaultScalingMatrix8x8Flag[ i − 6 ] )
            self.second_chroma_qp_index_offset = self._bs.se()
        self.rbsp_trailing_bits()

    def rbsp_trailing_bits(self):
        # if self.bits.more_data():
        self.rbsp_stop_one_bit = self._bs.f(1)
        assert self.rbsp_stop_one_bit == 1
        # self.params["rbsp_alignment_zero_bit"] = self.bits[self.bits.pos:].int
        while not self._bs.byte_aligned():
            assert self._bs.f(1) == 0  

    def __repr__(self):
        attrs = ', '.join(f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_'))
        return f'PPS({attrs})'
