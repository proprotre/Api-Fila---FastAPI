from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from datetime import date

data = date.today()
fila = [{"nome":"Vazio","data":f"{data.day}/{data.month}/{data.year}","atendido":"Vazio"}]
fila.append({"nome":"Gabriel","data":f"{data.day}/{data.month}/{data.year}","atendido":False})
fila.append({"nome":"Felipe","data":f"{data.day}/{data.month}/{data.year}","atendido":False})
fila.append({"nome":"Caravante","data":f"{data.day}/{data.month}/{data.year}","atendido":False})
fila.append({"nome":"Badaró","data":f"{data.day}/{data.month}/{data.year}","atendido":False})

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <html>
        <head>
            <title>Minha API - Gabriel Badaró</title>
        </head>
        <body style="text-align:center;">
            <h1>API para filas desenvolvido por Gabriel Badaró</h1>
            <h2>Dúvidas sobre como utilizar a nossa API para filas?</h2>
            <h3>Acesse o <a href="/docs">"/docs"</a> para documentação!</h3>
            <p>Para o desenvolvimento dessa API, foi utilizado a linguagem de programação python com o Framework FastAPI.</p>
        </body>
    </html>
    """

@app.get("/fila")
def exibirFila():
    aux = []
    if len(fila) == 1:
        raise HTTPException(status_code=200)
    else:
        for n in fila:
            if fila.index(n) == 0:
                pass
            else:
                aux.append({"Posição":fila.index(n),"Nome":n['nome'],"Data":n['data'],"atendido":n['atendido']})
        return aux

@app.get("/fila/{id:int}")
def exibirPosicao(id):
    for n in fila:
        if fila.index(n) == id:
            return {"Posição":fila.index(n),"Nome":n['nome'],"Data": n['data'],"atendido":n['atendido']}
        else:
            pass
    raise HTTPException(status_code=404,detail="Ops! O ID informado não foi encontrado :(")

@app.post("/fila")
def adicionar(nome:str = Query(max_length=20)):
    aux = len(fila)
    fila.append({"nome":nome,"data":f"{data.day}/{data.month}/{data.year}","atendido":False})
    return {"Adicionado":{"Posição":aux,"nome":nome,"data":f"{data.day}/{data.month}/{data.year}","atendido":False}}

@app.put("/fila")
def atender():
    if len(fila) == 1:
        return {"mensagem":"Fila vazia!"}
    else:
        del(fila[0])
        fila[0]["atendido"] = True
        return {"mensagem":"Atendendo o primeiro da fila!"}
        

@app.delete("/fila/{id:int}")
def remover(id):
    try:
        if fila[id]:
            del(fila[id])
            return {"mensagem":f"O ID '{id}' foi removido com sucesso!"}
    except(IndexError):
        raise HTTPException(status_code=404,detail="Ops! O ID informado não foi encontrado :(")
