#AV1 decoder tools
1. [Partitioning](#Partitioning)
2. [INTRA prediction](#intra)
    * [Angular modes](#angular_intra)
    * [Paeth mode](#paeth_intra)
    * [Smooth mode](#smooth_intra)
    * [DC mode](#dc_intra)
    * [PALETTE mode](#palette_intra)
    * [Filter Intra mode](#filter_intra)
    * [Chrome from Luma](#chroma_from_luma)
    * [Intra block copy](#intra_block_copy)
2. [INTER prediction](#inter)
3. [Transforms](#transforms)
4. [Quantization](#quantization)
5. [Deblocking](#deblocking)
6. [Post deblocking](#post_deblocking)
    * [CDEF](#cdef)
    * [Super resolution](#superres)
    * [Loop restoration](#loop_restoration)
7. [Film Grain](#film_grain)
8. [Entropy coding](#entropy_coding)

## <a id='Partitioning'>Partitioning</a>

* \[VP9\] Has SB of size 64x64 processed in raster order inside a tile. SB is recursively divided to 4 blocks in quad-tree manner (PARTITION\_SPLIT). Leaf of quad-tree can be coded as-is (PARTITION\_NONE) or additionally divided into 2 blocks (PARTITION\_HORZ or PARTITION\_VERT). Smallest block is 4x4 (in terms of Luma pixels), but most of prediction info is stored at 8x8 level (Intra/Inter, skip flag, single/compound, reference frame, interpolation filter, segment id, etc). Only few things are on 4x4, 4x8, 8x4 level (if any): MVs, Intra mode. Chroma partitioning of SB mimics Luma partitioning.
* \[AV1\]
    1. SB size is 128x128 or 64x64. Size is indicated by a flag in sequence header. Inside a tile SBs are processed in raster order.
    2. SB partitioning is similar to VP9 with additional partitioning options at "leaf" level.
        * As in VP9, SB is divided by recursive splitting [PARTITION\_SPLIT] in quad-tree manner.
        * Leaf of quad-tree has 6 more partition options in addition to PARTITION\_NONE, PARTITION\_HORZ and PARTITION\_VERT:
        ![partitions](pics\Partitioning.png)
        * Blocks inside leaf of partition quad-tree are called "partition units" (PartU or PU). E.g. if leaf is 16x16 and it was additionally divided as PARTITION\_HORZ\_A, then it contains two 8x8 PartUs and one 16x8 PartU.
        * Smallest Luma PU is 4x4. Thus PARTITION\_HORZ\_4 and PARTITION\_VERT\_4 are prohibited for 8x8 block.
        * Also PARTITION\_HORZ\_4 and PARTITION\_VERT\_4 are prohibited for 128x128 block (thus PU128x32, 32x128 are not allowed).
        * Chroma PU mimics Luma PU (after respective subsampling).
        * In bitstream PU holds coded coeffs by planes in following order: Y, Cb, Cr.
            * \[Exception\] When PU is 128x128, coeffs are stored by portions of 64x64 sub-blocks in Z-order (Y, Cb, Cr of sub-block 0, then Y, Cb, Cr of sub-block 1 etc.). The same is for 128x64 and 64x128 (2 64x64 sub-blocks).
        * For each plane in PU coded coeffs are stored by "transform units" (TUs). All TUs in Intra PU have same size and follow in bitstream in raster order. TUs inside Inter PU may have different sizes and follow in bitstream in hierarchical order (for details refer to [Transforms](#trans) section).
        * TU is always smaller or equal to PU.
    3. Smallest PU is 4x4. In comparison with VP9 most of mode/prediction info was moved from 8x8 to 4x4 level (by experiment \[CB4X4\]). Following things are set on 4x4, 4x8, 8x4 level:
        * Intra/Inter decision
        * Reference frame
        * Interp filter for Inter pred
        * More?
    4. This [CB4X4] experiment has more indirect consequences (e.g. granularity of blocks for getting spatial MV predictors was reduced from 8x8 to 4x4 as well).
## <a id='intra'>INTRA prediction</a>
* Luma and Chroma within same PU can use different Intra prediction (written to bitstream separately for Y and for UV). Cb, Cr share same mode. All Intra pred modes except IBC are applicable to:
    1. All PUs in key-frame
    2. All PUs in "intra_only" non-key frame
    3. Intra blocks in Inter frames
* Intra pred mode is indicated once for whole PU, but real Intra pred is done on TU basis. Most Intra pred modes are applicable for any valid square and rectangular TU shape/size. There are few exceptions (for Palette and "Filter Intra" modes).
* List of Intra pred modes (with respective mode value):
    1. DC\_PRED (0)
    2. V\_PRED (1), H\_PRED (2)
    3. \[Angular\] D45\_PRED (3), D135\_PRED (4), D113\_PRED (5), D157\_PRED (6), D203\_PRED (7), D67\_PRED (8)
    4. SMOOTH\_PRED (9), SMOOTH\_V\_PRED (10), SMOOTH\_H\_PRED (11)
    5. PAETH\_PRED (12)
    6. \[Chroma only\] UV\_CFL\_PRED (13)
    7. Palette (coded as sub-mode of DC pred)
    8. Filter Intra (coded as sub-mode of DC pred after Palette pred)
    9. Intra Block Copy - IBC (indicated by separate flag in UH)
* Intra pred mode is coded in NBAC as single multi-bit symbol.
* <a id='angular_intra'>Angular modes</a>:
    * \[Angles\] Formally 270 angles from 0 to 269. 3 zones [0-89], [90-180], [181-269] - clock counter-wise. Use pixels from bottom-left, left, top-left, top, top-right.
    * \[Syntax\] The angle is constructed as "_nominalAngle_" + ("_angleDelta_" * "_ANGLE\_STEP_"). "_nominal\_angle_" is indicated by pred mode. "_ANGLE\_STEP_" and range of "_angleDelta_" are hardcoded: 3 and [-3, 3] respectively (uniformly cover gaps between "_normative\_angles_"). "_nominal\_angles_" are 45, 67, 113, 135, 157, 203 (and V_PRED, H_PRED can also be treated as angular with angles 90 and 180 respectively). For 8x4, 4x8 and 4x4 PUs "_angleDelta_" is always 0 (i.e. only "_nominal\_angles_" are supportted). NBAC entropy probabilities for "_angleDelta_" are uniform on the range.
    * \[Algorithm\]:
        1. LUT holding tangents for each possible angle. 90 entries in the table represent all tangents for whole 270 degrees range (as tangent is calculable from "angle - 90"). LUT entry for particular tangent 1/dx is value dx scaled for 256 (because prediction precision is 1/256 pixel).
        2. Example for zone 0 (angles 0-89).  For pixel with coordinates (r, c) in the PU: decoder gets dx * 256 from the LUT, scales [r + 1] with this value and gets reference pixel location in top-right predictors row as sum 256* (c + (r+ 1) * dx), with precision 1/256 of a pixel:                                                       
        ![Intra pred](pics\Intra_pred.png)
        3. When projection doesn’t hit integer pixel, prediction value is calculated by 2-tap filter using values of neighboring integer pixels: (r(x) * (256 - d ) + r(x + 1) * d) >> 8. Prediction integer pixels are reconstructed pixels prior to deblocking (with some additional filtering applied - see below).                                                    
        ![Intra interp](pics\Intra_interpolation.png)
        4. <span style="color:grey">There was an attempt (experiment \[INTRA\_INTERP\]) to replace 2-tap with switchable 8-tap filter (8Tap, 8Tap\_sharp, 8Tap\_smooth) - approach similar to Inter MC filtering, but filters were different from MC. Finally it was rejected.</span>
        5. Instead, additional rules and filtering are applied to neighboring pixels to get prediction pixels for angular modes:
            * In VP9, if neighbor pixels (row or column) aren't available, they were replaced by (1 << bit\_depth) / 2. In AV1 missing neighbor row/column is replaced by value of closest pixel from available neighbor column/row.
            * Conditional filtering is applied to above and left neighboring pixels depending on angular mode. Angle between perpendicular to prediction line (row or column) and prediction direction is taken. Filtering is chosen depending on this angle. If this angle small (i.e. prediction direction is almost perpendicular to line of prediction pixels), there is simple filtering or no filter at all. More aggressive filtering is applied for bigger angles.                                                            
            ![Intra edge filter](pics\Intra_edge_filter.png)
            ![Intra edge filter modes](pics\Intra_edge_filter_modes.png)
            ![Intra edge filter strengths](pics\Intra_edge_filter_strengths.png)
            * Following neighboring pred pixels aren't filtered: top-left pixel, right-most available pixel from above, most-bottom available pixel from bottom-left, all pixels from top-right.
            * \[Syntax\] Flag in sequence header "enable_intra_edge_filter"
* <a id='paeth_intra'>Paeth mode</a>:
    * Similar to TM (True motion mode) in VP9. TM = Lj + Ti - TL                                           
    ![Paeth](pics\Paeth.png)
    * But in AV1 predictor is not TM itself. It's one of Lj, Ti, TL which has closest value to TM prediction value.
* <a id='smooth_intra'>Smooth mode</a>: Similar to HEVC PLANAR.
* <a id='dc_intra'>DC mode</a>: Same as in VP9, AVC, HEVC.
* <a id='palette_intra'>PALETTE mode</a>. In AV1 it's different from HEVC.
    * \[HEVC\] Palette directly sets pixel colors in CU. This requires big palette table (of size 128) to represent shades of grey with good precision. HEVC uses prediction of palette table. There is no transform for palette CUs. Palette mode affects deblocking (deblocking should be either disabled or strength should be reduced). Palette pixels are removed from neighbor pixel selection for regular Intra.
    * \[AV1\]
        1. Palette gives regular Intra prediction of PU. Then regular motion comp, transform-quant are applied. Small palette table (up to 8 entries) is enough because residual will take care about shades of grey.
        2. Palette table for a block can be predicted from colors of above and left neighbors. In AV1 it's called "Color Cache". There is a flag in bitstream to indicate use or not-use of Color Cache for particular block.
        3. Palette doesn't affect deblocking (could change in the final spec!!!). Palette pixels are treated as regular Intra for Intra pred of neighboring blocks.
        4. Smallest PU/TU size which can apply palette is 8x8. 
        5. As palette is treated as regular intra, palette PUs can be present in both Key- and Non-Key frames.
        6. \[Syntax\] Palette mode is coded as sub-mode of DC pred (if DC mode is chosen, there are additional binary flags to indicate Palette mode for Y and for UV ).
* <a id='filter_intra'>Filter Intra mode</a>.
    * Applied only for square, 2:1, 1:2 TX sizes <=32x32.
    * \[Syntax\] Filter Intra mode is coded as sub-mode of DC pred (there is binary flag "filter\_intra" following after flags for Palette mode). If Palette isn't set and "filter\_intra" is set, it's followed by SE representing 5 possible sub-modes.
    * 5 sub-modes: FILTER\_DC\_PRED, FILTER\_V\_PRED, FILTER\_H\_PRED, FILTER\_D153\_PRED, FILTER\_PAETH\_PRED.
    * \[Idea\] Filter Intra prediction block has more complex texture in comparison with other Intra pred modes. Each prediction pixel inside the TU is calculated from left (H), top (V) and top-left (D) neighbor pixels by simple equation X = clip\_for\_bitdepth(Cv*V + Ch*H + Cd*D). Calculations are spread recursively through the block in wavefront manner. So top and left pixels of TU use recon pixels of neighbor TU. Other inner pixels of TU use their inner left, top, top-left pixel neighbors. Coeffs Cv, Ch, Cd are hardcoded in the standard. Each of 5 sub-modes has own Cv, Ch, Cd values (for FILTER\_V\_PRED only Cv is non-zero, for FILTER\_H\_PRED only Ch is non-zero and so on).
    * \[Practical implementation in AV1\] It's clear that for each pixel recursive calculation process can be replaced by single equation with "original" pixels (pixels from neighbor TU) at input. This equation will contain multiple intermediate "clamping" operations. If we remove intermediate clamping operations and do clamping in the end only, we need additional bits for intermediate results, also we lose some precision in comparison with original recursive calculations, but at that cost we get ability to quickly calculate the whole block at once (no more wavefromt dependency). Need to find optimal block size to not overcomplicate equations for pixels (block shouldn't be too big), and also to benefit from simultaneous calculation for whole block (block should be big enough). In AV1 tradeoff is found as block size 4x2 (it has 7 neighboring pixels from top and left, and thus each pred pixel is calculated using 7-tap filter).
    * Algorithm:
        1. TU is divided to 4x2 blocks.
        2. For each of 5 sub-modes there are 8 hardcoded 7-tap filters (array 7\_taps[7][8] - 7 taps for each of 8 pixels in 4x2 block). Each filter gets neighboring pixels of 4x2 block (p0, p1, …,, p6) at input and produce one of 8 pixels of 4x2 block at output.                                       
        ![Filter_Intra](pics\Filter_Intra.png)
        3. All the pixels in 4x2 blocks are calculated at once (no dependencies inside 4x2 block) using equation: For each pixel k, k 0,…,7: X[k] = clip\_for\_bitdepth(7\_taps[k][0] * p0 + 7\_taps[k][1] * p1 + … + 7\_taps[k][6] * p6). Intel intention is to calculate whole 4x2 block in one cycle.
        4. 4x2 blocks depend on each other and processed in waterfront manner.
* <a id='chroma_from_luma'>Chroma from Luma (CFL)</a>.
    * For Chroma only. Can be applied to any PU block size and shape (square or rectangular). Has no impact to Luma (Luma can use any intra pred mode with no additional restrictions).
    * CFL forms regular Intra pred followed by motion comp, transform and quantization. 
    * Gives around 10% BDRATE gain for chroma component. 
    * The idea is to get Luma recon, remove DC part (average luminance characteristic) and take AC only (higher frequencies, characteristic of local luminance changes). Take DC pred for chroma block (predicted average luminance characteristic)  and add AC part (real local luminance changes) from Luma component.
    * \[Algorithm\] Input is Luma PU, output is prediction for Chroma PU.
        1. For each TU inside Luma PU:
            1. Get recon Luma pixels before in-loop filters.
                * Special case. It can happen that whole Luma TU is outside of picture boundary (must not be coded), but respective area in Chroma PU must be coded (because it's covered by bigger TU block). Then we simple padding (replication of border pixel) is used to propagate Luma recon pixels to outside area.
            2. Subsample to match with Chroma resolution with Box Filter (simple averaging function, e.g. for 420 - 2x2 average, for 422 - 1x2 average)
            3. Get average of subsampled block (DC part).
            4. Get AC part by subtracting DC part from subsampled block. This will form _processed Luma PU_.
        2. Read scaling factor αu for U (αv for V) from bitstream. αu (αv) is fractional signed number with 16 possible magnitudes  [0.125, 0.25, 0.375, …, 1.75, 1.875, 2.0]. Magnitude is encoded in NBAC as single 16-value multisymbol.
        3. Multiply pixels of _processed Luma PU_ by scaling factor for U(V).
        4. Calculate DC pred for U(V).
        5. Add multiplied _processed Luma_ PU to this DC pred
* <a id='intra_block_copy'>Intra block copy (IBC)</a>.
    * The idea is to use Inter prediction/reconstruction process within Intra frame.
    * \[Syntax\]
        1. Flag _allow\_screen\_content\_tools_ in UH
        2. If _allow\_screen\_content\_tools_ = 1, additional flag _allow\_intrabc_ in UH.
        3. If _allow\_intrabc_ = 1, there is _use\_intrabc_ flag on PU level
    * IBC PU has MV pointing to other block in the same frame. IBC PU passes usual Inter recon process (MV reconstruction, inverse transform-quant, motion comp), but with big amount of restrictions:
        1. Applied only for KEY\_FRAME and for Inter INTRA\_ONLY\_FRAME (can't be used inside regular Inter frame)
        2. When _allow\_intrabc_ = 1, all types of in-loop filtering are disabled for the whole frame (doesn't matter if it really contains IBC or not). So no filter-related syntax present in UH. 
            * Thus motion comp for IBC is done using recon pixels w/o any in-loop filtering.
        3. No temporal candidates in MV reconstruction process (only spatial candidates). But IBC blocks provide spatial MV candidates for neighboring IBC blocks.
        4. MV (for Luma) is always integer.
        5. Chroma MV still can be half pel fractional. But it's forced to use biliniar interpolation filter for MC.
        6. Only DCT\_DCT transform can be used within IBC PU.
        7. MVs for IBC PUs are restricted in direction and range:
            1. MV can't cross tile boundary regardless of tile boundary dependency/independency.
            2. Of course decoding must be causal, so IBC can use only previously reconstructed PUs in raster order.
            3. In addition extra 256 pixel delay is introduced for current row of SBs (IBC PU from particular SB can't use blocks from same SB row which are closer than 256 pixels to current PU). This limitation carries across to the previous SB row (to allow wavefront parallelism). Below is example of this limitation for left 64x64 blocks of 128x128 SB:
            ![IBC](pics\IBC.png)
## <a id='inter'>INTER prediction</a>
* <a id='reference_frames'>Reference frames</a>.
    * Following is just like in VP9:
        1. DPB size is 8 frames.
        2. DPB update is explicit (no sliding window). When frame is encoded/decoded, reconstruct of this frame may be written to one or more DBP slots. Each frame  (except repeated frames, they have _show\_existing\_frame_ = 1) has bit map _refresh\_frame\_flags_ (8 bits - one bit for each DPB slot) indicating which DPB slots are replaced with reconstruct of current frame. 
            1. 0xff means that frame is written to each DPB slot, 0x00 means that frame isn't written to DPB and can't be used as reference in the future.
            2. For key-frame _refresh\_frame\_flags_ isn't written to bitstream (it's always 0xff, so key-frame occupies whole DPB).
            3. It's requirement of the spec that for intra-only non-key frames (aka INTRA\_ONLY\_FRAME) _refresh\_frame\_flags_ can't be 0xff. So INTRA\_ONLY\_FRAME MUST not be random access point.
            4. Repeated frame takes _refresh\_frame\_flags_ map from the frame it repeats
        3. Each inter frame has array of active references _ref\_frame\_idx[]_ (so ref frame lists are signaled explicitly, in general case there is no default algo for ref list construction, with one exception for AV1 - see below). Each index in array has own name (e.g. VP9 has 3 active refs with names: idx = 1 is called LAST\_FRAME, idx = 1 is called GOLDEN\_FRAME, idx = 2 is called ALTREF\_FRAME; names are to deal with patent issues). Entries of _ref\_frame\_idx_ are indexes in DPB. Each entry of _ref\_frame\_idx_ can point to any DPB slot (repeats are OK).
        4. Dynamic reference scaling feature allows to change resolution w/o start of new sequence (i.e. w/o insertion of key frame with new sequence header). Encoder/decoder upscales/downscales reference frames to align resolution with current frame and then does encoding/decoding as usual. Upscale/downscale algo is normative (hardcoded in the standard). For both VP9 and AV1 max ref frame upscale ratio is 16, max ref frame downscale ratio is 2.
        5. Resolution of current frame can be taken from one of its active references (to avoid spending bits for explicit signaling).
    * In addition to VP9:
        1. 4 more active refs are added (up to 7 Inter refs per frame for AV1). New ref frames names: LAST2\_FRAME, LAST3\_FRAME,  BWDREF\_FRAME, ALTREF2\_FRAME. Total list has 7 refs divided to 2 groups:
            * Group 1: LAST\_FRAME, LAST2\_FRAME, LAST3\_FRAME, GOLDEN\_FRAME (indexes 0 - 3 in _ref\_frame\_idx[]_)
            * Group 2: BWDREF\_FRAME, ALTREF2\_FRAME, ALTREF\_FRAME (indexes 4-6 in _ref\_frame\_idx[]_)
        2. You can think about these 2 groups as about list 0 and list 1 in AVC/HEVC. Group 1 is usually used for forward refs, and Group 2 - for backward refs (and GOLDEN\_FRAME is like LTR in AVC/HEVC ref lists). But there are no actual limitations (Group 1 can contain future frames and vice versa).
        3. To save bits active refs can be signaled in reduced form ("short signaling"): only LAST\_FRAME and GOLDEF\_FRAME are signaled explicitly and the rest of active refs are calculated by hardcoded algo using order hints (it's mix of explicit signaling and ref list construction).
        4. Display order of frame is indicated by _order\_hint_ parameter in UH (similar to POC concept in AVC) which is mandatory present in UH of each non-repeated frame (i.e. frame with _show\_existing\_frame_=0).
            * _order\_hint_ is coded with number of bits indicated in sequence header. So it wraps from time to time.
            * AV1 spec doesn't give any rule or restriction for values of _order\_hint_. But to make it useful it should represent real temporal position of frames and thus truly represent temporal distance between frames.
            * All the decode tools based on order hints don't use value of _order\_hint_ directly. They use function _get\_relative\_dist(first\_hint, second\_hint)_ to correctly calculate temporal difference between frames (this function takes "raw" order\_hint values from bitstream and takes care about wrapping).
            * There is a flag _enable\_order\_hint_ in sequence header. If _enable\_order\_hint_=1 the sequence uses decoder tools based on display order of frames. Following decode features rely on order hints (they are disabled when _enable\_order\_hint_ = 0 in sequence header):
                * "Motion field" estimation and use of temporal MV candidates for MV reconstruction.
                * Weighted compound prediction (uses distances between current and ref frames to calculate weights for blending 2 blocks of prediction pixels to single prediction block).
                * "short signaling" for ref frames in UH.
                * Skip mode for PUs.
                * Use of negative ref frame sign bias (this tool improves accuracy of motion vector prediction for backward references).
        5. Frame id numbers (_current\_frame\_id_, _display\_frame\_id_, _delta\_frame\_id_) were added to uncompressed header. They are not required for decoding (there are no normative decoding tools using them as input), but they can be used by decoder to catch missing reference frames.
            * Each non-repeated frame (_show\_existing\_frame_=0) has _current\_frame\_id_ coded with number of bits signaled in sequence header (so it wraps from time to time). There is no strict rule for calculation of next current\_frame\_id from previous one (e.g. frame\_num in AVC had strict calculation rules to check gaps in frame\_nums). The only restriction for _current\_frame\_id_ is that difference between current id and previous id must be less than half of _current\_frame\_id_ coding range (if wrap occurred between pervious and current then current is treated w/o wrap for checking this restriction). This restriction isn't actual for KEY\_FRAME (it can have any _current\_frame\_id_ within range given by sequence header).
                * Encoder/Decoder internally holds current\_frame\_ids for all frames in DPB (in array RefFrameId[8]).
                * Missing references are controlled by explicit signaling of _delta\_frame\_id_ for each active reference in uncompressed header and comparison of (roughly) _current\_frame\_id_ + _delta\_frame\_id_ with respective entry of  RefFrameId[].
            * Each repeated frame has _display\_frame\_id_ which must be equal to RefFrameId[] entry for reference frame which is being repeated.
* <a id='inter_pred_modes'>Inter prediction modes (skip, single, compound)</a>.
    * There are 3 possible Inter prediction modes for PU: SKIP, SINGLE\_REFERENCE and COMPOUND\_REFERENCE (similar to bidirectional pred in AVC/HEVC).
    * Each non-repeated Inter frame has flag _reference\_select_ in UH. If _referene\_select_=0 then the only possible pred mode for Inter PU within current frame is SINGLE\_REFERENCE. If _referene\_select_=1 then Inter PU can use any of 3 modes with following limitations:
        1. SKIP and COMPOUND\_REFERENCE are applicable only for 8x8 and bigger PUs.
        2. For SKIP mode order hints MUST be enabled (_enable\_order\_hint_=1 in sequence header).
    * For each PU encoder/decoder internally uses array RefFrame[2] to indicate reference frame(s) used by this PU.
        1. For Intra PU RefFrame[0] = INTRA\_FRAME and RefFRame[1] = NONE (such notation allows IBC blocks to pass through regular Inter MC/recon process).
        2. For SKIP both entries of RefFrame[] are chosen as closest to current frame by order hints.
        3. For SINGLE\_REFERENCE RefFrame[0] holds one of active Inter refs and RefFRame[1] = NONE.
        4. For COMPOUND\_REFERENCE each entry of RefFrame[] holds one of active Inter refs.
    * skip\_mode: **ADD INFO ABOUT SKIP MODE!!!!**
    * If _skip\_mode_ flag for PU is 0, PU has additional flag _comp\_mode_ to choose between SINGLE\_REFERENCE and COMPOUND\_REFERENCE.
    * SINGLE\_REFERENCE mode (_comp\_mode_ = SINGLE\_REFERENCE): **ADD INFO ABOUT SINGLE REFERENCE MODE!!!!**
    * COMPOUND\_REFERENCE mode (_comp\_mode_ = COMPOUND\_REFERENCE): **ADD INFO ABOUT COMPOUND\_REFERENCE MODE!!!!**
* <a id='obmc'>Overlapped macroblock motion compensation (OBMC)</a>.
    * When OBMC is used, motion comp is changed to blend other prediction blocks into original prediction block.
    * \[Algorithm\]:
        1. Take regular Intra-prediction of current block (block C, and respective prediction P(C)).
        2. Get prediction blocks for blending:
            1. Take all top and left neighbor blocks (N blocks or Ns) of block C. If N is Inter, get MV(N)/ref(N). Let’s say that N has size Nx x Ny and C has size Cx x Cy
            2. Consider rectangular block Nc inside block C (aka overlapped region) which:
                * Has common border with block N.
                * Has size Nx x Cy/2 if N is top block, and has size Cx/2 x Ny is N is left block
            3. Get prediction blocks for blending (P(Nc)) by applying MV(N)/ref(N) to block Nc.
        3. Get OBMC prediction (Pobmc(C)) by blending all P(Nc) and P(C) for each particular overlapped region. If region is overlapped by 2 N blocks (both top and left), one 1-1 blending is done per turn (top is always first, left - second).
        4. Get regular P(C) for regions w/o overlap (left-right quarter of a block is always untouched by overlap)
        5. Combine all Pobmc(C) and P(C) to get final Inter-prediction of block C.
        6. For compound block C OBMC is done using final compound prediction for C (i.e.  P(C) are result of compound prediction). If N is compound, only one MV(N)/ref(N) is used to get P(N) for respective overlapped region.
        7. Not clear what MV to save for OBMC blocks for future use by neighboring and co-located blocks.. Also not clear which MVs to use to get P(N) if C is warp/global, and N is regular Intra.
    * Blending function:
        * Weighted sum of P(C) and P(N) pixels. Weight of P(N) decreases and P(C) increases at bigger distance from C block boundary (cosine-based function with early exit).                           
        ![OBMC_blending](pics\OBMC_blending_small.png)
        * Separate blending functions for top and left neighbors. For particular overlapped area top and left functions can be same or different.
        * For each block size SxS there is MASK function represented by SxS matrices with weights for P(C) and each P(N).
        * There is no need to store whole SxS matrices since they have duplicated columns and rows. In the code rows/columns with distinct values are stored as 1-D arrays with weights multiplied by 64.
    * \[Syntax\]:
        * Flag on frame level if OBMC can be used for blocks.
        * Syntax element _motion\_mode_ (if present) tells if OBMC or Local Warp is used to get Inter prediction for current block. OBMC and Local Warp are mutually exclusive
* <a id='global_motion'>Global Warp Motion</a>.                                                   
    ![Affine](pics\Affine_small.png)
    * \[Models\] Homography model is used to represent difference (warped motion) between current and reference frame. There are 4 models with respective complexities (how many hij params in the matrix H are different from Identity diagonal matrix):
        1. Identity (0 params)
        2. Simple translation (2 params)
        3. Rotzoom (simplified affine - "rotation + zoom" only) (4 params)
        4. Affine (full affine) (6 params)
    * \[Syntax\]
        1. Motion model and respective parameters for each reference frame (up to 6 active refs per frame) are stored in uncompressed header (if change between current and ref frame fit into one of models good enough). If there is no good hit to motion model then GM is disabled for a frame. Model parameters are coded as difference with respective parameters from prev frame.
        2. When GM is enabled on frame level, and PU is >=8x8, then ZEROMV pred mode for PU is overloaded with global motion parameters.
    * \[Warp projection\] Prediction for the PU is got by doing warp projection to the ref frame using GM params.
        1. Position projection for each pixel of current block: (x’, y’, 1)<sup>T</sup> = H * (x, y, 1)<sup>T</sup>. Some of projected pixels obviously may be not in int-pel position.
        2. Then 8-tap sub-pel interpolation. 8-tap filters are different for vertical and horizontal directions. They are predefined (no syntax in bitstream).
    * \[Restrictions\] GM doesn't support compound pred and can't be used together with OBMC.
* <a id='local_motion'>Local Warp Motion</a>.
    * Frame-based homomorphic model isn't sufficient when objects on the scene are moving in different directions or distributed at different scene depths. PU-based Local Warp models are used for such cases. Same models as for GM are used. Matrix H is generated per PU. The feature is super-heavy. Encoder isn't expected to be real-time when using this feature.
    * Matrix H is estimated from motions of neighbor blocks. Encoder and decoder do same calculations. Local motion is always assumed to be full affine.
        1. \[Pick neighbors\] Up to 8 neighbors from left, top, top-left. Neighbors are picked up till count 8 by pre-defined order. Neighbor must be coded with unidirectional Inter mode with same reference (if not - it's ignored).
        2. \[Estimation of matrix H\] h<sub>ij</sub> are estimated from MVs of current and neighbor blocks with following math:
        ![Local_warp_1](pics\Local_warp_1_small.png)
        ![Local_warp_2](pics\Local_warp_2_small.png)                                                  Where
            * (x<sub>i</sub>, y<sub>i</sub>) is center of current or neighbor block (i = 0 for cur block, i = 1 for 1st neighbor and so on).
            * (x<sub>i</sub>', y<sub>i</sub>') is projections of (x<sub>i</sub>, y<sub>i</sub>) at the reference frame.
        3. \[Syntax\] Syntax element _motion\_mode_ (if present) tells if OBMC or Local Warp is used to get Inter prediction for current block.  OBMC and Local Warp are mutually exclusive.
* <a id='mc_interpolation'>MC interpolation filters</a>.
    * **FOLLOWING INFO IS OBSOLETE, NEED TO ADD ACTUAL INFO!!!**
    * \[VP9\] has 1/8 pixel precision, uses 8-tap filters with 8 bit per tap. Has 3 filters: standard, smooth, sharp.
    * [AV1] still has 1/8 pel precision. New tools:
        1. \[Adopted\] Number of bits per tap reduced 8-> 7 (to always fit in 16-bit signed arithmetic). Number of taps is reduced 8->6 for standard and smooth, and remains 8 for sharp filer.
        2. <span style="color:grey">\[Rejected\] Additional 10Tap and 12Tap Sharp filter. Add 2 more 8Tap smooth filters (3 in total).</span>
        3. \[Adopted\] Dual filter.
            1. Use separate filter for each direction (vert, horz). It requires additional bits to code 2 filters instead of 1.
            2. For CABAC separate context is used to code filter mode for each direction (context depends on respective mode of neighboring blocks).
            3. If both vert and horz filters are 12Tap, vert is degraded to 8Tap (8Tap is done first, and then 12Tap).
## <a id='transforms'>Transforms</a>
## <a id='quantization'>Quantization</a>
## <a id='deblocking'>Deblocking</a>
## <a id='post_deblocking'>Post deblocking</a>
### <a id='cdef'>CDEF</a>
### <a id='superres'>Super resolution</a>
### <a id='loop_restoration'>Loop restoration</a>
## <a id='filmg_rain'>Film Grain</a>
## <a id='entropy_coding'>Entropy coding</a>

