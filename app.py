from flask import jsonify, Flask, url_for, request, redirect
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from flask_cors import CORS


app = Flask(__name__)
app.config['SECRET-KEY'] = 'bismillah'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///kasir_api.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)
CORS(app)



# --------------------------------------------------------------
# ---------------------- DB CONFIGURATION ----------------------
# --------------------------------------------------------------


class Kategori(db.Model):
    __tablename__ = "kategori"
    id_kategori = db.Column(db.Integer, primary_key = True)
    nama_kategori = db.Column(db.String(100), unique = True, nullable = False)


class Makanan(db.Model):
    __tablename = "makanan"
    id_makanan = db.Column(db.Integer, primary_key = True)
    nama_makanan = db.Column(db.String, nullable = False, unique = True)
    harga = db.Column(db.Integer, nullable = False)
    kategori_id = db.Column(db.Integer)


db.create_all()



# --------------------------------------------------------------
# ----------------------------- API ----------------------------
# --------------------------------------------------------------



@app.route('/')
def awal():
    return "REST API Kasir"


##### ----------------------- KATEGORI ----------------------- #####

@app.route('/get_all_kategori')
def get_all_kategori():

    all_kategori = Kategori.query.all()
    kategori_dict = []
    for kategori in all_kategori:
        data = {
            'id' : kategori.id_kategori,
            'nama_kategori' : kategori.nama_kategori
        }
        kategori_dict.append(data)

    json_return = kategori_dict

    json_return = jsonify(json_return)
    json_return.headers.add_header('Access-Control-Allow-Origin', '*')
    return json_return

@app.route('/get_kategori')
def get_kategori():
    id = request.args.get('id')
    kategori = Kategori.query.filter_by(id_kategori = id).first()
    return_json = {
        "id" : kategori.id_kategori,
        'nama_kategori' : kategori.nama_kategori
    }

    return_json = jsonify(return_json)
    return_json.headers.add_header('Access-Control-Allow-Origin', '*')
    return return_json


@app.route('/tambah_kategori', methods = ['POST'])
def tambah_kategori():

    check_req = request.headers.get('Content-Type')
    if check_req == 'application/json':
        try:
            nama_kategori = request.get_json()['nama_kategori']
            kategori = Kategori(
                nama_kategori = nama_kategori
            )
            db.session.add(kategori)
            db.session.commit()

            json_return = {
                "Berhasil" : f"Berhasil tambah kategori : {nama_kategori}"
            }

        except:
            json_return = {
                "Gagal": f"Gagal tambah kategori : {nama_kategori}, kemungkinan kategori tersebut sudah ada"
            }

    json_return = jsonify(json_return)
    json_return.headers.add_header('Access-Control-Allow-Origin', '*')
    return json_return


@app.route('/hapus_kategori')
def hapus_kategori():
    id = request.args.get('id')
    kategori_hapus = Kategori.query.get(id)
    if kategori_hapus:
        db.session.delete(kategori_hapus)
        db.session.commit()
        json_return = {
            "Berhasil" : f"Berhasil hapus kategori : { kategori_hapus.nama_kategori }"
        }

    json_return = jsonify(json_return)
    json_return.headers.add_header('Access-Control-Allow-Origin', '*')
    return json_return


@app.route('/edit_kategori', methods = ['POST'])
def edit_kategori():

    request.access_control_request_headers
    check = request.headers.get('Content-Type')
    if check == 'application/json':
        data_edit = request.get_json()
        id = data_edit['id']
        nama_baru = data_edit['nama']

        kategori_edit = Kategori.query.get(id)
        nama_lama = kategori_edit.nama_kategori

        kategori_edit.nama_kategori = nama_baru
        db.session.commit()

        json_return = {
            "Berhasil" : f"Berhasil ubah nama_kategori dari : {nama_lama} diubah jadi : {nama_baru}"
        }


    json_return = jsonify(json_return)
    json_return.headers.add_header('Access-Control-Allow-Origin', '*')
    return json_return







##### ----------------------- MAKANAN ----------------------- #####

@app.route('/get_all_makanan')
def get_all_makanan():

    all_makanan = Makanan.query.all()
    makanan_dict = []
    for makanan in all_makanan:
        data = {
            'id' : makanan.id_makanan,
            'nama' : makanan.nama_makanan ,
            'harga' : makanan.harga,
             'kategori' : makanan.kategori_id
        }
        makanan_dict.append(data)

    json_return = makanan_dict

    json_return = jsonify(json_return)

    json_return.headers.add_header('Access-Control-Allow-Origin', '*')
    return json_return


@app.route('/get_makanan')
def get_makanan():
    id = request.args.get('id')
    makanan = Makanan.query.filter_by(id_makanan = id).first()
    json_return = {
        'id': makanan.id_makanan,
        'nama': makanan.nama_makanan,
        'harga': makanan.harga,
        'kategori': makanan.kategori_id
    }

    json_return = jsonify(json_return)
    json_return.headers.add_header('Access-Control-Allow-Origin', '*')
    return json_return





@app.route('/tambah_makanan', methods = ['POST'])
def tambah_makanan():

    request.access_control_request_headers
    req_check = request.headers.get('Content-Type')
    if req_check == "application/json":
        data = request.get_json()
        nama = data['nama_makanan']
        harga = data['harga']
        kategori_id = data['id_kategori']

        makanan_baru = Makanan(
            nama_makanan = nama,
            harga = harga,
            kategori_id = kategori_id
        )

        db.session.add(makanan_baru)
        db.session.commit()

        json_return = {
            'Berhasil' : f'Berhasil tambahkan makanan : {nama}'
        }


    json_return = jsonify(json_return)
    json_return.headers.add_header('Access-Control-Allow-Origin', '*')
    return  json_return


@app.route('/edit_makanan', methods = ['POST'])
def edit_makanan():

    request.access_control_request_headers
    req_check = request.headers.get('Content-Type')
    if req_check == 'application/json':
        data = request.get_json()
        id_makanan = data['id_makanan']
        nama_baru = data['nama_baru']
        harga_baru = data['harga_baru']
        kategori_id = data['kategori_id']

    makanan_edit = Makanan.query.get(id_makanan)
    nama_lama = makanan_edit.nama_makanan

    makanan_edit.nama_makanan = nama_baru
    makanan_edit.harga = harga_baru
    makanan_edit.kategori_id = kategori_id

    db.session.commit()
    json_return = {
        "Berhasil" : f"Berhasil Ubah Info Makanan"
    }

    json_return = jsonify(json_return)
    json_return.headers.add_header('Access-Control-Allow-Origin', '*')
    return json_return


@app.route('/hapus_makanan')
def hapus_makanan():

    id = request.args.get('id')
    makanan_hapus = Makanan.query.get(id)
    db.session.delete(makanan_hapus)
    db.session.commit()

    json_return = {
        "Berhasil" : f"Berhasil hapus makanan : {makanan_hapus.nama_makanan}"
    }

    json_return = jsonify(json_return)
    json_return.headers.add_header('Access-Control-Allow-Origin', '*')
    return json_return






if __name__ == "__main__":
    app.run(debug= True)