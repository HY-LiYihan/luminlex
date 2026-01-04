import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Any
import api_utils
import streamlit as st

class QuestionGenerator:
    """题目生成器核心类"""
    
    def __init__(self):
        self.question_types = {
            "listening": {
                "name": "听力",
                "subtypes": ["short_conversation", "long_conversation", "passage", "news"]
            },
            "reading": {
                "name": "阅读",
                "subtypes": ["cloze", "matching", "multiple_choice", "true_false"]
            },
            "writing": {
                "name": "写作",
                "subtypes": ["argumentative", "descriptive", "narrative", "letter"]
            },
            "translation": {
                "name": "翻译",
                "subtypes": ["chinese_to_english", "english_to_chinese"]
            }
        }
        
        self.difficulty_levels = {
            "easy": {"name": "简单", "description": "适合初学者"},
            "medium": {"name": "中等", "description": "适合有一定基础的学习者"},
            "hard": {"name": "困难", "description": "适合高级学习者或考试准备"}
        }
        
        self.exam_types = {
            "cet4": {"name": "大学英语四级", "level": "medium"},
            "cet6": {"name": "大学英语六级", "level": "hard"},
            "tem4": {"name": "专业英语四级", "level": "medium"},
            "tem8": {"name": "专业英语八级", "level": "hard"},
            "ielts": {"name": "雅思", "level": "hard"},
            "toefl": {"name": "托福", "level": "hard"}
        }
        
        # 初始化可用AI平台
        self.available_platforms = {}
        self._init_ai_platforms()
    
    def _init_ai_platforms(self):
        """初始化可用的AI平台"""
        try:
            self.available_platforms = api_utils.probe_available_platforms()
        except Exception as e:
            print(f"初始化AI平台失败: {e}")
            self.available_platforms = {}
    
    def generate_question(self, 
                         exam_type: str,
                         question_type: str,
                         subtype: str,
                         difficulty: str,
                         topic: Optional[str] = None,
                         word_count: Optional[int] = None) -> Dict[str, Any]:
        """生成单个题目"""
        
        # 构建提示词
        prompt = self._build_prompt(exam_type, question_type, subtype, difficulty, topic, word_count)
        
        # 尝试使用AI API生成题目
        ai_result = self._generate_with_ai(prompt)
        
        if ai_result:
            return ai_result
        else:
            # 如果AI生成失败，返回模拟数据
            return self._generate_mock_question(exam_type, question_type, subtype, difficulty, topic)
    
    def _build_prompt(self,
                     exam_type: str,
                     question_type: str,
                     subtype: str,
                     difficulty: str,
                     topic: Optional[str],
                     word_count: Optional[int]) -> str:
        """构建AI提示词"""
        
        exam_name = self.exam_types.get(exam_type, {}).get("name", exam_type)
        qtype_name = self.question_types.get(question_type, {}).get("name", question_type)
        diff_name = self.difficulty_levels.get(difficulty, {}).get("name", difficulty)
        
        prompt = f"""请生成一道{exam_name}的{qtype_name}题目。

具体要求：
1. 题目类型：{subtype}
2. 难度级别：{diff_name}
3. 考试类型：{exam_name}
"""
        
        if topic:
            prompt += f"4. 主题：{topic}\n"
        
        if word_count:
            prompt += f"5. 字数要求：约{word_count}词\n"
        
        prompt += """
请以JSON格式返回，包含以下字段：
- question: 题目内容
- options: 选项列表（如果是选择题）
- answer: 正确答案
- explanation: 答案解析
- difficulty: 难度级别
- estimated_time: 预计完成时间（分钟）
"""
        
        return prompt
    
    def _generate_with_ai(self, prompt: str) -> Optional[Dict[str, Any]]:
        """使用AI API生成题目"""
        
        if not self.available_platforms:
            return None
        
        # 选择第一个可用的平台
        platform_id = list(self.available_platforms.keys())[0]
        platform_info = self.available_platforms[platform_id]
        
        try:
            # 构建消息
            messages = [
                {"role": "system", "content": "你是一个专业的英语教育专家，擅长生成各种英语考试题目。请严格按照要求的JSON格式返回题目。"},
                {"role": "user", "content": prompt}
            ]
            
            # 调用AI API
            response_text = api_utils.get_chat_response(
                platform=platform_id,
                api_key=platform_info["api_key"],
                model=platform_info["default_model"],
                messages=messages,
                temperature=0.3
            )
            
            # 尝试解析JSON响应
            try:
                # 提取JSON部分（AI可能会在回答中添加额外文本）
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    result = json.loads(json_str)
                    
                    # 验证必要字段
                    required_fields = ["question", "answer", "explanation", "difficulty", "estimated_time"]
                    if all(field in result for field in required_fields):
                        # 添加AI生成标记
                        result["generated_by_ai"] = True
                        result["ai_platform"] = platform_info["name"]
                        return result
                    else:
                        print(f"AI响应缺少必要字段: {result}")
                        return None
                else:
                    print(f"无法从AI响应中提取JSON: {response_text[:200]}...")
                    return None
                    
            except json.JSONDecodeError as e:
                print(f"解析AI响应JSON失败: {e}")
                print(f"响应内容: {response_text[:200]}...")
                return None
                
        except Exception as e:
            print(f"AI生成题目失败: {e}")
            return None
    
    def _generate_mock_question(self,
                              exam_type: str,
                              question_type: str,
                              subtype: str,
                              difficulty: str,
                              topic: Optional[str]) -> Dict[str, Any]:
        """生成模拟题目（用于测试）"""
        
        # 根据题目类型生成不同的模拟数据
        if question_type == "listening":
            return self._mock_listening_question(subtype, difficulty, topic)
        elif question_type == "reading":
            return self._mock_reading_question(subtype, difficulty, topic)
        elif question_type == "writing":
            return self._mock_writing_question(subtype, difficulty, topic)
        elif question_type == "translation":
            return self._mock_translation_question(subtype, difficulty, topic)
        else:
            return self._mock_general_question(question_type, subtype, difficulty, topic)
    
    def _mock_listening_question(self, subtype: str, difficulty: str, topic: Optional[str]) -> Dict[str, Any]:
        """模拟听力题目"""
        topics = ["校园生活", "工作面试", "旅游咨询", "学术讲座", "新闻播报"]
        selected_topic = topic or random.choice(topics)
        
        questions = [
            {
                "question": f"听一段关于{selected_topic}的对话，回答以下问题：对话中男士的主要观点是什么？",
                "options": ["A. 支持该计划", "B. 反对该计划", "C. 持中立态度", "D. 未明确表态"],
                "answer": "B",
                "explanation": "在对话的后半部分，男士明确表达了对该计划的担忧和反对意见。",
                "difficulty": difficulty,
                "estimated_time": 2
            },
            {
                "question": f"听一段关于{selected_topic}的短文，回答以下问题：文章的主要目的是什么？",
                "options": ["A. 介绍新产品", "B. 解释某个现象", "C. 提出建议", "D. 讲述个人经历"],
                "answer": "C",
                "explanation": "文章开头就表明了提出建议的目的，并在后续内容中详细阐述了具体建议。",
                "difficulty": difficulty,
                "estimated_time": 3
            }
        ]
        
        return random.choice(questions)
    
    def _mock_reading_question(self, subtype: str, difficulty: str, topic: Optional[str]) -> Dict[str, Any]:
        """模拟阅读题目"""
        topics = ["环境保护", "科技发展", "教育政策", "健康生活", "文化交流"]
        selected_topic = topic or random.choice(topics)
        
        questions = [
            {
                "question": f"阅读以下关于{selected_topic}的文章，选择最合适的标题：\n\n近年来，{selected_topic}越来越受到人们的关注。研究表明...",
                "options": [
                    "A. 新时代的挑战",
                    "B. 当前趋势分析", 
                    "C. 历史回顾",
                    "D. 未来展望"
                ],
                "answer": "B",
                "explanation": "文章主要分析了当前的发展趋势和现状，因此B选项最合适。",
                "difficulty": difficulty,
                "estimated_time": 3
            },
            {
                "question": f"阅读以下段落，选择可以填入空白处的最佳选项：\n\n{selected_topic}是一个复杂的问题，____需要多方合作才能解决。",
                "options": ["A. 因此", "B. 但是", "C. 然而", "D. 尽管"],
                "answer": "A",
                "explanation": "前后句是因果关系，'因此'最符合语境。",
                "difficulty": difficulty,
                "estimated_time": 2
            }
        ]
        
        return random.choice(questions)
    
    def _mock_writing_question(self, subtype: str, difficulty: str, topic: Optional[str]) -> Dict[str, Any]:
        """模拟写作题目"""
        topics = ["远程工作的利弊", "人工智能的影响", "环境保护责任", "文化多样性", "教育改革"]
        selected_topic = topic or random.choice(topics)
        
        word_requirements = {
            "easy": "120-150词",
            "medium": "150-180词", 
            "hard": "180-220词"
        }
        
        return {
            "question": f"请以'{selected_topic}'为题，写一篇议论文。\n要求：{word_requirements.get(difficulty, '150-180词')}，观点明确，论据充分。",
            "options": None,
            "answer": "这是一道写作题，需要学生自己完成作文。",
            "explanation": f"写作要点：1. 明确表达自己的观点；2. 提供2-3个支持论据；3. 适当使用连接词使文章连贯；4. 注意语法和拼写。",
            "difficulty": difficulty,
            "estimated_time": 30
        }
    
    def _mock_translation_question(self, subtype: str, difficulty: str, topic: Optional[str]) -> Dict[str, Any]:
        """模拟翻译题目"""
        if subtype == "chinese_to_english":
            sentences = [
                "随着科技的快速发展，人们的生活方式发生了巨大变化。",
                "环境保护是当今世界面临的最紧迫问题之一。",
                "文化交流有助于增进不同国家之间的理解和友谊。"
            ]
            selected_sentence = random.choice(sentences)
            
            return {
                "question": f"请将以下中文句子翻译成英文：\n\n{selected_sentence}",
                "options": None,
                "answer": "参考翻译：With the rapid development of technology, people's lifestyles have undergone tremendous changes.",
                "explanation": "翻译要点：注意时态一致，'快速发展'译为'rapid development'，'发生了巨大变化'译为'have undergone tremendous changes'。",
                "difficulty": difficulty,
                "estimated_time": 5
            }
        else:  # english_to_chinese
            sentences = [
                "Artificial intelligence is transforming various industries and changing the way we work.",
                "Sustainable development requires balancing economic growth with environmental protection.",
                "Learning a foreign language not only improves communication skills but also broadens one's horizons."
            ]
            selected_sentence = random.choice(sentences)
            
            return {
                "question": f"请将以下英文句子翻译成中文：\n\n{selected_sentence}",
                "options": None,
                "answer": "参考翻译：人工智能正在改变各个行业，并改变我们的工作方式。",
                "explanation": "翻译要点：注意专业术语的准确翻译，'transforming various industries'译为'改变各个行业'。",
                "difficulty": difficulty,
                "estimated_time": 5
            }
    
    def _mock_general_question(self, question_type: str, subtype: str, difficulty: str, topic: Optional[str]) -> Dict[str, Any]:
        """模拟通用题目"""
        return {
            "question": f"这是一道{question_type}类型的{subtype}题目，难度为{difficulty}。",
            "options": ["选项A", "选项B", "选项C", "选项D"],
            "answer": "选项B",
            "explanation": "这是答案解析，说明为什么选择这个答案。",
            "difficulty": difficulty,
            "estimated_time": 5
        }
    
    def generate_question_set(self,
                            exam_type: str,
                            question_types: List[str],
                            count_per_type: int = 5,
                            difficulty: str = "medium",
                            topic: Optional[str] = None) -> Dict[str, Any]:
        """生成一套题目集"""
        
        question_set = {
            "exam_type": exam_type,
            "difficulty": difficulty,
            "topic": topic,
            "generated_at": datetime.now().isoformat(),
            "questions": [],
            "summary": {}
        }
        
        total_questions = 0
        total_time = 0
        
        for qtype in question_types:
            for i in range(count_per_type):
                question = self.generate_question(
                    exam_type=exam_type,
                    question_type=qtype,
                    subtype=self.question_types.get(qtype, {}).get("subtypes", [""])[0],
                    difficulty=difficulty,
                    topic=topic
                )
                
                question["id"] = f"{qtype}_{i+1}"
                question["type"] = qtype
                question_set["questions"].append(question)
                
                total_questions += 1
                total_time += question.get("estimated_time", 5)
        
        # 生成摘要
        question_set["summary"] = {
            "total_questions": total_questions,
            "total_estimated_time": total_time,
            "question_types": question_types,
            "average_difficulty": difficulty
        }
        
        return question_set
    
    def save_question_set(self, question_set: Dict[str, Any], filename: Optional[str] = None) -> str:
        """保存题目集到文件"""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            exam_type = question_set.get("exam_type", "unknown")
            filename = f"data/question_set_{exam_type}_{timestamp}.json"
        
        # 确保目录存在
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(question_set, f, ensure_ascii=False, indent=2)
        
        return filename


# 单例实例
question_generator = QuestionGenerator()
