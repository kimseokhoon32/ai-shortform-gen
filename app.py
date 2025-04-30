import streamlit as st
import requests
import base64

# 페이지 설정
st.set_page_config(page_title="AI Shortform Generator", layout="centered")
st.title("🎬 AI Shortform Generator")

# 입력 폼
st.markdown("""
이 웹사이트는 다음 기능을 지원할 예정입니다:

1. 텍스트를 입력하면 AI 이미지 생성
2. 대사를 입력하면 음성 더빙 (예정)
3. 이미지 + 음성으로 영상 생성 (예정)
4. 자막도 자동으로 (예정)

(※ 현재는 이미지 생성 기능만 구현됨)
""")

# 프롬프트 입력받기
prompt = st.text_input("💬 캐릭터 설명 프롬프트를 입력하세요", placeholder="예: 둥글둥글하고 귀여운 핑크머리 여고생")

# 버튼 클릭 시 이미지 생성
if st.button("🪄 AI 캐릭터 이미지 생성"):
    if not prompt:
        st.warning("프롬프트를 입력해주세요!")
    else:
        with st.spinner("AI 이미지 생성 중... ⏳"):
            # Replicate API 호출
            url = "https://api.replicate.com/v1/predictions"
            headers = {
                "Authorization": "Token r8_VhgUwR0BsTSJhdc3VenQj97jsddO2Xc1KiHvR",
                "Content-Type": "application/json"
            }
            payload = {
                "version": "cb5ae0c47327b92f6c2ef3c8e43c79f36ecb489d4514e5b9d21b40c0b4b0966b",  # fofr/sdxl
                "input": {
                    "prompt": prompt,
                    "width": 512,
                    "height": 768
                }
            }
            response = requests.post(url, headers=headers, json=payload)
            prediction = response.json()

            # 상태 코드가 200인지 확인
            if response.status_code != 200:
                st.error(f"API 호출 실패! 상태 코드: {response.status_code}")
                st.error(f"API 응답 내용: {prediction}")
            else:
                if "urls" not in prediction:
                    st.error("이미지 생성 실패! 프롬프트를 바꿔보거나 다시 시도해보세요.")
                else:
                    # 결과 대기 URL에서 이미지 얻기
                    get_url = prediction["urls"]["get"]
                    for _ in range(60):
                        result = requests.get(get_url, headers=headers).json()
                        if result.get("status") == "succeeded":
                            image_url = result["output"][0]
                            st.image(image_url, caption="✅ 생성된 AI 캐릭터 이미지", use_column_width=True)
                            break
                        elif result.get("status") == "failed":
                            st.error("❌ 이미지 생성 중 오류가 발생했습니다.")
                            break
import requests

st.markdown("---")
st.header("🗣️ 캐릭터 대사 음성 만들기")

voice_text = st.text_area("🎤 캐릭터가 말할 대사를 입력하세요", placeholder="예: 안녕! 오늘도 좋은 하루야~")

if st.button("🔊 AI 음성 생성"):
    if not voice_text.strip():
        st.warning("대사를 입력해주세요!")
    else:
        with st.spinner("AI 음성 생성 중... 🎧"):
            tts_url = "https://api.elevenlabs.io/v1/text-to-speech/s21u2XK7NDoQMgL1OhtL"  # 기본 음성: Rachel
            headers = {
                "xi-api-key": "sk_885d14b9e4d950ce6df2e3144f469f9b6567c3759b6a3385",
                "Content-Type": "application/json"
            }
            payload = {
                "text": voice_text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.8
                }
            }

            response = requests.post(tts_url, headers=headers, json=payload)
            if response.status_code == 200:
                with open("output.mp3", "wb") as f:
                    f.write(response.content)
                audio_file = open("output.mp3", "rb")
                st.audio(audio_file.read(), format="audio/mp3")
                st.success("✅ 음성 생성 완료! 아래에서 재생해보세요.")
            else:
                st.error("❌ 음성 생성 실패. 다시 시도해주세요.")
