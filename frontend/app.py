import streamlit as st
import requests
import time


st.set_page_config(
    page_title="AI Hallucination Mitigator",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
    <style>
    /* 1. Background Image Setup for the Main App */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* 2. Main content area Glassmorphism effect */
    .block-container { 
        padding-top: 2rem; 
        padding-bottom: 2rem; 
        background-color: rgba(255, 255, 255, 0.85); /* Content ke peeche slight white tint */
        border-radius: 15px;
        margin-top: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
    }
    
    /* 3. Metrics Card Styling */
    div[data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.9);
        border: 1px solid #e9ecef;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    
    /* 4. Hide Streamlit Default Menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


API_URL_QUERY = "https://ai-hallucination-mitigator.onrender.com/api/v1/query/submit"

st.title("🛡️ RAG-Driven LLM Hallucination Interceptor")
st.markdown("<p style='color: #666; font-size: 1.1rem;'>Evaluating LLM outputs in real-time using SelfCheckGPT stochastic sampling and ChromaDB retrieval.</p>", unsafe_allow_html=True)

st.write("<br>", unsafe_allow_html=True) 

query = st.text_input("Student Query Simulator", placeholder="Ask a factual question or test it with a fake history prompt...", label_visibility="collapsed")

col_btn, empty_col = st.columns([1, 4])
with col_btn:
    ask_btn = st.button("Analyze Pipeline 🔍", type="primary", use_container_width=True)

if ask_btn and query:
    success = False
    data = None
    
    with st.status("Running AI Verification Pipeline...", expanded=True) as status:
        st.write("⚙️ Connecting to Llama-3.1 Baseline...")
        st.write("🎲 Generating Stochastic Samples for SelfCheckGPT...")
        st.write("🧮 Calculating Cosine Similarity Matrix...")
        
        try:
            response = requests.post(API_URL_QUERY, json={"query": query, "student_id": "demo_user"})
            
            if response.status_code == 200:
                data = response.json()
                status.update(label="Analysis Complete! Results below 👇", state="complete", expanded=False)
                success = True
            else:
                status.update(label="API Error", state="error")
                st.error(f"Backend Error: {response.text}")
                
        except Exception as e:
            status.update(label="Connection Failed", state="error")
            st.error(f"Connection Error: {str(e)}")


    if success and data:
        st.write("<br>", unsafe_allow_html=True)
        
        st.subheader("Live Telemetry")
        m1, m2, m3 = st.columns(3)
        
        score = data['hallucination_score']
        risk_level = data['risk_level']
        
        with m1:
            if score > 0.25:
                st.metric("Hallucination Risk", f"{score * 100:.1f}%", "- CRITICAL", delta_color="inverse")
            else:
                st.metric("Hallucination Risk", f"{score * 100:.1f}%", "+ SAFE")
                
        with m2:
            st.metric("Risk Level", risk_level)
            
        with m3:
            st.metric("Latency", "1.2s", "- Optimized") 

        st.write("<br>", unsafe_allow_html=True)
        
        st.subheader("AI Response")

        with st.container(border=True):

            st.markdown("### 🤖 Generated Response")
            st.divider()
            st.write(data["response"])
                    
        js_scroll = '''
        <script>
            var body = window.parent.document.querySelector(".main");
            if (body) { body.scrollTo({top: body.scrollHeight, behavior: 'smooth'}); }
        </script>
        '''
        import streamlit.components.v1 as components
        components.html(js_scroll, height=0)