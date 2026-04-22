这是一个demo# 教育人工智能"

> 基于 DeepSeek 大模型 + 智能检索的职业教育课程咨询机器人  
> **零向量数据库，关键词匹配，轻量级快速部署**

---


##✨ 项目亮点

- 🧠 **大模型驱动**：使用 DeepSeek 大语言模型理解用户问题，生成自然、专业的回答。
- 🔍 **智能检索**：采用关键词匹配算法，从课程库中快速定位最相关的课程信息。
- 🚀 **轻量级**：无需安装向量数据库或 Embedding 模型，依赖简单，运行成本极低。
- 💬 **友好交互** **：基于 Streamlit 构建聊天界面，支持对话历史，开箱即用。

---


## 📚 功能简介

- 回答关于**职业教育课程**的常见问题（适合人群、学习周期、核心内容、就业方向、价格等）。
- 支持多轮对话，自动检索最匹配的课程作为上下文。
- 侧边栏提供示例问题，一键清空对话历史。

---


##🛠️ 技术栈

| 类别       | 技术                              |
| ---------- | --------------------------------- |
| 前端交互   | Streamlit                         |
| 大模型     | DeepSeek API（兼容 OpenAI 接口）  |
| 检索方式   | 关键词匹配（TF-IDF 思想简化版）   |
| 开发语言   | Python 3.8+                       |

---


## 📦 安装与运行

### 1. 克隆仓库

```bash
git clone https://github.com/Myth-wangyun/edu-ai.git
cd 教育人工智能
2. 创建虚拟环境（推荐）
巴什
python -m venv venv
# 窗户
venv\Scripts\激活
# Mac/Linux
源 venv/bin/activate
3. 安装依赖
巴什
pip install -r requirements.txt
4. 配置 API Key
本项目使用 DeepSeek 大模型，你需要先在 DeepSeek 开放平台 注册并获取 API Key。

在项目根目录创建 .env 文件，填入：

环境
DEEPSEEK_API_KEY=你的API密钥
⚠️ 请勿将 .env 文件提交到 GitHub（已加入 .gitignore）。

5. 启动应用
巴什
streamlit run app.py
浏览器会自动打开 http://localhost:8501，开始咨询吧！

🧪 示例问题
“Python全栈课程适合零基础吗？”

“人工智能课程学费多少？”

“UI设计课程学多久？”

“大数据分析就业方向有哪些？”

📁 项目结构
text
.
├── app.py                  # 主程序
├── requirements.txt        # Python依赖
├── course_knowledge.txt    # 课程知识库（备用，当前直接内置于app.py）
├── .env                    # 环境变量（不提交）
├── .gitignore              # Git忽略规则
└── README.md               # 项目说明
📌 注意事项
API Key 安全：请勿将真实 Key 上传到公开仓库，已通过 .gitignore 忽略 .env。

检索方式：当前使用关键词匹配，适合小型课程库。如需大规模检索，建议替换为向量数据库（如 Chroma + Embedding）。

网络要求：需要能够正常访问 DeepSeek API 服务。

🤝 贡献与反馈
欢迎提交 Issue 或 Pull Request。如有任何问题，可通过 GitHub 联系作者。

📄 许可证
MIT License © 2025 Myth-wangyun

🌟 最后
如果这个项目对你有帮助，欢迎点亮 ⭐️ Star 支持一下～

text

---

## 🚀 如何更新到 GitHub

在项目目录 `D:\career-edu-assistant` 下打开终端，执行：

```bash
git add README.md
git commit -m "docs: 美化README，添加详细项目说明"
git push
