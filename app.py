import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from visualisation import *

app = dash.Dash()

X_test = pd.read_pickle("./X_test.pkl")

y_test = np.load('y_test.npy')
components_test = pca(y_test, X_test)

svc_pred = np.load('svc_pred.npy')
components_svc = pca(svc_pred, X_test)

fig1 = px.scatter(
    components_test,
    x=0,
    y=1,
    color=y_test,
    width=500,
    height=400,
    title='Classification des données test en 2D'
    )

fig2 = px.scatter(
    components_svc,
    x=0,
    y=1,
    color=svc_pred,
    width=500,
    height=400,
    title='Classification avec le modèle SVC en 2D'
    )

app.layout = html.Div(
    [
        html.H1(
            "Dashboard of my ML model", style={"color": "#011833"}
            ),
        dcc.Graph(
            id="visu_pca_test",
            figure=fig1,
            ),
        dcc.Graph(
            id="visu_pca_svc",
            figure=fig2,
        )
            ])

if __name__ == "__main__":
    app.run_server(debug=True)