# ============================================================
# 极简版职业教育课程咨询助手
# 使用关键词匹配检索相关课程，无需向量数据库和 embedding 模型
# 依赖：streamlit, langchain, langchain-community, openai
# 运行：streamlit run app.py
# ============================================================

import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import re

# ----------------------------- 配置 -----------------------------
DEEPSEEK_API_KEY = ""  # 请替换为您的有效 Key
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
MODEL_NAME = "deepseek-chat"

# 课程数据
COURSES = [
    {
        "name": "Python全栈开发工程师",
        "content": """
        课程名称: Python全栈开发工程师
        课程简介: 从零基础到精通Python后端开发及前端技术，涵盖Django、Flask、Vue.js等主流框架。
        适合人群: 希望从事Web开发、全栈开发的学员，具备基本计算机操作能力即可。
        学习周期: 6个月（全日制） / 10个月（周末班）
        核心内容:
          - Python基础语法与高级编程
          - MySQL、MongoDB数据库设计
          - Django框架实战（电商项目）
          - Flask轻量级框架
          - Vue.js前端交互开发
          - Linux部署与自动化运维
        就业方向: Python后端开发工程师、全栈开发工程师、自动化运维工程师
        参考价格: 19800元（支持分期付款）
        """
    },
    {
        "name": "人工智能与大模型应用开发",
        "content": """
        课程名称: 人工智能与大模型应用开发
        课程简介: 深入讲解机器学习、深度学习及大模型（LLM）原理与微调，结合企业级项目实战。
        适合人群: 具备Python基础，对AI感兴趣的学员；希望转型AI工程师的开发者。
        学习周期: 8个月（含企业实训）
        核心内容:
          - 机器学习算法（回归、分类、聚类）
          - 深度学习框架 PyTorch / TensorFlow
          - Transformer与BERT模型详解
          - 大模型（DeepSeek、Qwen）微调与部署
          - RAG检索增强生成、Agent开发
          - 实际项目：智能客服、文档问答系统
        就业方向: AI算法工程师、大模型应用开发工程师、数据科学家
        参考价格: 25800元（赠送GPU算力资源）
        """
    },
    {
        "name": "大数据分析与数据可视化",
        "content": """
        课程名称: 大数据分析与数据可视化
        课程简介: 培养大数据处理、分析与可视化能力，掌握Hadoop、Spark生态及BI工具。
        适合人群: 对数据敏感，希望从事数据分析、数据仓库方向的学员。
        学习周期: 5个月
        核心内容:
          - SQL高级查询与数据仓库建模
          - Python数据分析（Pandas、NumPy）
          - Hadoop + Hive离线处理
          - Spark Streaming实时计算
          - Tableau / Power BI 可视化仪表盘
          - 真实电商数据项目实战
        就业方向: 数据分析师、大数据开发工程师、BI工程师
        参考价格: 16800元（含认证考试辅导）
        """
    },
    {
        "name": "UI/UX全链路设计",
        "content": """
        课程名称: UI/UX全链路设计
        课程简介: 从用户研究到交互设计，再到高保真原型制作，培养全链路设计能力。
        适合人群: 对设计有热情，零基础可学，需要具备审美和创意思维。
        学习周期: 4个月
        核心内容:
          - 设计基础与色彩构成
          - Figma / Sketch 原型设计
          - 用户画像与体验地图
          - 动效设计（After Effects）
          - 作品集打造与面试辅导
        就业方向: UI设计师、UX设计师、产品经理助理
        参考价格: 12800元（赠送设计素材库会员）
        """
    },
    {
        "name": "嵌入式系统与物联网开发",
        "content": """
        课程名称: 嵌入式系统与物联网开发
        课程简介: 基于STM32、树莓派，学习嵌入式底层驱动及物联网云平台对接。
        适合人群: 电子、计算机相关专业学生，或有C语言基础。
        学习周期: 6个月
        核心内容:
          - C/C++编程与数据结构
          - 单片机原理与接口技术
          - RTOS实时操作系统
          - 物联网通信协议（MQTT、CoAP）
          - 阿里云IoT平台接入
          - 智能家居综合项目
        就业方向: 嵌入式软件工程师、物联网开发工程师
        参考价格: 18800元（提供硬件开发板）
        """
    }
]


def simple_retrieve(query):
    """
    简单关键词检索：计算问题中包含课程关键词的匹配分数，返回最相关的课程内容
    """
    # 预处理：提取问题中的关键词（这里简化为去除停用词）
    keywords = set(re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]+', query))
    # 停用词列表（简单示例）
    stopwords = {'的', '了', '是', '吗', '呢', '啊', '吧', '什么', '怎么', '如何', '哪个', '哪些', '有', '在', '和',
                 '与', '或', '及', '对', '从', '到', '给', '让', '为', '等', '之类', '之类', '什么', '哪里', '多少',
                 '多久', '价格', '费用', '学费', '学习', '课程', '适合', '就业', '方向', '内容', '周期', '时间', '班',
                 '班型', '模式', '形式', '上课', '学习方式'}
    keywords = [k for k in keywords if k not in stopwords and len(k) > 1]

    best_score = 0
    best_course = None
    for course in COURSES:
        text = course["name"] + " " + course["content"]
        score = sum(text.count(kw) for kw in keywords)
        if score > best_score:
            best_score = score
            best_course = course
    # 如果没匹配到，返回第一个课程
    if best_course is None:
        best_course = COURSES[0]
    return best_course


# ----------------------------- Streamlit 界面 -----------------------------
def main():
    st.set_page_config(page_title="清美教育课程咨询助手", page_icon="🤖")
    st.title("📚 清美教育 · 职业教育课程咨询助手")
    st.markdown("基于 **DeepSeek 大模型** + **简易检索**，为您解答课程相关问题。")
    st.markdown("---")

    # 初始化对话历史
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 显示历史消息
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 用户输入
    if prompt := st.chat_input("例如：Python全栈课程适合零基础吗？学费是多少？"):
        # 添加用户消息
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 检索最相关的课程
        with st.chat_message("assistant"):
            with st.spinner("正在检索课程信息..."):
                relevant_course = simple_retrieve(prompt)
                # 将课程内容作为上下文
                context = relevant_course["content"]

                # 构造 Prompt
                template = """你是一个专业的职业教育课程咨询助手。请严格根据以下提供的课程信息来回答用户的问题。
如果信息不足以回答问题，请说明“根据现有课程资料，暂时无法准确回答，建议咨询人工老师获取更详细信息”。
不要编造课程内容、价格或学习周期等细节。

相关课程信息：
{context}

用户问题：{question}
助手的回答（亲切、专业）："""

                prompt_template = PromptTemplate(
                    template=template,
                    input_variables=["context", "question"]
                )

                # 初始化 LLM
                llm = ChatOpenAI(
                    model=MODEL_NAME,
                    openai_api_key=DEEPSEEK_API_KEY,
                    openai_api_base=DEEPSEEK_BASE_URL,
                    temperature=0.3,
                    max_tokens=1024,
                    request_timeout=60
                )

                chain = LLMChain(llm=llm, prompt=prompt_template)

                try:
                    answer = chain.run(context=context, question=prompt)
                except Exception as e:
                    answer = f"调用AI服务时出现错误: {str(e)}。请检查API Key是否正确或网络连接。"
                    st.error(answer)

            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

    # 侧边栏
    with st.sidebar:
        st.header("📌 关于本助手")
        st.markdown("本版本使用**关键词匹配**检索课程，无需向量数据库，可快速运行。")
        st.markdown("生产环境可替换为向量检索（如 Chroma + Embedding）提升准确性。")
        st.markdown("---")
        st.header("💡 示例问题")
        st.markdown("- Python全栈课程适合零基础吗？")
        st.markdown("- 人工智能课程学费多少？")
        st.markdown("- UI设计课程学多久？")
        st.markdown("- 大数据分析就业方向有哪些？")
        if st.button("清空对话历史"):
            st.session_state.messages = []
            st.rerun()


if __name__ == "__main__":
    main()