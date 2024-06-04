from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import numpy as np


app = FastAPI()


def kirchhoff_matrix(graph):
    n = len(graph)
    D = np.zeros((n, n))
    for i in range(n):
        D[i, i] = len(graph[i])

    A = np.zeros((n, n))
    for i in range(n):
        for j in graph[i]:
            A[i, j] = 1

    K = (D - A).astype(int)
    return K


@app.post("/process_graph")
async def process_graph(request: Request):
    try:
        data = await request.json()
        edges = data.get("edges", [])

        #max_vertex = max(max(edge) for edge in edges) if edges else 0
        ls_adj = [[] for _ in range(len(edges))]

        for i, j in edges:
            ls_adj[i].append(j)
            ls_adj[j].append(i)

        K = kirchhoff_matrix(ls_adj)

        # Сохранение матрицы Кирхгофа
        np.save("kirchhoff_matrix.npy", K)
        np.save("edges.npy", edges)

        return JSONResponse(content={"message": "Matrices processed and saved."})
    except Exception as e:

        return JSONResponse(content={"error": str(e)}, status_code=500)


