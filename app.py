"""
VisionVoice Pro - World-Class AI Visual Assistance System
Developed by: Aditya Menon | RA2311026050050
Course: SEAI (21CSE312P) | SRM IST Tiruchirappalli
SDG Goals: SDG 3 (Health), SDG 4 (Education), SDG 10 (Reduced Inequalities)
"""

import streamlit as st
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
import easyocr
from ultralytics import YOLO
import os
import io
import time
import json
from datetime import datetime
import base64

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="VisionVoice Pro",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== SESSION STATE ====================
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'total_analyses' not in st.session_state:
    st.session_state.total_analyses = 0
if 'total_objects' not in st.session_state:
    st.session_state.total_objects = 0

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(0, 242, 254, 0.5);
    }
    
    .subtitle {
        text-align: center;
        color: #b8c5d6;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .result-box {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.1) 100%);
        border-left: 4px solid #4facfe;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #ffffff;
    }
    
    .hazard-box {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.15) 0%, rgba(255, 165, 2, 0.15) 100%);
        border-left: 4px solid #ff6b6b;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #ffffff;
    }
    
    .success-box {
        background: linear-gradient(135deg, rgba(46, 213, 115, 0.15) 0%, rgba(0, 242, 254, 0.15) 100%);
        border-left: 4px solid #2ed573;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: #ffffff;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border: none;
        padding: 0.7rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 172, 254, 0.6);
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(79, 172, 254, 0.3);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(79, 172, 254, 0.8);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #4facfe;
    }
    
    .metric-label {
        color: #b8c5d6;
        font-size: 0.9rem;
    }
    
    .footer {
        text-align: center;
        color: #8892a0;
        padding: 2rem 0;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 3rem;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
    .badge-success {
        background: rgba(46, 213, 115, 0.2);
        color: #2ed573;
        border: 1px solid #2ed573;
    }
    
    .badge-info {
        background: rgba(79, 172, 254, 0.2);
        color: #4facfe;
        border: 1px solid #4facfe;
    }
    
    .badge-warning {
        background: rgba(255, 165, 2, 0.2);
        color: #ffa502;
        border: 1px solid #ffa502;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border: 1px solid rgba(79, 172, 254, 0.2);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        background: rgba(255, 255, 255, 0.06);
        border-color: rgba(79, 172, 254, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown('<h1 class="main-title">👁️ VisionVoice Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">🌟 World-Class AI Visual Assistance System for the Visually Impaired 🌟</p>', unsafe_allow_html=True)

# ==================== METRICS ROW ====================
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(f'<div class="metric-card"><div class="metric-value">4</div><div class="metric-label">🤖 AI Models</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="metric-value">7</div><div class="metric-label">🌐 Languages</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><div class="metric-value">80+</div><div class="metric-label">🎯 Object Classes</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{st.session_state.total_analyses}</div><div class="metric-label">📊 Analyses</div></div>', unsafe_allow_html=True)
with col5:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{st.session_state.total_objects}</div><div class="metric-label">🔍 Objects Found</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## 🎯 VisionVoice Pro")
    st.markdown("---")
    
    st.markdown("### 👨‍💻 Developer Info")
    st.info("**Aditya Menon**\n\nRA2311026050050\n\nSEAI (21CSE312P)\n\nSRM IST Tiruchirappalli")
    
    st.markdown("---")
    st.markdown("### 🔑 API Configuration")
    api_key = st.text_input("Gemini API Key", type="password", help="Get your free key from aistudio.google.com")
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            st.success("✅ API Connected")
        except Exception as e:
            st.error(f"❌ API Error: {str(e)[:50]}")
    else:
        st.warning("⚠️ Enter API key to enable AI features")
    
    st.markdown("---")
    st.markdown("### 🌐 Output Language")
    language_map = {
        "🇬🇧 English": ("en", "English"),
        "🇮🇳 Hindi": ("hi", "Hindi"),
        "🇮🇳 Tamil": ("ta", "Tamil"),
        "🇮🇳 Telugu": ("te", "Telugu"),
        "🇮🇳 Kannada": ("kn", "Kannada"),
        "🇮🇳 Malayalam": ("ml", "Malayalam"),
        "🇮🇳 Bengali": ("bn", "Bengali"),
    }
    selected_language = st.selectbox("Select Language", list(language_map.keys()))
    lang_code, lang_name = language_map[selected_language]
    
    st.markdown("---")
    st.markdown("### ⚙️ Analysis Settings")
    detection_confidence = st.slider("🎯 Detection Confidence", 0.1, 1.0, 0.25, 0.05)
    voice_speed = st.radio("🔊 Voice Speed", ["Normal", "Slow"], horizontal=True)
    detail_level = st.select_slider(
        "📝 Description Detail",
        options=["Brief", "Standard", "Detailed", "Comprehensive"],
        value="Detailed"
    )
    
    enable_hazard_detection = st.checkbox("⚠️ Enable Hazard Detection", value=True)
    enable_color_analysis = st.checkbox("🎨 Enable Color Analysis", value=True)
    enable_spatial_info = st.checkbox("📐 Spatial Information", value=True)
    
    st.markdown("---")
    st.markdown("### ✨ Features")
    st.markdown("""
    <div class="badge badge-success">🔍 Object Detection</div>
    <div class="badge badge-success">📖 OCR Reading</div>
    <div class="badge badge-success">🤖 Scene Analysis</div>
    <div class="badge badge-success">🔊 Voice Output</div>
    <div class="badge badge-info">🌐 Multi-Language</div>
    <div class="badge badge-info">📸 Camera Input</div>
    <div class="badge badge-info">🎨 Annotations</div>
    <div class="badge badge-info">⚠️ Hazard Alerts</div>
    <div class="badge badge-warning">📊 Analytics</div>
    <div class="badge badge-warning">📜 History</div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🌍 SDG Goals")
    st.markdown("- **SDG 3:** Good Health & Well-being")
    st.markdown("- **SDG 4:** Quality Education")
    st.markdown("- **SDG 10:** Reduced Inequalities")
    
    st.markdown("---")
    if st.button("🗑️ Clear History"):
        st.session_state.analysis_history = []
        st.session_state.total_analyses = 0
        st.session_state.total_objects = 0
        st.rerun()

# ==================== TABS ====================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📤 Upload Image", "📸 Capture from Camera", "📊 Analysis History", "📈 Statistics", "ℹ️ About"])

# ==================== HELPER FUNCTIONS ====================

@st.cache_resource
def load_yolo_model():
    return YOLO('yolov8n.pt')

@st.cache_resource
def load_ocr_reader():
    return easyocr.Reader(['en'])

def detect_hazards(objects):
    hazard_keywords = {
        'car': '🚗 Vehicle nearby - exercise caution when crossing',
        'truck': '🚛 Large vehicle detected - stay alert',
        'motorcycle': '🏍️ Motorcycle nearby - listen carefully',
        'bicycle': '🚴 Bicycle in vicinity',
        'bus': '🚌 Bus detected - busy area',
        'knife': '🔪 Sharp object detected - handle with care',
        'scissors': '✂️ Sharp object detected - be cautious',
        'fire hydrant': '🚒 Fire hydrant - obstacle ahead',
        'stop sign': '🛑 Stop sign present',
        'traffic light': '🚦 Traffic signal nearby',
        'oven': '🔥 Heat source - hot surface',
        'microwave': '🔥 Heat appliance nearby',
        'toaster': '🔥 Heat appliance detected',
    }
    
    hazards = []
    for obj in objects:
        if obj.lower() in hazard_keywords:
            hazards.append(hazard_keywords[obj.lower()])
    return hazards

def analyze_colors(image):
    """Analyze dominant colors in image"""
    try:
        img_small = image.copy()
        img_small.thumbnail((100, 100))
        img_small = img_small.convert('RGB')
        pixels = list(img_small.getdata())
        
        # Simple color categorization
        color_counts = {'red': 0, 'green': 0, 'blue': 0, 'yellow': 0, 'white': 0, 'dark': 0}
        for r, g, b in pixels:
            if r > 200 and g > 200 and b > 200:
                color_counts['white'] += 1
            elif r < 50 and g < 50 and b < 50:
                color_counts['dark'] += 1
            elif r > g and r > b:
                color_counts['red'] += 1
            elif g > r and g > b:
                color_counts['green'] += 1
            elif b > r and b > g:
                color_counts['blue'] += 1
            elif r > 150 and g > 150 and b < 100:
                color_counts['yellow'] += 1
        
        total = sum(color_counts.values())
        if total > 0:
            sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
            top_colors = [c[0] for c in sorted_colors[:3] if c[1] > total * 0.05]
            return ", ".join(top_colors) if top_colors else "varied colors"
    except:
        pass
    return "varied colors"

def get_spatial_info(detections, img_width, img_height):
    """Determine spatial position of objects"""
    spatial_data = []
    for det in detections:
        x_center = (det['x1'] + det['x2']) / 2
        y_center = (det['y1'] + det['y2']) / 2
        
        # Horizontal position
        if x_center < img_width / 3:
            h_pos = "left"
        elif x_center < 2 * img_width / 3:
            h_pos = "center"
        else:
            h_pos = "right"
        
        # Vertical position
        if y_center < img_height / 3:
            v_pos = "top"
        elif y_center < 2 * img_height / 3:
            v_pos = "middle"
        else:
            v_pos = "bottom"
        
        spatial_data.append(f"{det['name']} on {v_pos}-{h_pos}")
    
    return spatial_data

def annotate_image(image, results, model):
    """Annotate image with bounding boxes"""
    img = image.convert('RGB').copy()
    draw = ImageDraw.Draw(img)
    
    colors = ['#00f2fe', '#4facfe', '#f093fb', '#2ed573', '#ffa502', '#ff6b6b', '#a55eea', '#26de81']
    
    for r in results:
        for i, box in enumerate(r.boxes):
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            label = f"{model.names[cls]} {conf:.2f}"
            color = colors[i % len(colors)]
            
            draw.rectangle([x1, y1, x2, y2], outline=color, width=4)
            
            try:
                font = ImageFont.truetype("arial.ttf", 18)
            except:
                font = ImageFont.load_default()
            
            text_bbox = draw.textbbox((x1, max(0, y1 - 25)), label, font=font)
            draw.rectangle(text_bbox, fill=color)
            draw.text((x1, max(0, y1 - 25)), label, fill='white', font=font)
    
    return img

def get_detail_prompt(level, lang_name, include_hazards, include_colors, include_spatial):
    """Generate Gemini prompt based on detail level"""
    
    base_prompts = {
        "Brief": "Briefly describe this image in 1-2 sentences for a visually impaired person.",
        "Standard": "Describe this image clearly for a visually impaired person in 3-4 sentences. Mention key objects, people, and setting.",
        "Detailed": "Provide a detailed description of this image for a visually impaired person. Include objects, people, colors, spatial arrangement, mood, and any text visible.",
        "Comprehensive": "Give a comprehensive, vivid description of this image for a visually impaired person. Include: 1) Overall scene and setting 2) All objects and their positions 3) People and their actions 4) Colors and lighting 5) Mood and atmosphere 6) Any potential hazards or points of interest 7) Visible text. Be thorough and informative."
    }
    
    prompt = base_prompts.get(level, base_prompts["Detailed"])
    
    if include_hazards:
        prompt += " Highlight any safety concerns or hazards."
    if include_colors:
        prompt += " Describe colors and lighting."
    if include_spatial:
        prompt += " Describe spatial relationships between objects (left, right, foreground, background)."
    
    prompt += f" Respond in {lang_name} only."
    
    return prompt

def get_gemini_model():
    """Get Gemini model with fallback options"""
    model_options = [
        'gemini-2.0-flash-exp',
        'gemini-1.5-flash-latest',
        'gemini-1.5-flash',
        'gemini-pro-vision',
    ]
    
    for model_name in model_options:
        try:
            model = genai.GenerativeModel(model_name)
            return model, model_name
        except:
            continue
    
    return None, None

# ==================== TAB 1: UPLOAD ====================
with tab1:
    uploaded_file = st.file_uploader(
        "📸 Drop your image here or click to browse",
        type=['jpg', 'jpeg', 'png', 'webp', 'bmp'],
        help="Supported formats: JPG, JPEG, PNG, WEBP, BMP"
    )

# ==================== TAB 2: CAMERA ====================
with tab2:
    camera_image = st.camera_input("📷 Take a photo")

# ==================== TAB 3: HISTORY ====================
with tab3:
    st.markdown("### 📜 Analysis History")
    if st.session_state.analysis_history:
        for idx, item in enumerate(reversed(st.session_state.analysis_history[-10:])):
            with st.expander(f"#{len(st.session_state.analysis_history) - idx} • {item['timestamp']} • {item['language']}"):
                col_a, col_b = st.columns([1, 2])
                with col_a:
                    if 'image' in item:
                        st.image(item['image'], width=200)
                with col_b:
                    st.markdown(f"**Objects Detected:** {item.get('object_count', 0)}")
                    st.markdown(f"**Objects:** {', '.join(item.get('objects', []))}")
                    if item.get('extracted_text'):
                        st.markdown(f"**Text Found:** {item['extracted_text'][:100]}...")
                    st.markdown(f"**Description:**")
                    st.info(item.get('description', 'N/A'))
    else:
        st.info("📭 No analysis history yet. Upload an image to start!")

# ==================== TAB 4: STATISTICS ====================
with tab4:
    st.markdown("### 📊 Real-Time Statistics")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("📊 Total Analyses", st.session_state.total_analyses)
    with col_b:
        st.metric("🔍 Total Objects Detected", st.session_state.total_objects)
    with col_c:
        avg = st.session_state.total_objects / max(st.session_state.total_analyses, 1)
        st.metric("⭐ Avg Objects/Image", f"{avg:.1f}")
    
    if st.session_state.analysis_history:
        st.markdown("### 🏆 Most Detected Objects")
        all_objects = []
        for item in st.session_state.analysis_history:
            all_objects.extend(item.get('objects', []))
        
        if all_objects:
            from collections import Counter
            counter = Counter(all_objects)
            top_objects = counter.most_common(10)
            
            for obj, count in top_objects:
                col_x, col_y = st.columns([1, 4])
                with col_x:
                    st.markdown(f"**{obj}**")
                with col_y:
                    st.progress(count / max([c for _, c in top_objects]))
        
        st.markdown("### 🌐 Languages Used")
        lang_counter = Counter(item.get('language', 'Unknown') for item in st.session_state.analysis_history)
        for lang, cnt in lang_counter.most_common():
            st.markdown(f"- **{lang}:** {cnt} times")
    else:
        st.info("📭 No statistics yet. Analyze some images!")

# ==================== TAB 5: ABOUT ====================
with tab5:
    st.markdown("""
    ### 🌟 About VisionVoice Pro
    
    **VisionVoice Pro** is an advanced AI-powered visual assistance system designed to empower visually impaired individuals 
    with real-time understanding of their surroundings.
    """)
    
    col_x, col_y = st.columns(2)
    with col_x:
        st.markdown("""
        #### 🚀 Core Features:
        - **🔍 Object Detection** — YOLOv8 detects 80+ object classes
        - **📖 Text Recognition** — EasyOCR text extraction
        - **🤖 Scene Description** — Google Gemini AI
        - **🔊 Voice Output** — Google TTS in 7 languages
        - **⚠️ Hazard Detection** — Identifies dangers
        - **📸 Live Camera** — Real-time analysis
        - **🎨 Visual Annotations** — Bounding boxes
        """)
    
    with col_y:
        st.markdown("""
        #### 💡 Advanced Features:
        - **📐 Spatial Information** — Object positioning
        - **🎨 Color Analysis** — Dominant colors
        - **📊 Real-time Analytics** — Live statistics
        - **📜 Analysis History** — Track all sessions
        - **🌐 Multi-Language Support** — 7 Indian languages
        - **⬇️ Audio Download** — Save audio output
        - **⚙️ Customizable Settings** — Personalized experience
        """)
    
    st.markdown("""
    #### 🎓 Academic Project:
    - **Student:** Aditya Menon
    - **Reg No:** RA2311026050050
    - **Course:** SEAI (21CSE312P)
    - **Institution:** SRM IST Tiruchirappalli
    
    #### 🌍 Impact:
    Aligned with UN Sustainable Development Goals — SDG 3 (Health), SDG 4 (Education) & SDG 10 (Reduced Inequalities)
    
    #### 🔗 Links:
    - **GitHub:** https://github.com/Aditya-5009/VisionVoice-Pro
    - **DockerHub:** https://hub.docker.com/r/adityamenon17/visionvoice
    - **Email:** am8845@srmist.edu.in
    """)

# ==================== MAIN ANALYSIS ====================

# Determine image source (priority: upload > camera)
image_source = uploaded_file if uploaded_file else camera_image

if image_source is not None:
    image = Image.open(image_source)
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📷 Original Image")
        st.image(image, use_container_width=True)
        
        st.markdown(f"""
        <div class="result-box">
        <b>📊 Image Info:</b><br>
        • Dimensions: {image.size[0]} × {image.size[1]} px<br>
        • Format: {image.format if image.format else 'Unknown'}<br>
        • Mode: {image.mode}<br>
        • Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🚀 AI Analysis Center")
        
        analyze_btn = st.button("🎯 ANALYZE IMAGE", type="primary", use_container_width=True)
        
        if analyze_btn:
            image_rgb = image.convert('RGB')
            image_rgb.save("temp_image.jpg")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Color Analysis
            dominant_colors = ""
            if enable_color_analysis:
                status_text.markdown("🎨 **Step 1/5:** Analyzing colors...")
                progress_bar.progress(15)
                dominant_colors = analyze_colors(image)
            
            # Object Detection
            status_text.markdown("🔍 **Step 2/5:** Detecting objects with YOLOv8...")
            progress_bar.progress(30)
            
            detected_objects = []
            detection_data = []
            annotated_img = None
            
            try:
                model = load_yolo_model()
                results = model("temp_image.jpg", conf=detection_confidence)
                
                for r in results:
                    for box in r.boxes:
                        cls = int(box.cls[0])
                        conf = float(box.conf[0])
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        detected_objects.append({
                            'name': model.names[cls],
                            'confidence': conf
                        })
                        detection_data.append({
                            'name': model.names[cls],
                            'confidence': conf,
                            'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2
                        })
                
                annotated_img = annotate_image(image, results, model)
                
            except Exception as e:
                st.error(f"Object Detection Error: {e}")
            
            # OCR
            status_text.markdown("📖 **Step 3/5:** Reading text with OCR...")
            progress_bar.progress(50)
            
            extracted_text = ""
            try:
                reader = load_ocr_reader()
                text_results = reader.readtext("temp_image.jpg")
                if text_results:
                    extracted_text = " ".join([t[1] for t in text_results])
            except Exception as e:
                st.warning(f"OCR Warning: {str(e)[:100]}")
            
            # Scene Description
            status_text.markdown("🤖 **Step 4/5:** Generating AI scene description...")
            progress_bar.progress(75)
            
            description = ""
            if api_key:
                try:
                    model_gemini, used_model = get_gemini_model()
                    
                    if model_gemini is None:
                        description = "⚠️ Could not connect to any Gemini model. Please verify your API key."
                    else:
                        prompt = get_detail_prompt(
                            detail_level, 
                            lang_name, 
                            enable_hazard_detection,
                            enable_color_analysis,
                            enable_spatial_info
                        )
                        
                        # Add detection context
                        if detected_objects:
                            unique_names = list(set([d['name'] for d in detected_objects]))
                            prompt += f"\n\nDetected objects: {', '.join(unique_names)}."
                        
                        if dominant_colors:
                            prompt += f" Dominant colors: {dominant_colors}."
                        
                        response = model_gemini.generate_content([prompt, image])
                        description = response.text
                        
                except Exception as e:
                    description = f"Could not generate description. Error: {str(e)[:200]}. Please verify your Gemini API key is valid."
            else:
                description = "⚠️ Please enter Gemini API key in sidebar to enable scene description."
            
            # TTS
            status_text.markdown("🔊 **Step 5/5:** Generating audio output...")
            progress_bar.progress(95)
            
            audio_bytes = None
            if description and not description.startswith("⚠️") and not description.startswith("Could not"):
                try:
                    full_text = description
                    if extracted_text:
                        full_text += f". Visible text: {extracted_text}"
                    
                    slow_speech = (voice_speed == "Slow")
                    tts = gTTS(text=full_text, lang=lang_code, slow=slow_speech)
                    tts.save("description.mp3")
                    
                    with open("description.mp3", "rb") as audio_file:
                        audio_bytes = audio_file.read()
                except Exception as e:
                    st.warning(f"Audio generation issue: {str(e)[:100]}")
            
            progress_bar.progress(100)
            status_text.markdown("✅ **Analysis Complete!**")
            time.sleep(0.5)
            progress_bar.empty()
            status_text.empty()
            
            # Update session state
            st.session_state.total_analyses += 1
            st.session_state.total_objects += len(detected_objects)
            
            unique_object_names = list(set([d['name'] for d in detected_objects]))
            
            history_item = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'language': selected_language,
                'object_count': len(detected_objects),
                'objects': unique_object_names,
                'extracted_text': extracted_text,
                'description': description[:500] if description else 'N/A',
                'image': image.copy()
            }
            st.session_state.analysis_history.append(history_item)
            
            # Display Results
            if annotated_img:
                st.markdown("#### 🎨 Annotated Detection")
                st.image(annotated_img, use_container_width=True)
            
            # Color Analysis
            if enable_color_analysis and dominant_colors:
                st.markdown("#### 🎨 Color Analysis")
                st.markdown(f'<div class="result-box">🎨 Dominant colors: <b>{dominant_colors}</b></div>', unsafe_allow_html=True)
            
            # Detected Objects
            st.markdown("#### 🔍 Detected Objects")
            if detected_objects:
                unique_objects = {}
                for obj in detected_objects:
                    name = obj['name']
                    if name not in unique_objects or obj['confidence'] > unique_objects[name]:
                        unique_objects[name] = obj['confidence']
                
                badges_html = ""
                for name, conf in unique_objects.items():
                    badges_html += f'<div class="badge badge-success">{name} ({conf:.0%})</div>'
                st.markdown(badges_html, unsafe_allow_html=True)
                
                # Spatial Info
                if enable_spatial_info and detection_data:
                    spatial = get_spatial_info(detection_data, image.size[0], image.size[1])
                    if spatial:
                        st.markdown("#### 📐 Spatial Layout")
                        spatial_html = ""
                        for s in spatial:
                            spatial_html += f'<div class="badge badge-info">{s}</div>'
                        st.markdown(spatial_html, unsafe_allow_html=True)
                
                # Hazards
                if enable_hazard_detection:
                    hazards = detect_hazards(list(unique_objects.keys()))
                    if hazards:
                        st.markdown("#### ⚠️ Safety Alerts")
                        for hazard in hazards:
                            st.markdown(f'<div class="hazard-box">{hazard}</div>', unsafe_allow_html=True)
            else:
                st.info("No objects detected. Try lowering detection confidence in sidebar.")
            
            # OCR Results
            st.markdown("#### 📖 Extracted Text")
            if extracted_text:
                st.markdown(f'<div class="result-box">📝 {extracted_text}</div>', unsafe_allow_html=True)
            else:
                st.info("No readable text found in image.")
            
            # AI Description
            st.markdown("#### 🤖 AI Scene Description")
            st.markdown(f'<div class="result-box">{description}</div>', unsafe_allow_html=True)
            
            # Audio
            if audio_bytes:
                st.markdown("#### 🔊 Audio Description")
                st.audio(audio_bytes, format='audio/mp3')
                
                st.download_button(
                    label="⬇️ Download Audio",
                    data=audio_bytes,
                    file_name=f"visionvoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3",
                    mime="audio/mp3"
                )
            
            # Success message
            st.markdown(f"""
            <div class="success-box">
            ✅ <b>Analysis Complete!</b><br>
            • Objects Detected: <b>{len(detected_objects)}</b><br>
            • Text Length: <b>{len(extracted_text)}</b> characters<br>
            • Description Length: <b>{len(description)}</b> characters<br>
            • Total Analyses: <b>{st.session_state.total_analyses}</b>
            </div>
            """, unsafe_allow_html=True)
            
            st.balloons()

else:
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: rgba(255,255,255,0.05); border-radius: 20px; margin: 2rem 0;">
        <h2>👋 Welcome to VisionVoice Pro!</h2>
        <p style="font-size: 1.1rem; color: #b8c5d6;">
            Upload an image or capture one with your camera to begin AI analysis.<br>
            Don't forget to add your Gemini API key in the sidebar! 🔑
        </p>
        <br>
        <p style="font-size: 3rem;">📸 → 🤖 → 🔊</p>
        <p style="color: #4facfe; font-weight: 600;">Capture → Analyze → Listen</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <p>🌟 <b>VisionVoice Pro</b> - Empowering Vision Through AI 🌟</p>
    <p>Developed by <b>Aditya Menon</b> | RA2311026050050 | SEAI (21CSE312P)</p>
    <p>SRM IST Tiruchirappalli | Aligned with UN SDGs 3, 4 & 10</p>
    <p style="margin-top: 1rem;">
        <span class="badge badge-info">YOLOv8</span>
        <span class="badge badge-info">EasyOCR</span>
        <span class="badge badge-info">Gemini 2.0</span>
        <span class="badge badge-info">gTTS</span>
        <span class="badge badge-info">Streamlit</span>
        <span class="badge badge-info">Docker</span>
    </p>
</div>
""", unsafe_allow_html=True)
