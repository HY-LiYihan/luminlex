import streamlit as st

# 页面标题
st.title("🏠 Luminlex - 英语教材生成系统")

# 应用简介
st.markdown("""
<div style='background-color: rgba(255, 214, 102, 0.1); padding: 1.5rem; border-radius: 12px; border-left: 4px solid var(--color-accent);'>
<h3 style='color: var(--color-primary); margin-top: 0;'>欢迎使用 Luminlex</h3>
<p style='color: var(--color-text); line-height: 1.6;'>
    Luminlex 是一个基于大语言模型的智能英语教材生成系统，专为英语教师、教育工作者和培训机构设计。
    系统能够自动生成四六级等英语考试题目，提供完整的教材解决方案。
</p>
</div>
""", unsafe_allow_html=True)

# 快速功能卡片
st.subheader("🚀 核心功能")

cols = st.columns(3)

with cols[0]:
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem; background-color: white; border-radius: 12px; border: 2px solid var(--color-accent); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); height: 100%;'>
        <div style='font-size: 2.5rem; margin-bottom: 1rem; color: var(--color-primary);'>📝</div>
        <h4 style='color: var(--color-primary); margin-bottom: 0.8rem;'>智能题目生成</h4>
        <p style='color: var(--color-text-secondary); line-height: 1.4;'>自动生成四六级听力、阅读、写作、翻译等各类题目</p>
    </div>
    """, unsafe_allow_html=True)

with cols[1]:
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem; background-color: white; border-radius: 12px; border: 2px solid var(--color-accent); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); height: 100%;'>
        <div style='font-size: 2.5rem; margin-bottom: 1rem; color: var(--color-primary);'>📚</div>
        <h4 style='color: var(--color-primary); margin-bottom: 0.8rem;'>教材管理</h4>
        <p style='color: var(--color-text-secondary); line-height: 1.4;'>管理教材模板、题目库，支持多种导出格式</p>
    </div>
    """, unsafe_allow_html=True)

with cols[2]:
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem; background-color: white; border-radius: 12px; border: 2px solid var(--color-accent); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); height: 100%;'>
        <div style='font-size: 2.5rem; margin-bottom: 1rem; color: var(--color-primary);'>⚙️</div>
        <h4 style='color: var(--color-primary); margin-bottom: 0.8rem;'>AI智能配置</h4>
        <p style='color: var(--color-text-secondary); line-height: 1.4;'>支持多个AI平台，灵活调节生成参数</p>
    </div>
    """, unsafe_allow_html=True)

# 考试类型介绍
st.subheader("🎯 支持的考试类型")

exam_types = [
    {"name": "大学英语四级", "code": "CET-4", "desc": "包含听力、阅读、写作、翻译完整题型"},
    {"name": "大学英语六级", "code": "CET-6", "desc": "更高难度，适合六级备考训练"},
    {"name": "专业英语四级", "code": "TEM-4", "desc": "英语专业基础阶段考试"},
    {"name": "专业英语八级", "code": "TEM-8", "desc": "英语专业高级阶段考试"},
    {"name": "雅思考试", "code": "IELTS", "desc": "国际英语语言测试系统"},
    {"name": "托福考试", "code": "TOEFL", "desc": "Test of English as a Foreign Language"}
]

for i in range(0, len(exam_types), 2):
    col1, col2 = st.columns(2)
    with col1:
        if i < len(exam_types):
            exam = exam_types[i]
            st.markdown(f"""
            <div style='padding: 1rem; background-color: rgba(255, 167, 38, 0.1); border-radius: 8px; margin-bottom: 1rem;'>
                <h4 style='color: var(--color-secondary); margin-bottom: 0.5rem;'>{exam['name']} ({exam['code']})</h4>
                <p style='color: var(--color-text-secondary); font-size: 0.9rem;'>{exam['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if i + 1 < len(exam_types):
            exam = exam_types[i + 1]
            st.markdown(f"""
            <div style='padding: 1rem; background-color: rgba(255, 167, 38, 0.1); border-radius: 8px; margin-bottom: 1rem;'>
                <h4 style='color: var(--color-secondary); margin-bottom: 0.5rem;'>{exam['name']} ({exam['code']})</h4>
                <p style='color: var(--color-text-secondary); font-size: 0.9rem;'>{exam['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

# 快速开始指南
st.subheader("📋 快速开始")

with st.expander("点击查看快速开始指南", expanded=False):
    st.markdown("""
    1. **配置AI平台**：在AI配置页面设置您的API密钥
    2. **选择考试类型**：根据需求选择CET-4、CET-6等考试类型
    3. **生成题目**：在题目生成页面选择题型和难度，点击生成
    4. **管理教材**：在教材管理页面查看、编辑和导出生成的题目
    5. **导出使用**：支持导出为PDF、Word等格式，直接用于教学
    
    **提示**：首次使用建议从CET-4基础题型开始尝试。
    """)

# 统计信息（模拟）
st.subheader("📊 系统统计")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="题目生成总数",
        value="1,248",
        delta="+124 本周"
    )

with col2:
    st.metric(
        label="活跃用户",
        value="89",
        delta="+12 本月"
    )

with col3:
    st.metric(
        label="平均生成时间",
        value="3.2秒",
        delta="-0.8秒 优化"
    )

# 页脚
st.divider()
st.markdown("""
<div style='text-align: center; color: var(--color-text-secondary); font-size: 0.9rem; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid var(--color-accent);'>
    <p><strong>Luminlex - 智能英语教材生成系统</strong></p>
    <p>版本: v1.0 | 最后更新: 2026年1月4日</p>
    <p>项目地址: <a href='https://github.com/HY-LiYihan/luminlex' target='_blank' style='color: var(--color-primary);'>GitHub</a></p>
</div>
""", unsafe_allow_html=True)
