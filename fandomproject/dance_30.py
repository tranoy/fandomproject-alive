import os
import subprocess
from glob import glob
import cv2
from cv2 import VideoWriter_fourcc, VideoWriter
import math
import mediapipe as mp
from statistics import mean
import numpy as np

OUTPUT_DIR="./media/output"  # "challenge/static/output"
UPLOAD_DIR="./media/challenge_upload"
EXIST_FLAG="-y" # ignore existing file, change to -y to always overwrite
PRAAT_PATH="./Praat.exe"  # "/Applications/Praat.app/Contents/MacOS/Praat"
SEARCH_INTERVAL = 30 # in secs
CURRENT_DIR = os.getcwd()  # 현재 폴더 위치 가져옴
# CROSSCORRELATE_FILE = 'C:/Users/User/Desktop/big_git/fandomproject/challenge/crosscorrelate.praat'

def compare_video(ref_clip, comparison_clip, nickname, title):
    # --------------------------------------------------------- VIDEO PROCESSING --------------------------------------------------------------------------------------


    def get_duration(filename): # returns the duration of a clip
        captured_video = cv2.VideoCapture(filename)

        fps = captured_video.get(cv2.CAP_PROP_FPS) # frame rate
        frame_count = captured_video.get(cv2.CAP_PROP_FRAME_COUNT)

        duration = (frame_count/fps) # in secs
        return duration


    def get_frame_count(filename): #returns the number of frames in a clip
        "return tuple of (captured video, frame count)"
        captured_video = cv2.VideoCapture(filename)

        frame_count = int(math.floor(captured_video.get(cv2.CAP_PROP_FRAME_COUNT)))
        return captured_video, frame_count

    # utils
    mpDraw = mp.solutions.drawing_utils
    mpPose = mp.solutions.pose

    def landmarks(video):
        pose = mpPose.Pose() # initialise pose object

        xy_landmard_coords = [] # we only care about x and y coords, NOT z
        frames = []
        landmarks = []

        # capture video
        captured_video, frame_count = get_frame_count(video)

        # process video
        for i in range(frame_count): 
            success, image = captured_video.read() # read frames one by one
            frames.append(image)
            imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # formatting

            # get landmarks
            landmarks_in_frame = pose.process(imgRGB)
            landmarks.append(landmarks_in_frame)
            # print(f"landmarks={landmarks[0]}")

            # information about the joint positions
            # xy_landmard_coords.append([(lm.x, lm.y) for lm in landmarks_in_frame.pose_landmarks.landmark])  # 원본
            if landmarks_in_frame.pose_landmarks is not None:
                xy_landmard_coords.append([(lm.x, lm.y) for lm in landmarks_in_frame.pose_landmarks.landmark])

        return xy_landmard_coords, frames, landmarks



    def difference(xy1, xy2, frames1, frames2, landmarks1, landmarks): # x and y positions of joints | frames | landmarks - info including z
        # all the joints we are using
        # ref: https://mediapipe.dev/images/mobile/pose_tracking_full_body_landmarks.png
        connections = [(16, 14), (14, 12), (12, 11), (11, 13), (13, 15), (12, 24), (11, 23), (24, 23), (24, 26), (23, 25), (26, 28), (25, 27)]

        # keep track of current number of out of sync frames (OFS)
        out_of_sync_frames = 0
        score = 100

        # number of frames
        num_of_frames = min(len(xy1), len(xy2)) # avoids empty displays

        print("Analysing dancers...")
        #writing our final video
        output_path = f'{OUTPUT_DIR}/output.mp4'  # 오디오없이 만들어질 output video 경로
        video = VideoWriter(output_path, VideoWriter_fourcc(*'h264'), 30.0, (2*720, 1280), isColor=True)

        for f in range(num_of_frames): # f = frame number

            # percentage difference of joints per frame
            percentage_dif_of_frames = []

            # get position of all joints for frame 1,2,3...etc
            p1, p2 = xy1[f], xy2[f]

            for connect in connections:
                j1, j2 = connect
                
                # gradients
                # [j] tells you the joint no. ,  [0] -> x coord , [1] -> y coord
                g1 = (p1[j1][1] - p1[j2][1]) / (p1[j1][0] - p1[j2][0])
                g2 = (p2[j1][1] - p2[j2][1]) / (p2[j1][0] - p2[j2][0])

                # difference (dancer1 taken as reference gradient)
                dif = abs((g1 - g2) / g1)
                percentage_dif_of_frames.append(abs(dif))

            # FINISHED analysing connections
            frame_dif = mean(percentage_dif_of_frames) # mean difference of all limbs per frame

            # DRAW LIVE COMPARISON
            frame_height, frame_width, _ = frames1[f].shape # dancer1 video is reference size
            mpDraw.draw_landmarks(frames1[f], landmarks1[f].pose_landmarks, mpPose.POSE_CONNECTIONS)
            mpDraw.draw_landmarks(frames2[f], landmarks[f].pose_landmarks, mpPose.POSE_CONNECTIONS)
            display = np.concatenate((frames1[f], frames2[f]), axis=1)

            colour = (0, 0, 255) if frame_dif > 7 else (255, 0, 0) # red = big difference, BAD!

            cv2.putText(display, f"Diff: {frame_dif:.2f}", (40, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, colour, 3)

            # could add warning pause / sign here
            if frame_dif > 7:
                out_of_sync_frames += 1 # use for deduction

            # live score
            score = ((f+1 - out_of_sync_frames) / (f+1)) * 100.0 # +1 to avoid divide by zero on first frame
            cv2.putText(display, f"Score: {score:.2f}%", (frame_width +40, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, colour, 3)

            #cv2.imshow(str(f), display)
            video.write(display)
            #cv2.waitKey(1) # show frame

        video.release() # finish capturing output video
        return score, output_path


    # --------------------------------------------------------- SYNCING -----------------------------------------------------------------------------------


    def extract_clip_name(path):
        "extract file name from the path, excluding file extension"
        return path.split('/')[-1].split(".")[0]

    # _cut.mp4에서 fps=30으로 맞춰서 생성하는 걸로 한번에 해결!!
    def convert_to_same_framerate(clip):
        "convert to 30p and return path to clip with 30fps"
        clip_30 = f"{OUTPUT_DIR}/{extract_clip_name(clip) + '_30'}.mp4"
        os.system(f"ffmpeg {EXIST_FLAG} -i {clip} -filter:v fps=30 {clip_30}")
        return clip_30
        
    

    def validate_reference_clip(ref_clip, comparison_clip):
        "validate reference clip is longer than comparison clip"
        ########### 원본 ###########
        # _, ref_clip_frame_count = get_frame_count(ref_clip)
        # _, comparision_clip_frame_count = get_frame_count(comparison_clip)
        # if not (ref_clip_frame_count > comparision_clip_frame_count): 
        #     print(f"Reference clip {ref_clip} has to be longer than comparision clip {comparison_clip}")
        #     sys.exit(-1)
        
        #### 프레임 수가 아니라 영상의 길이 비교로 수정 ####
        ref_clip_duration = get_duration(ref_clip)
        comparision_clip_duration = get_duration(comparison_clip)
        if not (ref_clip_duration <= comparision_clip_duration): 
            print(f"Comparision clip {comparison_clip} has to be longer than reference clip {ref_clip}")
            sys.exit(-1)


    def convert_to_wav(clip):
        "returns path to wav file of clip"

        clip_wav = f"{OUTPUT_DIR}/{extract_clip_name(clip)}.wav"
        command = f"ffmpeg {EXIST_FLAG} -i {clip} {clip_wav}"
        os.system(command)

        return clip_wav



    # IMPORTANT: The input clips might be difference lengths
    # -> trim clips so only compare when dancers are doing the same amount / section of the choreo
    def find_sound_offset(ref_wav, comparison_wav):
        # find offset between: ref.wav and clip_name.wav
        start_position = 0
        # command = f"{PRAAT_PATH} --run 'crosscorrelate.praat' {ref_wav} {comparison_wav} {start_position} {SEARCH_INTERVAL}"
        command = f'"{PRAAT_PATH}" --run "crosscorrelate.praat" {ref_wav} {comparison_wav} {start_position} {SEARCH_INTERVAL}'
        # note: code in separate praat file
        offset= subprocess.check_output(command, shell=True)
        offset = offset.decode('utf-8').replace('\x00', '')
        offset = offset.replace('-', '').strip()
        # print('=' * 1000)
        # print(f"OFFSET={offset}")
        # start_offset, end_offset = map(str, offset.split('\n'))
        # start_offset = start_offset.strip()
        # end_offset = end_offset.strip()
        # (did some formatting here to get the offset from b'0.23464366914074475\n' to 0.23464366914074475)
        # print(f"OFFSET={offset}")
        # offset이 사용되는 곳이 command 라인으로 사용되므로 굳이 float형일 필요없이 문자열로 변환해서 반환
        
        # start_offset = start_offset.decode('utf-8').replace('\x00', '')  # bytes타입을 str로 형변환 후 정규식 사용하여 null문자('\x00') 제거
        # start_offset = start_offset.replace('-', '').strip()  # '-'와 문자열의 앞뒤 공백 제거
        
        # end_offset = end_offset.decode('utf-8').replace('\x00', '')
        # end_offset = end_offset.replace('-', '').strip()
        
            # offset_str = str(offset)
        # print(f"start_offset={start_offset}")
            # trimmed_output = re.sub(r'\x00', '', offset_str)
            # trimmed_output = trimmed_output.replace('-', '')
            # trimmed_output = trimmed_output.strip()
        print('=' * 60)
            # print(f"trimmed_output={offset_str}")
        # print(f"start_offset={len(start_offset)}")
            # print(f"offset_str의 길이는 {len(offset_str)}")
        
        # ascii = [ord(s) for s in trimmed_output]
        # print(ascii)
        
            # for i, s in enumerate(offset_str):
            #     print(s)
            #     if s == None:
            #         print(f"trimmed_output의 {i}번째가 null값 입니다.")
            #         sys.exit(-1)
        print('=' * 60)
        # return abs(float(str(offset)[2:-3]))  # 원본
        # return 4.921131467462978 #4.921130702033572
        
        # if offset_str[0] == '-':
        #     offset_str = offset_str[1:]
        # return start_offset, end_offset
        return offset

    # --------------------------------------------------------- COMPUTE SYNC ------------------------------------------------------------------------

    # to make sure both clips are same length before comparison
    def trim_clips(ref_clip, comparison_clip, offset):
        # duration in secs 
        duration = get_duration(comparison_clip)

        ref_cut = f"{OUTPUT_DIR}/{extract_clip_name(ref_clip) + '_cut.mp4'}"
        comparison_cut = f"{OUTPUT_DIR}/{extract_clip_name(comparison_clip) + '_cut.mp4'}"

        # command = f"ffmpeg {EXIST_FLAG} -i {ref_clip} -ss {offset} -t {duration} {ref_cut}"  # 원본
        command = f"ffmpeg {EXIST_FLAG} -i {ref_clip} -ss 0 -t {duration} -filter:v fps=30 {ref_cut}"
        # command = f"ffmpeg {EXIST_FLAG} -i {ref_clip} -ss 0 -to {end_offset} {ref_cut}"
        # print(f"COMMAND={command}")
        os.system(command)
        # command = f"ffmpeg {EXIST_FLAG} -i {comparison_clip} -ss 0 -t {duration} {comparison_cut}"  # 원본
        command = f"ffmpeg {EXIST_FLAG} -i {comparison_clip} -ss {offset} -t {duration} -filter:v fps=30 {comparison_cut}"
        # command = f"ffmpeg {EXIST_FLAG} -i {comparison_clip} -ss {start_offset} -to {end_offset} {comparison_cut}"

        os.system(command)

        return ref_cut, comparison_cut
    
    # 오디오 겹치는 부분만 추출
    # def trim_audio(ref_clip_wav, start_offset, end_offset):
    #     audio_clip = f"{OUTPUT_DIR}/audio_clip.wav"
    #     command = f"ffmpeg {EXIST_FLAG} -i {ref_clip_wav} -ss {start_offset} -to {end_offset} {audio_clip}"
    #     return audio_clip


    def remove_final_videos():
        os.chdir(OUTPUT_DIR)
        
        command = "del *cut.mp4"
        os.system(command)
        # command = "del *30.mp4"
        # os.system(command)
        command = "del output.mp4"
        os.system(command)
        command = "del *.wav"
        os.system(command)
        
        os.chdir(CURRENT_DIR)  # 프로젝트 폴더로 이동
        
        # 업로드한 영상 삭제
        os.chdir(UPLOAD_DIR)
        command = "del *.mp4"
        os.system(command)
        
        os.chdir(CURRENT_DIR)  # 프로젝트 폴더로 이동
        
        
    def combine_audio_video(video, audio):
        outputV = f"{OUTPUT_DIR}/{nickname}_{title}_output.mp4"
        command = f"ffmpeg {EXIST_FLAG} -i {video} -i {audio} -c:v copy -c:a aac -strict experimental {outputV}"
        os.system(command)  # 오디오있는 output video 생성
        return outputV

    # --------------------------------------------------------- PREPARE VIDEOS --------------------------------------------------------------------------------------

    import sys
    # Launch with these arguments
    # python dance_30.py video/cyves.mov video/chuu.mov
    # python dance_30.py video/knock_step.mov video/knock1.mov

    #create output dir
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(CURRENT_DIR)
    
    # if len(sys.argv) < 3:
    #     print(f"Usage:\n {sys.argv[0]} <ref_clip> <comparison_clip>")
    #     sys.exit(-1)

    # ref_clip = sys.argv[1]
    # comparison_clip = sys.argv[2]
    
    # 동영상 규격 확인
    def get_video_dimensions(video_path):
        cap = cv2.VideoCapture(video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()
        return width, height
    
    def video_resize(comparison_clip, comparison_width, comparison_height):
        # 동영상 규격(720 * 1280) 리사이즈
        if comparison_width != 720 and comparison_height != 1280:
            end_idx = comparison_clip.find('.mp4')
            input_video = comparison_clip[:end_idx]
            command = f'ffmpeg {EXIST_FLAG} -i {input_video}.mp4 -vf "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2" -af "aresample=async=1:min_hard_comp=0.100000:first_pts=0" {input_video}_resized.mp4'
            os.system(command)  # 동영상 리사이즈, 저장
            
            comparison_clip = f'{input_video}_resized.mp4'
            return comparison_clip
            
        else:
            return comparison_clip
    
    
    comparison_width, comparison_height = get_video_dimensions(comparison_clip)
    print('-'*300, f"comparison_width={comparison_width}")
    print('-'*300, f"comparison_height={comparison_height}")
    comparison_clip = video_resize(comparison_clip, comparison_width, comparison_height)

    # FULL COMPARE
    # if not (len(sys.argv)>3 and sys.argv[3] == '--compare-only'):
    if not (ref_clip == None and comparison_clip == None):
        print(f"intial clips {ref_clip} {comparison_clip}")
        # ref_clip_30, comparison_clip_30 = convert_to_same_framerate(ref_clip), convert_to_same_framerate(comparison_clip)

        # validate reference clip
        print(f'this is the ref: {ref_clip} and comp: {comparison_clip}')
        validate_reference_clip(ref_clip, comparison_clip)


        # # convert to wav for audio analysis
        ref_clip_wav, comparison_clip_wav = convert_to_wav(ref_clip), convert_to_wav(comparison_clip)

        offset = find_sound_offset(ref_clip_wav, comparison_clip_wav)
        # start_offset, end_offset = find_sound_offset(ref_clip_wav, comparison_clip_wav)
        # gets no. secs the comp clip is ahead of the ref clip

        # ref_cut, comparison_cut = trim_clips(ref_clip_30, comparison_clip_30, offset)
        ref_cut, comparison_cut = trim_clips(ref_clip, comparison_clip, offset)
        
        # audio_clip = trim_audio(ref_clip_wav, start_offset, end_offset)
        print(ref_cut, comparison_cut)
    # # --------------------------------------------------------- MAIN --------------------------------------------------------------------------------------
    else:
    #     ### 원본 ###
    #     # ref_cut = sys.argv[1]
    #     # comparison_cut = sys.argv[2]
        
        ### 수정 ###
        ref_cut = ref_clip
        comparison_cut = comparison_clip

        
    # processing our two dancers
    print(f"model: {ref_cut}, comparision: {comparison_cut} \n")
    xy_dancer1, dancer1_frames, dancer1_landmarks = landmarks(ref_cut)
    xy_dancer2, dancer2_frames, dancer2_landmarks = landmarks(comparison_cut)

    score, output_path = difference(xy_dancer1, xy_dancer2, dancer1_frames, dancer2_frames, dancer1_landmarks, dancer2_landmarks)
    print(f"======={comparison_clip_wav}=======")
    output_path = combine_audio_video(output_path, ref_clip_wav)
    print(f"\n You are {score:.2f} % in sync with your model dancer!")
    print('IN fandomproject/dance_30.py')

    remove_final_videos()
    
    return score, output_path