import streamlit as st
from datetime import datetime

# --- 核心算法函数 ---
def calculate_wuyun_liuqi(year):
    tian_gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    di_zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    # 1. 计算干支
    gan_index = (year - 4) % 10
    zhi_index = (year - 4) % 12
    gan_zhi = f"{tian_gan[gan_index]}{di_zhi[zhi_index]}"

    # 2. 推算【岁运】
    yun_elements = ["土", "金", "水", "木", "火"]
    yun_idx = gan_index % 5
    yun_element = yun_elements[yun_idx]
    is_excess = (gan_index % 2 == 0)
    yun_type = "太过" if is_excess else "不及"
    
    # 3. 推算【司天】与【在泉】
    # 这里的索引对应逻辑：子(0)午(6) -> 少阴君火...
    liuqi_map = ["少阴君火", "太阴湿土", "少阳相火", "阳明燥金", "太阳寒水", "厥阴风木"]
    sitian_idx = zhi_index % 6
    sitian = liuqi_map[sitian_idx]
    zaiquan_idx = (sitian_idx + 3) % 6
    zaiquan = liuqi_map[zaiquan_idx]

    # 4. 简易运气同化逻辑 (进阶版)
    special_status = []
    # 岁会判断：岁运五行与地支方位五行一致
    # 这里仅示例，实际中医逻辑更复杂
    if (gan_zhi in ["癸巳", "癸亥", "乙卯", "乙酉"]): special_status.append("天符")
    if (gan_zhi in ["丁卯", "丙午", "乙未"]): special_status.append("岁会")

    return {
        "gan_zhi": gan_zhi,
        "yun": f"{yun_element}运{yun_type}",
        "yun_element": yun_element,
        "sitian": sitian,
        "zaiquan": zaiquan,
        "special": "、".join(special_status) if special_status else "平气年份"
    }

# --- Streamlit 界面设计 ---
st.set_page_config(page_title="中医五运六气查询", page_icon="☯️")

st.title("☯️ 中医五运六气推演")
st.markdown("通过干支历法推算全年的气候倾向与体质养生要点。")

# 侧边栏：年份选择
with st.sidebar:
    st.header("参数设置")
    selected_year = st.number_input("输入年份", value=datetime.now().year, step=1)
    st.info("注：本工具以每年‘立春’作为运气交替的分界。")

# 执行计算
res = calculate_wuyun_liuqi(selected_year)

# 结果展示区
col1, col2 = st.columns(2)

with col1:
    st.metric(label="当前年份", value=f"{selected_year}年", delta=res["gan_zhi"])
    st.subheader("核心运气")
    st.info(f"**大运（中运）：** {res['yun']}")
    st.warning(f"**司天（上半年）：** {res['sitian']}")
    st.success(f"**在泉（下半年）：** {res['zaiquan']}")

with col2:
    st.subheader("特殊格局")
    st.write(res["special"])
    
    st.subheader("五行生克提示")
    # 动态逻辑展示
    if "火" in res["yun"]:
        st.error("夏季注意心脑血管，预防热邪侵袭。")
    elif "水" in res["yun"]:
        st.blue("寒气偏重，宜温补肾阳，防寒湿。")
    elif "土" in res["yun"]:
        st.warning("注意脾胃运化，谨防湿邪困脾。")
    else:
        st.write("气机变化较为平缓，顺应四时养生即可。")

# 详细解析表格
st.divider()
st.subheader("📅 六步主客气分布 (概览)")
steps_data = {
    "时段": ["初之气 (立春-清明)", "二_之气 (清明-芒种)", "三之气 (芒种-立秋)", "四之气 (立秋-寒露)", "五之气 (寒露-大雪)", "终之气 (大雪-立春)"],
    "主气": ["厥阴风木", "少阴君火", "少阳相火", "太阴湿土", "阳明燥金", "太阳寒水"]
}
st.table(steps_data)

# 底部说明
st.caption("数据仅供中医爱好者学习交流，临床诊疗请遵医嘱。")
