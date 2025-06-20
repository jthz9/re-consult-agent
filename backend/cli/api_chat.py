import requests
import sys
import json

API_URL = "http://localhost:8000/api/chat"

def chat_with_api(message: str):
    payload = {"message": message}
    try:
        response = requests.post(API_URL, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"[질문] {message}")
        print(f"[응답] {data.get('response')}")
    except Exception as e:
        print(f"[오류] {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(e.response.text)

def main():
    print("재생에너지 AI 챗봇 API CLI (종료: exit)")
    while True:
        try:
            user_input = input("[사용자] ").strip()
            if user_input.lower() in ["exit", "quit", "종료"]:
                print("[시스템] 챗봇을 종료합니다.")
                break
            if not user_input:
                continue
            chat_with_api(user_input)
        except KeyboardInterrupt:
            print("\n[시스템] 챗봇을 종료합니다.")
            break

if __name__ == "__main__":
    main() 