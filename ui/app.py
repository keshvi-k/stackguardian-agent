import streamlit as st
import requests

API_URL = "http://localhost:8000/analyze"

st.set_page_config(page_title="StackGuardian", page_icon="🛡️", layout="wide")

st.markdown("""
# 🛡️ StackGuardian  
AI-powered troubleshooting agent for DevOps, CI/CD, Docker, and Kubernetes logs.
""")

log_input = st.text_area("Paste logs here:", height=250)

if st.button("🔍 Analyze Log"):
    if not log_input.strip():
        st.warning("⚠️ Please paste a log before analyzing.")
    else:
        with st.spinner("Analyzing logs... please wait ⏳"):
            try:
                response = requests.post(API_URL, json={"log": log_input})
                result = response.json()

                st.success("✅ Analysis Complete!")

                st.subheader("🧠 Summary")
                st.write(result.get("summary", "No summary available"))

                st.subheader("🔧 Steps to Fix")
                for step in result.get("steps", []):
                    st.write(f"- {step}")

                st.subheader("📄 Raw Output")
                st.json(result)

            except Exception as e:
                st.error(f"Error contacting backend: {e}")
