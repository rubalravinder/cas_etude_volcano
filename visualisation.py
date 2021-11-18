import pandas as pd
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
import plotly.express as px


def visu_pca(y_pred, X_test):
    """
    Input :
        - y_pred : numpy array of the prediction of the test dataset (y_test) with a ML model - OR just y_test
        - X_test : dataframe with the features used for the test dataset
    Output : returns a plot in 2D (after a PCA with 2 components) where each color is associated to one class in y
    """
    y_pred_df = pd.DataFrame(y_pred, index = X_test.index)
    data_merged = pd.merge(X_test,y_pred_df,left_index=True, right_index=True)
    data_merged.rename(columns={0:'y'}, inplace=True)
    pca = PCA(n_components=2)
    components = pca.fit_transform(data_merged)
    fig = px.scatter(components, x=0, y=1, color=data_merged["y"], width=500, height=400)
    fig.show()
