import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import base64
import random
import urllib.parse
from datetime import datetime

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI 减脂康复助手",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Global CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans SC', sans-serif;
    background-color: #0d0d0d;
    color: #f0f0f0;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1rem 1.2rem 4rem 1.2rem; max-width: 480px; margin: auto; }

/* Headings */
h1 { font-family: 'Space Mono', monospace; font-size: 1.4rem !important; color: #FF4C1F; letter-spacing: -0.5px; }
h2 { font-size: 1.05rem !important; color: #ffffff; margin-top: 0.5rem; }
h3 { font-size: 0.95rem !important; color: #aaaaaa; font-weight: 400; }

/* Tabs */
[data-testid="stTabs"] button {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #888;
    border-bottom: 2px solid transparent;
    padding: 0.5rem 0.8rem;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #FF4C1F;
    border-bottom: 2px solid #FF4C1F;
    background: transparent;
}

/* Cards */
.card {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.8rem;
}
.card-accent {
    border-left: 3px solid #FF4C1F;
}

/* Metric row */
.metric-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 8px;
    margin: 0.8rem 0;
}
.metric-box {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 10px;
    padding: 0.6rem 0.5rem;
    text-align: center;
}
.metric-val {
    font-family: 'Space Mono', monospace;
    font-size: 1.1rem;
    color: #FF4C1F;
    font-weight: 700;
}
.metric-label {
    font-size: 0.65rem;
    color: #777;
    margin-top: 2px;
}

/* Buttons */
.stButton > button {
    background: #FF4C1F;
    color: white;
    border: none;
    border-radius: 8px;
    font-family: 'Noto Sans SC', sans-serif;
    font-size: 0.88rem;
    font-weight: 500;
    padding: 0.5rem 1.2rem;
    width: 100%;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.85; }

/* Secondary button */
.stButton.secondary > button {
    background: #1a1a1a;
    border: 1px solid #333;
    color: #ccc;
}

/* Inputs */
.stTextInput input, .stNumberInput input, .stSelectbox > div > div {
    background: #1a1a1a !important;
    border: 1px solid #333 !important;
    color: #f0f0f0 !important;
    border-radius: 8px !important;
    font-size: 0.88rem !important;
}
.stTextArea textarea {
    background: #1a1a1a !important;
    border: 1px solid #333 !important;
    color: #f0f0f0 !important;
    border-radius: 8px !important;
    font-size: 0.88rem !important;
}
.stSelectbox label, .stNumberInput label, .stTextInput label, .stTextArea label {
    color: #aaa !important;
    font-size: 0.8rem !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #1a1a1a;
    border: 1px dashed #333;
    border-radius: 10px;
    padding: 0.5rem;
}
[data-testid="stFileUploader"] label { color: #888 !important; font-size: 0.8rem !important; }

/* Tag pills */
.tag {
    display: inline-block;
    background: #2a2a2a;
    color: #ccc;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    margin: 2px;
}
.tag-red { background: #2d1510; color: #FF6B4A; }
.tag-green { background: #0d2010; color: #4AFF7A; }

/* Divider */
.divider { border: none; border-top: 1px solid #222; margin: 0.8rem 0; }

/* Food result row */
.food-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.4rem 0;
    border-bottom: 1px solid #222;
    font-size: 0.82rem;
}
.food-row:last-child { border-bottom: none; }
.food-key { color: #888; }
.food-val { color: #f0f0f0; font-weight: 500; }

/* Exercise card */
.ex-card {
    background: #141414;
    border: 1px solid #2a2a2a;
    border-radius: 10px;
    padding: 0.7rem 0.9rem;
    margin-bottom: 0.5rem;
}
.ex-name { font-size: 0.9rem; color: #ffffff; font-weight: 500; }
.ex-detail { font-size: 0.75rem; color: #777; margin-top: 2px; }
.yt-link { font-size: 0.75rem; color: #FF4C1F; text-decoration: none; }

/* Spinner */
.stSpinner > div { border-top-color: #FF4C1F !important; }

/* Warning / info */
.stAlert { border-radius: 8px !important; font-size: 0.82rem !important; }

/* Top header bar */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.2rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid #1f1f1f;
}
.logo-text {
    font-family: 'Space Mono', monospace;
    font-size: 1rem;
    color: #FF4C1F;
    font-weight: 700;
}
.date-text {
    font-size: 0.7rem;
    color: #555;
}
</style>
""", unsafe_allow_html=True)

# ─── Gemini Init ─────────────────────────────────────────────────────────────
def get_gemini():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # 直接指定 1.5 版本，不再让它自动选 2.5
        return genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        st.error(f"连接 AI 失败：{str(e)}")
        st.stop()
        
# ─── Session State Init ───────────────────────────────────────────────────────
def init_state():
    defaults = {
        "profile": {},
        "food_results": [],
        "rehab_results": [],
        "workout_plan": "",
        "workout_date": "",
        "chat_history": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─── Header ──────────────────────────────────────────────────────────────────
today_str = datetime.now().strftime("%m/%d %a").upper()
st.markdown(f"""
<div class="topbar">
  <div class="logo-text">🔥 AI减脂助手</div>
  <div class="date-text">{today_str}</div>
</div>
""", unsafe_allow_html=True)

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 档案", "🍱 饮食", "🏋 运动", "🩹 康复", "💬 问诊"])

# ════════════════════════════════════════════════════════════════════
# TAB 1 — 基础档案
# ════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("#### 体测数据")

    upload_mode = st.radio("录入方式", ["📷 上传截图", "✏️ 手动输入"], horizontal=True, label_visibility="collapsed")

    if upload_mode == "📷 上传截图":
        img_file = st.file_uploader("上传体测截图", type=["jpg", "jpeg", "png", "webp"], label_visibility="collapsed")
        if img_file and st.button("🤖 AI 识别体测数据"):
            model = get_gemini()
            img = Image.open(img_file)
            with st.spinner("正在识别…"):
                prompt = """你是专业健康数据提取助手。从这张体测截图中提取以下数据，
如果某项数据不存在请填写"未知"。
请严格按照以下JSON格式回复，不要有任何其他文字：
{
  "weight": "体重(kg)",
  "body_fat": "体脂率(%)",
  "muscle_mass": "肌肉量(kg)",
  "visceral_fat": "内脏脂肪等级",
  "bmr": "基础代谢(kcal)",
  "bmi": "BMI"
}"""
                try:
                    resp = model.generate_content([prompt, img])
                    import json, re
                    raw = resp.text.strip()
                    match = re.search(r'\{.*\}', raw, re.DOTALL)
                    if match:
                        data = json.loads(match.group())
                        st.session_state.profile = data
                        st.success("✅ 识别成功")
                    else:
                        st.error("识别格式异常，请手动输入")
                except Exception as e:
                    st.error(f"识别失败：{e}")
    else:
        col1, col2 = st.columns(2)
        with col1:
            w = st.text_input("体重 (kg)", placeholder="例：75.5")
            bf = st.text_input("体脂率 (%)", placeholder="例：28.5")
            mm = st.text_input("肌肉量 (kg)", placeholder="例：52.0")
        with col2:
            vf = st.text_input("内脏脂肪等级", placeholder="例：9")
            bmr = st.text_input("基础代谢 (kcal)", placeholder="例：1680")
            bmi = st.text_input("BMI", placeholder="例：24.2")
        if st.button("💾 保存档案"):
            st.session_state.profile = {
                "weight": w or "未知", "body_fat": bf or "未知",
                "muscle_mass": mm or "未知", "visceral_fat": vf or "未知",
                "bmr": bmr or "未知", "bmi": bmi or "未知",
            }
            st.success("✅ 已保存")

    # Display profile
    p = st.session_state.profile
    if p:
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("**当前档案**")
        st.markdown(f"""
        <div class="metric-grid">
          <div class="metric-box"><div class="metric-val">{p.get('weight','—')}</div><div class="metric-label">体重 kg</div></div>
          <div class="metric-box"><div class="metric-val">{p.get('body_fat','—')}</div><div class="metric-label">体脂率 %</div></div>
          <div class="metric-box"><div class="metric-val">{p.get('muscle_mass','—')}</div><div class="metric-label">肌肉量 kg</div></div>
          <div class="metric-box"><div class="metric-val">{p.get('visceral_fat','—')}</div><div class="metric-label">内脏脂肪</div></div>
          <div class="metric-box"><div class="metric-val">{p.get('bmr','—')}</div><div class="metric-label">基础代谢</div></div>
          <div class="metric-box"><div class="metric-val">{p.get('bmi','—')}</div><div class="metric-label">BMI</div></div>
        </div>
        """, unsafe_allow_html=True)

        # AI 建议
        if st.button("📊 生成减脂分析报告"):
            model = get_gemini()
            profile_str = ", ".join([f"{k}={v}" for k, v in p.items()])
            with st.spinner("AI 分析中…"):
                prompt = f"""你是专业减脂顾问。根据以下体测数据，用简洁中文给出：
1. 当前身体状态评估（2句话）
2. 减脂目标建议（具体数字）
3. 每日热量缺口建议（kcal）
4. 针对内脏脂肪的3个关键行动建议

体测数据：{profile_str}

用简洁的卡片式格式输出，每项不超过3行。"""
                try:
                    resp = model.generate_content(prompt)
                    st.markdown(f'<div class="card card-accent">{resp.text}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"分析失败：{e}")

# ════════════════════════════════════════════════════════════════════
# TAB 2 — 饮食识别
# ════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("#### 饮食热量识别")
    food_img = st.file_uploader("拍一张食物照片", type=["jpg", "jpeg", "png", "webp"], key="food_upload", label_visibility="collapsed")

    visceral_fat_level = st.session_state.profile.get("visceral_fat", "未知")

    if food_img and st.button("🔍 AI 分析这餐"):
        model = get_gemini()
        img = Image.open(food_img)
        with st.spinner("AI 正在分析食物…"):
            prompt = f"""你是营养分析专家。分析这张食物图片，识别出所有食物，
对每种食物给出推算数据。用户内脏脂肪等级为：{visceral_fat_level}。

请严格按以下JSON数组格式回复，不要有任何其他文字：
[
  {{
    "name": "食物名称",
    "weight_g": "估算重量(克)",
    "calories": "热量(kcal)",
    "protein_g": "蛋白质(克)",
    "carbs_g": "碳水(克)",
    "fat_g": "脂肪(克)",
    "gi": "GI值(数字)",
    "visceral_comment": "针对内脏脂肪的点评(1句话)"
  }}
]"""
            try:
                import json, re
                resp = model.generate_content([prompt, img])
                raw = resp.text.strip()
                match = re.search(r'\[.*\]', raw, re.DOTALL)
                if match:
                    foods = json.loads(match.group())
                    st.session_state.food_results = foods
                else:
                    st.error("解析失败，请重试")
            except Exception as e:
                st.error(f"分析失败：{e}")

    # Display food results
    if st.session_state.food_results:
        total_cal = 0
        total_prot = 0
        for food in st.session_state.food_results:
            try: total_cal += float(str(food.get('calories','0')).replace('kcal','').strip())
            except: pass
            try: total_prot += float(str(food.get('protein_g','0')).replace('g','').strip())
            except: pass

            gi_val = str(food.get('gi', '0'))
            try:
                gi_num = float(re.sub(r'[^\d.]', '', gi_val))
                gi_color = "tag-red" if gi_num >= 70 else ("tag-green" if gi_num < 55 else "tag")
            except:
                gi_color = "tag"

            st.markdown(f"""
            <div class="card">
              <div style="font-size:0.92rem;font-weight:500;color:#fff;margin-bottom:0.4rem">
                {food.get('name','未知食物')}
              </div>
              <div class="food-row">
                <span class="food-key">估算重量</span><span class="food-val">{food.get('weight_g','—')} g</span>
              </div>
              <div class="food-row">
                <span class="food-key">热量</span><span class="food-val">{food.get('calories','—')} kcal</span>
              </div>
              <div class="food-row">
                <span class="food-key">蛋白质</span><span class="food-val">{food.get('protein_g','—')} g</span>
              </div>
              <div class="food-row">
                <span class="food-key">碳水</span><span class="food-val">{food.get('carbs_g','—')} g</span>
              </div>
              <div class="food-row">
                <span class="food-key">脂肪</span><span class="food-val">{food.get('fat_g','—')} g</span>
              </div>
              <div class="food-row">
                <span class="food-key">GI值</span>
                <span class="{gi_color} tag">{food.get('gi','—')}</span>
              </div>
              <div style="margin-top:0.5rem;font-size:0.75rem;color:#FF6B4A;background:#1f1010;border-radius:6px;padding:0.4rem 0.6rem">
                🫀 {food.get('visceral_comment','—')}
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card" style="border-color:#FF4C1F">
          <div style="display:flex;justify-content:space-between">
            <span style="color:#aaa;font-size:0.82rem">本餐合计热量</span>
            <span style="font-family:'Space Mono',monospace;color:#FF4C1F;font-size:1.1rem">{total_cal:.0f} kcal</span>
          </div>
          <div style="display:flex;justify-content:space-between;margin-top:4px">
            <span style="color:#aaa;font-size:0.82rem">蛋白质合计</span>
            <span style="font-size:0.88rem;color:#4AFF7A">{total_prot:.1f} g</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🗑️ 清除记录", key="clear_food"):
            st.session_state.food_results = []
            st.rerun()

# ════════════════════════════════════════════════════════════════════
# TAB 3 — 运动计划
# ════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("#### 今日运动计划")

    equipment_options = ["无器械（徒手）", "哑铃", "弹力带", "跳绳", "瑜伽垫", "拉力器", "跑步机", "划船机", "杠铃", "TRX"]
    selected_equipment = st.multiselect("选择你有的器械", equipment_options, default=["无器械（徒手）"], label_visibility="collapsed")

    goal_options = ["🔥 燃脂优先", "💪 增肌减脂", "🧘 恢复放松", "❤️ 心肺提升"]
    workout_goal = st.radio("今日目标", goal_options, horizontal=True, label_visibility="collapsed")

    duration = st.select_slider("训练时长", options=["15分钟", "20分钟", "30分钟", "45分钟", "60分钟"], value="30分钟")

    today = datetime.now().strftime("%Y-%m-%d")
    need_new = st.session_state.workout_date != today or not st.session_state.workout_plan

    if st.button("⚡ 生成今日计划" if need_new else "🔄 重新生成计划"):
        model = get_gemini()
        p = st.session_state.profile
        profile_hint = f"体重{p.get('weight','未知')}kg，体脂{p.get('body_fat','未知')}%，内脏脂肪{p.get('visceral_fat','未知')}级" if p else "体测数据未录入"
        seed = random.randint(1, 9999)
        equipment_str = "、".join(selected_equipment)
        with st.spinner("AI 生成个性化计划…"):
            prompt = f"""你是专业私教。根据以下信息生成一份今日运动计划（随机种子:{seed}，确保每次不重样）：

用户信息：{profile_hint}
可用器械：{equipment_str}
今日目标：{workout_goal}
训练时长：{duration}
日期：{today}

请生成包含热身、主训练、拉伸的完整计划。格式要求：
- 每个动作单独一行
- 格式：动作名 | 组数×次数或时间 | 简短要点
- 热身和拉伸各2-3个动作，主训练4-6个动作
- 最后给出本次训练预估消耗热量范围
- 语言简洁，适合手机查看"""
            try:
                resp = model.generate_content(prompt)
                st.session_state.workout_plan = resp.text
                st.session_state.workout_date = today
            except Exception as e:
                st.error(f"生成失败：{e}")

    if st.session_state.workout_plan:
        lines = st.session_state.workout_plan.strip().split('\n')
        current_section = ""
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # Detect section headers
            if any(kw in line for kw in ["热身", "主训练", "拉伸", "冷却", "有氧", "力量"]) and '|' not in line:
                current_section = line
                st.markdown(f'<div style="font-size:0.8rem;color:#FF4C1F;font-family:Space Mono,monospace;margin:0.8rem 0 0.3rem 0;text-transform:uppercase">{line}</div>', unsafe_allow_html=True)
            elif '|' in line:
                parts = [p.strip() for p in line.split('|')]
                name = parts[0] if len(parts) > 0 else line
                sets = parts[1] if len(parts) > 1 else ""
                tip = parts[2] if len(parts) > 2 else ""
                # YouTube search link
                yt_query = urllib.parse.quote(f"{name} 教学 正确动作")
                yt_url = f"https://www.youtube.com/results?search_query={yt_query}"
                st.markdown(f"""
                <div class="ex-card">
                  <div class="ex-name">{name}</div>
                  <div class="ex-detail">{sets}{' · ' + tip if tip else ''}</div>
                  <a href="{yt_url}" target="_blank" class="yt-link">▶ YouTube 教程</a>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="font-size:0.8rem;color:#666;padding:0.2rem 0">{line}</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# TAB 4 — 康复系统
# ════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("#### 伤痛康复方案")

    body_parts = {
        "🧠 颈部": "颈部", "🦾 肩膀": "肩膀", "💪 手肘": "手肘",
        "🖐 手腕": "手腕", "🫁 上背": "上背部", "⬛ 腰部": "腰部",
        "🍑 髋部": "髋部", "🦵 膝盖": "膝盖", "🦶 踝关节": "踝关节",
        "👣 足底": "足底筋膜"
    }

    selected_part = st.selectbox("选择不适部位", list(body_parts.keys()), label_visibility="collapsed")
    part_name = body_parts[selected_part]

    pain_level = st.select_slider("疼痛程度", options=["轻微不适", "隐隐作痛", "明显疼痛", "严重疼痛"], value="隐隐作痛")
    pain_duration = st.radio("持续时间", ["< 3天", "3-7天", "1-4周", "> 1个月"], horizontal=True, label_visibility="collapsed")
    pain_desc = st.text_area("描述一下症状（可选）", placeholder="例：久坐后加重，活动后好转…", height=60, label_visibility="collapsed")

    if st.button("🩹 生成康复方案"):
        model = get_gemini()
        with st.spinner("AI 生成康复计划…"):
            prompt = f"""你是运动康复治疗师。为以下情况生成康复方案：

部位：{part_name}
疼痛程度：{pain_level}
持续时间：{pain_duration}
症状描述：{pain_desc or '无'}

请生成：
1. 可能原因分析（1-2句）
2. 康复动作（4-6个），每个格式为：
   动作名 | 组数/时间 | 动作要点 | 注意事项
3. 日常注意事项（3条）
4. 何时需要就医（1条）

语言简洁，适合手机阅读。"""
            try:
                resp = model.generate_content(prompt)
                st.session_state.rehab_results = resp.text
            except Exception as e:
                st.error(f"生成失败：{e}")

    if st.session_state.rehab_results:
        result_text = st.session_state.rehab_results
        lines = result_text.strip().split('\n')

        in_exercise_section = False
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Section detection
            if any(kw in line for kw in ["可能原因", "日常注意", "何时就医", "注意事项"]) and '|' not in line:
                in_exercise_section = False
                st.markdown(f'<div style="font-size:0.8rem;color:#FF4C1F;font-family:Space Mono,monospace;margin:0.8rem 0 0.3rem 0">{line}</div>', unsafe_allow_html=True)
            elif any(kw in line for kw in ["康复动作", "训练动作", "锻炼动作"]) and '|' not in line:
                in_exercise_section = True
                st.markdown(f'<div style="font-size:0.8rem;color:#FF4C1F;font-family:Space Mono,monospace;margin:0.8rem 0 0.3rem 0">{line}</div>', unsafe_allow_html=True)
            elif '|' in line:
                in_exercise_section = True
                parts = [p.strip() for p in line.split('|')]
                name = parts[0].lstrip('0123456789.-• ') if parts else line
                sets = parts[1] if len(parts) > 1 else ""
                tip = parts[2] if len(parts) > 2 else ""
                caution = parts[3] if len(parts) > 3 else ""
                yt_query = urllib.parse.quote(f"{name} 康复训练 教学")
                yt_url = f"https://www.youtube.com/results?search_query={yt_query}"
                st.markdown(f"""
                <div class="ex-card">
                  <div class="ex-name">{name}</div>
                  <div class="ex-detail">{sets}{' · ' + tip if tip else ''}</div>
                  {f'<div class="ex-detail" style="color:#FF6B4A">⚠ {caution}</div>' if caution else ''}
                  <a href="{yt_url}" target="_blank" class="yt-link">▶ YouTube 康复教程</a>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="font-size:0.82rem;color:#aaa;padding:0.15rem 0;line-height:1.5">{line}</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# TAB 5 — AI 问诊
# ════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("#### AI 健康问诊")

    # Display chat history
    for msg in st.session_state.chat_history:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            st.markdown(f"""
            <div style="display:flex;justify-content:flex-end;margin-bottom:0.5rem">
              <div style="background:#FF4C1F;color:white;border-radius:12px 12px 2px 12px;
                padding:0.5rem 0.8rem;max-width:80%;font-size:0.85rem;line-height:1.5">
                {content}
              </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display:flex;justify-content:flex-start;margin-bottom:0.5rem">
              <div style="background:#1a1a1a;color:#f0f0f0;border:1px solid #2a2a2a;
                border-radius:12px 12px 12px 2px;padding:0.5rem 0.8rem;
                max-width:85%;font-size:0.85rem;line-height:1.5">
                {content}
              </div>
            </div>""", unsafe_allow_html=True)

    # Quick question chips
    quick_qs = ["内脏脂肪怎么降？", "我该吃多少蛋白质？", "空腹有氧有效吗？", "断食减脂安全吗？"]
    cols = st.columns(2)
    for i, q in enumerate(quick_qs):
        with cols[i % 2]:
            if st.button(q, key=f"quick_{i}"):
                st.session_state._pending_question = q

    # Text input
    user_input = st.text_input("问我任何减脂康复问题…", key="chat_input", label_visibility="collapsed", placeholder="输入问题后按回车…")

    # Handle input (either quick button or text)
    pending = getattr(st.session_state, '_pending_question', None)
    final_input = pending or user_input

    if final_input and final_input.strip():
        if pending:
            st.session_state._pending_question = None

        model = get_gemini()
        p = st.session_state.profile
        profile_ctx = ""
        if p:
            profile_ctx = f"用户档案：体重{p.get('weight','?')}kg，体脂{p.get('body_fat','?')}%，内脏脂肪{p.get('visceral_fat','?')}级，基础代谢{p.get('bmr','?')}kcal。"

        system_prompt = f"""你是专业的减脂康复AI顾问，擅长营养学、运动科学和康复医学。
{profile_ctx}
请用简洁专业的中文回答用户问题，控制在150字以内，适合手机阅读。
给出实用可操作的建议，避免空洞的套话。"""

        st.session_state.chat_history.append({"role": "user", "content": final_input})

        # Build conversation for API (last 6 turns to save tokens)
        history_for_api = st.session_state.chat_history[-12:]
        messages = []
        for msg in history_for_api:
            messages.append({"role": msg["role"], "content": msg["content"]})

        # Prepend system context to first user message
        if messages and messages[0]["role"] == "user":
            messages[0]["content"] = system_prompt + "\n\n用户问题：" + messages[0]["content"]

        with st.spinner("AI 思考中…"):
            try:
                # Build history for gemini chat
                chat_msgs = []
                for m in messages[:-1]:
                    role = "user" if m["role"] == "user" else "model"
                    chat_msgs.append({"role": role, "parts": [m["content"]]})

                chat = model.start_chat(history=chat_msgs)
                resp = chat.send_message(messages[-1]["content"])
                answer = resp.text
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.session_state.chat_history.append({"role": "assistant", "content": f"出错了：{e}"})

        st.rerun()

    if len(st.session_state.chat_history) > 0:
        if st.button("🗑️ 清除对话", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:2rem;padding-top:1rem;border-top:1px solid #1f1f1f">
  <div style="font-size:0.65rem;color:#444">
    AI 建议仅供参考，不替代专业医疗意见<br>
    Powered by Gemini · Built with Streamlit
  </div>
</div>
""", unsafe_allow_html=True)
