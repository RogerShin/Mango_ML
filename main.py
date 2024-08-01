# # main.py
# import dash
# from dash import dcc, html
# import dash_table
# from alldata.taipei_mk1_irwin import taipei_mk1

# # 使用 taipei_mk1 函數來獲取 DataFrame
# # 確保 '台北一' 是你需要的市場名稱
# df_taipei_mk1 = taipei_mk1('台北一')

# # 生成 Dash 應用程式
# app = dash.Dash(__name__)

# # 定義應用程式佈局
# app.layout = html.Div([
#     html.H1('台北一市場的芒果交易資料'),

#     # 資料表格顯示
#     dash_table.DataTable(
#         id='table',
#         columns=[{"name": i, "id": i} for i in df_taipei_mk1.columns],
#         data=df_taipei_mk1.to_dict('records'),
#         style_table={'overflowX': 'auto'},
#         page_size=10,  # 設置每頁顯示10行
#     ),

#     # 可以加上其他圖表或組件
#     # dcc.Graph(...), 
# ])

# # 運行應用程式
# if __name__ == '__main__':
#     app.run_server(debug=True)


import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from alldata.taipei_mk1_irwin import taipei_mk1, anal_mk1_data

# 生成 Dash 應用程式
app = dash.Dash(__name__)

# 定義應用程式佈局
app.layout = html.Div([
    html.H1('台北市場的芒果交易資料'),

    # 下拉選單選擇市場
    dcc.Dropdown(
        id='market-dropdown',
        options=[
            {'label': '台北一', 'value': '台北一'},
            {'label': '台北二', 'value': '台北二'}
        ],
        value='台北一'  # 預設值
    ),

    # 主要資料表格顯示
    html.Div([
        html.H2('主要資料表格'),
        dash_table.DataTable(
            id='table',
            columns=[],
            data=[],
            style_table={'overflowX': 'auto'},
            page_size=10,  # 設置每頁顯示10行
        ),
    ]),

    # 全部資料分布狀況表格顯示
    html.Div([
        html.H2('全部資料分布狀況'),
        dash_table.DataTable(
            id='descr-table',
            columns=[],
            data=[],
            style_table={'overflowX': 'auto'},
            page_size=10,  # 設置每頁顯示10行
        ),
    ]),

    # 圖片顯示
    html.Div([
        html.H2('圖像顯示'),
        html.Img(id='box-plot', src=''),
        # html.Img(id='distribution-plot', src=''),
    ]),

])

# 定義回調函數來更新表格
@app.callback([
    Output('table', 'columns'),
    Output('table', 'data'),
    Output('descr-table', 'columns'),
    Output('descr-table', 'data'),
    Output('box-plot', 'src')],
    # Output('distribution-plot', 'src')],
    Input('market-dropdown', 'value')
)
def update_table(selected_market):
    # 使用 taipei_mk1 函數來獲取 DataFrame
    df_taipei_mk1 = taipei_mk1(selected_market)
    # 使用 anal_mk1_data 函數來獲取分析數據
    all_descr, box_plot, skew, kurt, distribution_plot = anal_mk1_data(df_taipei_mk1)
    
    # 更新 DataTable 的 columns 和 data
    columns = [{"name": i, "id": i} for i in df_taipei_mk1.columns]
    data = df_taipei_mk1.to_dict('records')

    # 更新全部資料分布狀況表格的 columns 和 data
    descr_columns = [{"name": i, "id": i} for i in all_descr.columns]
    descr_data = all_descr.reset_index().to_dict('records')

    # 更新圖片的 src 屬性
    box_plot_src = '/asswts/irwin_box_plot_1.png'
    # distribution_plot_src = '/assets/distribution_plot.png'

    return columns, data, descr_columns, descr_data, box_plot_src

# 運行應用程式
if __name__ == '__main__':
    app.run_server(debug=True)
