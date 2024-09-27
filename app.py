from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Sostituisci con una chiave segreta reale per la produzione

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'teams' not in session:
        session['teams'] = []
    if 'players' not in session:
        session['players'] = []

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add_team':
            team_name = request.form.get('team_name')
            if team_name:
                session['teams'].append(team_name)
                session.modified = True
        elif action == 'add_player':
            player_name = request.form.get('player_name')
            if player_name:
                session['players'].append(player_name)
                session.modified = True
        return redirect(url_for('home'))

    return render_template('home.html', teams=session['teams'], players=session['players'])

@app.before_request
def make_session_permanent():
    session.permanent = True


@app.route('/draw', methods=['GET'])
def draw():
    if 'teams' in session and 'players' in session:
        pairs = []
        teams = session['teams'].copy()
        players = session['players'].copy()
        while teams and players:
            team = random.choice(teams)
            player = random.choice(players)
            pairs.append((team, player))
            teams.remove(team)
            players.remove(player)
        return render_template('draw.html', pairs=pairs)
    return redirect(url_for('home'))


@app.route('/update_items', methods=['POST'])
def update_items():
    action = request.json['action']
    name = request.json['name']
    type = request.json['type']

    if action == 'delete':
        if type == 'team' and name in session['teams']:
            session['teams'].remove(name)
        elif type == 'player' and name in session['players']:
            session['players'].remove(name)
        session.modified = True

    elif action == 'edit':
        newName = request.json['newName']
        if type == 'team' and name in session['teams']:
            index = session['teams'].index(name)
            session['teams'][index] = newName
        elif type == 'player' and name in session['players']:
            index = session['players'].index(name)
            session['players'][index] = newName
        session.modified = True

    return jsonify(success=True)

def clean_input(input_string):
    """Utility function to clean user input before storing it in the session."""
    return input_string.strip()

if __name__ == '__main__':
    app.run(debug=True)
