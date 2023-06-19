import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

st.header("AgGrid Demo `Part 3`")
with st.expander("🤩 What I plan to demonstrate today ? ", expanded=False):
    st.markdown(
        """
                
                ◻ 1. Implementing `button` within AgGrid table
                
                ◻ 2. Display any `update` made from the user-end
                
                ◻ 3. `Download` the AgGrid table
                
                ◻ 4. `Connect` to Database
                """
    )

# Create an AgGrid table from a pandas DataFrame
d = {"Type": ["Notebook", "DVDs"], "Quantity": [1, 2], "Price": [400, 200]}
df = pd.DataFrame(data=d)

AgGrid(df)

# JS方法，用于增加一行到AgGrid表格
js_add_row = JsCode(
    """
function(e) {
    let api = e.api;
    let rowPos = e.rowIndex + 1; 
    api.applyTransaction({addIndex: rowPos, add: [{}]});
    console.log(e);
};
"""
)

# 为'🔧'列增加一个按钮
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
                    background-color: #71DC87;
                    border: 2px solid black;
                    color: #D05732;
                    text-align: center;
                    display: inline-block;
                    font-size: 12px;
                    font-weight: bold;
                    height: 2em;
                    width: 10em;
                    border-radius: 12px;
                    padding: 0px;
                }
                </style>
                <button id='click-button' 
                    class="btn_add" 
                    >&#x2193; 在下方添加一行</button>
            </span>
        `;
        }
        getGui() {
            return this.eGui;
        }
    };
    """
)

gd = GridOptionsBuilder.from_dataframe(df)

gd.configure_default_column(editable=True)

# 配置 "🔧"列，用于接收返回的单元格
# 同时配置点击按钮函数
gd.configure_column(
    field="🔧",
    onCellClicked=js_add_row,
    cellRenderer=cellRenderer_addButton,
    lockPosition="left",
)

gridoptions = gd.build()


# AgGrid Table with Button Feature
# Streamlit Form helps from rerunning on every widget-click
# Also helps in providing layout

with st.form("Inventory") as f:
    st.header("Inventory List 🔖")

    # Inside the form, we are displaying an AgGrid table using the AgGrid function.
    # The allow_unsafe_jscode parameter is set to True,
    # which allows us to use JavaScript code in the AgGrid configuration
    # The theme parameter is set to 'balham',
    # which applies the Balham theme to the table
    # The height parameter is set to 200,
    # which specifies the height of the table in pixels.
    # The fit_columns_on_grid_load parameter is set to True,
    # which ensures that the columns of the table are resized to fit
    # the width of the table when it is first displayed

    response = AgGrid(
        df,
        gridOptions=gridoptions,
        editable=True,
        allow_unsafe_jscode=True,
        theme="balham",
        height=200,
        fit_columns_on_grid_load=True,
    )
    st.write(" *Note: Don't forget to hit enter ↩ on new entry.*")
    st.form_submit_button("Confirm item(s) 🔒", type="primary")

# 触发按钮时，提交ag表格
st.subheader("更新后的数据")
# Fetch the data from the AgGrid Table
res = response["data"]
st.table(res)


# 绘制数据
st.subheader("绘制数据")
st.bar_chart(data=res, x="Type", y="Price")
