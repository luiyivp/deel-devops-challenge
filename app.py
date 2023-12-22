from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

db = SQLAlchemy(app)

class ReverseIP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_ip = db.Column(db.String(15))
    reversed_ip = db.Column(db.String(15))

@app.route('/')
def get_reverse_ip():
    original_ip = request.remote_addr
    reversed_ip = '.'.join(reversed(original_ip.split('.')))

    reverse_ip_entry = ReverseIP(original_ip=original_ip, reversed_ip=reversed_ip)
    db.session.add(reverse_ip_entry)
    db.session.commit()

    return f'Your IP: {original_ip} | Reverse IP: {reversed_ip}'

@app.route('/ips')
def get_all_ips():
    with app.app_context():
        all_entries = ReverseIP.query.all()

    entries_list = [
        {'original_ip': entry.original_ip, 'reversed_ip': entry.reversed_ip}
        for entry in all_entries
    ]

    return jsonify({'ips': entries_list})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=5000)
