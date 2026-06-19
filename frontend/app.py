import streamlit as st
import requests
import streamlit.components.v1 as components

st.set_page_config(page_title="LLM Hallucination Interceptor", layout="wide")

# Custom CSS with Background Image
st.markdown("""
    <style>
    .stApp { background-image: url("https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072"); background-size: cover; }
    .block-container { background-color: rgba(255, 255, 255, 0.85); border-radius: 15px; backdrop-filter: blur(4px); }
    </style>
""", unsafe_allow_html=True)

# REPLACE THIS URL WITH YOUR LIVE RENDER URL
BASE_URL = "https://ai-hallucination-backend.onrender.com"
API_URL_QUERY = f"{BASE_URL}/api/v1/query/submit"

st.title("🛡️ RAG-Driven LLM Hallucination Interceptor")

query = st.text_input("Student Query Simulator", placeholder="Ask a factual question...")

if st.button("Analyze Pipeline 🔍", type="primary"):
    with st.status("Running Pipeline...", expanded=True) as status:
        try:
            response = requests.post(API_URL_QUERY, json={"query": query, "student_id": "demo_user"})
            if response.status_code == 200:
                data = response.json()
                status.update(label="Analysis Complete!", state="complete", expanded=False)
                
                st.subheader("Live Telemetry")
                st.metric("Hallucination Risk", f"{data['hallucination_score'] * 100:.1f}%")
                
                col1, col2 = st.columns(2)
                with col1: st.info(f"Baseline: {data['baseline_response']}")
                with col2: st.success(f"Final: {data['final_response']}")
        except:
            st.error("Backend Connection Error!")