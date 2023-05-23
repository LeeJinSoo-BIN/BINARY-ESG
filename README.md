# 다중 이용 시설의 사석화 문제 해결

## NOW U SEAT ME

> 프로젝트 기간: 2022.11 - 2022.12.2<br>
> 팀명 : BINARY ESG <br>
> 팀원 : 이진수, 이정민, 이현규, 박상규, 정지윤
<br>

--------

<br>

### 1. 개요
<img src="meeting_notes/image/사석화.png" width="400"/> <br>
다중 이용 시설에 짐만 놓고 자리를 비우는 ```'사석화 현상'``` 이 증가하고 있다. <br>
이로인해 필요한 사람이 해당 자리를 이용하지 못하는 경우가 발생하고있다. <br>
=> 일정 시간 이상 짐만 있는 경우, 자리의 짐을 치워 해당 자리를 이용 가능하게 하는 자리 관리 시스템을 제공한다.

<br>

### 2. 시스템 구성도

<img src="https://github.com/LeeJinSoo-BIN/BINARY-ESG/blob/main/meeting_notes/image/%E1%84%89%E1%85%B5%E1%84%89%E1%85%B3%E1%84%90%E1%85%A6%E1%86%B7_%E1%84%80%E1%85%AE%E1%84%89%E1%85%A5%E1%86%BC%E1%84%83%E1%85%A9.png" width="500"/>

<br>

### 3. 서비스 흐름도

<img src="https://github.com/LeeJinSoo-BIN/BINARY-ESG/blob/main/meeting_notes/image/%E1%84%89%E1%85%A5%E1%84%87%E1%85%B5%E1%84%89%E1%85%B3_%E1%84%92%E1%85%B3%E1%84%85%E1%85%B3%E1%86%B7%E1%84%83%E1%85%A9.png" width="500"/>


<br>

### 4. 진행 방법
 
1. JAVA11(필수), Python(필수), Git(필수), IntelliJ(권장)를 버전에 맞게 설치<br>
오른쪽의 링크를 통해 다운로드 가능 --
[다운로드 링크](https://drive.google.com/drive/folders/1oitvIpHet7atcvQY0g3Xx4U4xmP1Xmzh?usp=share_link)

2. 사전학습 모델 다운로드 --
[다운로드 링크](https://drive.google.com/file/d/1Bz1a2DGd0IfnLQquAkWJBorITRpq3xbs/view?usp=share_link)

3. git clone <br>
```git clone https://github.com/LeeJinSoo-BIN/BINARY-ESG.git```

4. 아래의 코드를 통해 필요한 라이브러리 추가 설치(pip가 설치되어있다고 가정)<br>
```setup.sh``` (window)<br>
 ```sh setup.sh``` (linux)

5. 아래의 코드를 통해 flask를 실행 <br>
```python3 model/detector/binary_esg_flask.py```

6. 아래의 코드를 통해 H2를 실행 후 사진처럼 JDBC URL 정보 설정 후 연결 <br>
```DB/h2/bin/h2.sh``` (window)<br>
 ```sh DB/h2/bin/h2.sh``` (linux)

	<img src="DB/h2_info.png" width="300"/>
<br>

7. clone 받은 폴더 안의 ```back-end``` 폴더를 spring boot를 통해 Open 후 ```ESGApplication``` 실행

<br>


### 5. 개발 환경 

|| tool |
| ------ | ------ |
| 개발언어 | ![issue badge](https://img.shields.io/badge/Java-11-blue.svg) ![issue badge](https://img.shields.io/badge/javascript-blue.svg) ![issue badge](https://img.shields.io/badge/python-3-blue.svg) |
| 데이터베이스 | ![issue badge](https://img.shields.io/badge/H2-1.4.200-lightgrey.svg) |
| 웹 서버 | ![issue badge](https://img.shields.io/badge/Spring%20Framework-2.7.5-green.svg) ![issue badge](https://img.shields.io/badge/thymeleaf-gray.svg) ![issue badge](https://img.shields.io/badge/jQuery-gray.svg) ![issue badge](https://img.shields.io/badge/Bootstrap-gray.svg)  |
| 모델 서버 | ![issue badge](https://img.shields.io/badge/mmdetection-2.25.2-green.svg) ![issue badge](https://img.shields.io/badge/torch-1.13.0+cu117-green.svg) ![issue badge](https://img.shields.io/badge/Flask-gray.svg)|
| 모델학습 환경 | NVIDIA-SMI 450.66 <br> Driver Version: 450.66 <br> CUDA Version: 11.0 <br> GeForce RTX 2080 Ti |
| 개발환경 | Windows10 64bit <br> Ubuntu 18.04.2 LTS |



<br>

### 6. 기대 효과

자리 현황을 3가지 상태 (이용 가능, 이용 중, 장시간 짐만 방치) 로 구분 <br>
→ **이용자와 관리자가 한눈에 보기 쉽게 함** <br>
<br>
장시간 짐만 있어 방치됐던 자리의 순환을 통해 <br>
→ **더 많은 사람들의 자리 이용을 기대 가능** <br>
<br>
인공지능을 통해 별도의 작업 없이 주기적으로 자리 상태 자동 갱신 <br>
→ **관리자의 다중 이용 시설 관리를 편리** <br>
<br>
```‘다중 이용 시설의 사석화’```를 관리함으로써, 효율적인 자리 이용 및 관리가 가능할 것으로 예상됨


<br>


### 7. 역할
| 이름 | 역할 |
| --- | --- |
| 이진수 | 인공지능 |
| 정지윤 | 데이터 수집, 디자인 |
| 이정민 | 인공지능 서버와 웹 서버 연결 |
| 이현규 | 백엔드 |
| 박상규 | 프론트 엔드 |


