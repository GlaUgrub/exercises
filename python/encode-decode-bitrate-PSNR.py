import os
import subprocess
import re

def exit_on_error(msg):
    print(msg)
    sys.exit()

def get_float(string):
    m = re.search(r"[\d.]+", string)
    if m == None:
        exit_on_error("[ERROR]: no number in the line:\" " + string + "\"")
    return m.group()

def get_psnr(lines, channel):
    pattern = "avg_metric=" + channel +"-PSNR"
    for line in lines:
        if (pattern in line):
            return get_float(line)


#folders and apps
foldern = r"D:\MEDIASDK_STREAMS\YUV"
bin_folder = r"D:\Lab\eQuana\bin"
tmp_folder = r"D:\Lab\eQuana\tmp"
mfx_transcoder = os.path.join(bin_folder, "mfx_transcoder.exe")
mfx_player = os.path.join(bin_folder, "mfx_player.exe")
metrics_calc_lite = os.path.join(bin_folder, "metrics_calc_lite.exe")
folder_to_fix = r"D:\Lab\eQuana\.cache\1080p60_base_layer.qp.c6d91079bd36f0efb37a6e84f11d5209"

label = "1080p60_base_layer"

streams = {
    "bq_terrace_1920x1080p" : {
        "frames_in"  : 593,
        "frames_out" : 297,
        "fps" : 60,
        "qps" : [34, 31, 27, 25],
        "sizes" : [],
        "bitrates" : [],
        "psnrsY" : [],
        "psnrsU" : [],
        "psnrsV" : []
    },
    "crowd_run_1920x1080p" : {
        "frames_in"  : 497,
        "frames_out" : 249,
        "fps" : 50,
        "qps" : [38, 34, 30, 26],
        "sizes" : [],
        "bitrates" : [],
        "psnrsY" : [],
        "psnrsU" : [],
        "psnrsV" : []
    },
    "ducks_take_off_1920x1080p" : {
        "frames_in"  : 497,
        "frames_out" : 249,
        "fps" : 50,
        "qps" : [37, 35, 31, 28],
        "sizes" : [],
        "bitrates" : [],
        "psnrsY" : [],
        "psnrsU" : [],
        "psnrsV" : []
    },
    "park_joy_1920x1080" : {
        "frames_in"  : 497,
        "frames_out" : 249,
        "fps" : 50,
        "qps" : [37, 33, 29, 26],
        "sizes" : [],
        "bitrates" : [],
        "psnrsY" : [],
        "psnrsU" : [],
        "psnrsV" : []
    }
}

# streams = {
#     "bq_terrace_1920x1080p" : {
#         "frames_in"  : 593,
#         "frames_out" : 297,
#         "fps" : 60,
#         "qps" : [34, 31, 27, 25],
#         "sizes" : [],
#         "bitrates" : [],
#         "psnrsY" : [],
#         "psnrsU" : [],
#         "psnrsV" : []
#     }
# }

# streams = {    
#     "crowd_run_1920x1080p" : {
#         "frames_in"  : 497,
#         "frames_out" : 249,
#         "fps" : 50,
#         "qps" : [38, 34, 30, 26],
#         "sizes" : [],
#         "bitrates" : [],
#         "psnrsY" : [],
#         "psnrsU" : [],
#         "psnrsV" : []
#     }
# }


for stream in streams:
    #prepare local params
    frames_in = streams[stream]["frames_in"]
    frames_out = streams[stream]["frames_out"]
    formal_fps_in = streams[stream]["fps"]
    formal_fps_out = int (formal_fps_in / 2)
    fps_out = 30
    
    name_in = "_".join([stream, str(frames_in), str(formal_fps_in)]) + ".yuv"
    yuv_name_out =  "_".join([stream, str(frames_out), str(formal_fps_out)]) + ".yuv"
    path_in = os.path.join(foldern, name_in)
    
    qp_idx = 0

    for qp in streams[stream]["qps"]:
        #encoding
        name_coded = ".".join([label, "qp", "qp-" + str(qp), yuv_name_out, "h265"])
        path_coded = os.path.join(tmp_folder, name_coded)
        cmd = " ".join([mfx_transcoder, "h264 -i", path_in, "-o", path_coded, "-w 1920 -h 1080 -hw -g 1000 -r 8 -RateControlMethod 3 -QPI", str(qp), "-QPP", str(qp), "-QPB", str(qp), "-BRefType 2 -GPB 16"])
#         subprocess.run(cmd)
        
        #decoding
        name_decoded = ".".join([name_coded, "yuv"])
        path_decoded = os.path.join(tmp_folder, name_decoded)
        cmd = " ".join([mfx_player, "-i", path_coded, "-o", path_decoded, "-sw"])
#         subprocess.run(cmd)
        
        #calc and save bitrate
        size_bytes = os.stat(path_coded).st_size
        streams[stream]["sizes"].append(size_bytes)
        size_bits = size_bytes * 8
        bitrate = size_bits * fps_out / frames_out
        streams[stream]["bitrates"].append(bitrate)
        
        #calc and save psnr
        path_ref = os.path.join(foldern, yuv_name_out)
        path_log = os.path.join(tmp_folder, "tmp.log")
        log = open(path_log, 'w')
        cmd = " ".join([metrics_calc_lite, "-i1", path_ref, "-i2", path_decoded, "-w 1920", "-h 1080", "psnr all"])        
        print(cmd)
        subprocess.run(cmd, stdout=log)
        log.close()
        with open(path_log, 'r') as log:
            lines = []
            for line in log:
                lines.append(line.strip())
            psnr = get_psnr(lines, "Y")
            streams[stream]["psnrsY"].append(psnr)
            psnr = get_psnr(lines, "U")
            streams[stream]["psnrsU"].append(psnr)
            psnr = get_psnr(lines, "V")
            streams[stream]["psnrsV"].append(psnr)

        files = [f for f in os.listdir(folder_to_fix) if os.path.isfile(os.path.join(folder_to_fix, f))]
        for file in files:
            path_to_file = os.path.join(folder_to_fix, file)
            if (stream in file and str(qp) in file and "details" not in file):
                bad_file = open(path_to_file, "r")
                good_file_name = ".".join(["qp-" + str(qp), yuv_name_out, "yaml"])
                path_to_good_file = os.path.join(folder_to_fix, good_file_name)
                good_file = open(path_to_good_file, "w")
                
                bad_lines = []
                for bad_line in bad_file:
                    good_line = bad_line
                    if "frames" in bad_line:
                        good_line = re.sub(r'[\d]+', str(frames_out), bad_line, 1)
                    if "file_size" in bad_line:
                        good_line = re.sub(r'[\d]+', str(streams[stream]["sizes"][qp_idx]), bad_line, 1)
                    if "PSNR" in bad_line:
                        bad_line = re.sub(r'U: [\d]+', "U: " + str(streams[stream]["psnrsU"][qp_idx]), bad_line, 1)
                        bad_line = re.sub(r'V: [\d]+', "V: " + str(streams[stream]["psnrsV"][qp_idx]), bad_line, 1)
                        good_line = re.sub(r'Y: [\d]+', "Y: " + str(streams[stream]["psnrsY"][qp_idx]), bad_line, 1)
                    if "real_bitrate" in bad_line:
                        good_line = re.sub(r'[\d.]+', str(streams[stream]["bitrates"][qp_idx]), bad_line, 1)
                    good_file.write(good_line)
                    
                good_file.close()
                bad_file.close()
        
        qp_idx = qp_idx + 1
        
    print(streams[stream])
