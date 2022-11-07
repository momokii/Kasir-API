from flask import jsonify, Flask, url_for, request, redirect
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

app = Flask(__name__)
app.config['SECRET-KEY'] = 'bismillah'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///kasir_api.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)



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
    try:
        all_kategori = Kategori.query.all()
        kategori_dict = {}
        for kategori in all_kategori:
            kategori_dict[kategori.id_kategori] = kategori.nama_kategori

        json_return = kategori_dict
    except:
        json_return = {
            "Gagal" : "Gagal Mengambil data seluruh Kategori"
        }

    json_return = jsonify(json_return)
    json_return.headers.add_header('Access-Control-Allow-Origin', '*')
    return json_return


@app.route('/tambah_kategori')
def tambah_kategori():
    try:
        nama_kategori = request.args.get('nama_kategori')
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
    try:
        id = request.args.get('id')
        kategori_hapus = Kategori.query.get(id)
        if kategori_hapus:
            db.session.delete(kategori_hapus)
            db.session.commit()
            json_return = {
                "Berhasil" : f"Berhasil hapus kategori : { kategori_hapus.nama_kategori }"
            }
        else:
            json_return = {
                "Gagal" : "ID dimasukan tidak ditemukan!"
            }
    except:
        json_return = {
            "Gagal" : "Penghapusan kategori gagal!"
        }
    finally:
        json_return = jsonify(json_return)
        json_return.headers.add_header('Access-Control-Allow-Origin', '*')
        return json_return


@app.route('/edit_kategori')
def edit_kategori():
    try:
        id = request.args.get('id')
        nama_baru = request.args.get('nama_ganti')

        kategori_edit = Kategori.query.get(id)
        nama_lama = kategori_edit.nama_kategori

        if kategori_edit:
            try:
                kategori_edit.nama_kategori = nama_baru
                db.session.commit()

                json_return = {
                    "Berhasil" : f"Berhasil ubah nama_kategori dari : {nama_lama} diubah jadi : {nama_baru}"
                }
            except:
                json_return = {
                    "Gagal" : f"Gagal ubah kategori dari {nama_lama} menjadi {nama_baru}, nama tersebut kemungkinan sudah ada"
                }
        else:
            json_return = {
                "Gagal" : "ID dicari tidak ditemukan"
            }
    except:
        json_return = {
            "Gagal" : "Edit Kategori Gagal"
        }
    finally:
        json_return = jsonify(json_return)
        json_return.headers.add_header('Access-Control-Allow-Origin', '*')
        return json_return


##### ----------------------- MAKANAN ----------------------- #####

@app.route('/get_all_makanan')
def get_all_makanan():

    all_makanan = Makanan.query.all()
    makanan_dict = {}
    for makanan in all_makanan:
        makanan_dict[makanan.id_makanan] = {
            'nama' : makanan.nama_makanan ,
            'harga' : makanan.harga,
             'kategori' : makanan.kategori_id
        }

    json_return = makanan_dict
    for data in makanan_dict:
        print(data)
    json_return = jsonify(json_return)
    json_return.headers.add_header('Access-Control-Allow-Origin', '*')
    return json_return



@app.route('/tambah_makanan')
def tambah_makanan():
    try:
        nama = request.args.get('nama_makanan')
        harga = int(request.args.get('harga'))
        kategori_id = request.args.get('id_kategori')

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

    except:
        json_return = {
            'Gagal' : f'Gagal tambahkan makanan : {nama}, kemungkinan nama tersebut sudah ada'
        }

    json_return = jsonify(json_return)
    json_return.headers.add_header('Access-Control-Allow-Origin', '*')
    return  json_return


@app.route('/edit_makanan')
def edit_makanan():
    try:
        id_makanan = request.args.get('id')
        nama_baru = request.args.get('nama_baru')
        harga_baru = request.args.get('harga_baru')
        kategori_id = request.args.get('id_kategori_baru')

        makanan_edit = Makanan.query.get(id_makanan)
        nama_lama = makanan_edit.nama_makanan
        if makanan_edit:
            try:
                makanan_edit.nama_makanan = nama_baru
                makanan_edit.harga = harga_baru
                makanan_edit.kategori_id = kategori_id

                db.session.commit()
                json_return = {
                    "Berhasil" : f"Berhasil Ubah Info Makanan"
                }
            except:
                json_return = {
                    'Gagal' : f"Gagal ubah nama dari {nama_lama} menjadi {nama_baru} tidak bisa, nama {nama_baru} sudah ada pada sistem"
                }
    except:
        json_return = {
            "Gagal" : "Edit Gagal"
        }
    finally:
        json_return = jsonify(json_return)
        json_return.headers.add_header('Access-Control-Allow-Origin', '*')
        return json_return


@app.route('/hapus_makanan')
def hapus_makanan():
    try:
        id = request.args.get('id')
        makanan_hapus = Makanan.query.get(id)
        if makanan_hapus:
            db.session.delete(makanan_hapus)
            db.session.commit()

            json_return = {
                "Berhasil" : f"Berhasil hapus makanan : {makanan_hapus.nama_makanan}"
            }
        else:
            json_return = {
                "Gagal" : f"Id dicari tidak ada"
            }
    except:
        json_return = {
            "Gagal" : "Gagal melakukan Hapus Makanan"
        }
    finally:
        json_return = jsonify(json_return)
        json_return.headers.add_header('Access-Control-Allow-Origin', '*')
        return json_return






if __name__ == "__main__":
    app.run(debug= True)