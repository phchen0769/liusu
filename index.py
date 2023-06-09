import os

import base64
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder

from db_operator import out_sql
from body_create import createBody
from url_send import get_token, info_send


# 初始化 站点显示参数
st.set_page_config(
    page_title="学生留宿管理系统",
    page_icon="🇨🇳",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None,
)


# 显示侧边栏
def show_sidebar(stu_info_df, sys_info_df):
    # 标题
    st.sidebar.markdown("# 学生留宿管理系统")

    # 导出当前数据
    # @st.cache_data
    # def convert_df(df):
    #     return df.to_csv().encode("utf-8")

    # csv = convert_df(stu_info_df)
    # st.sidebar.download_button(
    #     label="导出数据为excel",
    #     data=csv,
    #     file_name="学生信息.csv",
    #     mime="text/csv",
    # )
    st.sidebar.markdown("***")

    # 创建一个提交表单
    with st.sidebar.form("sys_info_form"):
        # 创建者ID
        creater = st.sidebar.text_input(label="创建者ID", value=sys_info_df.values[0][0])

        # 所属部门
        department = st.sidebar.selectbox(
            label="所属部门", options=("信息技术系", "机电技术系", "财经商贸系", "公共基础部")
        )

        # 班级
        class_name = st.sidebar.text_input(label="班级", value=sys_info_df.values[0][2])

        # 第几周
        week = st.sidebar.number_input(
            label="第几周(填写数字)", value=10, min_value=1, max_value=25
        )

        # 申请原因
        reason = st.sidebar.text_input("申请原因（可为空）")

        # 变更情况
        option = st.sidebar.selectbox(
            label="变更情况", options=("申请临时留宿", "申请临时不留宿", "申请长期留宿", "申请取消长期留宿")
        )

        # 表单提交
        if st.form_submit_button("提交"):
            # 生成access_token
            access_token = get_token()
            # access_token = "PwUOUcUozgN2cPAZNPEYZBN1F9kZ9nkZf9WVy3-wB7zNwb1tZNt7sYZELie71Qy_zPwYHqDfjjXt6kiZutnJcj7aYmhNc5iY8I5JC3fOKNw030VZfkgeBPje1qoRnvwxgXd2rWi2bVCWxqROLzneMmUGdi4Z3mMkWvdHuXk7Y_eExiinej96DkivplHqoFckoacBf5AMiDaCiXlf7Rceog"

            # 构建待发送消息的主体
            body_json = build_body.createBody("./students_info.xlsx")

            # 发送请求
            info_send(access_token, body_json)


# 显示content内容
def show_content(stu_info_df):
    # 下载导入模板
    with open("students_info.xlsx", "rb") as file:
        st.download_button(
            label="下载导入模板", data=file, file_name="student_info.xlsx", mime="ms-excel"
        )

    # 文件上传栏
    uploaded_file = st.file_uploader(
        label="导入数据", type=["xlsx"], accept_multiple_files=False
    )

    st.markdown("***")
    st.markdown("#### 学生留宿信息")
    # st.markdown("![](https://pic.imgdb.cn/item/64827a781ddac507ccf95116.jpg)")

    if stu_info_df.empty:
        # 创建一个空容器，用于占位
        container = st.container()
        container.write("学生信息表为空！")
    else:
        AgGrid(
            pd.DataFrame(stu_info_df, columns=stu_info_df.columns),
            fit_columns_on_grid_load=True,
            height=1500,
            editable=True,
            enable_enterprise_modules=True,
        )


if __name__ == "__main__":
    # 从数据库获取，学生留宿信息
    stu_info_df = out_sql("stu_info")

    # 从数据库获取，系统信息
    sys_info_df = out_sql("sys_info")

    show_sidebar(stu_info_df, sys_info_df)
    show_content(stu_info_df)
