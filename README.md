# 💻 Research-WebcamHandMouse

## Preview

![Preview](Preview.png)

---

## Introduction

> Python, OpenCV, MediaPipe를 이용하여 웹캠만으로 마우스를 제어하는 Hand Tracking 프로젝트  
> Arduino HID를 이용한 실제 USB 마우스와 Python Virtual Mouse를 모두 지원하는 듀얼 출력 구조를 구현하였다.

---

## Requirements

> Python Version : 3.9.8 이상 권장

```cmd
pip install -r requirements.txt
```

---

## Note

> OpenCV를 이용한 웹캠 입력  
> MediaPipe Hands 기반 손 추적  
> Arduino Leonardo / Pro Micro HID 지원  
> Python Virtual Mouse(PyAutoGUI) 지원  
> 단일 손 추적 최적화

---

# Webcam Hand Mouse

## 📌 개요

웹캠으로 손을 추적하여 마우스를 제어하는 프로젝트.

동일한 손 추적 엔진을 기반으로 두 가지 출력 방식을 지원한다.

- **Arduino HID**를 이용하여 운영체제에서 실제 USB 마우스로 인식되는 방식
- **PyAutoGUI**를 이용하여 별도의 하드웨어 없이 Python만으로 동작하는 가상 마우스 방식

단순히 손가락 좌표를 따라가는 수준이 아니라 실제 마우스처럼 자연스럽게 사용할 수 있도록 다양한 움직임 보정 알고리즘을 적용하였다.

---

# 📌 프로젝트 목표

- 웹캠만으로 마우스 제어
- Arduino HID 지원
- Python Virtual Mouse 지원
- 높은 반응속도
- 자연스러운 커서 움직임
- 클릭 오동작 최소화
- 확장 가능한 구조

---

# 📌 실행 방법

## Arduino HID 버전

```cmd
python main.py
```

Arduino Leonardo / Pro Micro가 연결되어 있어야 한다.

---

## Virtual Mouse 버전

```cmd
python main_virtual.py
```

별도의 하드웨어 없이 PyAutoGUI를 이용하여 마우스를 제어한다.

---

# 📌 주요 기능

## 🖱️ 마우스 이동

- MediaPipe Hands 기반 손 추적
- 손 중심(Palm Center) 기반 포인터 이동
- X/Y 감도 개별 조절
- Deadzone 적용
- 최대 이동량 제한
- Alpha Smoothing 적용
- 저지연 동작

---

## 👆 클릭

초기 방식

- 검지 끝 좌표를 포인터 기준으로 사용

문제점

- 클릭 시 검지가 움직여 커서도 함께 흔들림

개선 방식

- 손 중심(Palm Center)을 포인터 기준으로 변경
- 엄지와 검지 사이 거리(Pinch)로 클릭 판정

적용 알고리즘

- Pinch Distance Threshold
- Pinch Hold 판정
- 짧은 Pinch = Click
- 긴 Pinch = Press 유지
- 자동 Release 감지

이를 통해 일반 클릭과 드래그를 자연스럽게 구분할 수 있도록 구현하였다.

---

## 🤏 드래그

- Pinch 유지 시 Left Button Press
- 손 이동 시 Drag
- Pinch 해제 시 Release

---

## ⚙️ 움직임 보정

현재 적용

- Deadzone
- Alpha Smoothing
- Max Movement Clamp
- Sensitivity 조절
- Palm Tracking

향후 적용 예정

- Velocity Filter
- Adaptive Smoothing
- Motion Prediction
- Kalman Filter

---

## 🔌 마우스 출력 방식

### 1. Arduino HID

```
Python

↓

Serial (115200bps)

↓

Arduino Leonardo / Pro Micro

↓

USB HID Mouse
```

지원 명령

- Move
- Left Click
- Right Click
- Middle Click
- Left Press
- Left Release
- Right Press
- Right Release
- Scroll

---

### 2. Python Virtual Mouse

```
Python

↓

PyAutoGUI

↓

Operating System

↓

Virtual Mouse Input
```

별도의 Arduino 없이 Python만으로 마우스를 제어한다.

---

# 📂 프로젝트 구조

```text
project/

│

├── main.py                 # Arduino HID 버전
├── main_virtual.py         # Virtual Mouse 버전
├── config.py
├── mediapipe_tracker.py

├── communication/
│   ├── serial_sender.py
│   └── virtual_mouse.py

├── firmware/
│   └── firmware.ino

└── requirements.txt
```

---

# 📌 기술 스택

### Python

- OpenCV
- MediaPipe
- PySerial
- PyAutoGUI
- NumPy

### Firmware

- Arduino
- USB HID Mouse Library

### Hardware

- Webcam
- Arduino Leonardo / Pro Micro (선택)

---

# 📌 Config

현재 주요 설정

```python
# MediaPipe

MAX_NUM_HANDS = 1
MODEL_COMPLEXITY = 1
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.7

# Mouse

SENSITIVITY_X = 2.3
SENSITIVITY_Y = 2.3
DEADZONE = 1
MAX_MOVE = 60

# Smoothing

ENABLE_SMOOTHING = True
SMOOTHING_ALPHA = 0.35
```

모든 움직임은 Config만 수정하여 쉽게 튜닝할 수 있도록 설계하였다.

---

# 📌 리팩토링

### 초기 구조

```text
main.py

 ├── Camera
 ├── Tracking
 ├── Gesture
 └── Mouse Control
```

### 현재 구조

```text
main.py / main_virtual.py

           │
           ▼

mediapipe_tracker.py

           │
           ▼

Gesture Detection

           │
           ▼

Output Layer

     ┌──────────────┐
     │              │
     ▼              ▼

serial_sender   virtual_mouse
```

손 추적과 제스처 처리를 `mediapipe_tracker.py` 내부로 이동하고, 출력 계층을 분리하여 Arduino HID와 Virtual Mouse를 동일한 인터페이스로 사용할 수 있도록 구조를 개선하였다.

---

# 📌 개발 과정에서 해결한 문제

### 검지 기반 포인터

문제

- 클릭 시 검지가 움직여 커서도 함께 흔들림

해결

- 손 중심(Palm Center) 기반 포인터로 변경

---

### Raw Tracking

문제

- MediaPipe 좌표를 그대로 사용하여 떨림 발생

해결

- Alpha Smoothing
- Deadzone
- 이동량 제한 적용

---

### Pinch 오동작

문제

- 거리만 비교하면 클릭과 드래그를 구분하기 어려움

해결

- Distance Threshold
- Hold Time
- Press / Release 상태 관리

---

### 출력 방식 확장

문제

- Arduino HID에 종속된 구조

해결

- 출력 계층(Output Layer) 분리
- Arduino HID와 Virtual Mouse를 동일한 인터페이스로 지원

---

### 구조 개선

문제

- Gesture 처리 코드가 `main.py`에 집중

해결

- `mediapipe_tracker.py`로 리팩토링
- 유지보수성 향상

---

# 📌 향후 개발 예정

- Scroll Gesture 개선
- Right Click Gesture
- Double Click Gesture
- Multi Gesture
- Multi Monitor 지원
- 손 인식 안정성 향상
- Adaptive Smoothing
- Kalman Filter
- FPS 최적화
- GUI 설정 프로그램
- 사용자별 프로필 저장

---

# 📌 최종 목표

- 웹캠만으로 자연스럽게 사용할 수 있는 핸드 트래킹 마우스 구현
- Arduino HID와 Python Virtual Mouse를 모두 지원하는 듀얼 출력 구조 제공
- 실제 USB 마우스와 유사한 사용감 제공
- 누구나 확장하여 사용할 수 있는 오픈소스 Hand Tracking Mouse 플랫폼 구축