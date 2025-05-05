import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

# تنظیمات اولیه
st.set_page_config(
    page_title="پیش‌بینی هوشمند محصول",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS سفارشی
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');
    
    * {
        font-family: 'Vazirmatn', sans-serif !important;
    }
    
    .stApp {
        background: #f8fff8;
    }
    
    .header-gradient {
        background: linear-gradient(135deg, #4CAF50 0%, #2196F3 100%);
        padding: 4rem 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        margin-bottom: 3rem;
    }
    
    .prediction-box {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #4CAF50;
        margin: 2rem 0;
    }
    
    .stSlider > div > div > div > div {
        background: #4CAF50 !important;
    }
    
    .st-bb {
        background-color: transparent !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #4CAF50 0%, #2196F3 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 12px 30px !important;
        font-size: 1.2rem !important;
        transition: all 0.3s !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(76,175,80,0.4);
    }
    
    footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        border-top: 1px solid #eee;
        margin-top: 3rem;
    }
    </style>
""", unsafe_allow_html=True)

# داده‌ها و مدل
data = pd.DataFrame({
    'area': [1, 2, 3, 4, 5],
    'rainfall': [10, 20, 30, 40, 50],
    'fertilizer': [100, 200, 300, 400, 500],
    'yield': [1000, 1500, 2000, 2500, 3000]
})

features = ['area', 'rainfall', 'fertilizer']
model = LinearRegression().fit(data[features], data['yield'])

# هدر
st.markdown("""
    <div class="header-gradient">
        <h1 style="color: white; text-align: center; font-size: 2.5rem; margin: 0;">🌾 پیش‌بینی عملکرد محصول</h1>
        <p style="color: rgba(255,255,255,0.9); text-align: center; font-size: 1.2rem; margin: 1rem 0 0;">
        سیستم پیشرفته پیش‌بینی کشاورزی مبتنی بر هوش مصنوعی</p>
    </div>
""", unsafe_allow_html=True)

# نوار کناری
with st.sidebar:
    st.markdown("### 🎛 پارامترهای ورودی")
    area = st.slider("🌾 مساحت زمین (هکتار)", 1, 10, 3)
    rainfall = st.slider("🌧️ بارندگی (میلی‌متر)", 10, 100, 30)
    fertilizer = st.slider("🌱 مصرف کود (کیلوگرم)", 100, 500, 300)
    
    if st.button("🚜 محاسبه عملکرد"):
        with st.spinner("در حال محاسبه..."):
            input_data = [[area, rainfall, fertilizer]]
            prediction = model.predict(input_data)[0]
            st.session_state.prediction = prediction

# بخش اصلی
col1, col2 = st.columns([1, 2])

with col1:
    if 'prediction' in st.session_state:
        st.markdown(f"""
            <div class="prediction-box">
                <h3 style="color: #2c3e50; margin: 0;">پیش‌بینی عملکرد</h3>
                <div style="font-size: 2.5rem; color: #4CAF50; font-weight: bold; text-align: center; margin: 1rem 0;">
                    {st.session_state.prediction:.0f} کیلوگرم
                </div>
                <div style="text-align: center; color: #666;">
                    در هکتار 🌟
                </div>
            </div>
        """, unsafe_allow_html=True)

with col2:
    if 'prediction' in st.session_state:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data['area'],
            y=data['yield'],
            mode='markers+lines',
            name='داده واقعی',
            line=dict(color='#4CAF50', width=2),
            marker=dict(size=10, color='#2196F3')
        ))
        fig.add_trace(go.Scatter(
            x=[area],
            y=[st.session_state.prediction],
            mode='markers',
            name='پیش‌بینی شما',
            marker=dict(size=15, color='#FF5722'),
            hoverinfo='text',
            text=[f"پیش‌بینی: {st.session_state.prediction:.0f} kg"]
        ))
        fig.update_layout(
            title="📈 نمودار تحلیل عملکرد",
            xaxis_title="مساحت زمین (هکتار)",
            yaxis_title="عملکرد (کیلوگرم)",
            template="plotly_white",
            hovermode="x unified",
            plot_bgcolor='rgba(245,245,245,0.9)',
            paper_bgcolor='rgba(255,255,255,0.9)',
            margin=dict(l=20, r=20, t=40, b=20),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("""
    <footer>
        <p>© 2023 سامانه هوشمند کشاورزی | توسعه داده شده با ❤️ و Streamlit</p>
    </footer>
""", unsafe_allow_html=True)
