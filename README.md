# 다중 이용 시설의 효율적인 좌석 관리 서비스

## NOW U SEAT ME

>  프로젝트 기간: 2022.11 - 2022.12.2<br>
> 팀명 : BINARY ESG <br>
> 팀원 : 이진수, 이정민, 이현규, 박상규, 정지윤

<br>

--------

<br>

### 1. 진행 방법
 
1. JAVA11(필수), Python(필수), Git(필수), IntelliJ(권장)를 버전에 맞게 설치<br>
오른쪽의 링크를 통해 다운로드 가능 --
[다운로드 링크](https://drive.google.com/drive/folders/1oitvIpHet7atcvQY0g3Xx4U4xmP1Xmzh?usp=share_link)

2. git clone <br>
```git clone https://github.com/LeeJinSoo-BIN/BINARY-ESG.git```

3. 아래의 코드를 통해 필요한 라이브러리 추가 설치(pip가 설치되어있다고 가정)<br>
```setup.sh``` (window)<br>
 ```sh setup.sh``` (linux)


4. 아래의 코드를 통해 flask를 실행 <br>
```python3 model/detector/binary_esg_flask.py```

5. 아래의 코드를 통해 H2를 실행 후 사진처럼 JDBC URL 정보 설정 후 연결 <br>
```DB/h2/bin/h2.sh``` (window)<br>
 ```sh DB/h2/bin/h2.sh``` (linux)

	<img src="DB/h2_info.png" width="300"/>
<br>

6. clone 받은 폴더 안의 ```back-end``` 폴더를 spring boot를 통해 Open 후 ```ESGApplication``` 실행

<br>


### 2. 개발 환경 

|| tool |
| ------ | ------ |
| 개발언어 | ![issue badge](https://img.shields.io/badge/Java-11-blue.svg) ![issue badge](https://img.shields.io/badge/javascript-blue.svg) ![issue badge](https://img.shields.io/badge/python-3-blue.svg) |
| 데이터베이스 | ![issue badge](https://img.shields.io/badge/H2-1.4.200-lightgrey.svg) |
| 웹 서버 | ![issue badge](https://img.shields.io/badge/Spring%20Framework-2.7.5-green.svg) ![issue badge](https://img.shields.io/badge/thymeleaf-gray.svg) ![issue badge](https://img.shields.io/badge/jQuery-gray.svg) ![issue badge](https://img.shields.io/badge/Bootstrap-gray.svg)  |
| 모델 서버 | ![issue badge](https://img.shields.io/badge/mmdetection-2.25.2-green.svg) ![issue badge](https://img.shields.io/badge/torch-1.13.0+cu117-green.svg) ![issue badge](https://img.shields.io/badge/Flask-gray.svg)|
| 모델학습 환경 | NVIDIA-SMI 450.66 <br> Driver Version: 450.66 <br> CUDA Version: 11.0 <br> GeForce RTX 2080 Ti |
| 개발환경 | Windows10 64bit <br> Ubuntu 18.04.2 LTS |



<br>

### 3. 시스템 구성도

<img src="https://github.com/LeeJinSoo-BIN/BINARY-ESG/blob/main/meeting_notes/image/%E1%84%89%E1%85%B5%E1%84%89%E1%85%B3%E1%84%90%E1%85%A6%E1%86%B7_%E1%84%80%E1%85%AE%E1%84%89%E1%85%A5%E1%86%BC%E1%84%83%E1%85%A9.png" width="500"/>

<br>

### 4. 서비스 흐름도

<img src="https://github.com/LeeJinSoo-BIN/BINARY-ESG/blob/main/meeting_notes/image/%E1%84%89%E1%85%A5%E1%84%87%E1%85%B5%E1%84%89%E1%85%B3_%E1%84%92%E1%85%B3%E1%84%85%E1%85%B3%E1%86%B7%E1%84%83%E1%85%A9.png" width="500"/>
