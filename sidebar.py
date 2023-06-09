import os

import base64
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder

from db_operator import out_sql


# 显示侧边栏
def show_sidebar():
    uploaded_file = st.sidebar.file_uploader("excel文件", type=["xlsx"])

    # if uploaded_file is None:
    #     st.stop()

    # # 装饰器，表示这是一个缓存函数
    # @st.cache_data
    # def load_data(uploaded_file):
    #     print("执行加载数据")
    #     return pd.read_excel(uploaded_file,None)

    # dfs = load_data(uploaded_file)

    # 读取所有工作表
    # names = list(dfs.keys())

    # 选择的工作表
    # sheet_selects = st.multiselect("工作表",names,[])

    # if len(sheet_selects)==0:
    #     st.stop()

    # for cell in sheet_selects:
    #     df = dfs[cell]
    #     st.sidebar.dataframe(df)
    # st.dataframe(df)

    # 取工作表“申请学生信息”内容
    # st.dataframe(dfs["申请学生信息"])
    # st.dataframe.dfs.columns["序号"]
    # 取表中“学生姓名”的数据
    # st.dataframe(dfs["申请学生信息"]["学生姓名"],dfs["申请学生信息"]["学生手机"])
    # st.sidebar.dataframe(dfs["运行参数"])

    if st.sidebar.button("下载模板"):
        # get_binary_file_downloader_html(file_path, file_label),
        # st.markdown(unsafe_allow_html=True)
        st.markdown(
            """<style>#root > div:nth-child(1) > div > div > div > div > section > div > div:nth-child(1) > div > div:nth-child(2) > div > button {background-color: rgb(255 75 75 / 50%);} </style>""",
            unsafe_allow_html=True,
        )

    if st.sidebar.button("导入"):
        "导入成功！"

    stu_info_df = out_sql("stu_info")
    options_builder = GridOptionsBuilder.from_dataframe(stu_info_df)
    options_builder.configure_default_column(
        groupable=True,
        value=True,
        enableRowGroup=True,
        aggFunc="sum",
        editable=True,
        wrapText=True,
        autoHeight=True,
    )
    options_builder.configure_column("stu_name", pinned="left")
    options_builder.configure_column("stu_phone", pinned="left")
    grid_options = options_builder.build()
    AgGrid(stu_info_df, grid_options, theme="blue")
    AgGrid(stu_info_df, grid_options)

    sys_info_df = out_sql("sys_info")
    if not sys_info_df.empty:
        AgGrid(
            pd.DataFrame(sys_info_df, columns=sys_info_df.columns),
            fit_columns_on_grid_load=True,
            # height=100,
            editable=True,
            enable_enterprise_modules=True,
        )

    # stu_info_df = out_sql("stu_info")
    # if not sys_info_df.empty:
    #     AgGrid(
    #         pd.DataFrame(stu_info_df, columns=stu_info_df.columns),
    #         fit_columns_on_grid_load=True,
    #         height=1500,
    #         editable=True,
    #         enable_enterprise_modules=True,
    #     )


if __name__ == "__main__":
    show_sidebar()
