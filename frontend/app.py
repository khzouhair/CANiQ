import streamlit as st
import requests
from datetime import datetime
import folium
from streamlit_folium import st_folium
import time
import pandas as pd
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="CANiQ - Assistant Intelligent CAN 2025",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS amélioré avec animations et effets modernes
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    :root {
        --can-green: #7c0f40;
        --can-green-dark: #7c0f40;
        --can-green-light: #7c0f40;
        --can-gold: #2aed9a;
        --can-gold-dark: #1fa36b;
        --can-red: #ED1C24;
        --can-black: #1A1A1A;
        --can-gray: #F5F5F5;
        --can-white: #FFFFFF;
        --shadow-sm: 0 2px 8px rgba(0, 132, 61, 0.08);
        --shadow-md: 0 4px 16px rgba(0, 132, 61, 0.12);
        --shadow-lg: 0 8px 32px rgba(0, 132, 61, 0.16);
        --shadow-xl: 0 20px 60px rgba(0, 132, 61, 0.25);
    }
    
    /* Reset Streamlit */
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .main .block-container {
        padding-top: 100px;
        max-width: 100%;
    }
    
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    /* Top Navigation Bar - FIXED avec glassmorphism */
    .top-nav {
        background: #7c0f40;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        padding: 0;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 9999;
        box-shadow: 0 8px 32px rgba(0, 132, 61, 0.3);
        border-bottom: 2px solid var(--can-gold);
    }
    
    .nav-container {
        max-width: 1600px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 3rem;
    }
    
    .nav-logo {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1.2rem 0;
        animation: slideInLeft 0.6s ease-out;
    }
    
    .nav-logo h1 {
        color: var(--can-white);
        font-size: 2rem;
        font-weight: 900;
        letter-spacing: -0.5px;
        margin: 0;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
    }
    
    .nav-logo .can-year {
        color: var(--can-gold);
        font-size: 0.95rem;
        font-weight: 700;
        background: rgba(255, 184, 28, 0.2);
        padding: 0.4rem 1rem;
        border-radius: 25px;
        margin-left: 0.5rem;
        border: 2px solid var(--can-gold);
        box-shadow: 0 4px 15px rgba(255, 184, 28, 0.3);
    }
    
    .nav-menu {
        display: flex;
        gap: 0.5rem;
        align-items: center;
    }
    
    .nav-user {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.7rem 1.5rem;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 30px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        animation: slideInRight 0.6s ease-out;
    }
    
    .nav-user-icon {
        width: 35px;
        height: 35px;
        background: var(--can-gold);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        color: var(--can-green-dark);
        font-size: 1.1rem;
    }
    
    .nav-user-name {
        color: var(--can-white);
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    /* Content Wrapper */
    .content-wrapper {
        padding: 3rem;
        max-width: 1600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Hero Section avec animation de particules */
    .hero-section {
        background: linear-gradient(135deg, var(--can-green) 0%, var(--can-white) 100%);
        padding: 4.5rem 3rem;
        border-radius: 24px;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow-xl);
        animation: fadeInUp 0.8s ease-out;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 700px;
        height: 700px;
        background: radial-gradient(circle, rgba(255, 184, 28, 0.2) 0%, transparent 70%);
        border-radius: 50%;
        animation: pulse 4s ease-in-out infinite;
    }
    
    .hero-section::after {
        content: '⚽';
        position: absolute;
        font-size: 15rem;
        opacity: 0.05;
        right: -50px;
        bottom: -50px;
        animation: rotate 20s linear infinite;
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
    }
    
    .hero-title {
        color: var(--can-white);
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 1rem;
        letter-spacing: -1.5px;
        text-shadow: 3px 3px 10px rgba(0, 0, 0, 0.3);
        animation: fadeInUp 0.8s ease-out 0.2s both;
    }
    
    .hero-subtitle {
        color: var(--can-gold);
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        animation: fadeInUp 0.8s ease-out 0.4s both;
    }
    
    .hero-info {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.1rem;
        font-weight: 400;
        animation: fadeInUp 0.8s ease-out 0.6s both;
    }
    
    .hero-badge {
        display: inline-block;
        background: var(--can-gold);
        color: var(--can-green-dark);
        padding: 0.7rem 1.8rem;
        border-radius: 30px;
        font-weight: 800;
        font-size: 0.95rem;
        margin-top: 1.5rem;
        box-shadow: 0 6px 20px rgba(255, 184, 28, 0.4);
        animation: fadeInUp 0.8s ease-out 0.8s both;
        transition: all 0.3s ease;
    }
    
    .hero-badge:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 25px rgba(255, 184, 28, 0.5);
    }
    
    /* Cards améliorées avec hover effects */
    .pro-card {
        background: var(--can-white);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: var(--shadow-md);
        margin-bottom: 2rem;
        border: 1px solid rgba(0, 132, 61, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .pro-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, var(--can-green), var(--can-gold));
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.4s ease;
    }
    
    .pro-card:hover::before {
        transform: scaleX(1);
    }
    
    .pro-card:hover {
        box-shadow: var(--shadow-xl);
        transform: translateY(-8px);
        border-color: var(--can-gold);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 2px solid var(--can-gray);
    }
    
    .card-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: var(--can-green-dark);
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    
    .card-title::before {
        content: '';
        width: 6px;
        height: 30px;
        background: var(--can-gold);
        border-radius: 3px;
    }
    
    .card-badge {
        background: linear-gradient(135deg, var(--can-gold) 0%, var(--can-gold-dark) 100%);
        color: var(--can-white);
        padding: 0.5rem 1.2rem;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(255, 184, 28, 0.3);
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* Buttons avec animations */
    div.stButton > button {
        background: linear-gradient(135deg, var(--can-white) 0%, #f8f9fa 100%);
        color: var(--can-green);
        border: 2px solid var(--can-green);
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        font-weight: 700;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(0, 132, 61, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    div.stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: var(--can-green);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    div.stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    div.stButton > button:hover {
        color: var(--can-white);
        border-color: var(--can-green);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 132, 61, 0.3);
    }
    
    div.stButton > button span {
        position: relative;
        z-index: 1;
    }
    
    /* Primary button */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--can-green) 0%, var(--can-green-dark) 100%);
        color: var(--can-white);
        border: none;
    }
    
    div.stButton > button[kind="primary"]::before {
        background: var(--can-gold);
    }
    
    /* Input Fields avec focus effects */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        padding: 1rem 1.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: var(--can-white);
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: var(--can-green);
        box-shadow: 0 0 0 4px rgba(0, 132, 61, 0.1);
        transform: translateY(-2px);
    }
    
    /* Login Page améliorée */
    .login-container {
        max-width: 500px;
        width: 100%;
        background: var(--can-white);
        padding: 2rem;
        border-radius: 28px;
        box-shadow: 0 30px 90px rgba(0, 0, 0, 0.25);
        margin: 0rem auto 5rem auto;
        animation: fadeInUp 0.8s ease-out;
        border-top: 5px solid var(--can-gold);
    }
    
    .login-logo {
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .login-logo h1 {
        color: var(--can-green-dark);
        font-size: 4rem;
        font-weight: 900;
        margin: 0 0 0.5rem 0;
        letter-spacing: -2px;
        animation: bounceIn 1s ease-out;
    }
    
    .login-logo .year {
        color: var(--can-gold);
        font-size: 1.5rem;
        font-weight: 800;
        animation: fadeIn 1s ease-out 0.3s both;
    }
    
    .login-logo p {
        color: #666;
        font-size: 1.05rem;
        margin-top: 1rem;
        font-weight: 500;
        animation: fadeIn 1s ease-out 0.6s both;
    }
    
    .login-divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, var(--can-gold), transparent);
        margin: 2.5rem 0;
        border-radius: 2px;
    }
    
    /* Source Cards avec animations */
    .source-card {
        background: linear-gradient(135deg, #f8f9fa 0%, var(--can-white) 100%);
        padding: 1.5rem;
        border-radius: 14px;
        margin: 1rem 0;
        border-left: 5px solid var(--can-gold);
        transition: all 0.3s ease;
        box-shadow: var(--shadow-sm);
    }
    
    .source-card:hover {
        background: linear-gradient(135deg, #E8F5E9 0%, #F1F8E9 100%);
        transform: translateX(10px);
        box-shadow: var(--shadow-md);
        border-left-color: var(--can-green);
    }
    
    .source-card strong {
        color: var(--can-green-dark);
        font-weight: 800;
        font-size: 1.05rem;
    }
    
    /* History Items améliorés */
    .history-item {
        background: var(--can-white);
        padding: 1.3rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid var(--can-green);
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-sm);
        position: relative;
        overflow: hidden;
    }
    
    .history-item::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        width: 4px;
        background: var(--can-gold);
        transform: scaleY(0);
        transition: transform 0.3s ease;
    }
    
    .history-item:hover::before {
        transform: scaleY(1);
    }
    
    .history-item:hover {
        background: var(--can-gray);
        transform: translateX(8px);
        box-shadow: var(--shadow-md);
    }
    
    /* Alerts améliorées */
    .alert {
        padding: 1.3rem 1.8rem;
        border-radius: 14px;
        margin: 1.5rem 0;
        font-weight: 600;
        border-left: 5px solid;
        animation: slideInRight 0.5s ease-out;
    }
    
    .alert-success {
        background: linear-gradient(135deg, #E8F5E9 0%, #F1F8E9 100%);
        border-left-color: var(--can-green);
        color: var(--can-green-dark);
    }
    
    .alert-error {
        background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%);
        border-left-color: var(--can-red);
        color: #C62828;
    }
    
    .alert-info {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        border-left-color: #2196F3;
        color: #1565C0;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(40px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes bounceIn {
        0% {
            opacity: 0;
            transform: scale(0.3);
        }
        50% {
            opacity: 1;
            transform: scale(1.05);
        }
        70% {
            transform: scale(0.9);
        }
        100% {
            transform: scale(1);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
            opacity: 1;
        }
        50% {
            transform: scale(1.05);
            opacity: 0.8;
        }
    }
    
    @keyframes rotate {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--can-green), var(--can-gold));
        border-radius: 10px;
    }
    
    /* File Uploader */
    .stFileUploader>div>div {
        border-radius: 14px;
        border: 3px dashed var(--can-green);
        padding: 3rem;
        background: linear-gradient(135deg, #f8f9fa 0%, var(--can-white) 100%);
        transition: all 0.3s ease;
    }
    
    .stFileUploader>div>div:hover {
        border-color: var(--can-gold);
        background: linear-gradient(135deg, #E8F5E9 0%, #F1F8E9 100%);
        transform: scale(1.02);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: var(--can-gray);
        border-radius: 12px;
        font-weight: 700;
        color: var(--can-green-dark);
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: #E8F5E9;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .nav-container {
            padding: 0 1.5rem;
            flex-direction: column;
            gap: 1rem;
        }
        
        .content-wrapper {
            padding: 1.5rem;
        }
        
        .hero-title {
            font-size: 2.2rem;
        }
        
        .hero-subtitle {
            font-size: 1.2rem;
        }
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--can-gray);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, var(--can-green), var(--can-gold));
        border-radius: 10px;
        border: 2px solid var(--can-gray);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, var(--can-green-dark), var(--can-gold-dark));
    }
</style>
""", unsafe_allow_html=True)

# Configuration API
API_BASE_URL = "http://localhost:8000"

# Initialisation session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Accueil" 
if 'total_questions' not in st.session_state:
    st.session_state.total_questions = 0
if 'total_docs' not in st.session_state:
    st.session_state.total_docs = 0



# Navigation horizontale
def show_navigation():
    username_initial = st.session_state.username[0].upper() if st.session_state.username else "U"
    
    st.markdown(f"""
    <div class="top-nav">
        <div class="nav-container">
            <div class="nav-logo">
                <h1>CANiQ</h1>
                <span class="can-year">CAN 2025</span>
            </div>
            <div class="nav-menu">
                <!-- Navigation buttons will be here -->
            </div>
            <div class="nav-user">
                <div class="nav-user-icon">{username_initial}</div>
                <span class="nav-user-name">{st.session_state.username}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation fonctionnelle 
    col0, col1, col2, col3, col4 = st.columns([1, 1, 1, 1, 2])

    with col0:
        if st.button("Accueil", key="btn_home", use_container_width=True):
            st.session_state.current_page = "Accueil" 
            st.rerun()
    
    with col1:
        if st.button("Assistant", key="btn_assistant", use_container_width=True):
            st.session_state.current_page = "Assistant"
            st.rerun()
    
    with col2:
        if st.button("Carte", key="btn_carte", use_container_width=True):
            st.session_state.current_page = "Carte"
            st.rerun()
    
    with col3:
        if st.button("Indexation", key="btn_index", use_container_width=True):
            st.session_state.current_page = "Indexation"
            st.rerun()

    with col4:
        col_empty, col_logout = st.columns([1, 1])
        with col_logout:
            if st.button("Déconnexion", key="btn_logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.session_state.history = []
                st.rerun()

# Fonction de login
def login_page():
    st.markdown("""
    <div class="login-container">
        <div class="login-logo">
            <h1>CANiQ</h1>
            <p class="year">2025</p>
            <p>Assistant Intelligent pour la Coupe d'Afrique des Nations</p>
        </div>
        <div class="login-divider"></div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Connexion")
        username = st.text_input(
            "Nom d'utilisateur", 
            placeholder="Entrez votre identifiant",
            key="login_username"
        )
        password = st.text_input(
            "Mot de passe", 
            type="password", 
            placeholder="Entrez votre mot de passe",
            key="login_password"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Se connecter", use_container_width=True, type="primary"):
            if username == "user" and password == "user":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Connexion réussie!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Identifiants incorrects")
        
        st.info("Utilisez: user / user")

# Page Assistant
def assistant_page():
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2.5, 1.5])
    
    with col1:
        st.markdown("""
        <div class="pro-card slide-in">
            <div class="card-header">
                <h2 class="card-title">Poser une Question</h2>
                <span class="card-badge">RAG Intelligence</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        question = st.text_area(
            "Votre question",
            placeholder="Exemple: Quelles sont les équipes favorites pour remporter la CAN 2025 ?",
            height=120,
            key="main_question"
        )
        
        with st.expander("Paramètres Avancés"):
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                top_k = st.slider("Nombre de sources", 1, 10, 1)
            with col_p2:
                allow_deser = st.checkbox("Mode Développeur", value=True)
        
        col_btn1, col_btn2 = st.columns([3, 1])
        with col_btn1:
            search_btn = st.button("Rechercher", use_container_width=True, type="primary")
        with col_btn2:
            if st.button("Effacer", use_container_width=True):
                st.rerun()
        
        if search_btn and question:
            with st.spinner("Recherche en cours..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                try:
                    payload = {
                        "question": question,
                        "top_k": top_k,
                        "allow_dangerous_deserialization": allow_deser,
                        "history": st.session_state.history[-6:]
                    }
                    
                    response = requests.post(
                        f"{API_BASE_URL}/ask",
                        json=payload,
                        timeout=600
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        st.markdown('<div class="pro-card slide-in">', unsafe_allow_html=True)
                        st.markdown('<div class="card-header"><h2 class="card-title">Réponse</h2></div>', unsafe_allow_html=True)
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); 
                                    padding: 2rem; border-radius: 16px; 
                                    line-height: 1.9; color: #1A1A1A; font-size: 1.05rem;
                                    border-left: 4px solid var(--can-gold);
                                    box-shadow: var(--shadow-sm);">
                            {data["answer"]}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if data.get("sources"):
                            st.markdown("<br>", unsafe_allow_html=True)
                            with st.expander(f"Sources Consultées ({len(data['sources'])})", expanded=True):
                                for idx, src in enumerate(data["sources"], 1):
                                    st.markdown(f"""
                                    <div class="source-card">
                                        <strong>Source {idx}:</strong> {src['source']}<br><br>
                                        <small style="color: #555;">{src['text'][:300]}...</small>
                                    </div>
                                    """, unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.session_state.history.append({
                            "role": "user",
                            "text": question,
                            "timestamp": datetime.now().strftime("%H:%M")
                        })
                        st.session_state.total_questions += 1
                        
                    else:
                        st.error(f"Erreur API: {response.json().get('error', 'Erreur inconnue')}")
                
                except Exception as e:
                    st.error(f"Erreur: {str(e)}")
    
    with col2:
        st.markdown('<div class="card-header"><h2 class="card-title">Historique</h2></div>', unsafe_allow_html=True)
        
        if st.session_state.history:
            user_history = [h for h in st.session_state.history if h["role"] == "user"]
            
            for idx, item in enumerate(reversed(user_history[-8:])):
                st.markdown(f"""
                <div class="history-item">
                    <strong style="color: var(--can-green); font-size: 0.9rem;">Question {len(user_history)-idx}:</strong><br>
                    <span style="color: #333; font-size: 0.95rem;">{item['text'][:80]}{'...' if len(item['text']) > 80 else ''}</span>
                    <div style="font-size: 0.75rem; color: #999; margin-top: 0.7rem; display: flex; align-items: center; gap: 0.3rem;">
                        🕐 {item.get('timestamp', '')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; color: #999;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📭</div>
                <p>Aucune question posée</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Fonction pour extraire les données du CSV
def extraire_donnees_csv(chemin_fichier):
    try:
        df = pd.read_csv(chemin_fichier)
        
        # Coordonnées GPS approximatives des villes marocaines
        coords_villes = {
            'Casablanca': [33.5731, -7.5898],
            'Tanger': [35.7595, -5.8340],
            'Marrakech': [31.6295, -7.9811],
            'Agadir': [30.4278, -9.5981],
            'Rabat': [34.0209, -6.8416],
            'Fès': [34.0331, -5.0003]
        }
        
        stades_data = {}
        
        for index, row in df.iterrows():
            nom_stade = row.get('Stade', row.get('stade', row.get('Nom', '')))
            ville = row.get('Ville', row.get('ville', ''))
            capacite = row.get('Capacité', row.get('Capacite', row.get('capacite', 0)))
            match = row.get('Match le plus proche', row.get('Match', row.get('match', '')))
            date = row.get('Date', row.get('date', ''))
            
            # Nettoyer et formater les données
            if pd.notna(nom_stade) and pd.notna(ville):
                # Gérer la capacité (enlever les espaces et convertir en int)
                try:
                    capacite_int = int(str(capacite).replace(' ', '').replace(',', ''))
                    capacite_formattee = f"{capacite_int:,}".replace(',', ' ')
                except:
                    capacite_formattee = str(capacite)
                
                # Obtenir les coordonnées de la ville
                coords = coords_villes.get(ville, [31.7917, -7.0926])  
                
                # Créer l'entrée du dictionnaire
                stades_data[nom_stade] = {
                    'ville': ville,
                    'coords': coords,
                    'capacite': capacite_formattee,
                    'match': f"{match} - {date}" if pd.notna(date) else match,
                    'date': date if pd.notna(date) else ''
                }
        
        return stades_data
    
    except Exception as e:
        st.error(f"Erreur lors de l'extraction du CSV: {str(e)}")
        return {}


def carte_page(chemin_csv):
    
    # Extraire les données du CSV
    STADES = extraire_donnees_csv(chemin_csv)
    
    if not STADES:
        st.error("Impossible de charger les données des stades depuis le PDF.")
        return
    
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
    
    st.markdown('<div class="pro-card slide-in">', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="card-header">
            <h2 class="card-title">Carte Interactive des Stades</h2>
            <span class="card-badge">{len(STADES)} Stades</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Layout avec filtres à gauche et carte à droite
    col_filters, col_map = st.columns([1, 3])
    
    with col_filters:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 16px; 
                    box-shadow: var(--shadow-md); margin-bottom: 1rem;">
            <h3 style="color: #00843D; margin-bottom: 1.5rem; font-weight: 800; 
                       font-size: 1.2rem; display: flex; align-items: center; gap: 0.5rem;">
                Filtres
            </h3>
        """, unsafe_allow_html=True)
        
        # Filtre 1: Stade
        st.markdown("""
        <p style="margin-bottom: 0.5rem; font-weight: 600; color: #00843D; font-size: 0.95rem;">
            Stade
        </p>
        """, unsafe_allow_html=True)
        stade_filtre = st.selectbox(
            "Sélectionner un stade",
            ["Tous les stades"] + list(STADES.keys()),
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Filtre 2: Ville
        st.markdown("""
        <p style="margin-bottom: 0.5rem; font-weight: 600; color: #00843D; font-size: 0.95rem;">
            Ville
        </p>
        """, unsafe_allow_html=True)
        villes = ["Toutes les villes"] + sorted(list(set([info['ville'] for info in STADES.values()])))
        ville_filtre = st.selectbox(
            "Sélectionner une ville",
            villes,
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Filtre 3: Capacité minimale
        st.markdown("""
        <p style="margin-bottom: 0.5rem; font-weight: 600; color: #00843D; font-size: 0.95rem;">
            Capacité minimale
        </p>
        """, unsafe_allow_html=True)
        capacites = [int(info['capacite'].replace(' ', '')) for info in STADES.values()]
        capacite_min_possible = min(capacites)
        capacite_max_possible = max(capacites)
        
        # Vérifier si toutes les capacités sont identiques
        if capacite_min_possible == capacite_max_possible:
            st.info(f"Capacité unique: {capacite_min_possible:,} places".replace(',', ' '))
            capacite_min = capacite_min_possible
        else:
            capacite_min = st.slider(
                "Capacité minimale",
                min_value=capacite_min_possible,
                max_value=capacite_max_possible,
                value=capacite_min_possible,
                step=5000,
                label_visibility="collapsed"
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Info box sur les filtres actifs
        filtres_actifs = []
        if stade_filtre != "Tous les stades":
            filtres_actifs.append(f"{stade_filtre}")
        if ville_filtre != "Toutes les villes":
            filtres_actifs.append(f"{ville_filtre}")
        if capacite_min_possible != capacite_max_possible and capacite_min > capacite_min_possible:
            filtres_actifs.append(f"Capacité ≥ {capacite_min:,}".replace(',', ' '))
        
        if filtres_actifs:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #E8F5E9 0%, #F1F8E9 100%); 
                        padding: 1rem; border-radius: 12px; border-left: 4px solid #FFB81C;">
                <p style="margin: 0; font-weight: 600; color: #00843D; font-size: 0.9rem;">
                    Filtres actifs:
                </p>
                <p style="margin: 0.5rem 0 0 0; color: #555; font-size: 0.85rem; line-height: 1.6;">
                    {' • '.join(filtres_actifs)}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with col_map:
        stades_filtres = {}
        for stade, info in STADES.items():
            if stade_filtre != "Tous les stades" and stade != stade_filtre:
                continue
            if ville_filtre != "Toutes les villes" and info['ville'] != ville_filtre:
                continue
            capacite_stade = int(info['capacite'].replace(' ', ''))
            if capacite_stade < capacite_min:
                continue
            stades_filtres[stade] = info
        
        # Déterminer le centre et zoom de la carte
        if len(stades_filtres) == 1:
            center = list(stades_filtres.values())[0]["coords"]
            zoom = 12
        elif len(stades_filtres) > 0:
            # Calculer le centre moyen
            lats = [info["coords"][0] for info in stades_filtres.values()]
            lons = [info["coords"][1] for info in stades_filtres.values()]
            center = [sum(lats) / len(lats), sum(lons) / len(lons)]
            zoom = 6
        else:
            center = [31.7917, -7.0926]
            zoom = 6
        
        m = folium.Map(
            location=center,
            zoom_start=zoom,
            tiles="CartoDB positron"
        )
        
        # Ajouter les marqueurs
        for stade, info in stades_filtres.items():
            tooltip_html = f"""
            <div style="font-family: Poppins, sans-serif; padding: 0.5rem;">
                <strong style="color: #00843D; font-size: 1rem;">{stade}</strong><br>
                <span style="color: #666; font-size: 0.85rem;">{info['ville']}</span><br>
                <hr style="margin: 0.5rem 0; border: none; border-top: 1px solid #eee;">
                <span style="color: #555; font-size: 0.85rem;">Prochain match:</span><br>
                <span style="color: #333; font-size: 0.9rem; font-weight: 600;">{info['match']}</span>
            </div>
            """
            
            popup_html = f"""
            <div style="font-family: Poppins, sans-serif; width: 240px; padding: 0.5rem;">
                <h4 style="color: #00843D; margin: 0 0 12px 0; font-weight: 800; font-size: 1.1rem;">
                    {stade}
                </h4>
                <p style="margin: 8px 0; color: #333; font-size: 0.95rem;">
                    <strong>Ville:</strong> {info['ville']}
                </p>
                <p style="margin: 8px 0; color: #333; font-size: 0.95rem;">
                    <strong>Capacité:</strong> {info['capacite']} places
                </p>
                <p style="margin: 8px 0; padding: 10px; background: #f5f5f5; 
                          border-radius: 8px; border-left: 3px solid #FFB81C; font-size: 0.9rem;">
                    <strong>Match:</strong><br>
                    <span style="color: #555;">{info['match']}</span>
                </p>
            </div>
            """
            
            folium.Marker(
                location=info["coords"],
                popup=folium.Popup(popup_html, max_width=280),
                tooltip=folium.Tooltip(tooltip_html, sticky=True),
                icon=folium.Icon(
                    color="green",
                    icon="info-sign",
                    prefix='glyphicon'
                )
            ).add_to(m)
        
        st_folium(m, width=None, height=600)
        
        if len(stades_filtres) == 0:
            st.warning("Aucun stade ne correspond aux filtres sélectionnés.")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="pro-card">
        <div class="card-header">
            <h2 class="card-title">Informations Détaillées</h2>
            <span class="card-badge">{len(stades_filtres)} Stade(s)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Afficher les stades filtrés
    if len(stades_filtres) > 0:
        cols = st.columns(3)
        for idx, (stade, info) in enumerate(stades_filtres.items()):
            with cols[idx % 3]:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); 
                            padding: 1.8rem; border-radius: 16px; margin-bottom: 1.5rem;
                            box-shadow: var(--shadow-md); border: 1px solid rgba(0, 132, 61, 0.1);
                            transition: all 0.3s ease; cursor: pointer;"
                     onmouseover="this.style.transform='translateY(-8px)'; this.style.boxShadow='0 20px 60px rgba(0, 132, 61, 0.25)';"
                     onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 16px rgba(0, 132, 61, 0.12)';">
                    <h4 style="color: #00843D; margin-bottom: 1rem; font-weight: 800; font-size: 1.15rem;
                               display: flex; align-items: center; gap: 0.5rem;">
                         {stade}
                    </h4>
                    <p style="margin: 0.6rem 0; color: #555; font-size: 0.95rem;">
                        <strong style="color: #00843D;">Ville:</strong> {info['ville']}
                    </p>
                    <p style="margin: 0.6rem 0; color: #555; font-size: 0.95rem;">
                        <strong style="color: #00843D;">Capacité:</strong> {info['capacite']} places
                    </p>
                    <div style="background: linear-gradient(135deg, #E8F5E9 0%, #F1F8E9 100%); 
                                padding: 1rem 1.2rem; border-radius: 10px; margin-top: 1rem;
                                border-left: 4px solid #FFB81C;">
                        <strong style="color: #00843D; font-size: 0.9rem;">Prochain match:</strong><br>
                        <small style="color: #555; font-size: 0.9rem; line-height: 1.6;">{info['match']}</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Page Indexation
def indexation_page():
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.markdown("""
            <div class="card-header">
                <h2 class="card-title"> Réindexation</h2>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                    padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;
                    border-left: 4px solid #2196F3;">
            <p style="margin: 0; color: #1565C0; font-weight: 500; line-height: 1.7;">
                <strong> Information:</strong><br>
                Reconstruit l'index vectoriel à partir de tous les documents disponibles.<br><br>
                <strong> Avertissement:</strong> Cette opération peut prendre plusieurs minutes.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        force_reindex = st.checkbox("Supprimer l'index existant", value=True)
        
        if st.button("Lancer la Réindexation", use_container_width=True, type="primary"):
            with st.spinner("Indexation en cours..."):
                progress_bar = st.progress(0)
                
                try:
                    url = f"{API_BASE_URL}/reindex"
                    if force_reindex:
                        url += "?force=true"
                    
                    for i in range(100):
                        time.sleep(0.02)
                        progress_bar.progress(i + 1)
                    
                    response = requests.post(url, timeout=600)
                    
                    if response.status_code == 200:
                        data = response.json()
                        chunks = data.get('chunks_indexed', 0)
                        st.session_state.total_docs = chunks
                        
                        st.markdown(f"""
                        <div class="alert alert-success">
                            <strong>Indexation Réussie!</strong><br>
                             <strong>{chunks}</strong> chunks ont été indexés avec succès.
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        error = response.json().get('detail', 'Erreur inconnue')
                        st.markdown(f"""
                        <div class="alert alert-error">
                            <strong>Erreur lors de l'indexation</strong><br>
                            {error}
                        </div>
                        """, unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"Erreur: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.markdown("""
            <div class="card-header">
                <h2 class="card-title">Ajouter des Documents</h2>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8F5E9 0%, #F1F8E9 100%); 
                    padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;
                    border-left: 4px solid #00843D;">
            <p style="margin: 0; color: #006430; font-weight: 500; line-height: 1.7;">
                <strong>Information:</strong><br>
                Importez de nouveaux documents pour enrichir la base.<br>
                <strong>Formats:</strong> PDF, DOCX, TXT<br>
                <strong>Taille max:</strong> 200 MB
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Sélectionner un fichier",
            type=["pdf", "docx", "txt"]
        )
        
        if uploaded_file:
            file_size_kb = uploaded_file.size / 1024
            file_size_display = f"{file_size_kb:.1f} KB" if file_size_kb < 1024 else f"{file_size_kb/1024:.1f} MB"
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%); 
                        padding: 1.3rem; border-radius: 12px; margin: 1.5rem 0;
                        border-left: 4px solid #FFB81C; box-shadow: var(--shadow-sm);">
                <strong style="color: #E65100; font-size: 1rem;">Fichier sélectionné:</strong><br>
                <span style="color: #555; font-size: 0.95rem; display: flex; align-items: center; gap: 0.5rem; margin-top: 0.5rem;">
                     <strong>{uploaded_file.name}</strong> ({file_size_display})
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        force_reindex_upload = st.checkbox("Réindexer après upload", value=False)
        
        if st.button("Uploader le Document", use_container_width=True, type="primary"):
            if uploaded_file:
                with st.spinner("Upload en cours..."):
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                        url = f"{API_BASE_URL}/upload"
                        if force_reindex_upload:
                            url += "?force=true"
                        
                        response = requests.post(url, files=files, timeout=600)
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.markdown(f"""
                            <div class="alert alert-success">
                                <strong>Fichier uploadé avec succès!</strong><br>
                                {data.get('file_saved')}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error("Erreur lors de l'upload")
                    
                    except Exception as e:
                        st.error(f"Erreur: {str(e)}")
            else:
                st.warning("Veuillez sélectionner un fichier")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def accueil_page():
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-section">
        <div class="hero-content">
            <h1 class="hero-title">⚽ Bienvenue sur CANiQ Intelligence</h1>
            <p class="hero-subtitle">Votre Assistant Expert pour la CAN 2025</p>
            <p class="hero-info">Posez vos questions et découvrez tout sur la compétition</p>
            <span class="hero-badge">Maroc 2025</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        show_navigation()
        
        if st.session_state.current_page == "Accueil":
            accueil_page()
        elif st.session_state.current_page == "Assistant":
            assistant_page()
        elif st.session_state.current_page == "Carte":
            carte_page("stades_can2025.csv")
        elif st.session_state.current_page == "Indexation":
            indexation_page()

if __name__ == "__main__":
    main()
