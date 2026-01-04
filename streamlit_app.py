import streamlit as st

# 页面配置 - 暖色调主题
st.set_page_config(
    page_title="Luminlex - 英语题目生成器",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"  # 隐藏侧边栏
)

# 自定义CSS - 暖色调设计
st.markdown("""
<style>
    /* ==================== 暖色调颜色变量定义 ==================== */
    :root {
        /* 主色调 - 暖色系 */
        --color-primary: #FF6B35;      /* 主色：橙色，用于标题和重要元素 */
        --color-secondary: #FFA726;    /* 辅助色：浅橙色，用于次要元素 */
        --color-accent: #FFD166;       /* 强调色：金黄色，用于强调和特殊状态 */
        
        /* 背景色 - 暖色调 */
        --color-bg: #FFF8F0;           /* 主背景色：浅米色 */
        --color-bg-card: #FFFFFF;      /* 卡片背景色：白色 */
        
        /* 文字颜色 */
        --color-text: #5D4037;         /* 主文字颜色：深棕色 */
        --color-text-secondary: #8D6E63; /* 次要文字颜色：浅棕色 */
        
        /* 按钮颜色 */
        --color-button: #FF6B35;       /* 主要按钮颜色：橙色 */
        --color-button-hover: #FF8A65; /* 按钮悬停色：浅橙色 */
    }
    
    /* 页面主体背景 */
    .stApp {
        background-color: var(--color-bg) !important;
        color: var(--color-text) !important;
    }
    
    /* 主内容区域 */
    .main .block-container {
        background-color: var(--color-bg) !important;
        padding-top: 1rem;
        max-width: 800px;
    }
    
    /* 标题样式 */
    h1 {
        color: var(--color-primary) !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
        text-align: center;
        border-bottom: 3px solid var(--color-accent);
        padding-bottom: 0.5rem;
    }
    
    h2 {
        color: var(--color-secondary) !important;
        font-weight: 600 !important;
        margin-top: 1.5rem !important;
    }
    
    h3 {
        color: var(--color-accent) !important;
        font-weight: 500 !important;
    }
    
    /* 按钮样式 */
    .stButton button {
        background-color: var(--color-button) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        width: 100%;
    }
    
    .stButton button:hover {
        background-color: var(--color-button-hover) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3) !important;
    }
    
    /* 卡片样式 */
    .stCard {
        background-color: var(--color-bg-card) !important;
        border-radius: 12px !important;
        border: 2px solid var(--color-accent) !important;
        padding: 1.5rem !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 1rem;
    }
    
    /* 输入框样式 */
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] {
        background-color: white !important;
        border: 2px solid var(--color-accent) !important;
        border-radius: 8px !important;
        color: var(--color-text) !important;
    }
    
    /* 成功/警告/错误消息样式 */
    .stAlert {
        border-radius: 8px !important;
        border-left: 4px solid !important;
    }
    
    .stAlert.success {
        border-left-color: #4CAF50 !important;
        background-color: rgba(76, 175, 80, 0.1) !important;
    }
    
    .stAlert.error {
        border-left-color: #F44336 !important;
        background-color: rgba(244, 67, 54, 0.1) !important;
    }
    
    .stAlert.info {
        border-left-color: var(--color-primary) !important;
        background-color: rgba(255, 107, 53, 0.1) !important;
    }
    
    /* 分隔线 */
    hr {
        margin: 1.5rem 0 !important;
        border: none !important;
        height: 2px !important;
        background: linear-gradient(to right, transparent, var(--color-accent), transparent) !important;
    }
    
    /* 完全隐藏侧边栏 */
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* 隐藏侧边栏切换按钮 */
    .st-emotion-cache-1oe5cao {
        display: none !important;
    }
    
    /* 调整主内容区域宽度 */
    .main .block-container {
        max-width: 1000px !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# 直接导入Home页面
import pages.Home as home_page

# 运行Home页面
home_page.main()
