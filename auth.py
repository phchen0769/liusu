import streamlit as st
import streamlit_authenticator as stauth

import index
from db_operator import out_sql


# 初始化 站点显示参数
st.set_page_config(
    page_title="学生留宿管理系统",
    page_icon="🇨🇳",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None,
)

# 创建空的字典
credentials = {"usernames": {}}

# 从数据库读取用户信息
user_df = out_sql("users").values

for user in user_df:
    user_dict = dict(
        {
            user[1]: {
                "password": user[2],
                "name": user[3],
                "email": user[4],
            }
        }
    )
    credentials["usernames"].update(user_dict)


# 把密码转换成hash密码
# hashed_passwords = stauth.Hasher(["123"]).generate()

# print(hashed_passwords)


# cookie信息
cookie = {
    "expiry_days": 30,
    "key": "Fedorov is handsome man.",  # 必须是字符串
    "name": "liusu_cookie",
    "preauthorized": {"emails": "phchen0769@gmail.com"},
}

# 实例化authenticator对象
authenticator = stauth.Authenticate(
    credentials,
    cookie["name"],
    cookie["key"],
    cookie["expiry_days"],
    # 用于注册检查
    cookie["preauthorized"],
)

# 生成登录框
name, authentication_status, username = authenticator.login("登录", "main")

# 登录页面的注册按钮和重置密码按钮
# if st.session_state["authentication_status"] is None:
# btn1, btn2 = st.columns(2)
# with btn1:
#     if st.button("注册"):
#         # 注册按钮
#         try:
#             if authenticator.register_user("注册", preauthorization=False):
#                 st.success("用户注册成功。")
#         except Exception as e:
#             st.error(e)

# with btn2:
#     if st.button("忘记密码"):
#         with st.container():
#             # 忘记密码
#             try:
#                 (
#                     username_forgot_pw,
#                     email_forgot_password,
#                     random_password,
#                 ) = authenticator.forgot_password("忘记密码")
#                 if username_forgot_pw:
#                     st.success("密码已发送邮箱。")
#                 # Random password to be transferred to user securely
#                 else:
#                     st.error("Username not found")
#             except Exception as e:
#                 st.error(e)

# 跨页面使用校验状态
if st.session_state["authentication_status"]:
    with st.container():
        #  重置密码、更新个人信息、退出
        # cols1, cols2, cols3, cols4 = st.columns(4)
        # cols1.markdown(f"欢迎{st.session_state['name']}")

        # # 重置密码按钮
        # with cols2.container():
        #     if st.button("重置密码"):
        #         # 重置密码
        #         try:
        #             if authenticator.reset_password(username, "重置密码"):
        #                 st.success("密码重置成功！")
        #         except Exception as e:
        #             st.error(e)

        # with cols3.container():
        #     if st.button("更新个人信息"):
        #         # 更新用户详细信息
        #         try:
        #             if authenticator.update_user_details(username, "更新个人信息"):
        #                 st.success("个人信息更新成功。")
        #         except Exception as e:
        #             st.error(e)

        # # 退出按钮
        # with cols4.container():
        #     # 退出登录
        #     authenticator.logout("退出", "main", key="unique_key")

        cols1, cols2 = st.columns(2)
        cols1.markdown(f"欢迎{st.session_state['name']}")

        # 退出按钮
        with cols2.container():
            # 退出登录
            authenticator.logout("退出", "main", key="unique_key")

    index.main()  # 进入业务应用
elif st.session_state["authentication_status"] is False:
    st.error("用户名或密码错误！")
elif st.session_state["authentication_status"] is None:
    st.warning("请输入你的用户名和密码。")
