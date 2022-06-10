from flask import Flask, render_template, request
import Classes as cl
import Funcoes as fun
app=Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def homepage():
    variavel = "Trabalhando com requisitos"
    if request.method=="GET":
        return render_template("home.html",variavel=variavel)
    else:
        f = request.files['file']
        requisito = fun.tratar_requisitos(f)
        escolha = request.form.get("options")
        try:
            escolha=int(escolha)
            texto=cl.Texto(requisito)
            Data, headings = fun.caminho(escolha,texto)
            return render_template("home.html", variavel=variavel, headings=headings, data=Data,opcao=escolha)
        except BaseException as err:
            print(err)
            return render_template("home.html",variavel=variavel)
@app.route('/instrucoes', methods=["GET"])
def instrucoes():
    return render_template("instrucoes.html")
"""
@app.route('/aboutus', methods=["GET"])
def aboutus():
    return render_template("aboutus.html")
"""
if __name__ == "__main__":
    app.run(debug=True)