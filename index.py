import streamlit as st
import pandas as pd
from st_aggrid import (
    AgGrid,
    JsCode,
    DataReturnMode,
    GridUpdateMode,
    GridOptionsBuilder,
)

from db_operator import (
    out_sql,
    to_sql_stu_info,
    update_sys_info_table,
    read_xlsx,
    del_data,
)
from body_create import body_create_df, DEPARTMENT_DICT, OPTION_DICT
from info_send import get_token, info_send

# 打开aggrid调试信息
# js_console = JsCode(
#     """
# function(e) {
#     debugger;
#     alert(e.node.data);
#     console.log(e);
#     console.log(e.node.data);
#     console.log(e.node.selected);
#     console.log('jay');
#     console.log(e.rowIndex);
#     return e.node.data
# };
# """
# )

# JS方法，用于增加一行到AgGrid表格
js_add_row = JsCode(
    """
function(e) {
    let api = e.api;
    let rowPos = e.rowIndex + 1;
    // 数据转换成JSON
    api.applyTransaction({addIndex: rowPos, add: [{}]})
    };
"""
)

# 为'🌟'列增加一个按钮
cellRenderer_addButton = JsCode(
    """
    class BtnCellRenderer {
        init(params) {
            this.params = params;
            this.eGui = document.createElement('div');
            this.eGui.innerHTML = `
            <span>
                <style>
                .btn_add {
                    background-color: #EAECEE;
                    # border: 1px solid black;
                    color: #AEB6BF;
                    text-align: center;
                    display: inline-block;
                    font-size: 12px;
                    font-weight: bold;
                    height: 2em;
                    width: 5em;
                    border-radius: 12px;
                    padding: 0px;
                }
                </style>
                <button id='click-button' 
                    class="btn_add" 
                    >&#x2193; 添加</button>
            </span>
        `;
        }
        getGui() {
            return this.eGui;
        }
    };
    """
)


# 定义动态表格，并返回操作数据
def aggrid(stu_info_df):
    if stu_info_df.empty:
        # 创建一个空容器，用于占位
        container = st.container()
        container.markdown("# 学生信息表为空！")
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

        gd = GridOptionsBuilder.from_dataframe(stu_info_df)
        # 打开ag-grid调试信息,选择后输出调试信息
        # gd.configure_grid_options(onRowSelected=js_console)
        # 配置列的默认设置
        # gd.configure_auto_height(autoHeight=True)
        gd.configure_default_column(
            # # 可编辑
            editable=True,
        )
        gd.configure_column(
            field="id",
            header_name="序号",
            width=70,
        )
        gd.configure_column(
            field="stu_name",
            header_name="学生姓名",
            width=100,
        )
        gd.configure_column(
            field="stu_phone",
            header_name="学生手机",
            width=100,
        )
        gd.configure_column(
            field="par_name",
            header_name="家长姓名",
            width=100,
        )
        gd.configure_column(
            field="par_phone",
            header_name="家长手机",
            width=100,
        )
        gd.configure_column(
            field="dormitory",
            header_name="宿舍号",
            width=100,
        )
        gd.configure_column(
            field="address",
            header_name="家庭住址",
            width=500,
        )
        gd.configure_column(
            field="🌟",
            onCellClicked=js_add_row,
            cellRenderer=cellRenderer_addButton,
            lockPosition="left",
            width=70,
        )
        gd.configure_selection(
            selection_mode="multiple",
            use_checkbox=True,
            # 预选
            # pre_selected_rows=[{"id": 1}, {"id": 2}],
            # suppressRowClickSelection=False,
        )
        # 表格右侧工具栏
        gd.configure_side_bar()
        # 分页
        gd.configure_pagination(
            # 取消自动分页
            paginationAutoPageSize=False,
            # 30页一分页
            paginationPageSize=30,
        )

        gridoptions = gd.build()

        # 渲染表格
        grid_res = AgGrid(
            stu_info_df,
            gridOptions=gridoptions,
            fit_columns_on_grid_load=True,
            update_mode=GridUpdateMode.GRID_CHANGED,
            data_return_mode=DataReturnMode.AS_INPUT,
            allow_unsafe_jscode=True,
            theme="streamlit",
            # streamlit,alpine,balham,material
        )
        # 返回数据
        return grid_res


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
        # 根据selectbox传来的key返回department的value
        def department_to_value(key):
            return DEPARTMENT_DICT[key]

        # 根据selectbox传来的key返回department的value
        def option_to_value(key):
            return OPTION_DICT[key]

        # input控件：创建者ID
        creater = st.sidebar.text_input(label="创建者ID", value=sys_info_df.values[0][1])

        # selectbox控件，所属部门
        department = st.sidebar.selectbox(
            label="所属部门",
            options=(list(DEPARTMENT_DICT.keys())),
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
            options=(list(OPTION_DICT.keys())),
            index=sys_info_df.values[0][6],
            format_func=option_to_value,
        )

        sb_col1, sb_col2 = st.columns(2)

        with sb_col1:
            st.info("第三步：")
        # form_submit_button控件，表单提交按钮

        with sb_col2:
            if st.form_submit_button("更新", help="保存系统配置信息到数据库。"):
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

                # 把数据保存到数据库中
                if update_sys_info_table(sys_info_df):
                    st.success("设置已更新！")


# 显示content内容
def show_content(stu_info_df, sys_info_df):
    con_col1, con_col2 = st.columns(2)

    with con_col1:
        st.info("第一步：")
        # download_btn控件，下载导入模板
        with open("students_info.xlsx", "rb") as file:
            st.download_button(
                label="下载导入模板",
                data=file,
                file_name="student_info.xlsx",
                mime="ms-excel",
            )

    with con_col2:
        st.info("第二步：")
        # file_uploader控件，上传excle表
        uploaded_file = st.file_uploader(
            label="导入数据", type=["xlsx"], accept_multiple_files=False
        )
        if uploaded_file:
            # 读取上传的excel表
            df = read_xlsx(uploaded_file)[1]
            # 数据导入数据库
            to_sql_stu_info(df)
            st.success("导入成功！")

    st.markdown("***")

    # form控件，学生信息不为空，显示控件
    if not stu_info_df.empty:
        tab_col1, tab_col2 = st.columns(2)
        with tab_col1:
            st.info("第四步：")
        with tab_col2:
            st.markdown("#### 学生信息")

        # form控件，表单
        with st.form("stu_info_form"):
            # aggrid控件
            grid_res = aggrid(stu_info_df)
            selection = grid_res["selected_rows"]

            # 设置按钮布局
            col1, col2, col3, col4, col5, col6 = st.columns(6)

            with col1:
                st.warning("第五步：非必须")

            with col2:
                if st.form_submit_button("保存", help="保存修改的学生信息。"):
                    if del_data(id=0) and to_sql_stu_info(grid_res.data):
                        st.success("学生信息已保存！")
                    else:
                        st.error("保存失败！")

            with col3:
                st.info("第六步：")

            with col4:
                # form_submit_btn控件，表单提交
                if st.form_submit_button("提交", help="提交选中学生到企业微信。"):
                    if not len(selection) == 0:
                        # 生成access_token
                        access_token = get_token()

                        # 构建待发送消息的主体
                        body_json = body_create_df(sys_info_df, selection)

                        # 发送请求
                        result = info_send(access_token, body_json)
                        st.error(f"{result}")
                    else:
                        st.error("没有选中需要提交的学生。")

            with col5:
                st.warning("第七步：非必须")

            with col6:
                # form_submit_btn控件，表单提交--删除被选中学生信息
                if st.form_submit_button(
                    "删除学生信息", help="删除被选中学生信息,如果所有学生都没有被选中，则删除所有学生信息。"
                ):
                    if len(selection):
                        for i in selection:
                            del_data(i["id"])
                        st.success("学生信息已删除！")
                    else:
                        if del_data(id=0):
                            st.success("学生信息已清空！")
                        else:
                            st.error("删除失败！")

    else:
        # st.markdown("### 学生留宿信息为空！请先导入数据。")
        st.error("学生留宿信息为空！请先导入数据。")


def main():
    # 隐藏made with streamlit
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    # 从数据库获取，学生留宿信息
    stu_info_df = out_sql("stu_info")

    # 从数据库获取，系统信息
    sys_info_df = out_sql("sys_info")

    # 显示siderbar页
    show_sidebar(sys_info_df)

    # 显示content页
    show_content(stu_info_df, sys_info_df)

    st.info("作者：陈沛华，时间：2023年6月20日")


if __name__ == "__main__":
    main()
