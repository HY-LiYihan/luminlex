import streamlit as st
import json
import random
from datetime import datetime

def main():
    """主函数"""
    
    # 页面标题
    st.title("📚 Luminlex - 英语题目生成器")
    
    # 简单介绍
    st.markdown("""
    <div style='background-color: rgba(255, 214, 102, 0.1); padding: 1rem; border-radius: 12px; border-left: 4px solid #FFD166; margin-bottom: 1.5rem;'>
    <p style='color: #5D4037; line-height: 1.5; margin: 0;'>
        一个简单的英语题目生成工具，点击按钮即可生成四六级等英语考试题目。
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 初始化session state
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
    if "question_history" not in st.session_state:
        st.session_state.question_history = []
    
    # 创建两列布局
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # 题目生成选项
        st.subheader("🎯 生成选项")
        
        # 考试类型
        exam_type = st.selectbox(
            "选择考试类型",
            options=["CET-4", "CET-6", "TEM-4", "TEM-8", "IELTS", "TOEFL"],
            index=0,
            help="选择要生成的考试类型"
        )
        
        # 题目类型
        question_type = st.selectbox(
            "选择题目类型",
            options=["听力", "阅读", "写作", "翻译"],
            index=1,
            help="选择题目类型"
        )
        
        # 难度
        difficulty = st.selectbox(
            "选择难度",
            options=["简单", "中等", "困难"],
            index=1,
            help="选择题目难度"
        )
        
        # 主题（可选）
        topic = st.text_input(
            "主题（可选）",
            placeholder="例如：环境保护、科技、教育等",
            help="指定题目主题，留空则随机生成"
        )
        
        # 生成按钮
        generate_btn = st.button(
            "✨ 生成题目",
            type="primary",
            use_container_width=True
        )
    
    with col2:
        # 题目展示区域
        st.subheader("📝 生成的题目")
        
        if generate_btn:
            with st.spinner("正在生成题目..."):
                # 生成模拟题目
                question = generate_mock_question(exam_type, question_type, difficulty, topic)
                
                # 保存到session state
                st.session_state.current_question = question
                st.session_state.question_history.append({
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "exam_type": exam_type,
                    "question_type": question_type,
                    "question": question
                })
                
                st.success("题目生成成功！")
        
        # 显示当前题目
        if st.session_state.current_question:
            question = st.session_state.current_question
            
            # 题目卡片
            st.markdown(f"""
            <div style='background-color: white; padding: 1.5rem; border-radius: 12px; border: 2px solid #FFD166; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);'>
                <h3 style='color: #FF6B35; margin-top: 0;'>题目内容</h3>
                <p style='color: #5D4037; line-height: 1.6;'>{question['content']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 如果有选项，显示选项
            if question.get('options'):
                st.markdown("**选项：**")
                for option in question['options']:
                    st.markdown(f"- {option}")
            
            # 答案和解析
            col_a, col_b = st.columns(2)
            
            with col_a:
                with st.expander("查看答案", expanded=False):
                    st.markdown(f"**正确答案：**\n\n{question['answer']}")
            
            with col_b:
                with st.expander("查看解析", expanded=False):
                    st.markdown(f"**解析：**\n\n{question['explanation']}")
            
            # 题目信息
            st.markdown(f"""
            **考试类型**：{question['exam_type']}  
            **题目类型**：{question['question_type']}  
            **难度**：{question['difficulty']}  
            **生成时间**：{question['generated_at']}
            """)
            
            # 操作按钮
            st.divider()
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔄 重新生成", use_container_width=True):
                    st.session_state.current_question = None
                    st.rerun()
            
            with col2:
                # 下载JSON
                json_data = json.dumps(question, ensure_ascii=False, indent=2)
                st.download_button(
                    label="📥 下载题目",
                    data=json_data,
                    file_name=f"question_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
        else:
            st.info("👈 请在左侧选择选项并点击'生成题目'按钮")
    
    # 历史记录
    if st.session_state.question_history:
        st.divider()
        st.subheader("📜 生成历史")
        
        # 只显示最近5条记录
        for i, record in enumerate(st.session_state.question_history[-5:]):
            with st.expander(f"{record['timestamp']} - {record['exam_type']} {record['question_type']}", expanded=False):
                st.markdown(f"**考试类型**：{record['exam_type']}")
                st.markdown(f"**题目类型**：{record['question_type']}")
                st.markdown(f"**题目内容**：{record['question']['content'][:100]}...")
                
                if st.button(f"重新加载此题", key=f"reload_{i}"):
                    st.session_state.current_question = record['question']
                    st.rerun()
    
    # 页脚
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #8D6E63; font-size: 0.9rem; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #FFD166;'>
        <p><strong>Luminlex - 简单英语题目生成器</strong></p>
        <p>版本: v1.0 | 最后更新: 2026年1月4日</p>
    </div>
    """, unsafe_allow_html=True)

def generate_mock_question(exam_type, question_type, difficulty, topic=None):
    """生成模拟题目"""
    
    # 如果没有指定主题，使用随机主题
    if not topic:
        topics = ["环境保护", "科技发展", "教育政策", "健康生活", "文化交流", "经济发展", "社会问题", "人工智能"]
        topic = random.choice(topics)
    
    # 根据题目类型生成不同的题目
    if question_type == "听力":
        questions = [
            f"听一段关于{topic}的对话，回答以下问题：对话中女士的主要观点是什么？",
            f"听一段关于{topic}的短文，回答以下问题：文章的主要目的是什么？",
            f"听一段关于{topic}的新闻，回答以下问题：新闻中提到的主要数据是什么？"
        ]
        content = random.choice(questions)
        options = ["A. 支持该计划", "B. 反对该计划", "C. 持中立态度", "D. 未明确表态"]
        answer = random.choice(["A", "B", "C"])
        explanation = "根据对话/短文/新闻的内容分析，可以得出此答案。"
    
    elif question_type == "阅读":
        questions = [
            f"阅读以下关于{topic}的文章，选择最合适的标题。",
            f"阅读以下段落，选择可以填入空白处的最佳选项。",
            f"阅读以下文章，回答后面的问题。"
        ]
        content = random.choice(questions)
        options = ["A. 新时代的挑战", "B. 当前趋势分析", "C. 历史回顾", "D. 未来展望"]
        answer = random.choice(["A", "B", "C", "D"])
        explanation = "根据文章内容和上下文分析，可以得出此答案。"
    
    elif question_type == "写作":
        content = f"请以'{topic}'为题，写一篇议论文。\n要求：观点明确，论据充分，字数150-180词。"
        options = None
        answer = "这是一道写作题，需要学生自己完成作文。"
        explanation = f"写作要点：1. 明确表达自己的观点；2. 提供2-3个支持论据；3. 适当使用连接词使文章连贯；4. 注意语法和拼写。"
    
    else:  # 翻译
        if random.choice([True, False]):
            sentences = [
                "随着科技的快速发展，人们的生活方式发生了巨大变化。",
                "环境保护是当今世界面临的最紧迫问题之一。",
                "文化交流有助于增进不同国家之间的理解和友谊。"
            ]
            content = f"请将以下中文句子翻译成英文：\n\n{random.choice(sentences)}"
            answer = "参考翻译：With the rapid development of technology, people's lifestyles have undergone tremendous changes."
        else:
            sentences = [
                "Artificial intelligence is transforming various industries and changing the way we work.",
                "Sustainable development requires balancing economic growth with environmental protection.",
                "Learning a foreign language not only improves communication skills but also broadens one's horizons."
            ]
            content = f"请将以下英文句子翻译成中文：\n\n{random.choice(sentences)}"
            answer = "参考翻译：人工智能正在改变各个行业，并改变我们的工作方式。"
        
        options = None
        explanation = "翻译要点：注意时态一致，专业术语准确翻译，保持原文意思不变。"
    
    return {
        "content": content,
        "options": options,
        "answer": answer,
        "explanation": explanation,
        "exam_type": exam_type,
        "question_type": question_type,
        "difficulty": difficulty,
        "topic": topic,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

if __name__ == "__main__":
    main()
