from .macroblock import Macroblock

SLICE_TYPES = {0:"P",1:"B",2:"I",3:"SP",4:"SI",5:"P",6:"B",7:"I",8:"SP",9:"SI"}

class Slice:
    def __init__(self, bits, nalu, sps, ppss):
        self._bits = bits

        self._nalu = nalu
        self._sps = sps
        self._pps_list = ppss

        self._mbs = []

        self.slice_header()
        
        self.slice_variables()

        # self.slice_data()

    def __repr__(self):
        attrs = ', '.join(f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_'))
        return f'Slice({attrs})'

    def slice_header(self):
        self.IdrPicFlag = 1 if self._nalu.nal_unit_type == 5 else 0

        self.first_mb_in_slice = self._bits.ue()
        self.slice_type_int = self._bits.ue()
        self.slice_type = SLICE_TYPES[self.slice_type_int % 5]
        self.pic_parameter_set_id = self._bits.ue()
        self._pps = self._pps_list[self.pic_parameter_set_id]
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
        if self._sps.pic_order_cnt_type == 0 :
            self.pic_order_cnt_lsb = \
                self._bits.u(self._sps.log2_max_pic_order_cnt_lsb_minus4 + 4)
            if (self._pps.bottom_field_pic_order_in_frame_present_flag > 0) and \
               (self.field_pic_flag == 0) :
                self.delta_pic_order_cnt_bottom = self._bits.se()
        self.delta_pic_order_cnt = []
        if (self._sps.pic_order_cnt_type == 1) and \
           (self.delta_pic_order_always_zero_flag == 0) :
            self.delta_pic_order_cnt.append(self._bits.se())
            if self.bottom_field_pic_order_in_frame_present_flag and (not self.field_pic_flag) :
                self.delta_pic_order_cnt.append(self._bits.se())
        if self._pps.redundant_pic_cnt_present_flag > 0 :
            self.redundant_pic_cnt = self._bits.ue()
        if self.slice_type == "B" :
            self.direct_spatial_mv_pred_flag = self._bits.u(1)
        if self.slice_type == "P" or self.slice_type == "SP" or self.slice_type == "B" :
            self.num_ref_idx_active_override_flag = self._bits.u(1)
            if self.num_ref_idx_active_override_flag > 0 :
                self.num_ref_idx_l0_active_minus1 = self._bits.ue()
                if self.slice_type == "B" :
                    self.num_ref_idx_l1_active_minus1 = self._bits.ue()
        if self._nalu.nal_unit_type == 20 or self._nalu.nal_unit_type == 21 :
            self.ref_pic_list_mvc_modification()
        else:
            self.ref_pic_list_modification()
        if (self._pps.weighted_pred_flag > 0) and \
           ((self.slice_type == "P") or (self.slice_type == "SP")) or \
           ((self._pps.weighted_bipred_idc == 1) and (self.slice_type == "B")) :
            self.pred_weight_table()
        if self._nalu.nal_ref_idc != 0 :
            self.dec_ref_pic_marking()
        if self._pps.entropy_coding_mode_flag and \
           (self.slice_type != "I") and \
           (self.slice_type != "SI") :
            self.cabac_init_idc = self._bits.ue()
        self.slice_qp_delta = self._bits.se()
        if (self.slice_type == "SP") or (self.slice_type == "SI") :
            if self.slice_type == "SP" :
                self.sp_for_switch_flag = self._bits.u(1)
            self.slice_qs_delta = self._bits.se()
        if self._pps.deblocking_filter_control_present_flag :
            self.disable_deblocking_filter_idc = self._bits.ue()
            if self.disable_deblocking_filter_idc != 1 :
                self.slice_alpha_c0_offset_div2 = self._bits.se()
                self.slice_beta_offset_div2 = self._bits.se()
        if self._pps.num_slice_groups_minus1 > 0 and \
           self.slice_group_map_type >= 3 and \
           self.slice_group_map_type <= 5:
            #WIP UV
            print("slice_group_change_cycle NOT impl")
            #self.slice_group_change_cycle = self.bits.u()

    def ref_pic_list_mvc_modification(self):
        print("ref_pic_list_mvc_modification NOT IMPL")

    def ref_pic_list_modification(self):
        if (self.slice_type_int % 5 != 2) and (self.slice_type_int % 5 != 4) :
            self.ref_pic_list_modification_flag_l0 = self._bits.u(1)
            if self.ref_pic_list_modification_flag_l0 :
                while True :
                    self.modification_of_pic_nums_idc = self._bits.ue()
                    if self.modification_of_pic_nums_idc == 0 or \
                       self.modification_of_pic_nums_idc == 1 :
                        self.abs_diff_pic_num_minus1 = self._bits.ue()
                    elif self.modification_of_pic_nums_idc == 2 :
                        self.long_term_pic_num = self._bits.ue()
                    if self.modification_of_pic_nums_idc == 3:
                        break
        if self.slice_type_int % 5 == 1 :
            self.ref_pic_list_modification_flag_l1 = self._bits.u(1)
            if self.ref_pic_list_modification_flag_l1: 
                while True :
                    self.modification_of_pic_nums_idc = self._bits.ue()
                    if (self.modification_of_pic_nums_idc == 0) or \
                       (self.modification_of_pic_nums_idc == 1) :
                        self.abs_diff_pic_num_minus1 = self._bits.ue()
                    elif self.modification_of_pic_nums_idc == 2 :
                        self.long_term_pic_num = self._bits.ue()
                    if self.modification_of_pic_nums_idc == 3 :
                        break


    def pred_weight_table(self):
        print("pred_weight_table NOT impl")
        pass

    def dec_ref_pic_marking(self):
        if self.IdrPicFlag :
            self.no_output_of_prior_pics_flag = self._bits.u(1)
            self.long_term_reference_flag = self._bits.u(1)
        else :
            self.adaptive_ref_pic_marking_mode_flag = self._bits.u(1)
            if self.adaptive_ref_pic_marking_mode_flag :
                while True :
                    memory_management_control_operation = self._bits.ue()
                    self.memory_management_control_operation = memory_management_control_operation
                    if memory_management_control_operation == 1 or \
                       memory_management_control_operation == 3 :
                        self.difference_of_pic_nums_minus1 = self._bits.ue()
                    if memory_management_control_operation == 2 :
                        self.long_term_pic_num = self._bits.ue()
                    if memory_management_control_operation == 3 or \
                       memory_management_control_operation == 6 :
                        self.long_term_frame_idx = self._bits.ue()
                    if memory_management_control_operation == 4 :
                        self.max_long_term_frame_idx_plus1 = self._bits.ue()
                    if memory_management_control_operation == 0 :
                        break

    def slice_variables(self):
        self.PrevRefFrameNum = 0 if self._nalu.nal_unit_type == 5 else 1 # TO BE FIXED
        self.MbaffFrameFlag = self._sps.mb_adaptive_frame_field_flag and \
                                     (not self.field_pic_flag)
        self.PicWidthInMbs = self._sps.pic_width_in_mbs_minus1 + 1
        self.PicWidthInSamples_L = self.PicWidthInMbs * 16
        self.PicWidthInSamples_C = self.PicWidthInMbs * self._sps.MbWidthC
        self.PicHeightInMapUnits = self._sps.pic_height_in_map_units_minus1 + 1
        self.FrameHeightInMbs = ( 2 - self._sps.frame_mbs_only_flag ) * self.PicHeightInMapUnits
        self.PicHeightInMbs = self.FrameHeightInMbs / ( 1 + self.field_pic_flag )
        self.PicSizeInMapUnits = self.PicWidthInMbs * self.PicHeightInMapUnits
        self.PicSizeInMbs = self.PicWidthInMbs * self.PicHeightInMbs
        self.PicHeightInSamples_L = int(self.PicHeightInMbs * 16)
        self.PicHeightInSamples_C = int(self.PicHeightInMbs * self._sps.MbHeightC)
        # self.S_prime_L = array_2d(self.PicWidthInSamples_L, self.PicHeightInSamples_L, 0)
        # self.S_prime_Cb = array_2d(self.PicWidthInSamples_C, self.PicHeightInSamples_C, 0)
        # self.S_prime_Cr = array_2d(self.PicWidthInSamples_C, self.PicHeightInSamples_C, 0)
        # self.mb_to_slice_group_map()
    
    def slice_data(self):
        if self._pps.entropy_coding_mode_flag :
            while self.bits.byte_aligned():
                self.cabac_alignment_one_bit = self._bits.f(1)
        self.CurrMbAddr = self.first_mb_in_slice * ( 1 + self.MbaffFrameFlag )
        moreDataFlag = True
        prevMbSkipped = False
        while True:
            if self.slice_type != "I" and self.slice_type != "SI" :
                if not self._pps.entropy_coding_mode_flag :
                    self.mb_skip_run = self.bits.ue()
                    prevMbSkipped = self.mb_skip_run > 0 
                    for i in range(self.mb_skip_run) :
                        self._mbs.append(Macroblock(self, len(self.mbs), pskip=True))
                        self.CurrMbAddr = self.NextMbAddress( self.CurrMbAddr )
                    if self.mb_skip_run > 0 :
                        moreDataFlag = self._bits.more_rbsp_data( )
                else :
                    self.mb_skip_flag = self._bits.ae()
                    moreDataFlag = not self.mb_skip_flag
            if moreDataFlag :
                if self.MbaffFrameFlag and ( self.CurrMbAddr % 2 == 0 or ( self.CurrMbAddr % 2 == 1 and prevMbSkipped ) ) :
                    self.mb_field_decoding_flag = self._bits.ae() if self._pps.entropy_coding_mode_flag else self._bits.u(1)
                mb = Macroblock(self, len(self._mbs))
                self._mbs.append(mb)
            if not self._pps.entropy_coding_mode_flag :
                moreDataFlag = self._bits.more_rbsp_data()
            else :
                if self.slice_type != "I" and self.slice_type != "SI" :
                    prevMbSkipped = self.mb_skip_flag
                if self.MbaffFrameFlag and self.CurrMbAddr % 2 == 0 :
                    moreDataFlag = True
                else :
                    self.end_of_slice_flag = self._bits.ae()
                    moreDataFlag = not self.end_of_slice_flag
            self.CurrMbAddr = self.NextMbAddress(self.CurrMbAddr)
            if not moreDataFlag:
                break

    def NextMbAddress(self,n):
        i=n+1 
        while i < self.PicSizeInMbs and self.MbToSliceGroupMap[i] != self.MbToSliceGroupMap[n] :
            i += 1
        return i
    
