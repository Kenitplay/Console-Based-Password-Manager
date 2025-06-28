from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text 
import hashlib
import os

app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passwords.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


if not os.path.exists("passwords.db"):
    print("Creating new database.")
else:
    try:
        with app.app_context():
            db.session.execute("SELECT password_plain FROM credential LIMIT 1")
    except Exception:
        print("Rebuilding database due to schema mismatch.")
        os.remove("passwords.db")


def sha256(text_input):
    return hashlib.sha256(text_input.encode()).hexdigest()


class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password_plain = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)


@app.route('/credentials', methods=['GET'])
def list_credentials():
    creds = Credential.query.order_by(Credential.id).all()
    return jsonify([
        {
            "id": c.id,
            "site": c.site,
            "username": c.username,
            "password": c.password_plain,
            "hash": c.password_hash
        } for c in creds
    ])

@app.route('/credentials', methods=['POST'])
def add_credential():
    try:
        data = request.get_json(force=True)
        plain = data['password']
        new_cred = Credential(
            site=data['site'],
            username=data['username'],
            password_plain=plain,
            password_hash=sha256(plain)
        )
        db.session.add(new_cred)
        db.session.commit()
        return jsonify({"message": "Added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/credentials/<int:cred_id>', methods=['PUT'])
def update_credential(cred_id):
    cred = Credential.query.get_or_404(cred_id)
    data = request.get_json(force=True)
    if 'site' in data:
        cred.site = data['site']
    if 'username' in data:
        cred.username = data['username']
    if 'password' in data:
        cred.password_plain = data['password']
        cred.password_hash = sha256(data['password'])
    db.session.commit()
    return jsonify({"message": "Updated"}), 200


@app.route('/credentials/<int:cred_id>', methods=['DELETE'])
def delete_credential(cred_id):
    cred = Credential.query.get_or_404(cred_id)
    db.session.delete(cred)
    db.session.commit()

   
    creds = Credential.query.order_by(Credential.id).all()
    for index, c in enumerate(creds, start=1):
        c.id = index
    db.session.commit()


    db.session.execute(text("DELETE FROM sqlite_sequence WHERE name='credential'"))
    db.session.commit()

    return jsonify({"message": "Deleted and IDs reassigned"}), 200


if _name_ == '_main_':
    with app.app_context():
        db.create_all()
    print("📡 Server running on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000)
