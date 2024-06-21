class SPS:
    def __init__(self, bits):
        self._bits = bits

        self.seq_parameter_set_data()
        self.sps_not_present()
        self.rbsp_trailing_bits()

    def __repr__(self):
        attrs = ', '.join(f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_'))
        return f'SPS({attrs})'

    def seq_parameter_set_data(self):
        self.profile_idc = self._bits.u(8)
        self.constraint_set0_flag = self._bits.u(1)
        self.constraint_set1_flag = self._bits.u(1)
        self.constraint_set2_flag = self._bits.u(1)
        self.constraint_set3_flag = self._bits.u(1)
        self.constraint_set3_flag = self._bits.u(1)
        self.constraint_set3_flag = self._bits.u(1)
        self.reserved_zero_2bits = self._bits.u(2)
        self.level_idc = self._bits.u(8)
        self.seq_parameter_set_id = self._bits.ue()
        if self.profile_idc == 100 or self.profile_idc == 110 or self.profile_idc == 122 or self.profile_idc == 244 or self.profile_idc == 44 or self.profile_idc == 83 or self.profile_idc == 86 or self.profile_idc == 118 or self.profile_idc == 128 or self.profile_idc == 138 or self.profile_idc == 139 or self.profile_idc == 134 or self.profile_idc == 135 :
            raise NameError('sps:26 not impl')
        

        self.log2_max_frame_num_minus4 = self._bits.ue()
        self.pic_order_cnt_type = self._bits.ue()
        if self.pic_order_cnt_type == 0 :
            self.log2_max_pic_order_cnt_lsb_minus4 = self._bits.ue()
        elif self.pic_order_cnt_type == 1:
            self.delta_pic_order_always_zero_flag = self._bits.u(1)
            self.offset_for_non_ref_pic = self._bits.se()
            self.offset_for_top_to_bottom_field = self._bits.se()
            self.num_ref_frames_in_pic_order_cnt_cycle = self._bits.ue()
            self.offset_for_ref_frame = []
            for i in range(self.num_ref_frames_in_pic_order_cnt_cycle):
                self.offset_for_ref_frame.append(self.se())
        self.max_num_ref_frames = self._bits.ue()
        self.gaps_in_frame_num_value_allowed_flag = self._bits.u(1)
        self.pic_width_in_mbs_minus1 = self._bits.ue()
        self.pic_height_in_map_units_minus1 = self._bits.ue()
        self.frame_mbs_only_flag = self._bits.u(1)
        if not self.frame_mbs_only_flag:
            self.mb_adaptive_frame_field_flag = self._bits.u(1)
        else:
            self.mb_adaptive_frame_field_flag = 0
        self.direct_8x8_inference_flag = self._bits.u(1)
        self.frame_cropping_flag = self._bits.u(1)
        if self.frame_cropping_flag:
            self.frame_crop_left_offset = self._bits.ue()
            self.frame_crop_right_offset = self._bits.ue()
            self.frame_crop_top_offset = self._bits.ue()
            self.frame_crop_bottom_offset = self._bits.ue()
        self.vui_parameters_present_flag = self._bits.u(1)
        if self.vui_parameters_present_flag:
            self.vui_parameters()

    def vui_parameters(self):
        self.aspect_ratio_info_present_flag = self._bits.u(1)
        if self.aspect_ratio_info_present_flag:
            self.aspect_ratio_idc = self._bits.u(8)
            if self.aspect_ratio_idc == self.Extended_SAR:
                self.sar_width = self._bits.u(16)
                self.sar_height = self._bits.u(16)
        self.overscan_info_present_flag = self._bits.u(1)
        if self.overscan_info_present_flag:
            self.overscan_appropriate_flag = self._bits.u(1)
        self.video_signal_type_present_flag = self._bits.u(1)
        if self.video_signal_type_present_flag:
            self.video_format = self._bits.u(3)
            self.video_full_range_flag = self._bits.u(1)
            self.colour_description_present_flag = self._bits.u(1)
            if self.colour_description_present_flag:
                self.colour_primaries = self._bits.u(8)
                self.transfer_characteristics = self._bits.u(8)
                self.matrix_coefficients = self._bits.u(8)
        self.chroma_loc_info_present_flag = self._bits.u(1)
        if self.chroma_loc_info_present_flag:
            self.chroma_sample_loc_type_top_field = self._bits.ue()
            self.chroma_sample_loc_type_bottom_field = self._bits.ue()
        self.timing_info_present_flag = self._bits.u(1)
        if self.timing_info_present_flag:
            self.num_units_in_tick = self._bits.u(32)
            self.time_scale = self._bits.u(32)
            self.fixed_frame_rate_flag = self._bits.u(1)
        self.nal_hrd_parameters_present_flag = self._bits.u(1)
        if self.nal_hrd_parameters_present_flag:
            self.hrd_parameters()
        self.vcl_hrd_parameters_present_flag = self._bits.u(1)
        if self.vcl_hrd_parameters_present_flag:
            self.hrd_parameters()
        if self.nal_hrd_parameters_present_flag or self.vcl_hrd_parameters_present_flag:
            self.low_delay_hrd_flag = self._bits.u(1)
        self.pic_struct_present_flag = self._bits.u(1)
        self.bitstream_restriction_flag = self._bits.u(1)
        if self.bitstream_restriction_flag:
            self.motion_vectors_over_pic_boundaries_flag = self._bits.u(1)
            self.max_bytes_per_pic_denom = self._bits.ue()
            self.max_bits_per_mb_denom = self._bits.ue()
            self.log2_max_mv_length_horizontal = self._bits.ue()
            self.log2_max_mv_length_vertical = self._bits.ue()
            self.max_num_reorder_frames = self._bits.ue()
            self.max_dec_frame_buffering = self._bits.ue()

    def hrd_parameters(self):
        self.cpb_cnt_minus1 = self._bits.ue()
        self.bit_rate_scale = self._bits.u(4)
        self.cpb_size_scale = self._bits.u(4)

        self.bit_rate_value_minus1 = []
        self.cpb_size_value_minus1 = []
        self.cbr_flag = []
        for SchedSelIdx in range(self.cpb_cnt_minus1 + 1):
            self.bit_rate_value_minus1.append(self._bits.ue())
            self.cpb_size_value_minus1.append(self._bits.ue())
            self.cbr_flag.append(self._bits.u(1))
        self.initial_cpb_removal_delay_length_minus1 = self._bits.u(5)
        self.cpb_removal_delay_length_minus1 = self._bits.u(5)
        self.dpb_output_delay_length_minus1 = self._bits.u(5)
        self.time_offset_length = self._bits.u(5)

    def rbsp_trailing_bits(self):
        self.rbsp_stop_one_bit = self._bits.f(1)
        assert self.rbsp_stop_one_bit == 1
        while not self._bits.byte_aligned():
            assert self._bits.f(1) == 0  

    def sps_not_present(self):
        keys = self.__dict__.keys()
        if "separate_colour_plane_flag" not in keys:
            self.separate_colour_plane_flag = 0
