# 这里写的是：Python代码->通过Streamlit，绘制Web界面

import streamlit as st
from langchain.memory import ConversationBufferMemory  # 会话记忆体
from utils import get_response


# 1. 设置左侧的菜单栏
with st.sidebar:
    # 让用户录入他的API KEY
    api_key = st.text_input('请输入Tongyi账号的API KEY：', type='password')
    # 设置链接提示，用户点击后，会跳转到：获取API KEY的页面
    st.markdown('[获取Tongyi账号的API KEY](https://cnn.com)', unsafe_allow_html=True)

# 2. 设置页面标题
st.title('通义聊天机器人')

# 3. 创建会话记忆体，即：会话保持记录，记录：聊天记录
if 'memory' not in st.session_state:
    st.session_state['memory'] = ConversationBufferMemory()
    st.session_state['message'] = [{'role': 'ai', 'content': '您好，我是你的AI助手，有什么可以帮助你的吗？'}, {'role': 'human', 'content': '你好，我有问题'}]

# 4. 创建消息区，即：遍历会话记忆体中的所有聊天记录，并打印到消息区
for message in st.session_state['message']:
    # message的数据格式：{'role': 'ai', 'content': '您好，我是你的AI助手，有什么可以帮助你的吗？'}
    with st.chat_message(message['role']):  # 设置角色，即：显示消息来源
        st.write(message['content'])  # 显示消息内容





# 5. 创建文本框，接收用户录入的问题
prompt = st.chat_input('请录入您的问题：')

# 6. 判断如果用户录入的内容不为空，就显示到：页面（消息区）
if prompt:
    # 7. 判断用户是否已经录入了API KEY，如果没有录入，则提示用户录入
    if not api_key:
        st.warning('请先录入API KEY!')
        st.stop()

    # 8. 走到这里，说明：1.用户录入了数据；2.用户录入了具体的问题
    # 把用户录入的信息，添加到：会话记忆体中
    st.session_state['message'].append({'role': 'human', 'content': 'prompt'})
    # 把用户录入的信息，打印到：主窗体中
    st.chat_message('human').markdown(prompt)

    # 9. 调用自定义函数，获取ai回复的结果
    # 细节：加入等待提示。
    with st.spinner('AI正在思考中'):
        content = get_response(prompt, st.session_state['memory'], api_key)

    # 10. 把ai回复的消息添加到记忆体中，并添加到消息区中
    st.session_state['message'].append({'role': 'ai', 'content': content})
    st.chat_message('ai').markdown(content)