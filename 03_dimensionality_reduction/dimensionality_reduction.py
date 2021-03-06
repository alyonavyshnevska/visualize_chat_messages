import umap
from src.visualize import create_tf_idf_matrix, create_history_dataframe
import matplotlib.pyplot as plt
import seaborn as sns
from yellowbrick.text import TSNEVisualizer
import plotly.graph_objs as go
import plotly.plotly as py
import plotly.tools as plttools
import numpy as np

plttools.set_credentials_file(username='gigi_karlo_', api_key='Vm4QxLy6m3t2gSIAEysa')

def save_embeddings_to_file():
    history = create_history_dataframe('data', one_year=False)
    tfidf, feature_matrix, target, df_import = create_tf_idf_matrix(history, 'chat_number',
                                                                    ['index', 'date', 'msg_len', 'name'])

    assert feature_matrix.shape == (1288, 369)
    assert target.shape == (1288,)

    reducer = umap.UMAP(random_state=42)
    embedding = reducer.fit_transform(feature_matrix)
    np.save('embedding-test.npy', embedding)



def visualise_with_yellowbrick(feature_matrix, labels_tfidf):
    tsne = TSNEVisualizer(title="Chat Messages Clusters", alpha = 0.7)
    tsne.fit(feature_matrix, np.array(labels_tfidf))
    tsne.finalize()
    tsne.poof()


def visualise_with_sns(embedding, labels):
    sns.set(context="paper", style="white")

    fig, ax = plt.subplots(figsize=(12, 10))
    plt.scatter(
        embedding[:, 0], embedding[:, 1]
    )
    plt.setp(ax, xticks=[], yticks=[])
    plt.title("Chat Text Data in Two Dimensions", fontsize=18)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()


def visualise_with_plotly(embedding, history, file_name):

    # Create a trace
    trace = go.Scatter(
        x=embedding[:, 0],
        y=embedding[:, 1],
        text=history['chat_number'],
        mode='markers',
        name = "Chat Messages",
        showlegend=True,
        marker=dict(
            size=16,
            color=history['chat_number'],  # set color equal to a variable
            colorscale='Viridis',
            showscale=True
            )
    )

    data = [trace]

    mylayout = go.Layout(
        title="TFIDF Scores for Chat Messages from 5 Different Chats"
    )

    fig = go.Figure(data=data, layout=mylayout)

    #plot([go.Scatter(x=embedding[:, 0], y=embedding[:, 1])])
    #off_plot(data, filename='scatterplot_02.html')
    py.plot(data, filename = file_name, auto_open=True)


def visualize_3d(embedding, history, file_name, target):
    trace1 = go.Scatter3d(
        x=embedding[:, 0],
        y=embedding[:, 1],
        z=history['msg_len'],
        mode='markers',
        text=history['chat_number'],
        marker=dict(
            size=12,
            color=history['chat_number'],  # set color to an array/list of desired values
            colorscale='Viridis',  # choose a colorscale
            opacity=0.8
        )
    )

    data = [trace1]
    layout = go.Layout(
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        )
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=file_name)




if __name__ == '__main__':
    history = create_history_dataframe('data', one_year=False)
    tfidf, feature_matrix, target, df_import = create_tf_idf_matrix(history, 'chat_number',
                                                                     ['index', 'date', 'msg_len', 'name'])
    labels = np.array(target)
    embedding = np.load('embedding.npy')

    visualise_with_plotly(embedding, history, '2d_reduced')
