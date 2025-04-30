import streamlit as st

st.set_page_config(page_title="AI Shortform Generator", layout="centered")

st.title("🎬 AI Shortform Generator")

st.markdown("""
이 웹사이트는 다음 기능을 지원할 예정입니다:

1. 텍스트를 입력하면 AI 이미지 생성  
2. 대사를 입력하면 음성 더빙  
3. 이미지 + 음성으로 자동 영상 생성  
4. 자막도 자동으로!

(※ 현재는 UI만 구성된 초기 버전입니다)
""")

prompt = st.text_input("💬 캐릭터 설명 프롬프트를 입력하세요")
script = st.text_area("📝 캐릭터가 말할 대사")

if st.button("🔄 AI 숏폼 생성 시작"):
    st.info("⚙ 기능 구현 예정입니다. 다음 단계에서 이미지, 음성, 자막 기능 추가할 거예요!")
