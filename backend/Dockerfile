# Python 3.11 베이스 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 설치 (한 번에 설치하여 레이어 최소화)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    mecab \
    libmecab-dev \
    mecab-ipadic-utf8 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Python 의존성 파일 복사
COPY requirements.txt .

# 프로덕션 의존성만 설치 (개발 도구 제외)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 환경 변수 설정
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# 포트 노출
EXPOSE 8000

# 기본 명령어
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 