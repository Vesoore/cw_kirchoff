from io import BytesIO

import streamlit as st
import requests
import os
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''

st.sidebar.header("Input edges")
with st.sidebar:
    n = st.slider("Choose count of edges in graph and enter them separated by space (numbering from 0)", 0, 40)
    edges = []
    for i in range(n):
        value = st.text_input(f"edge {i + 1}:")
        if value:  # Ensure that the value is not empty
            try:
                edge = list(map(int, value.split()))
                if len(edge) == 2:  # Ensure that there are exactly 2 vertices in the edge
                    edges.append(edge)
                else:
                    st.warning(f"Invalid input for edge {i + 1}. Please enter exactly two integers.")
            except ValueError:
                st.warning(f"Invalid input for edge {i + 1}. Please enter valid integers.")

if st.sidebar.button("next"):
    data = {
        "edges": edges
    }

    try:
        response = requests.post("http://127.0.0.1:8001 /process_graph", json=data)

        if response.status_code == 200:
            st.success("Matrices processed and saved.")

        else:
            #st.error(f"Error processing data: {response.content}")
            st.error('check the correctness of the entered data')
    except requests.RequestException as e:
        st.error(f"Request failed: {e}")

def count_spanning_trees(kir_matrix):

    L_minor = np.delete(kir_matrix, 0, axis=0)
    L_minor = np.delete(L_minor, 0, axis=1)

    determinant = np.linalg.det(L_minor)

    return int(round(determinant)), L_minor


def latex_matrix(matrix):
    K = r'\begin{pmatrix}'
    for row in matrix:
        K += ' & '.join(map(str, row)) + r'\\'
    K += r'\end{pmatrix}'
    ans = 'kirchhoff \\ matrix' + r'\\' + 'K = ' + K + r'\\'

    c, minor = count_spanning_trees(matrix)
    M = r'\begin{vmatrix}'
    for row in minor:
        M += ' & '.join(map(str, row)) + r'\\'
    M += r'\end{vmatrix}'

    ans += "count \\ of \\ trees" + r'\\' "A_{0,0} = " + M + " = " + str(c)

    return ans


def draw_graph(edges):
    G = nx.Graph()
    G.add_edges_from(edges)

    # Рисуем граф
    plt.figure(figsize=(6, 4))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='black', linewidths=1,
            font_size=15)

    # Сохраняем граф в буфер
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return buf


if st.button("show matrices"):
    K = np.load("kirchhoff_matrix.npy")
    buf = draw_graph(edges)
    st.subheader("Original graph")
    st.image(buf, use_column_width=True)
    st.subheader("Count of spanning trees")
    st.latex(latex_matrix(K))

