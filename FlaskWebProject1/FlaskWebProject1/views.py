"""
Routes and views for the flask application.
"""

import os
import mdutils
from collections import Counter
from ftplib import FTP
from datetime import datetime
import flask
from flask import render_template, Flask, request, url_for
from flask import jsonify
app = Flask(__name__)

import sqlalchemy
import requests
import smtplib
import random
import aiohttp
from flask_paginate import Pagination, get_page_args
class Pokemon:
    def __init__(self, id, name, url, hp, attack, defense, abilities, image):
        __tablename__ = "pokemons"
        self.id = id
        self.name = name
        self.url = url
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.abilities = abilities
        self.image = image
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

def pagination(offset=0, per_page=100):
    cursor = conn.raw_connection().cursor()
    cursor.execute("SELECT * FROM pokemons")
    result = cursor.fetchall()
    return result[offset: offset+100]

@app.route("/pokemon/<pokemon>", methods=['GET', 'POST'])
def contact(pokemon):
    """Renders the contact page."""
    cursor = conn.raw_connection().cursor()
    cursor.execute(f"SELECT * FROM pokemons WHERE name = '{pokemon}'")
    result = cursor.fetchone()
    cursor.execute(f"SELECT * FROM feedbacks WHERE pokemon_id = {result[0]}")
    if request.method == 'POST':
        feedbck = request.form.get('text-feedback')
        rate = request.form.get('rate')
        cursor = conn.raw_connection().cursor()
        result = cursor.execute(f"SELECT * FROM pokemons WHERE name = '{pokemon}'")
        result = cursor.fetchone()
        cursor.execute(f"INSERT INTO feedbacks(pokemon_id, feedback, rate) VALUES ({result[0]}, '{feedbck}', '{rate}')")
    cursor.execute(f"SELECT * FROM feedbacks WHERE pokemon_id = '{result[0]}'")
    feedbacks = cursor.fetchall()
    return render_template(
        'contact.html',
        pokemon=result,
        feedbacks=feedbacks, 
        title=f"Информация о покемоне {pokemon}",
        message='Your contact page.'
    )

@app.route("/save/<pokemon>", methods=['GET', 'POST'])
def save_pokemon(pokemon):
    ftp = FTP('127.0.0.1')
    ftp.login('user', 'ftp_password')
    cursor = conn.raw_connection().cursor()
    cursor.execute(f"SELECT * FROM pokemons WHERE name = '{pokemon}'")
    pokemon = cursor.fetchone()  
    md = mdutils.MdUtils(file_name=f'{pokemon[1]}', title=f'{pokemon[1]}')
    md.write(f'HP: {pokemon[2]}\nАтака: {pokemon[3]}\nЗащита: {pokemon[4]}\nСпособности: {pokemon[5]}')
    md.create_md_file()
    folder_name = datetime.now().strftime('%Y-%m-%d')
    ftp.mkd(folder_name)
    ftp.cwd(folder_name)
    file_ftp = open(f'{pokemon[1]}.md', 'rb')
    ftp.storbinary(f'STOR {pokemon[1]}.md', file_ftp)
    ftp.close()
    return render_template(
        'save.html',
        pokemon=pokemon[1],
        )


@app.route("/pokemon/random", methods=['GET', 'POST'])
def randomed():
    """Renders the contact page."""
    cursor = conn.raw_connection().cursor()
    cursor.execute("SELECT * FROM pokemons")
    result = cursor.fetchall()
    rand = random.randint(1, len(result))
    cursor.execute(f"SELECT * FROM pokemons WHERE id = '{rand}'")
    result = cursor.fetchone()
    cursor.execute(f"SELECT * FROM feedbacks WHERE pokemon_id = {rand}")
    feedbacks = cursor.fetchall()
    return render_template(
        'contact.html',
        pokemon=result,
        feedbacks=feedbacks, 
        title=f"Информация о покемоне {result[1]}",
        message='Your contact page.'
    )
@app.route('/search', methods=['GET', 'POST'])
def search():
    print('search')
    p, per_p, offset = get_page_args()
    per_p = 100
    cursor = conn.raw_connection().cursor()
    cursor.execute(f"SELECT * FROM pokemons WHERE name ILIKE '{request.form.get('search')}%')")
    result = cursor.fetchall()
    total = len(result)
    print(total)
    result = pagination(offset=(p - 1) * 100, per_page=100)
    paginating = Pagination(page=p, per_page=100, total=total, css_framework='bootstrap5')
    """Renders the about page."""
    return render_template(
        'about.html',
        title='Pokemons',
        data=result,
        page=p,
        per_page=per_p,
        paginating=paginating
    )

conn = sqlalchemy.create_engine("postgresql://postgres:postgres@localhost/pokemons")
@app.route('/pokemons', methods=['GET', 'POST'])
def about():
    p, per_p, offset = get_page_args()
    per_p = 100
    cursor = conn.raw_connection().cursor()
    cursor.execute("SELECT * FROM pokemons")
    result = cursor.fetchall()
    total = len(result)
    search = request.form.get('search')
    total = len(result)
    result = pagination(offset=(p - 1) * 100, per_page=100)
    paginating = Pagination(page=p, per_page=100, total=total, css_framework='bootstrap5')
    
    return render_template(
        'about.html',
        title=f'Pokemons',
        data=result,
        page=p,
        per_page=per_p,
        paginating=paginating
    )



@app.route('/fight/<selected>', methods=['GET', 'POST'])
def fight(selected):
    cursor = conn.raw_connection().cursor()
    cursor.execute(f"SELECT * FROM pokemons WHERE name = '{selected}'")
    pokemon = cursor.fetchone()
    cursor.execute("SELECT * FROM pokemons")
    result = cursor.fetchall()
    randomed = random.randint(1, len(result))
    cursor.execute(f"SELECT * FROM pokemons WHERE id = {randomed}")
    randomed = cursor.fetchone()
    return render_template(
        'fight.html',
        title='Fight',
        selected=pokemon,
        randomed=randomed
        )


@app.route('/fight/<selected>/vs/<randomed>/fast/', methods=['GET', 'POST'])
def fast_fight(selected, randomed):
    cursor = conn.raw_connection().cursor()
    cursor.execute(f"SELECT * FROM pokemons WHERE id = {selected}")
    pokemon = cursor.fetchone()
    pokemon_hp = pokemon[2]
    pokemon_attack = pokemon[3]
    cursor.execute(f"SELECT * FROM pokemons WHERE id = {randomed}")
    randomed = cursor.fetchone()
    randomed_hp = randomed[2]
    randomed_attack = randomed[3]
    rounds = 1
    winner = ''
    while (True):
        pokemon_number = random.randint(0, 9)
        randomed_number = random.randint(0, 9)
        if (pokemon_number % 2 == randomed_number % 2): 
            randomed_hp -= pokemon_attack
        else:
            pokemon_hp -= randomed_attack
        if pokemon_hp <= 0 or randomed_hp <= 0: break
        rounds += 1
    if randomed_hp == 0: 
            winner = pokemon[1]
    else:
            winner = randomed[1]
    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    server.login('dekanadze2103@mail.ru', os.getenv('SMTP_Password'))
    server.set_debuglevel(1)
    server.sendmail('dekanadze2103@mail.ru', 'dekanadze02.02@mail.ru', f'Привет, прошло сражение между {pokemon[1]} и {randomed[1]}. Победил {winner}, количество раундов: {rounds}.'.encode('utf-8'))
    server.quit()
    return render_template(
        'result.html',
        title='Fight',
        selected=pokemon[1],
        randomed=randomed[1],
        winner=winner,
        rounds=rounds
        )

import time
p = []
headers = {
        'Content-Type': 'application/json',
        'accept': 'application/json',
    }

Pokemons = []
@app.route('/get', methods=['GET', 'POST'])
async def get_pokemons(pokemons, count):
    conn = sqlalchemy.create_engine("postgresql://postgres:postgres@localhost/pokemons")
    async with aiohttp.ClientSession() as session:
        for number in range(0, count):
            pokemon_url = pokemons[number]['url']
            async with session.get(pokemon_url) as resp:
                pokemon = await resp.json()
                name = pokemon['name']
                hp = pokemon['stats'][0]['base_stat']
                attack = pokemon['stats'][1]['base_stat']
                defense = pokemon['stats'][2]['base_stat']
                abilities = [ability['ability']['name'] for ability in pokemon['abilities']]
                image = ''
                if pokemon['sprites']['other']['home']['front_default'] != 'null':
                    image = pokemon['sprites']['other']['home']['front_default']
                elif pokemon['sprites']['front_default'] != 'null':
                    image = pokemon['sprites']['front_default']

                conn.connect().execute(f"INSERT INTO pokemons(name, hp, attack, defense, abilities, image) values ('{name}', {hp}, {attack}, {defense}, array{abilities}, '{image}')")
def pokemon_json(j):
    try:
        print(j, requests.get(j, headers=headers).json()['abilities'])
        p.append(1)
        time.sleep(2)
    finally:
        print()
@app.route("/pokemon/<pokemon>", methods=['GET', 'POST'])
def feedback(pokemon):
        feedbck = request.form.get('text-feedback')
        rate = request.form.get('rate')
        cursor = conn.raw_connection().cursor()
        result = cursor.execute(f"SELECT * FROM pokemons WHERE name = '{pokemon}'")
        result = cursor.fetchone()
        cursor.execute(f"INSERT INTO feedbacks(pokemon_id, feedback, rate) VALUES ({result[0]}, '{feedbck}', '{rate}')")
        cursor.execute(f"SELECT * FROM feedbacks WHERE pokemon_id = '{result[0]}'")
        feedbacks = cursor.fetchall()
        cursor = conn.connect()
        return render_template(
        'contact.html',
        pokemon=result,
        feedbacks=feedbacks,
        title=f"Информация о покемоне {pokemon}",
        message='Your contact page.'
    )

count = requests.get("https://pokeapi.co/api/v2/pokemon/").json()['count']
pokemons = requests.get(f"https://pokeapi.co/api/v2/pokemon/?limit={count}").json()['results']

if __name__ == '__main__':
    app.run(debug=True)

