import streamlit as st
from st_aggrid import AgGrid, ColumnsAutoSizeMode
import pandas as pd

# _ Input data
df = pd.DataFrame(
    {
        "Category": ["Fruit", "Fruit", "Vegetable", "Vegetable"],
        "Items": ["Apple", "Banana", "Tomato", "Carrots"],
        "Price": [1.04, 1.15, 1.74, 1.5],
    }
)

# _ Ag Grid table
st.markdown("# Issue: how to get group selection?")
st.write("Try selecting an aggregate, and then an atomic record")

grid_options = {
    "columnDefs": [
        {"field": "Category", "rowGroup": True, "hide": True},
        {"field": "Items"},
        {"field": "Price"},
    ],
    "rowSelection": "single",
}

# _ Playing with response
response = AgGrid(
    df,
    grid_options,
    columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
)

if response["selected_rows"]:
    selection = response["selected_rows"][0]

    st.write(
        "Current selection is provided as a nested dictionary, requesting `['selected_rows'][0]` value of AgGrid response:"
    )
    st.write(selection)

    if "Items" in selection:
        st.markdown("#### Good!")
        Category = selection["Category"]
        Item = selection["Items"]
        Price = selection["Price"]
        st.write(
            f"We know everything about current selection: you picked a `{Category}` called `{Item}`, with price `{Price}`!"
        )
    else:
        st.markdown("#### Bad!")
        nodeId = response["selected_rows"][0]["_selectedRowNodeInfo"]["nodeId"]
        st.write(
            f"All we know is that a node with Id `{nodeId}` is selected.\n\r How do we know if you're looking for a `Fruit` or a `Vegetable`?"
        )

# 增加行
    # if 'n_rows' not in st.session_state:
    #     st.session_state.n_rows = 1

    # add = st.button(label="add")

    # if add:
    #     st.session_state.n_rows += 1
    #     st.experimental_rerun()

    # for i in range(st.session_state.n_rows):
    #     #add text inputs here
    #     st.text_input(label="列名", key=i) # 传递一个索引作为key