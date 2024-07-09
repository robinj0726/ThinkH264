class PPS:
    def __init__(self, bits):
        self._bits = bits

        self.pic_parameter_set_rbsp()
        self.rbsp_trailing_bits()

    def pic_parameter_set_rbsp(self):
        self.pic_parameter_set_id = self._bits.read_ue_v("PPS: pic_parameter_set_id")
        self.seq_parameter_set_id = self._bits.read_ue_v("PPS: seq_parameter_set_id")
        self.entropy_coding_mode_flag = self._bits.read_u_1("PPS: entropy_coding_mode_flag")
        self.bottom_field_pic_order_in_frame_present_flag = self._bits.read_u_1("PPS: bottom_field_pic_order_in_frame_present_flag")
        self.num_slice_groups_minus1 = self._bits.read_ue_v("PPS: num_slice_groups_minus1")
        if self.num_slice_groups_minus1 > 0 :
            self.slice_group_map_type = self._bits.read_ue_v("PPS: slice_group_map_type")
            if self.slice_group_map_type == 0 :
                self.run_length_minus1 = []
                for i in range(self.num_slice_groups_minus1+1):
                    self.run_length_minus1.append(self._bits.read_ue_v(f"PPS: run_length_minus1[{i}]"))
            elif self.slice_group_map_type == 2 :
                self.top_left = []
                self.bottom_right = []
                for i in range(self.num_slice_groups_minus1):
                    self.top_left.append(self._bits.read_ue_v(f"PPS: top_left[{i}]"))
                    self.bottom_right.append(self._bits.read_ue_v(f"PPS: bottom_right[{i}]"))
            elif self.slice_group_map_type == 3 or \
                 self.slice_group_map_type == 4 or \
                 self.slice_group_map_type == 5 :
                self.slice_group_change_direction_flag = self._bits.read_u_1("PPS: slice_group_change_direction_flag")
                self.slice_group_change_rate_minus1 = self._bits.read_ue_v("PPS: slice_group_change_rate_minus1")
            elif self.slice_group_map_type == 6 :
                self.pic_size_in_map_units_minus1 = self._bits.read_ue_v("PPS: pic_size_in_map_units_minus1")
                self.slice_group_id = []
                from math import ceil, log2
                for i in range(self.pic_size_in_map_units_minus1+1):
                    tmp = self._bits.u(ceil(log2(self.num_slice_groups_minus1+1)))
                    self.slice_group_id.append(tmp)
        self.num_ref_idx_l0_default_active_minus1 = self._bits.read_ue_v("PPS: num_ref_idx_l0_default_active_minus1")
        self.num_ref_idx_l1_default_active_minus1 = self._bits.read_ue_v("PPS: num_ref_idx_l1_default_active_minus1")
        self.weighted_pred_flag = self._bits.read_u_1("PPS: weighted_pred_flag")
        self.weighted_bipred_idc = self._bits.read_u_v(2, "PPS: weighted_bipred_idc")
        self.pic_init_qp_minus26 = self._bits.read_se_v("PPS: pic_init_qp_minus26")
        self.pic_init_qs_minus26 = self._bits.read_se_v("PPS: pic_init_qs_minus26")
        self.chroma_qp_index_offset = self._bits.read_se_v("PPS: chroma_qp_index_offset")
        self.deblocking_filter_control_present_flag = self._bits.read_u_1("PPS: deblocking_filter_control_present_flag")
        self.constrained_intra_pred_flag = self._bits.read_u_1("PPS: constrained_intra_pred_flag")
        self.redundant_pic_cnt_present_flag = self._bits.read_u_1("PPS: redundant_pic_cnt_present_flag")

        if self._bits.more_rbsp_data() :
            self.transform_8x8_mode_flag = self._bits.read_u_1("PPS: transform_8x8_mode_flag")
            self.pic_scaling_matrix_present_flag = self._bits.read_u_1("pic_scaling_matrix_present_flag")
            if self.pic_scaling_matrix_present_flag > 0 :
                upper = (2 if self.chroma_format_idc != 3 else 6) * self.transform_8x8_mode_flag
                self.pic_scaling_list_present_flag = []
                for i in range(upper) :
                    elem = self._bits.read_u_1(f"PPS: pic_scaling_list_present_flag[{i}]")
                    self.pic_scaling_list_present_flag.append(elem)
                    if elem > 0:
                        raise NameError("scaling_list not impl")
                        if i < 6 :
                            pass
                            #scaling_list( ScalingList4x4[ i ], 16, UseDefaultScalingMatrix4x4Flag[ i ] )
                        else:
                            pass
                            #scaling_list( ScalingList8x8[ i − 6 ], 64, UseDefaultScalingMatrix8x8Flag[ i − 6 ] )
            self.second_chroma_qp_index_offset = self._bits.read_se_v("PPS: second_chroma_qp_index_offset")

    def rbsp_trailing_bits(self):
        # if self.bits.more_data():
        self.rbsp_stop_one_bit = self._bits.f(1)
        assert self.rbsp_stop_one_bit == 1
        # self.params["rbsp_alignment_zero_bit"] = self.bits[self.bits.pos:].int
        while not self._bits.byte_aligned():
            assert self._bits.f(1) == 0  

    def __repr__(self):
        attrs = ', '.join(f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_'))
        return f'PPS({attrs})'
