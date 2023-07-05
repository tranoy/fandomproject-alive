import os
import subprocess
from glob import glob
import cv2
from cv2 import VideoWriter_fourcc, VideoWriter
import math
import mediapipe as mp
from statistics import mean
import numpy as np

OUTPUT_DIR="./media/output"
UPLOAD_DIR="./media/challenge_upload"
EXIST_FLAG="-y" # 파일이 존재해도 무시, overwrite 허용하지 않으려면 -n
PRAAT_PATH="./Praat.exe"
SEARCH_INTERVAL = 30 # in secs
CURRENT_DIR = os.getcwd()  # 현재 폴더 위치


def compare_video(ref_clip, comparison_clip, nickname, title):
    """
    두 영상을 비교해 score와 최종 결과 영상의 경로를 반환
    Args:
        ref_clip: 비교 영상
        comparison_clip: 사용자 영상
        nickname: 사용자 ID
        title: 댄스 챌린지 노래 제목

    Return:
        score: 사용자 댄스 영상의 평균 점수
        output_path: 결과 영상이 저장된 경로

    """


    # --------------------------------------------------------- VIDEO PROCESSING --------------------------------------------------------------------------------------


    def get_duration(filename): 
        """
        영상의 길이 구하기
        Arg:
            filename: 영상

        Return: 영상의 길이(초)
        """
        captured_video = cv2.VideoCapture(filename)

        fps = captured_video.get(cv2.CAP_PROP_FPS) # frame rate
        frame_count = captured_video.get(cv2.CAP_PROP_FRAME_COUNT)

        duration = (frame_count/fps) # in secs
        return duration


    def get_frame_count(filename):
        """
        영상의 frame개수를 측정
        Arg:
            filename: 영상
        Returns:
            captured_video: 튜플 형태의 (catured video, 프레임 개수)
            frame_count: 영상의 프레임 개수
        """
        "return tuple of (captured video, frame count)"
        captured_video = cv2.VideoCapture(filename)

        frame_count = int(math.floor(captured_video.get(cv2.CAP_PROP_FRAME_COUNT)))
        return captured_video, frame_count

    # utils
    mpDraw = mp.solutions.drawing_utils
    mpPose = mp.solutions.pose

    def landmarks(video):
        """
        비디오의 각 프레임에서 랜드마크를 추출
        Arg:
            video: 동영상
        Returns:
            xy_landmard_coords: 각 프레임에서 추출된 랜드마크의 x및 y좌표를 저장한 리스트
            frames: 비디오의 각 프레임 이미지를 저장한 리스트 
            landmarks: 각 프레임에서 추출된 랜드마크 데이터를 저장한 리스트
        """
        pose = mpPose.Pose() # initialise pose object

        xy_landmard_coords = [] # we only care about x and y coords, NOT z
        frames = []
        landmarks = []

        # capture video
        captured_video, frame_count = get_frame_count(video)

        # process video
        for i in range(frame_count): 
            success, image = captured_video.read() # 각 프레임을 읽어옴
            frames.append(image)
            imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # formatting

            # get landmarks
            landmarks_in_frame = pose.process(imgRGB)
            landmarks.append(landmarks_in_frame)
            # print(f"landmarks={landmarks[0]}")

            # 관절 위치에 관한 정보
            if landmarks_in_frame.pose_landmarks is not None:
                xy_landmard_coords.append([(lm.x, lm.y) for lm in landmarks_in_frame.pose_landmarks.landmark])

        return xy_landmard_coords, frames, landmarks



    def difference(xy1, xy2, frames1, frames2, landmarks1, landmarks): # x and y positions of joints | frames | landmarks - info including z
        """
        주어진 두 개의 랜드마크(x, y 좌표), 프레임 이미지 및 랜드마크 데이터를 비교하여 차이를 분석
        Args:
            xy1: 참조 영상의 랜드마크 x, y좌표를 저장하는 리스트
            xy2: 비교 영상의 랜드마크 x, y좌표를 저장하는 리스트
            frames1: 참조 영상의 프레임 이미지를 저장하는 리스트
            frames2: 비교 영상의 프레임 이미지를 저장하는 리스트
            landmarks1: 참조 영상의 랜드마크 데이터를 저장하는 리스트
            landmarks: 비교 영상의 랜드마크 데이터를 저장하는 리스트

        Returns:
            score: 비디오의 프레임별 분석 결과를 기반으로 계산된 점수
            output_path: 분석 결과를 포함한 비디오 파일의 경로
        """

        # 사용하는 모든 관절
        # ref: https://mediapipe.dev/images/mobile/pose_tracking_full_body_landmarks.png
        connections = [(16, 14), (14, 12), (12, 11), (11, 13), (13, 15), (24, 23), (24, 26), (23, 25), (26, 28), (25, 27)]  # 어깨와 골반 이음 제거

        # 동기화되지 않은 현재 프레임(OFS) 수 추적
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
        """
        비디오의 경로로부터 파일 확장자를 제외한 영상의 이름을 추출
        Arg:
            path: 비디오 경로
        
        Return: 
            path.split('/')[-1].split(".")[0]: 비디오 경로에서 추출한 파일 이름
        """
        
        return path.split('/')[-1].split(".")[0]
      

    def validate_reference_clip(ref_clip, comparison_clip):
        """
        참조 영상 유효성 검사
        참조 영상이 비교 영상보다 길어야 함
        그렇지 않으면 안내 문구 출력 후 시스템 비정상 종료
        Args:
            ref_clip: 참조 영상
            comparison_clip: 비교 영상, 즉 사용자 입력 영상
        """
        
        ref_clip_duration = get_duration(ref_clip)
        comparision_clip_duration = get_duration(comparison_clip)
        if not (ref_clip_duration <= comparision_clip_duration): 
            print(f"Comparision clip {comparison_clip} has to be longer than reference clip {ref_clip}")
            sys.exit(-1)


    def convert_to_wav(clip):
        """
        오디오 분석을 위해 wav파일 형식으로 변환
        Arg:
            clip: 영상
        Return:
            clip_wav: 영상에서 오디오만 추출한 파일 경로
        """

        clip_wav = f"{OUTPUT_DIR}/{extract_clip_name(clip)}.wav"
        command = f"ffmpeg {EXIST_FLAG} -i {clip} {clip_wav}"
        os.system(command)

        return clip_wav



    # 중요: 입력 클립의 길이가 다를 수 있음
    # -> trim clips은 댄서들이 같은 양의 안무/섹션을 하고 있을 때만 비교
    def find_sound_offset(ref_wav, comparison_wav):
        """
        두 오디오 파일간의 오디오 오프셋 찾기
        Args:
            ref_wav: 참조 영상의 오디오 파일
            comparison_wav: 비교 영상의 오디오 파일

        Return:
            offset: 오디오 오프셋(두 영상 오디오의 동일한 부분의 시작점)
        """
        start_position = 0
        # 참고: 별도의 praat 파일 실행 코드
        command = f'"{PRAAT_PATH}" --run "crosscorrelate.praat" {ref_wav} {comparison_wav} {start_position} {SEARCH_INTERVAL}'
        offset= subprocess.check_output(command, shell=True)
        offset = offset.decode('utf-8').replace('\x00', '')
        offset = offset.replace('-', '').strip()
        # print('=' * 100)
        # print(f"OFFSET={offset}")
        # print('=' * 100)
        return offset

    # --------------------------------------------------------- COMPUTE SYNC ------------------------------------------------------------------------

    # to make sure both clips are same length before comparison
    def trim_clips(ref_clip, comparison_clip, offset):
        """
        두 영상을 주어진 offset을 기준으로 자름
        Args:
            ref_clip: 참조 영상
            comparison_clip: 비교 영상
            offset: 두 영상 오디오의 오프셋

        Returns:
            ref_cut: offset을 기준으로 자른 참조 영상
            comparison_cut: offset을 기준으로 자른 비교 영상
        """
        # duration in secs 
        duration = get_duration(comparison_clip)

        ref_cut = f"{OUTPUT_DIR}/{extract_clip_name(ref_clip) + '_cut.mp4'}"
        comparison_cut = f"{OUTPUT_DIR}/{extract_clip_name(comparison_clip) + '_cut.mp4'}"

        command = f"ffmpeg {EXIST_FLAG} -i {ref_clip} -ss 0 -t {duration} -filter:v fps=30 {ref_cut}"
        os.system(command)
        
        command = f"ffmpeg {EXIST_FLAG} -i {comparison_clip} -ss {offset} -t {duration} -filter:v fps=30 {comparison_cut}"
        os.system(command)

        return ref_cut, comparison_cut


    def remove_final_videos():
        """
        영상을 비교하며 생긴 부가 파일들 제거
        """
        os.chdir(OUTPUT_DIR)
        
        command = "del *cut.mp4"
        os.system(command)
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
        """
        분석 결과를 포함한 비디오 파일(오디오 없음)과 오디오 결합하여 오디오 있는 비디오 파일 생성
        Args:
            video: 분석 결과를 포함한 비디오 파일(오디오 없음)
            audio: 참조 영상의 오디오 파일(.wav)

        Return:
            outputV: 오디오가 있는 분석 결과를 포함한 비디오 파일
        """
        outputV = f"{OUTPUT_DIR}/{nickname}_{title}_output.mp4"
        command = f"ffmpeg {EXIST_FLAG} -i {video} -i {audio} -c:v copy -c:a aac -strict experimental {outputV}"
        os.system(command)  # 오디오있는 output video 생성
        return outputV

    # --------------------------------------------------------- PREPARE VIDEOS --------------------------------------------------------------------------------------

    import sys
    # Launch with these arguments
    # python dance_30.py video/cyves.mov video/chuu.mov

    # output경로 생성
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # print(CURRENT_DIR)
    
   
    
    def get_video_dimensions(video_path):
        """
        동영상 규격 확인
        Args:
            video_path: 사용자 입력 영상

        Returns: 
            width: 사용자 입력 영상 프레임의 너비
            height: 사용자 입력 영상 프레임의 높이
        """
        cap = cv2.VideoCapture(video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()
        return width, height
    
    def video_resize(comparison_clip, comparison_width, comparison_height):
        """
        사용자 입력 영상 규격을 (720 * 1280)으로 리사이즈
        Args:
            comparison_clip: 사용자 입력 영상
            comparison_width: 사용자 입력 영상 프레임의 너비
            comparison_height: 사용자 입력 영상 프레임의 높이
        
        Return:
            comparison_clip: 프레임의 너비와 높이가 720 * 1280으로 리사이즈된 사용자 입력 영상
        """
        if comparison_width != 720 and comparison_height != 1280:
            end_idx = comparison_clip.find('.mp4')
            input_video = comparison_clip[:end_idx]
            command = f'ffmpeg {EXIST_FLAG} -i {input_video}.mp4 -vf "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2" -af "aresample=async=1:min_hard_comp=0.100000:first_pts=0" {input_video}_resized.mp4'
            os.system(command)  # 동영상 리사이즈, 저장
            
            comparison_clip = f'{input_video}_resized.mp4'
            return comparison_clip
            
        else:
            return comparison_clip
    
    
    comparison_width, comparison_height = get_video_dimensions(comparison_clip)  # 동영상 규격 확인
    # print('-'*300, f"comparison_width={comparison_width}")
    # print('-'*300, f"comparison_height={comparison_height}")
    comparison_clip = video_resize(comparison_clip, comparison_width, comparison_height) # 사용자 입력 영상 규격(720 * 1280)으로 리사이즈

    # 영상 비교
    if not (ref_clip == None and comparison_clip == None):
        print(f"intial clips {ref_clip} {comparison_clip}")

        # 참조 영상 유효성 검사
        print(f'this is the ref: {ref_clip} and comp: {comparison_clip}')
        validate_reference_clip(ref_clip, comparison_clip)


        # 오디오 분석을 위해 wav파일 형식으로 변환
        ref_clip_wav, comparison_clip_wav = convert_to_wav(ref_clip), convert_to_wav(comparison_clip)

        # 두 영상의 오디오 오프셋 찾기
        offset = find_sound_offset(ref_clip_wav, comparison_clip_wav)

        # offset을 기준으로 두 영상 자르기
        ref_cut, comparison_cut = trim_clips(ref_clip, comparison_clip, offset)
        # print(ref_cut, comparison_cut)

    # --------------------------------------------------------- MAIN --------------------------------------------------------------------------------------
    else:
        ref_cut = ref_clip
        comparison_cut = comparison_clip

        
    # processing our two dancers
    print(f"model: {ref_cut}, comparision: {comparison_cut} \n")
    xy_dancer1, dancer1_frames, dancer1_landmarks = landmarks(ref_cut)
    xy_dancer2, dancer2_frames, dancer2_landmarks = landmarks(comparison_cut)

    # 두 영상을 비교한 점수와 결과 영상 생성
    score, output_path = difference(xy_dancer1, xy_dancer2, dancer1_frames, dancer2_frames, dancer1_landmarks, dancer2_landmarks)

    # 두 영상을 비교한 결과 영상과 참조 영상의 오디오 파일을 결합
    output_path = combine_audio_video(output_path, ref_clip_wav)

    print(f"\n You are {score:.2f} % in sync with your model dancer!")
    print('IN fandomproject/dance_30.py')

    # 영상을 비교하며 생긴 부가파일들 제거
    remove_final_videos()
    
    return score, output_path