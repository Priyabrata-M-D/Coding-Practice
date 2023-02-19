from dash import Dash,html,dcc

app = Dash()

app.layout=html.Div(children=[
    html.Label("Select The State :"),
    dcc.Dropdown(["Ap","Goa","TN","Kerala"],"Goa"),
    html.Br(),
    html.Br(),

    html.Label("Multiple state selection :"),
    dcc.Dropdown(["Ap","Goa","TN","Kerala"],["Goa"],multi=True),
    html.Br(),


    html.Label("Radio items: "),
    dcc.RadioItems(["Ap","Goa","TN","Kerala"],"Goa"),
    html.Br(),
    
    html.Label("check boxes: "),
    dcc.Checklist(["Ap","Goa","TN","Kerala"],
                    ["Ap","Goa","TN"]),
    html.Br(),

    html.Label("Username: "),
    dcc.Input(value='UserName',type='text'),
    html.Label("Password: "),
    dcc.Input(value='*******',type='password'),
    html.Br(),

    html.Label('Age'),
    dcc.Slider(
        min=0,
        max=10,
        marks={i:f'Label {i}' if i==1 else str(i) for i in range(1,10)},
        value=9,
    ),
],
style={'backgroundColor': 'green', 'margin':100, 'padding': 30, 'flex':3}
)

if __name__=='__main__':
    app.run_server(debug=True)