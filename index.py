import os

import base64
import streamlit as st
import pandas as pd
from st_aggrid import (
    AgGrid,
    ColumnsAutoSizeMode,
    DataReturnMode,
    GridUpdateMode,
    GridOptionsBuilder,
)

from db_operator import (
    out_sql,
    to_sql_stu_info,
    to_sql_sys_info,
    update_sys_info_table,
    read_xlsx,
    del_data,
)
from body_create import body_create_df
from info_send import get_token, info_send

# 初始化 站点显示参数
st.set_page_config(
    page_title="学生留宿管理系统",
    page_icon="🇨🇳",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None,
)


# 定义动态表格，并返回操作数据
def aggrid(stu_info_df):
    if stu_info_df.empty:
        # 创建一个空容器，用于占位
        container = st.container()
        container.write("学生信息表为空！")
    else:
        # 更改显示的列
        # rencolnames = {
        #     "id": "序号",
        #     "stu_name": "学生姓名",
        #     "stu_phone": "学生手机",
        #     "par_name": "家长姓名",
        #     "par_phone": "家长手机",
        #     "dormitory": "宿舍号",
        #     "address": "家庭住址",
        #     "is_choice": "是否被选中",
        # }
        # stu_info_df = stu_info_df.rename(columns=rencolnames)

        gb = GridOptionsBuilder.from_dataframe(stu_info_df)
        # 配置列的默认设置
        gb.configure_default_column(
            # 自动高度
            autoHeight=True,
            # 可调节宽度
            resizable=True,
            # 可过滤
            filterable=True,
            # 可排序
            sorteable=True,
            # 可编辑
            editable=True,
        )
        gb.configure_column(field="id", header_name="序号", width=70, editable=False)
        gb.configure_column(field="stu_name", header_name="学生姓名", width=100)
        gb.configure_column(field="stu_phone", header_name="学生手机", width=100)
        gb.configure_column(field="par_name", header_name="家长姓名", width=100)
        gb.configure_column(field="par_phone", header_name="家长手机", width=100)
        gb.configure_column(field="dormitory", header_name="宿舍号", width=100)
        gb.configure_column(field="address", header_name="家庭住址", width=400)
        gb.configure_selection(selection_mode="multiple", use_checkbox=True)
        gb.configure_side_bar()
        # 分页
        gb.configure_pagination(
            enabled=True,
            paginationAutoPageSize=True,
            # paginationPageSize=5,
        )
        gridoptions = gb.build()

        # 渲染表格
        grid_response = AgGrid(
            stu_info_df,
            gridOptions=gridoptions,
            # columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
            fit_columns_on_grid_load=True,
            update_mode=GridUpdateMode.GRID_CHANGED,
            data_return_mode=DataReturnMode.AS_INPUT,
            allow_unsafe_jscode=True,
            theme="streamlit",
            # streamlit,alpine,balham,material
            # height=2000,
        )
        # 返回数据

        return grid_response


# 显示侧边栏
def show_sidebar(sys_info_df):
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
    # st.sidebar.markdown("***")

    # 创建一个提交表单
    with st.sidebar.form("sys_info_form"):
        # 定义selectbox显示用的department字典
        department_dict = {0: "信息技术系", 1: "机电技术系", 2: "财经商贸系", 3: "公共基础部"}

        # 定义selectbox显示用的option字典
        option_dict = {
            0: "申请临时留宿",
            1: "申请临时不留宿",
            2: "申请长期留宿",
            3: "申请取消长期留宿",
        }

        # 根据selectbox传来的key返回department的value
        def department_to_value(key):
            return department_dict[key]

        # 根据selectbox传来的key返回department的value
        def option_to_value(key):
            return option_dict[key]

        # input控件：创建者ID
        creater = st.sidebar.text_input(label="创建者ID", value=sys_info_df.values[0][1])

        # selectbox空间，所属部门
        department = st.sidebar.selectbox(
            label="所属部门",
            options=(list(department_dict.keys())),
            index=sys_info_df.values[0][2],
            format_func=department_to_value,
        )

        # input控件，班级
        class_name = st.sidebar.text_input(label="班级", value=sys_info_df.values[0][3])

        # number_input控件，第几周
        week = st.sidebar.number_input(
            label="第几周(填写数字)", value=sys_info_df.values[0][4], min_value=1, max_value=25
        )

        # text_input控件，申请原因
        reason = st.sidebar.text_input(
            label="申请原因（可为空）", value=sys_info_df.values[0][5]
        )

        # selectbox控件，变更情况
        option = st.sidebar.selectbox(
            label="变更情况",
            options=(list(option_dict.keys())),
            index=sys_info_df.values[0][6],
            format_func=option_to_value,
        )

        # form_submit_button，表单提交按钮
        if st.form_submit_button("更新"):
            # 把数据转换成pf
            sys_info_df = pd.DataFrame(
                {
                    "creater": creater,
                    "department": department,
                    "class_name": class_name,
                    "week": week,
                    "reason": reason,
                    "option": option,
                },
                index=[0],
            )
            # 把数据保存到数据中
            if update_sys_info_table(sys_info_df):
                st.write("设置已更新！")


# 显示content内容
def show_content(stu_info_df, sys_info_df):
    # download_btn控件，下载导入模板
    with open("students_info.xlsx", "rb") as file:
        st.download_button(
            label="下载导入模板", data=file, file_name="student_info.xlsx", mime="ms-excel"
        )

    # btn控件，清空学生信息
    if st.button(label="清空学生信息"):
        if del_data():
            st.write("学生信息已清空！")

    # file_uploader控件，上传excle表
    uploaded_file = st.file_uploader(
        label="导入数据", type=["xlsx"], accept_multiple_files=False
    )
    if uploaded_file:
        # 读取上传的excel表
        df = read_xlsx(uploaded_file)[1]
        # 数据导入数据库
        to_sql_stu_info(df)

    st.markdown("***")
    st.markdown("#### 学生留宿信息")
    # st.markdown("![](https://pic.imgdb.cn/item/64827a781ddac507ccf95116.jpg)")

    # form控件，学生信息不为空，显示控件
    if not stu_info_df.empty:
        with st.form("stu_info_form"):
            # aggrid控件
            response = aggrid(stu_info_df)

            # form_submit_btn控件，表单提交
            if st.form_submit_button("提交"):
                selection = response["selected_rows"]

                # 生成access_token
                access_token = get_token()

                # 构建待发送消息的主体
                body_json = body_create_df(sys_info_df, selection)

                # 发送请求
                info_send(access_token, body_json)
    else:
        st.write("学生留宿信息为空！请先导入数据。")


def main():
    # 从数据库获取，学生留宿信息
    stu_info_df = out_sql("stu_info")

    # 从数据库获取，系统信息
    sys_info_df = out_sql("sys_info")

    # 显示siderbar
    show_sidebar(sys_info_df)
    show_content(stu_info_df, sys_info_df)


if __name__ == "__main__":
    main()
