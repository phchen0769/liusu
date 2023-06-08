"""
   运行此代码，请使用
   streamlit run 'pd_test.py'
"""

import streamlit as st
import pandas as pd

# 显示表格
def show_tables():
    uploaded_file = st.sidebar.file_uploader("excel文件", type=["xlsx"])

    if uploaded_file is None:
        st.stop()

    # 装饰器，表示这是一个缓存函数
    @st.cache_data
    def load_data(uploaded_file):
        print("执行加载数据")
        return pd.read_excel(uploaded_file,None)

    dfs = load_data(uploaded_file)

    # 读取所有工作表
    names = list(dfs.keys())

    # 选择的工作表
    sheet_selects = st.multiselect("工作表",names,[])

    if len(sheet_selects)==0:
        st.stop()

    # 选择的工作表
    tabs = st.tabs(sheet_selects)

    for tab,name in zip(tabs,sheet_selects):
        with tab:
            df = dfs[name]
        st.sidebar.dataframe(df)
        st.dataframe(df)