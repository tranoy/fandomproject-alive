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

## Setup

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
    <img src="https://blog.kakaocdn.net/dn/MLksq/btsnaMZfaRr/C4jr5GIqAFAwxksHUCx3S1/img.gif" witdh="900" height="300">
    <br>
    <text> ⇒ 홈 화면 우측 상단의 ul태그를 통해서 챌린지, 앨범자켓 제작 등의 서비스 이용 가능 </text>
</details>

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
