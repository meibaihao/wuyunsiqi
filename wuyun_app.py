import streamlit as st
from datetime import datetime

# --- 核心算法函数 ---
def calculate_wuyun_liuqi(year):
    tian_gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    di_zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    gan_index = (year - 4) % 10
    zhi_index = (year - 4) % 12
    gan_zhi = f"{tian_gan[gan_index]}{di_zhi[zhi_index]}"

    # 岁运
    yun_elements = ["土", "金", "水", "木", "火"]
    yun_idx = gan_index % 5
    yun_element = yun_elements[yun_idx]
    is_excess = (gan_index % 2 == 0)
    yun_type = "太过" if is_excess else "不及"
    
    # 司天与在泉
    liuqi_map = ["少阴君火", "太阴湿土", "少阳相火", "阳明燥金", "太阳寒水", "厥阴风木"]
    sitian_idx = zhi_index % 6
    sitian = liuqi_map[sitian_idx]
    zaiquan_idx = (sitian_idx + 3) % 6
    zaiquan = liuqi_map[zaiquan_idx]

    # 特殊格局判断
    special_status = []
    # 简单示例逻辑
    if (gan_zhi in ["癸巳", "癸亥", "乙卯", "乙酉"]): special_status.append("天符")
    if (gan_zhi in ["丁卯", "丙午", "乙未"]): special_status.append("岁会")

    return {
        "gan_zhi": gan_zhi,
        "yun": f"{yun_element}运{yun_type}",
        "yun_element": yun_element,
        "sitian": sitian,
        "zaiquan": zaiquan,
        "special": "、".join(special_status) if special_status else "平气年份",
        "is_excess": is_excess
    }

# --- 界面配置 ---
st.set_page_config(page_title="中医五运六气推演", page_icon="☯️", layout="wide")

# --- 侧边栏：参数与色调控制 ---
with st.sidebar:
    st.header("⚙️ 设置中心")
    selected_year = st.number_input("选择年份", value=2026, step=1)
    
    st.divider()
    # 色调调整按钮（颜色选择器）
    theme_color = st.color_picker("界面强调色调", "#8B4513") 
    st.caption("调整此颜色可改变标题和部分装饰线的色调")
    
    st.divider()
    st.info("提示：五运六气以‘立春’为岁首交替。")

# --- 动态样式注入 ---
# 使用 HTML/CSS 注入来根据用户选的颜色调整样式
st.markdown(f"""
    <style>
    .main-title {{
        color: {theme_color};
        text-align: center;
        font-weight: bold;
        font-size: 3rem;
        margin-bottom: 20px;
    }}
    .stMetric {{
        background-color: {theme_color}10;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid {theme_color};
    }}
    </style>
    """, unsafe_allow_html=True)

# 执行计算
res = calculate_wuyun_liuqi(selected_year)

# --- 主界面展示 ---
st.markdown(f'<div class="main-title">☯️ {selected_year}年 五运六气推演</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # 顶部核心指标
    c1, c2 = st.columns(2)
    c1.metric("干支历", res["gan_zhi"])
    c2.metric("年份格局", res["special"])

    st.divider()

    # 运气详细卡片
    st.subheader("📋 年度运气报告")
    
    # 岁运
    st.write(f"### 🌀 大运（中运）：`{res['yun']}`")
    if res["is_excess"]:
        st.write("👉 **气候特点**：本年岁运之气偏盛，需注意对应脏腑的实证。")
    else:
        st.write("👉 **气候特点**：本年岁运之气不足，需防范克制之气乘虚而入。")

    # 司天在泉
    col_a, col_b = st.columns(2)
    with col_a:
        st.warning(f"**司天（上半年）**\n\n{res['sitian']}")
    with col_b:
        st.success(f"**在泉（下半年）**\n\n{res['zaiquan']}")

    st.divider()

    # 健康与养生
    st.subheader("💡 养生建议")
    if "火" in res["yun_element"]:
        st.error("【火运】夏季注意心脑血管保护，清热养阴。")
    elif "水" in res["yun_element"]:
        st.info("【水运】寒气偏重，宜温补肾阳，预防寒湿痹痛。")
    elif "土" in res["yun_element"]:
        st.warning("【土运】注意脾胃运化，雨水较多，防湿邪困脾。")
    elif "木" in res["yun_element"]:
        st.success("【木运】风气较盛，注意肝胆疏泄与情绪调节。")
    elif "金" in res["yun_element"]:
        st.write("⚪ **【金运】** 金气清肃，注意宣肺止咳，养护皮肤。")
    
    st.divider()
    
    # 底部说明表
    st.subheader("📅 六步主气分布参考")
    steps_data = {
        "时段": ["初之气", "二之气", "三之气", "四之气", "五之气", "终之气"],
        "节气范围": ["立春-清明", "清明-芒种", "芒种-立秋", "立秋-寒露", "寒露-大雪", "大雪-立春"],
        "主气": ["厥阴风木", "少阴君火", "少阳相火", "太阴湿土", "阳明燥金", "太阳寒水"]
    }
    st.table(steps_data)

st.caption(f"当前推演基于公元纪年法转化。设置色调：{theme_color}")
