#

# 🏆 A-LIVE : K-POP 팬덤을 위한 AI 퍼펙트 댄싱 경쟁 서비스

> 2023.05.26 ~ 2023.07.11 KT AIVLE 전남/전북 33조 빅프로젝트<br> > _'A-live'는 아이돌 팬덤들을 위한 플랫폼으로 자신이 도전한 챌린지 영상을 기반으로 정확도를 측정하고 참여자들의 실시간 랭킹을 확인할 수 있습니다. 또한 본인이 일러스트화 하고 싶은 앨범자켓을 선택해 커스터마이징 할 수 있는 AI서비스입니다_

<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbKQwvz%2Fbtsm9u5QTU7%2FnJM1GD3ujkBgma68oWcg4k%2Fimg.png" width="1000" height="460">
<br>

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https://github.com/Junobee25/ai-33-project&count_bg=%236EFF00&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

## 팀 구성

- `AI전남/전북 9반 33조`

|                       [🏆조창근](https://github.com/geun98)                       |                      [배준오](https://github.com/Junobee25)                      |                     [김규리](https://github.com/GYURI-KIM)                      |                      [송준원](https://github.com/tranoy)                       |                      [이진하](https://github.com/Haariiii)                      |                     [이민흠](https://github.com/Leecoderse)                     |
| :-------------------------------------------------------------------------------: | :------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------: | :----------------------------------------------------------------------------: | :-----------------------------------------------------------------------------: | :-----------------------------------------------------------------------------: |
| <img width="130px" src="https://avatars.githubusercontent.com/u/105584915?v=4" /> | <img width="130px" src="https://avatars.githubusercontent.com/u/109403631?v=4"/> | <img width="130px" src="https://avatars.githubusercontent.com/u/66521889?v=4"/> | <img width="130px" src="https://avatars.githubusercontent.com/u/38881159?v=4"> | <img width="130px" src="https://avatars.githubusercontent.com/u/124108779?v=4"> | <img width="130px" src="https://avatars.githubusercontent.com/u/118246579?v=4"> |
|                                     **AI/BE**                                     |                                    **FE/BE**                                     |                                    **FE/BE**                                    |                                   **AI/BE**                                    |                                    **AI/BE**                                    |                                    **AI/BE**                                    |

## 목차

[1. 개발 배경 및 목적](#1-개발-배경-및-목적)

[2. 기능](#2-기능-및-UI/UX)

[3. 서비스 FLOW](#3-서비스-FLOW)

[4. 3 Tier Architecture](#4-3-Tier-Architecture)

[5. DB 설계](#5-DB-설계)

[6. 개발 환경](#6-개발-환경)

[7. 유저 가이드](#7-유저-)

---

## 1. 개발 배경 및 목적

> 💡 **'AI기술을 통해 팬들에게 창작과 참여의 기회를 제공하기 위해서 개발하게 되었다.'** 팬더스트리는 팬(fan)과 인더스트리(industy)의 합성어로 팬덤 기반의 비지니스 산업을 말합니다.
> 팬더스트리는 상품을 보고 구매하는 것이 아니라 스타를 보고 구매하는 팬덤 소비의 특징을 가지고 있습니다. 2020년 IBK 투자증권이 발표한 '팬덤 경제학' 보고서에 따르면 팬덤 경제는 7.9조원에 달하는 것으로 나타났습니다. 이처럼 강한 팬덤은 소비자의 구매력에 상당한 영향력을 행사하며, 이를 기반으로 한 팬더스트리의 규모도 클 것이라고 예상됩니다. <U>**이 서비스의 기획의도는 이러한 팬덤층을 타겟으로 한 플랫폼을 제공함으로써 팬들에게 창작과 참여의 기회를 제공하고, 엔터테이먼트에게는 아티스트 홍보와 팬덤층 확보에 도움을 주고자 하는 것입니다.**</U>

<br>

- `기존 팬덤 플랫폼`

  1. 팬덤 커뮤니티 앱 - 아티스트와 팬과의 연결 (위버스, 리슨, 광야클럽, 버블)
  2. 투표 앱 - 팬덤의 참여독려를 위해 다양한 서비스 제공 (뮤빗, 아이돌챔프, 스타플래닛)
  3. 굿즈 거래 앱 - 굿즈거래를 통한 팬과의 유대감 결성(위버스샵, 포카마켓)
  4. 콘텐츠 시청 앱 - 콘텐츠 경험 확상을 위한 소통형 플랫폼 (엠넷 플러스, 아이돌 플러스)

<br>

- 위와 같은 기존의 서비스에서 팬덤끼리의 소통과 앨범 홍보 효과를 더욱 강화하기 위해 **A-live**(댄스 챌린지)를 기획

- `🏆A-live`

  - 사용자는 현재 진행 중인 아이돌 댄스 숏폼을 확인 가능
  - 참고 영상을 기반으로 사용자가 춘 영상의 정확도를 AI 모델이 측정
  - 실시간 랭킹 페이지에 본인의 랭킹이 올라감
  - 일러스트화 하고 싶은 앨범 자켓 선택
  - 원하는 화풍 선택 후 화풍에 따른 커스텀 앨범 자켓 생성
  - 팬덤 플랫폼 서비스로 사이트 접속과 이용시간을 늘림으로 팬덤층의 유출을 방지, 지속적인 소비자 층을 유지 시킬 것이라고 예상
  - 커스터마이징한 앨범 자켓 이미지와 댄스 챌린지로 아티스트의 음원과 영상 조회수가 상승 될 것이라고 예상

<br>

## 2. 기능 및 UI/UX

- `서비스 주요 기능`

<details>
    <summary>메인 화면</summary>
    <div markdown="1">
    <br>
    <img src="https://github.com/Junobee25/ai-33-project/assets/109403631/94e59b22-1b10-478c-8e28-777637430e9b" witdh="900" height="300">
    <br>
    <text> ⇒ 홈 화면 우측 상단의 ul태그를 통해서 챌린지, 앨범자켓 제작 등의 서비스 이용 가능 </text>
</details>

<details>
    <summary><strong>1) 회원가입/로그인</strong></summary>
        <div markdown="1">  
            <h3>📝 이용약관/개인정보/회원가입</h3>
            <img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FciAK3n%2Fbtsm8h7hi9j%2F6PK2EdV3i3r5HQ5jUTBDck%2Fimg.png" width="700" height="412">
            <h3>🔒 로그인</h3>
            <img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fd2RwCk%2Fbtsm4Cc5qD7%2FumTOTQHGJESrRTBvgGY41K%2Fimg.png" width="700" height="412">
        </div>
</details>

<details>
  <summary><strong>2) 현재 진행중인 챌린지 페이지 / 로그인 된 사용자 챌린지 참여 페이지</strong></summary>
   <div markdown="1"> 
    <br>      
     <img src="https://t1.daumcdn.net/tistory_admin/static/images/pc-image-censoring-v1.gif" width="650" height="350">
     <br>
     <text>⇒ 고객이 상담할 수 있는 상담사를 선택해 상담을 신청할 수 있다</text>
   </div>
 </details>

  <details>
  <summary><strong>3) 동영상 업로드 모달 창</strong></summary>
   <div markdown="1"> 
    <br>      
     <img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FvhhhR%2Fbtsm8M0d6hR%2FFdldWmGO25zZNlKXFeXKqK%2Fimg.png" width="655" height="400">
     <br>
     <text>⇒ 고객이 상담할 수 있는 상담사를 선택해 상담을 신청할 수 있다.</text>
   </div>
 </details>

 <details>
  <summary><strong>4) 챌린지 영상 점수 결과가 나오는 페이지</strong></summary>
   <div markdown="1"> 
    <br>      
     <img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FHnN8n%2Fbtsm838xhgr%2FnWeG8s4dxGQuvqR3N904m0%2Fimg.png" width="500" height="300">
     <br>
     <text>⇒ 참여한 챌린지 영상과 함께 AI모델을 통한 점수 측정 결과를 확인할 수 있다.</text>
   </div>
 </details>

  <details>
  <summary><strong>5) 챌린지 랭킹 페이지</strong></summary>
   <div markdown="1"> 
    <br>      
     <img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdtcnQZ%2Fbtsm9BcSd3O%2F1PYkdvaaKcuK021TyiYYW0%2Fimg.png" width="500" height="300">
     <br>
     <text>⇒ 총 챌린지 참여자 수 와 본인의 랭킹을 확인 할 수 있다.</text>
   </div>
 </details>

   <details>
  <summary><strong>6) 앨범자켓 일러스트화 기능</strong></summary>
   <div markdown="1"> 
    <br> 
    <h3>🖌 앨범자켓 일러스트화</h3>
     <img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbRuu2M%2Fbtsm1TziFu4%2FDreLxfZQED3jm9R3KTbqnk%2Fimg.png" width="500" height="500">
     <h3>🖌 일러스트화 결과</h3>
     <img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbDe3h9%2Fbtsm8QauPPd%2FIshTgKrjCqPIp3ioVzJtVK%2Fimg.png" width="500" height="500">
     <br>
     <text>⇒ 자신이 원하는 아이돌의 앨범 자켓을 원하는 화풍으로 일러스트화 할 수 있다.</text>
   </div>
 </details>

 <details>
  <summary><strong>7) 챌린지 참가자들의 모든 영상을 확일할 수 있는 전체 공유 게시판 </strong></summary>
   <div markdown="1"> 
    <br>    
     <h3>📝 전체 게시판 </h3>  
     <img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FCMoh9%2Fbtsm9wbypUj%2F9gZ1n4jsybMclfCtTSl201%2Fimg.png" width="650" height="350">
     <h3>🔎 게시물 상세보기 </h3>
     <img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FWHfiW%2Fbtsm4C5c1SV%2Fh0rm48j6mCXiD9EkReANK1%2Fimg.png">
     <br>
     <text>⇒ 모든 사용자는 챌린지 참가자들의 모든 게시물을 확인 할 수 있다. 게시물 ID정보와 일치하는 사용자는 수정 및 삭제가 가능하다.</text>
   </div>
 </details>
<br>

`AI 주요 기능`

 <details>
    <summary><strong>1) 사용자가 춘 영상데이터를 기반으로 정확도를 측정 </strong></summary>
    <text>1. Pose Estimation Model(Blaze Pose)를 이용해서 사용자의 관절 위치를 찾음</text>
    <br>
    <text>2. 비교하려는 팔, 다리 부분의 관절 위치를 찾음</text>
    <br>
    <text>3. 관절 접합부의 (x,y)좌표를 이용하여 기울기를 계산</text>
    <br>
    <text>4. 원본 영상의 춤과 사용자 사이의 기울기 차이를 백분율로 구한 후 모든 관절의 접합부에 대해 반복하고 평균을 구함</text>
    <br>
    <text>5. 4번을 모든 프레임에 대해서 반복</text>
 </details>
  <details>
    <summary><strong>2) 앨범자켓을 일러스트 화</strong></summary>
    <text>=> 모델 학습 방법</text>
    <text>1. 카툰 이미지셋과 실사 이미지셋을 준비</text>
    <br>
    <text>2. train:test 비율을 9:1로 분리</text>
    <br>
    <text>3. 카툰 데이터셋을 edge smooting을 적용</text>
    <br>
    <text>4. 모델을 사용하여 best epoch를 구한 후 저장</text>
    <br>
    <text>5. 비저장한 모델을 Transformer를 통해 적용</text>
    <br>
 </details>

<br>

## 3. 서비스 FLOW

- `주요 기능 Flow 1`
  ![서비스 흐름](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FvvY4S%2Fbtsm9CvZsFl%2FvFDvAIi5DkDLnMXVkY17ZK%2Fimg.png)
- `주요 기능 Flow 2`
  ![서비스 흐름](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F7dqWW%2Fbtsm8OqeCZ1%2Fc1jeknNX8hRkolGKIquur1%2Fimg.png)
- `서비스 Flow`
  ![서비스FLOW](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fb3DsRI%2Fbtsm7xWPhTG%2FqtnQzxEPEsAckNCfXvKkrK%2Fimg.png)
  <br>

## 4. 3 Tier Architecture

![아키텍쳐](https://github.com/Junobee25/ai-33-project/assets/109403631/f661a3a5-8306-4e67-be2b-8bba9dc34a5e)

<br>

## 5. DB 설계

- `ERD`
  ![ERD](https://github.com/Junobee25/ai-33-project/assets/109403631/97b0bac5-5f72-4bfd-afa8-700f9e9bcac5)

<br>

## 6. 개발 환경

- `Front-End`

  |                                                      HTML                                                      |                                                      CSS                                                      |                                                      JS                                                      |                                                      Bootstrap                                                      |
  | :------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------: |
  | ![html](https://user-images.githubusercontent.com/68097036/151471705-99458ff8-186c-435b-ac5c-f348fd836e40.png) | ![css](https://user-images.githubusercontent.com/68097036/151471805-14e89a94-59e8-468f-8192-c10746b93896.png) | ![js](https://user-images.githubusercontent.com/68097036/151471854-e0134a79-b7ef-4a0f-99fd-53e8ee5baf50.png) | ![bootstrap](https://user-images.githubusercontent.com/68097036/151480381-2b23a8af-c6b4-43a6-96a6-ea69e0b953e0.png) |

- `Back-End`

  |                                                        Python                                                         |                                                          Django                                                           |                                                         Sqlite3                                                          |
  | :-------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------: |
  | ![pngwing com](https://user-images.githubusercontent.com/68097036/151479684-a85d26d4-e79e-47c9-9023-bf6d92f57536.png) | ![pngwing com (1)](https://user-images.githubusercontent.com/68097036/151466729-9cad0405-85ad-454e-815a-1a4fd065f8b7.png) | <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/SQLite370.svg/2560px-SQLite370.svg.png" width="300"> |

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/Junobee25/ai-33-project.git
$ cd fandomproject
```

Next, set up your virtual environment

```sh
$ python -m venv (virtual environment name)
```

One `pip` install requirements

```sh
(env)$ pip install -r requirements.txt
```

Once clone and path setup is complete.

```sh
(env)$ python manage.py runserver
```
