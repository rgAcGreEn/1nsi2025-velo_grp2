from flask import Flask, render_template, request, make_response, redirect
import json
import datetime
from hashlib import md5

CHEMIN_DONNEES = "./donnees.json"
CHEMIN_UTILISATEURS = "./utilisateurs.json"

app = Flask(__name__)

def dateAujourdhui() -> datetime.date:
    return datetime.date.today()

def hachage(mot_de_passe_en_clair):
    return md5(mot_de_passe_en_clair.encode('utf-8')).hexdigest()

@app.route('/')
def home():
    distanceAujourdhui = 0
    distanceAnnee = 0
    for distance in donneesDistances.values():
        distanceAnnee += sum(distance["distances"])
        if datetime.date.fromisoformat(distance["date"]) == dateAujourdhui():
            distanceToday += distance["distances"][-1]
    return render_template('home.html',distanceAujourdhui=distanceAujourdhui,distanceAnnee=distanceAnnee)

@app.route('/connexion')
def pageConnexion():
    return render_template("connexion.html")

@app.route('/inscription')
def pageInscription():
    return render_template("inscription.html")

@app.route('/utilisateur')
def pageUtilisateur():
    return render_template("utilisateur.html")

@app.route("/traitement", methods=['POST'])
def traitement():
    donnees = dict(request.form)

    if donnees['mot_de_passe']==donnees['confirmation']:
        return render_template('utilisateur.html')
    else :
        return render_template('inscription.html', Adresse=donnees['adresse_mail'], Nom=donnees['nom_d_utilisateur'])


@app.route('/traitementConnexion', methods=['POST'])
def traitementConnection():
    donnees = dict(request.form)

    invalide = False
    if donnees.get("username") is None:
        invalide = True
    elif donnees.get("password") is None:
        invalide = True
    elif donneesUtilisateurs.get(donnees["username"]) is None:
        invalide = True
    elif donneesUtilisateurs[donnees["username"]] != hachage(donnees["password"]):
        invalide = True

    if invalide:
        return redirect("/connexion")

    reponse = redirect("/utilisateur")
    # code pour ajouter cookies à mettre ici
    return reponse
          
if __name__ == '__main__':
    with open(CHEMIN_DONNEES) as f:
        donneesDistances = json.load(f)
    with open(CHEMIN_UTILISATEURS) as f:
        donneesUtilisateurs = json.load(f)
    app.run(debug=True, host='0.0.0.0', port=5000)