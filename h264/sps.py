import numpy as np
from .tracer import tracer

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
        self.profile_idc = self._bits.read_u_v(8, "SPS: profile_idc")
        self.constraint_set0_flag = self._bits.read_u_1("SPS: constraint_set0_flag")
        self.constraint_set1_flag = self._bits.read_u_1("SPS: constraint_set1_flag")
        self.constraint_set2_flag = self._bits.read_u_1("SPS: constraint_set2_flag")
        self.constraint_set3_flag = self._bits.read_u_1("SPS: constraint_set3_flag")
        self.constraint_set4_flag = self._bits.read_u_1("SPS: constraint_set4_flag")
        self.constraint_set5_flag = self._bits.read_u_1("SPS: constraint_set5_flag")
        self.reserved_zero_2bits = self._bits.read_u_v(2, "SPS: reserved_zero_2bits")
        self.level_idc = self._bits.read_u_v(8, "SPS: level_idc")
        self.seq_parameter_set_id = self._bits.read_ue_v("SPS: seq_parameter_set_id")
        if self.profile_idc == 100 or self.profile_idc == 110 or self.profile_idc == 122 or self.profile_idc == 244 or self.profile_idc == 44 or self.profile_idc == 83 or self.profile_idc == 86 or self.profile_idc == 118 or self.profile_idc == 128 or self.profile_idc == 138 or self.profile_idc == 139 or self.profile_idc == 134 or self.profile_idc == 135 :
            self.chroma_format_idc = self._bits.read_ue_v("SPS: chroma_format_idc")
            if self.chroma_format_idc == 3:
                self.separate_colour_plane_flag = self._bits.read_u_1("SPS: separate_colour_plane_flag")
            self.bit_depth_chroma_minus8 = self._bits.read_ue_v("SPS: bit_depth_chroma_minus8")
            self.bit_depth_luma_minus8 = self._bits.read_ue_v("SPS: bit_depth_luma_minus8")
            self.qpprime_y_zero_transform_bypass_flag = self._bits.read_u_1("SPS: qpprime_y_zero_transform_bypass_flag")
            self.seq_scaling_matrix_present_flag = self._bits.read_u_1("SPS: seq_scaling_matrix_present_flag")
            if self.seq_scaling_matrix_present_flag:
                self.seq_scaling_list_present_flag = np.zeros((12), dtype=int)
                self.ScalingList4x4 = np.zeros((6, 16), dtype=int)
                self.UseDefaultScalingMatrix4x4Flag = np.zeros((6), dtype=int)
                self.ScalingList8x8 = np.zeros((6, 64), dtype=int)
                self.UseDefaultScalingMatrix8x8Flag = np.zeros((6), dtype=int)
                
                for i in range(8 if self.chroma_format_idc != 3 else 12):
                    self.seq_scaling_list_present_flag[i] = self._bits.read_u_1(f"SPS: seq_scaling_list_present_flag[{i}]")
                    if self.seq_scaling_list_present_flag[i]:
                        if i < 6:
                            self.scaling_list(self.ScalingList4x4[i], 16, self.UseDefaultScalingMatrix4x4Flag[i])
                        else:
                            self.scaling_list(self.ScalingList8x8[i-6] ,64, self.UseDefaultScalingMatrix8x8Flag[i-6])
                        
        self.log2_max_frame_num_minus4 = self._bits.read_ue_v("SPS: log2_max_frame_num_minus4")
        self.pic_order_cnt_type = self._bits.read_ue_v("SPS: pic_order_cnt_type")
        if self.pic_order_cnt_type == 0 :
            self.log2_max_pic_order_cnt_lsb_minus4 = self._bits.read_ue_v("SPS: log2_max_pic_order_cnt_lsb_minus4")
        elif self.pic_order_cnt_type == 1:
            self.delta_pic_order_always_zero_flag = self._bits.read_u_1("SPS: delta_pic_order_always_zero_flag")    
            self.offset_for_non_ref_pic = self._bits.read_se_v("SPS: offset_for_non_ref_pic")
            self.offset_for_top_to_bottom_field = self._bits.read_se_v("SPS: offset_for_top_to_bottom_field")
            self.num_ref_frames_in_pic_order_cnt_cycle = self._bits.read_ue_v("SPS: num_ref_frames_in_pic_order_cnt_cycle")
            self.offset_for_ref_frame = []
            for i in range(self.num_ref_frames_in_pic_order_cnt_cycle):
                self.offset_for_ref_frame.append(self.se())
        self.max_num_ref_frames = self._bits.read_ue_v("SPS: max_num_ref_frames")
        self.gaps_in_frame_num_value_allowed_flag = self._bits.read_u_1("SPS: gaps_in_frame_num_value_allowed_flag")
        self.pic_width_in_mbs_minus1 = self._bits.read_ue_v("SPS: pic_width_in_mbs_minus1")
        self.pic_height_in_map_units_minus1 = self._bits.read_ue_v("SPS: pic_height_in_map_units_minus1")
        self.frame_mbs_only_flag = self._bits.read_u_1("SPS: frame_mbs_only_flag")
        if not self.frame_mbs_only_flag:
            self.mb_adaptive_frame_field_flag = self._bits.read_u_1("SPS: mb_adaptive_frame_field_flag")
        else:
            self.mb_adaptive_frame_field_flag = 0
        self.direct_8x8_inference_flag = self._bits.read_u_1("SPS: direct_8x8_inference_flag")
        self.frame_cropping_flag = self._bits.read_u_1("SPS: frame_cropping_flag")
        if self.frame_cropping_flag:
            self.frame_crop_left_offset = self._bits.read_ue_v("SPS: frame_crop_left_offset")
            self.frame_crop_right_offset = self._bits.read_ue_v("SPS: frame_crop_right_offset")
            self.frame_crop_top_offset = self._bits.read_ue_v("SPS: frame_crop_top_offset")
            self.frame_crop_bottom_offset = self._bits.read_ue_v("SPS: frame_crop_bottom_offset")
        self.vui_parameters_present_flag = self._bits.read_u_1("SPS: vui_parameters_present_flag")
        if self.vui_parameters_present_flag:
            self.vui_parameters()

    def scaling_list(self, scalingList, sizeOfScalingList):
        lastScale = 8
        nextScale = 8
        for j in range(sizeOfScalingList):
            if nextScale != 0:
                self.delta_scale = self._bits.read_se_v("SPS: delta_scale")
                nextScale = (lastScale + self.delta_scale + 256) % 256
            scalingList[j] = lastScale if nextScale == 0 else nextScale
            lastScale = scalingList[j]

    def vui_parameters(self):
        self.aspect_ratio_info_present_flag = self._bits.read_u_1("VUI: aspect_ratio_info_present_flag")
        if self.aspect_ratio_info_present_flag:
            self.aspect_ratio_idc = self._bits.read_u_v(8, "VUI: aspect_ratio_idc")
            if self.aspect_ratio_idc == self.Extended_SAR:
                self.sar_width = self._bits.read_u_v(16, "VUI: sar_width")
                self.sar_height = self._bits.read_u_v(16, "VUI: sar_height")
        self.overscan_info_present_flag = self._bits.read_u_1("VUI: overscan_info_present_flag")
        if self.overscan_info_present_flag:
            self.overscan_appropriate_flag = self._bits.read_u_1("VUI: overscan_appropriate_flag")
        self.video_signal_type_present_flag = self._bits.read_u_1("VUI: video_signal_type_present_flag")
        if self.video_signal_type_present_flag:
            self.video_format = self._bits.read_u_v(3, "VUI: video_format")
            self.video_full_range_flag = self._bits.read_u_1("VUI: video_full_range_flag")
            self.colour_description_present_flag = self._bits.read_u_1("VUI: colour_description_present_flag")
            if self.colour_description_present_flag:
                self.colour_primaries = self._bits.read_u_v(8, "VUI: colour_primaries")
                self.transfer_characteristics = self._bits.read_u_v(8, "VUI: transfer_characteristics")
                self.matrix_coefficients = self._bits.read_u_v(8, "VUI: matrix_coefficients")
        self.chroma_loc_info_present_flag = self._bits.read_u_1("VUI: chroma_loc_info_present_flag")
        if self.chroma_loc_info_present_flag:
            self.chroma_sample_loc_type_top_field = self._bits.read_ue_v("VUI: chroma_sample_loc_type_top_field")
            self.chroma_sample_loc_type_bottom_field = self._bits.read_ue_v("VUI: chroma_sample_loc_type_bottom_field")
        self.timing_info_present_flag = self._bits.read_u_1("VUI: timing_info_present_flag")
        if self.timing_info_present_flag:
            self.num_units_in_tick = self._bits.read_u_v(32, "VUI: num_units_in_tick")
            self.time_scale = self._bits.read_u_v(32, "VUI: time_scale")
            self.fixed_frame_rate_flag = self._bits.read_u_1("VUI: fixed_frame_rate_flag")
        self.nal_hrd_parameters_present_flag = self._bits.read_u_1("VUI: nal_hrd_parameters_present_flag")
        if self.nal_hrd_parameters_present_flag:
            self.hrd_parameters()
        self.vcl_hrd_parameters_present_flag = self._bits.read_u_1("VUI: vcl_hrd_parameters_present_flag")
        if self.vcl_hrd_parameters_present_flag:
            self.hrd_parameters()
        if self.nal_hrd_parameters_present_flag or self.vcl_hrd_parameters_present_flag:
            self.low_delay_hrd_flag = self._bits.read_u_1("VUI: low_delay_hrd_flag")
        self.pic_struct_present_flag = self._bits.read_u_1("VUI: pic_struct_present_flag")
        self.bitstream_restriction_flag = self._bits.read_u_1("VUI: bitstream_restriction_flag")
        if self.bitstream_restriction_flag:
            self.motion_vectors_over_pic_boundaries_flag = self._bits.read_u_1("VUI: motion_vectors_over_pic_boundaries_flag")
            self.max_bytes_per_pic_denom = self._bits.read_ue_v("VUI: max_bytes_per_pic_denom")
            self.max_bits_per_mb_denom = self._bits.read_ue_v("VUI: max_bits_per_mb_denom")
            self.log2_max_mv_length_horizontal = self._bits.read_ue_v("VUI: log2_max_mv_length_horizontal")
            self.log2_max_mv_length_vertical = self._bits.read_ue_v("VUI: log2_max_mv_length_vertical")
            self.max_num_reorder_frames = self._bits.read_ue_v("VUI: max_num_reorder_frames")
            self.max_dec_frame_buffering = self._bits.read_ue_v("VUI: max_dec_frame_buffering")
        
    def hrd_parameters(self): 
        self.cpb_cnt_minus1 = self._bits.read_ue_v("SPS: cpb_cnt_minus1")
        self.bit_rate_scale = self._bits.read_u_v(4, "SPS: bit_rate_scale")
        self.cpb_size_scale = self._bits.read_u_v(4, "SPS: cpb_size_scale")

        self.bit_rate_value_minus1 = []
        self.cpb_size_value_minus1 = []
        self.cbr_flag = []
        for SchedSelIdx in range(self.cpb_cnt_minus1 + 1):
            self.bit_rate_value_minus1.append(self._bits.read_ue_v("SPS: bit_rate_value_minus1"))
            self.cpb_size_value_minus1.append(self._bits.read_ue_v("SPS: cpb_size_value_minus1"))
            self.cbr_flag.append(self._bits.read_u_1("SPS: cbr_flag"))
        self.initial_cpb_removal_delay_length_minus1 = self._bits.read_u_v(5, "SPS: initial_cpb_removal_delay_length_minus1")
        self.cpb_removal_delay_length_minus1 = self._bits.read_u_v(5, "SPS: cpb_removal_delay_length_minus1")
        self.dpb_output_delay_length_minus1 = self._bits.read_u_v(5, "SPS: dpb_output_delay_length_minus1")
        self.time_offset_length = self._bits.read_u_v(5, "SPS: time_offset_length")

    def rbsp_trailing_bits(self):
        self.rbsp_stop_one_bit = self._bits.f(1)
        assert self.rbsp_stop_one_bit == 1
        while not self._bits.byte_aligned():
            assert self._bits.f(1) == 0  

    def sps_not_present(self):
        keys = self.__dict__.keys()
        if "chroma_format_idc" not in keys:
            self.chroma_format_idc = 1
        if "separate_colour_plane_flag" not in keys:
            self.separate_colour_plane_flag = 0
            self.ChromaArrayType = self.chroma_format_idc
        if self.chroma_format_idc == 1 and self.separate_colour_plane_flag == 0:
            self.SubWidthC = 2
            self.SubHeightC = 2
        elif self.chroma_format_idc == 2 and self.separate_colour_plane_flag == 0:
            self.SubWidthC = 2
            self.SubHeightC = 1
        elif self.chroma_format_idc == 3 and self.separate_colour_plane_flag == 0:
            self.SubWidthC = 1
            self.SubHeightC = 1
        if self.chroma_format_idc == 0 or self.separate_colour_plane_flag == 1:
            self.MbWidthC = 0
            self.MbHeightC = 0
        else:
            self.MbWidthC = 16 // self.SubWidthC
            self.MbHeightC = 16 // self.SubHeightC
        if "bit_depth_luma_minus8" not in keys:
            self.bit_depth_luma_minus8 = 0
            self.BitDepth_Y = 8 + self.bit_depth_luma_minus8
            self.QpBdOffset_Y = 6 * self.bit_depth_luma_minus8
        if "bit_depth_chroma_minus8" not in keys:
            self.bit_depth_chroma_minus8 = 0
            self.BitDepth_C = 8 + self.bit_depth_chroma_minus8
            self.QpBdOffset_C = 6 * self.bit_depth_chroma_minus8
        if "qpprime_y_zero_transform_bypass_flag" not in keys:
            self.qpprime_y_zero_transform_bypass_flag = 0
        if "mb_adaptive_frame_field_flag" not in keys:
            self.mb_adaptive_frame_field_flag = 0
