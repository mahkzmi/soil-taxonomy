import dash
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=['assets/styles.css'])
server = app.server

def classify_soil(texture, ph, drainage, organic, depth):
    # تصمیم ساده‌شده بر اساس داده‌ها
    if organic == 'زیاد':
        return ('Histosols', 'Fibrists', 'خاک آلی، با زهکشی ضعیف، عمدتاً در مرداب‌ها')
    if drainage == 'ضعیف' and texture == 'رسی':
        return ('Ultisols', 'Aquults', 'خاک قدیمی، اسیدی، زهکشی ضعیف')
    if drainage == 'خوب' and ph >= 6.0 and ph <= 7.5 and texture == 'لومی':
        return ('Mollisols', 'Udolls', 'خاک حاصلخیز، مناسب کشاورزی')
    if drainage == 'متوسط' and texture == 'سیلتی':
        return ('Alfisols', 'Udalfs', 'خاک نسبتاً حاصلخیز، PH متوسط')
    if texture == 'شنی' and drainage == 'خوب':
        return ('Entisols', 'Psamments', 'خاک جوان، تکامل نیافته')
    if ph < 5.5:
        return ('Oxisols', 'Udox', 'خاک شدیداً اسیدی، مناطق گرمسیری')
    return ('Inceptisols', 'Aquepts', 'خاک نسبتاً جوان، زهکشی ضعیف')

app.layout = html.Div(className="container", children=[
    html.H1("سامانه آنلاین طبقه‌بندی خاک - رویش"),
    html.H3("ساخته‌شده توسط شرکت زامیتک"),

    html.Div(className="card", children=[
        html.Label("بافت خاک:"),
        dcc.Dropdown(
            id='texture',
            options=[
                {'label': 'شنی', 'value': 'شنی'},
                {'label': 'لومی', 'value': 'لومی'},
                {'label': 'رسی', 'value': 'رسی'},
                {'label': 'سیلتی', 'value': 'سیلتی'}
            ],
            value='لومی'
        ),

        html.Label("pH خاک:"),
        dcc.Input(id='ph', type='number', value=6.5, step=0.1),

        html.Label("زهکشی خاک:"),
        dcc.Dropdown(
            id='drainage',
            options=[
                {'label': 'خوب', 'value': 'خوب'},
                {'label': 'متوسط', 'value': 'متوسط'},
                {'label': 'ضعیف', 'value': 'ضعیف'}
            ],
            value='خوب'
        ),

        html.Label("مواد آلی:"),
        dcc.Dropdown(
            id='organic',
            options=[
                {'label': 'کم', 'value': 'کم'},
                {'label': 'زیاد', 'value': 'زیاد'}
            ],
            value='کم'
        ),

        html.Label("عمق خاک:"),
        dcc.Dropdown(
            id='depth',
            options=[
                {'label': 'کم‌عمق', 'value': 'کم‌عمق'},
                {'label': 'عمیق', 'value': 'عمیق'}
            ],
            value='عمیق'
        ),

        html.Button('طبقه‌بندی کن', id='submit-btn', n_clicks=0),
        html.Div(id='result-output', className='result')
    ])
])

@app.callback(
    Output('result-output', 'children'),
    Input('submit-btn', 'n_clicks'),
    Input('texture', 'value'),
    Input('ph', 'value'),
    Input('drainage', 'value'),
    Input('organic', 'value'),
    Input('depth', 'value')
)
def update_output(n_clicks, texture, ph, drainage, organic, depth):
    if n_clicks > 0:
        order, suborder, desc = classify_soil(texture, ph, drainage, organic, depth)
        return html.Div([
            html.H4(f"Order: {order}"),
            html.H5(f"Suborder: {suborder}"),
            html.P(desc)
        ])
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)