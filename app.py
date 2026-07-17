import os
from flask import Flask,render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Membuat jalur absolut yang aman untuk Windows maupun Linux
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Produk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama= db.Column(db.String(100), nullable=False)
    harga= db.Column(db.Integer, nullable=False)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nama_produk=request.form['nama']
        harga_produk=request.form['harga']

        baru=Produk(nama=nama_produk, harga=harga_produk)
        db.session.add(baru)
        db.session.commit()
        return redirect(url_for('index'))
    semua_produk=Produk.query.all()
    return render_template('index.html', produk=semua_produk)

@app.route('/hapus/<int:id>')
def hapus(id):
    produk_hapus=Produk.query.get_or_404(id)
    db.session.delete(produk_hapus)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
