FROM tiangolo/uwsgi-nginx-flask:latest

# 컨테이너 안에서 작업할 폴더
WORKDIR /app

# 현재 프로젝트 전체를 /app 으로 복사
COPY . /app

# 컨테이너가 시작되면 app_team.py 실행
CMD ["python", "app_team.py"]
