from flask import Flask, render_template, request, redirect, url_for, flash
from game import *
from form import *

app = Flask(__name__)
app.secret_key = 'asdfasdfasdfaskjdlhflwgejnlhus'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/formularz', methods=['POST', 'GET'])
def wypelnij_formularz():
    global gracz_1, gracz_2

    form_gracze = ImionaGraczy()

    if form_gracze.validate_on_submit() and form_gracze.potwierdz.data:
        gracz_1 = form_gracze.gracz_1.data
        gracz_2 = form_gracze.gracz_2.data

        return redirect(url_for('gra'))

    return render_template('formularz.html', form_gracze=form_gracze)


@app.route('/gra', methods=['POST', 'GET'])
def gra():
    global gra, gracz_1, gracz_2, na_stole
    gra = Game(gracz_1=gracz_1, gracz_2=gracz_2)

    gra.init_game()

    na_stole = gra.na_stole
    domino_gracza = [gra.gracze[0].domino_gracza, gra.gracze[1].domino_gracza]
    form = WybierzKostke()

    if form.validate_on_submit():
        gra.start(form.kostka.data)

        if gra.koniec:
            return render_template("koniec.html", wygrany=gra.turn)
        return redirect(url_for('gra'))

    return render_template('game.html', domino_gracza=domino_gracza, form=form, na_stole=na_stole, ruch_gracza=gra.turn, gracze=gra.imiona)


@app.route('/wyloz_kostke/<kostka>')
def wyloz_kostke(kostka):
    global gra

    if kostka not in gra.gracze[gra.turn].domino_gracza:
        flash('Brak pasujacej')

    try:
        gra.ruch_gracza(kostka)
        gra.czy_zakonczyc_gre()

        if gra.koniec:
            return redirect(url_for('koniec.html'))

        gra.zmiana_gracza()

    except AssertionError as e:
        return redirect(url_for('dobierz_kostke'))

    return redirect(url_for('gra'))


@app.route('/dobierz_kostke')
def dobierz_kostke():
    global gra
    gra.ruch_gracza()
    gra.zmiana_gracza()

    return redirect(url_for('gra'))


@app.route('/koniec_gry')
def koniec():
    global gra

    wygrany = gra.imiona[gra.turn]
    przegrany = gra.imiona[(gra.turn + 1) % 2]

    koniec_gry = gra.koniec

    return render_template('koniec.html', wygrany=wygrany[0], przegrany=przegrany[0], koniec_gry=koniec_gry)


if __name__ == "__main__":
    app.run(debug=True)
