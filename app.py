from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
import uvicorn

app = FastAPI()

app.mount("/styles", StaticFiles(directory="styles"), name="styles")

@app.get("/", response_class=HTMLResponse)
def read_form():
    with open("templates/index.html", "r", encoding='UTF-8') as file:
        form_html = file.read()
    return form_html 

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(request: Request):
    form_data = await request.form()
    name = form_data["name"]
    return f"""
    <script>
        alert("Formulário submetido com sucesso: {name}!\\nRedirecionando para outra página.");
        setTimeout(function() {{
            window.location.href="/result";
        }}, 1000);
    </script>
    """

@app.get("/result", response_class=HTMLResponse)
def show_results():
    with open("templates/result.html", "r", encoding='UTF-8') as file:
        result_html = file.read()
    return result_html

@app.get("/account", response_class=HTMLResponse)
def create_account():
    with open("templates/account.html", "r", encoding='UTF-8') as file:
        account_html = file.read()
    return account_html

@app.post("/success", response_class=HTMLResponse)
async def account_success(request: Request):
    account_form_data = await request.form()
    user = account_form_data["user"]
    email = account_form_data["email"]
    return f"""
    <h1>Conta criada com sucesso!</h1>
    <p>Usuário: {user}</p>
    <p>Email: {email}</p>
    <p>Senha: <span style="color: red">confidencial</span></p>
    """


if __name__ == "__main__":
    uvicorn.run(app, port=7777)