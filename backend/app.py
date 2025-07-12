from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pymysql
import redis
import os
import bcrypt
from werkzeug.utils import secure_filename
from datetime import timedelta, datetime
from functools import wraps
from apscheduler.schedulers.background import BackgroundScheduler

# ================ Konfigurasi Aplikasi ================
app = Flask(__name__)
app.secret_key = 'secret_key_po_kantin'
app.permanent_session_lifetime = timedelta(days=1)
CORS(app, supports_credentials=True)

# ================ Redis dan Flask-Limiter ================
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
limiter = Limiter(get_remote_address, app=app, storage_uri="redis://localhost:6379", enabled=False)

# ================ Konfigurasi Upload Folder ================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
UPLOAD_MENU_FOLDER = os.path.join(BASE_DIR, 'uploads', 'menu')
UPLOAD_BUKTI_FOLDER = os.path.join(BASE_DIR, 'uploads', 'bukti')
os.makedirs(UPLOAD_MENU_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_BUKTI_FOLDER, exist_ok=True)

app.config['UPLOAD_MENU_FOLDER'] = UPLOAD_MENU_FOLDER
app.config['UPLOAD_BUKTI_FOLDER'] = UPLOAD_BUKTI_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ================ Koneksi Database MySQL ================
def get_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='po_makanan',
        cursorclass=pymysql.cursors.DictCursor
    )

# ================ Middleware Role ================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'message': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user', {}).get('role') != 'admin':
            return jsonify({'message': 'Akses ditolak'}), 403
        return f(*args, **kwargs)
    return decorated_function

# =================== AUTH ===================
@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    data = request.json
    email = data['email']
    password = data['password'].encode('utf-8')
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM user WHERE email=%s", (email,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password, user['password'].encode('utf-8')):
            session.permanent = True
            session['user'] = {'id': user['id'], 'role': user['role']}
            return jsonify({'message': 'Login sukses', 'role': user['role'], 'id': user['id'], 'nama': user['nama']}), 200
        return jsonify({'message': 'Login gagal'}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    nama = data.get('nama')
    email = data.get('email')
    password = data.get('password')
    no_telp = data.get('no_telp')

    if not all([nama, email, password, no_telp]):
        return jsonify({'message': 'Semua field wajib diisi'}), 400
    
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM user WHERE email=%s", (email,))
        if cursor.fetchone():
            return jsonify({'message': 'Email sudah digunakan'}), 400
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("""
            INSERT INTO user (nama, email, password, no_telp, role)
            VALUES (%s, %s, %s, %s, 'pembeli')
        """, (nama, email, hashed_password, no_telp))
        db.commit()
    return jsonify({'message': 'Registrasi berhasil'})

@app.route('/admin/users', methods=['GET'])
@admin_required
def daftar_user():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT id, nama, email, no_telp, role FROM user")
        users = cursor.fetchall()
    return jsonify(users)

@app.route('/user/edit', methods=['PUT'])
@login_required
def edit_profil():
    data = request.json
    nama = data.get('nama')
    email = data.get('email')
    no_telp = data.get('no_telp')

    user_id = session['user']['id']
    
    db = get_db()
    with db.cursor() as cursor:
        # Cek apakah email sudah digunakan oleh user lain
        cursor.execute("SELECT id FROM user WHERE email = %s AND id != %s", (email, user_id))
        existing = cursor.fetchone()
        if existing:
            return jsonify({'message': 'Email sudah digunakan oleh pengguna lain'}), 400

        # Lakukan update profil
        cursor.execute("""
            UPDATE user SET nama=%s, email=%s, no_telp=%s WHERE id=%s
        """, (nama, email, no_telp, user_id))
        db.commit()
    
    return jsonify({'message': 'Profil berhasil diperbarui'})

@app.route('/user/profile', methods=['GET'])
@login_required
def lihat_profil():
    user_id = session['user']['id']
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT nama, email, no_telp FROM user WHERE id=%s", (user_id,))
        user = cursor.fetchone()
    return jsonify(user)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'message': 'Logged out'})

# =================== MENU (admin only) ===================
@app.route('/upload-menu', methods=['POST'])
@admin_required
def upload_menu():
    if 'gambar' not in request.files:
        return jsonify({'message': 'File gambar tidak ditemukan'}), 400
    file = request.files['gambar']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'message': 'File tidak valid'}), 400

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_MENU_FOLDER'], filename))

    nama = request.form.get('namaMenu')
    harga = request.form.get('harga')
    stok = request.form.get('stok')
    kategori = request.form.get('kategori')

    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("INSERT INTO menu (namaMenu, harga, stok, kategori, gambar) VALUES (%s, %s, %s, %s, %s)",
                       (nama, harga, stok, kategori, filename))
        db.commit()
        return jsonify({'message': 'Menu berhasil ditambahkan'})


@app.route('/menu', methods=['GET'])
def get_menu():
    db = get_db()
    try:
        with db.cursor() as cursor:
            # Ambil hanya menu yang aktif
            cursor.execute("SELECT * FROM menu")
            result = cursor.fetchall()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route('/menu/<int:idMenu>', methods=['GET'])
def get_single_menu(idMenu):
    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM menu WHERE idMenu = %s AND isActive = 1", (idMenu,))
            result = cursor.fetchone()
            if result:
                return jsonify(result)
            else:
                return jsonify({"error": "Menu not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
    
@app.route('/menu/update/<int:idMenu>', methods=['PUT'])
@admin_required
def update_menu(idMenu):
    data = request.get_json()
    # List untuk menampung bagian SET dari query
    set_clauses = []
    # List untuk menampung nilai yang akan di-update
    values = []

    if 'nama' in data:
        set_clauses.append("namaMenu = %s")
        values.append(data['nama'])
    if 'harga' in data:
        set_clauses.append("harga = %s")
        values.append(data['harga'])
    if 'stok' in data:
        set_clauses.append("stok = %s")
        values.append(data['stok'])
    if 'kategori' in data:
        set_clauses.append("kategori = %s")
        values.append(data['kategori'])
    if 'gambar' in data:
        # Asumsi 'gambar' adalah nama file (string)
        set_clauses.append("gambar = %s")
        values.append(data['gambar'])
    
    if not set_clauses:
        return jsonify({"error": "No valid fields provided for update."}), 400
    
    # Gabungkan semua bagian SET menjadi satu string
    set_query_part = ", ".join(set_clauses)
    
    # Buat query SQL lengkap
    sql_query = f"UPDATE menu SET {set_query_part} WHERE idMenu = %s"
    
    # Tambahkan idMenu ke akhir list values
    values.append(idMenu)
    
    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute(sql_query, tuple(values))
            db.commit()
            if cursor.rowcount == 0:
                return jsonify({
                    "message": f"No changes made to menu with id {idMenu}.",
                    "menu_id": idMenu,
                    "updated_data": data
                }), 200
        
        return jsonify({
                "message": "Menu updated successfully!",
                "menu_id": idMenu,
                "updated_data": data
            }),200
    except pymysql.connector.Error as err:
        db.rollback() # Batalkan perubahan jika ada error
        return jsonify({"error": f"Failed to update menu: {err}"}), 500
    finally:
        db.close()

@app.route('/menu/delete/<int:idMenu>', methods=['DELETE'])
@admin_required
def delete_menu(idMenu):
    """
    Melakukan soft delete: Mengubah status menu menjadi tidak aktif (is_active = 0)
    daripada menghapusnya secara permanen.
    """
    db = get_db()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with db.cursor() as cursor:
            # Query UPDATE untuk menonaktifkan menu, bukan DELETE
            sql_query = "UPDATE menu SET isActive = 0 WHERE idMenu = %s"
            values = (idMenu,) 
            cursor.execute(sql_query, values)
            
            if cursor.rowcount == 0:
                return jsonify({"error": f"Menu with id {idMenu} not found or already inactive."}), 404
        
        db.commit()
        
        return jsonify({
            "message": "Menu successfully archived (soft deleted)!",
            "archived_menu_id": idMenu
        })
    except pymysql.Error as err:
        db.rollback()
        return jsonify({"error": f"Failed to archive menu: {err}"}), 500
    finally:
        db.close()

@app.route('/menu/restore/<int:idMenu>', methods=['PUT'])
@admin_required
def restore_menu(idMenu):
    """
    Mengaktifkan kembali (restore) menu yang telah diarsipkan (soft deleted)
    dengan mengubah status is_active menjadi 1.
    """
    db = get_db()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with db.cursor() as cursor:
            # Query UPDATE untuk mengaktifkan kembali menu
            sql_query = "UPDATE menu SET isActive = 1 WHERE idMenu = %s"
            values = (idMenu,)
            cursor.execute(sql_query, values)

            # Cek apakah ada baris yang di-update.
            # Jika 0, berarti menu tidak ditemukan atau memang sudah aktif.
            if cursor.rowcount == 0:
                return jsonify({"error": f"Menu with id {idMenu} not found or already active."}), 404
        
        db.commit()
        
        return jsonify({
            "message": "Menu successfully restored!",
            "restored_menu_id": idMenu
        })
    except pymysql.Error as err:
        db.rollback()
        return jsonify({"error": f"Failed to restore menu: {err}"}), 500
    finally:
        db.close()

@app.route('/admin/statistik/<string:tanggal>', methods=['GET'])
@admin_required
def statistik_lengkap_harian(tanggal):
    """
    Endpoint lengkap untuk mendapatkan semua statistik harian dalam satu panggilan.
    Mengembalikan:
    1. Ringkasan (total pesanan dan pendapatan).
    2. Rincian penjualan per kategori.
    untuk tanggal yang spesifik dalam format YYYY-MM-DD.
    """
    # 1. Validasi format tanggal
    try:
        datetime.strptime(tanggal, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Format tanggal tidak valid. Gunakan format YYYY-MM-DD."}), 400

    db = get_db()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with db.cursor() as cursor:
            # 2. Query pertama untuk ringkasan harian (total pesanan dan pendapatan)
            query_ringkasan = """
                SELECT 
                    COUNT(idPesanan) as total_pesanan,
                    COALESCE(SUM(totalHarga), 0) as total_pendapatan
                FROM pesanan
                WHERE tanggalPesanan = %s
            """
            cursor.execute(query_ringkasan, (tanggal,))
            ringkasan = cursor.fetchone()

            # 3. Query kedua untuk penjualan per kategori pada hari itu
            query_kategori = """
                SELECT 
                    m.kategori,
                    COUNT(k.idKeranjang) as jumlah_terjual
                FROM pesanan p
                JOIN keranjang k ON p.keranjang_id = k.idKeranjang
                JOIN menu m ON k.menu_id = m.idMenu
                WHERE p.tanggalPesanan = %s
                GROUP BY m.kategori
                ORDER BY jumlah_terjual DESC
            """
            cursor.execute(query_kategori, (tanggal,))
            penjualan_kategori = cursor.fetchall()
            
            # 4. Gabungkan hasil dalam satu objek JSON
            hasil_akhir = {
                "ringkasan": ringkasan,
                "penjualan_per_kategori": penjualan_kategori
            }
            
            return jsonify(hasil_akhir)
            
    except pymysql.Error as err:
        return jsonify({"error": f"Gagal mengambil statistik: {err}"}), 500
    finally:
        if db:
            db.close()



@app.route('/gambar/menu/<filename>')
def get_gambar_menu(filename):
    return send_from_directory(app.config['UPLOAD_MENU_FOLDER'], filename)

# =================== KERANJANG ===================
@app.route('/keranjang', methods=['POST'])
@login_required
def tambah_keranjang():
    data = request.get_json(force=True)
    jumlah = int(data['jumlah'])
    user_id = session['user']['id']
    menu_id = data['menu_id']

    db = get_db()
    with db.cursor() as cursor:
        # Cek apakah menu sudah ada di keranjang user
        cursor.execute("""
            SELECT idKeranjang, jumlah, subtotal FROM keranjang
            WHERE user_id=%s AND menu_id=%s AND statusKeranjang='active'
        """, (user_id, menu_id))
        existing = cursor.fetchone()

        cursor.execute("SELECT harga FROM menu WHERE idMenu = %s", (menu_id,))
        menu = cursor.fetchone()
        if not menu:
            return jsonify({'message': 'Menu tidak ditemukan'}), 404

        harga = float(menu['harga'])

        if existing:
            # Update jumlah dan subtotal
            new_jumlah = existing['jumlah'] + jumlah
            new_subtotal = new_jumlah * harga
            cursor.execute("""
                UPDATE keranjang SET jumlah=%s, subtotal=%s
                WHERE idKeranjang=%s
            """, (new_jumlah, new_subtotal, existing['idKeranjang']))
            db.commit()
            return jsonify({'message': 'Jumlah menu di keranjang diperbarui', 'subtotal': new_subtotal})
        else:
            # Insert baru
            subtotal = jumlah * harga
            cursor.execute("""
                INSERT INTO keranjang (jumlah, subtotal, tanggalDitambahkan, user_id, menu_id, statusKeranjang)
                VALUES (%s, %s, CURDATE(), %s, %s, 'active')
            """, (jumlah, subtotal, user_id, menu_id))
            db.commit()
            return jsonify({'message': 'Ditambahkan ke keranjang', 'subtotal': subtotal})

@app.route('/keranjang/<int:user_id>', methods=['GET'])
@login_required
def lihat_keranjang(user_id):
    if user_id != session['user']['id']:
        return jsonify({'message': 'Forbidden'}), 403

    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT k.*, m.namaMenu FROM keranjang k JOIN menu m ON k.menu_id = m.idMenu WHERE k.user_id=%s AND k.statusKeranjang='active'", (user_id,))
        return jsonify(cursor.fetchall())
    
@app.route('/keranjang/delete/<int:idKeranjang>', methods=['DELETE'])
@login_required
def delete_keranjang(idKeranjang):
    """Menghapus item spesifik dari keranjang milik user yang sedang login."""
    user_id = session['user']['id']
    db = get_db()
    if not db: return jsonify({"error": "Database connection failed"}), 500

    try:
        with db.cursor() as cursor:
            # Query DELETE dengan tambahan user_id untuk keamanan
            # Memastikan user hanya bisa menghapus item miliknya sendiri
            sql_query = "DELETE FROM keranjang WHERE idKeranjang = %s AND user_id = %s"
            values = (idKeranjang, user_id)
            cursor.execute(sql_query, values)

            if cursor.rowcount == 0:
                return jsonify({"error": "Item keranjang tidak ditemukan atau Anda tidak punya akses."}), 404
        
        db.commit()
        return jsonify({"message": "Item berhasil dihapus dari keranjang."})
    except pymysql.Error as err:
        db.rollback()
        return jsonify({"error": f"Gagal menghapus item: {err}"}), 500
    finally:
        db.close()

@app.route('/keranjang/total/<int:user_id>', methods=['GET'])
@login_required
def total_harga(user_id):
    if user_id != session['user']['id']:
        return jsonify({'message': 'Forbidden'}), 403

    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT COALESCE(SUM(subtotal), 0) as total FROM keranjang WHERE user_id=%s AND statusKeranjang='active'", (user_id,))
        return jsonify(cursor.fetchone())

# =================== PESANAN ===================
@app.route('/pesan', methods=['POST'])

@login_required
def buat_pesanan():
    now = datetime.now()
    batas_awal_po = now.replace(hour=8, minute=0, second=0, microsecond=0)
    batas_akhir_po = (now + timedelta(days=1)).replace(hour=7, minute=59, second=0, microsecond=0)

    if not (batas_awal_po <= now <= batas_akhir_po):
        return jsonify({'message': 'PO hanya dapat dilakukan mulai jam 08:00 hari ini sampai jam 07:59 besok pagi'}), 403

    if 'pembayaran' not in request.files:
        return jsonify({'message': 'File pembayaran wajib dikirim'}), 400

    file = request.files['pembayaran']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'message': 'File tidak valid'}), 400

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_BUKTI_FOLDER'], filename))

    keranjang_id = request.form.get('keranjang_id')
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT k.subtotal, k.jumlah, m.idMenu, m.stok 
            FROM keranjang k 
            JOIN menu m ON k.menu_id = m.idMenu 
            WHERE k.idKeranjang = %s AND k.user_id = %s AND k.statusKeranjang = 'active'
        """, (keranjang_id, session['user']['id']))
        keranjang = cursor.fetchone()

        if not keranjang:
            return jsonify({'message': 'Keranjang tidak ditemukan atau sudah dipesan'}), 404

        if keranjang['jumlah'] > keranjang['stok']:
            return jsonify({'message': 'Stok tidak mencukupi'}), 400

        totalHarga = keranjang['subtotal']

        cursor.execute("""
            INSERT INTO pesanan (keranjang_id, pembayaran, totalHarga, statusPemesanan)
            VALUES (%s, %s, %s, 'Diproses')
        """, (keranjang_id, filename, totalHarga))

        cursor.execute("UPDATE keranjang SET statusKeranjang='ordered' WHERE idKeranjang=%s", (keranjang_id,))
        cursor.execute("UPDATE menu SET stok = stok - %s WHERE idMenu = %s", (keranjang['jumlah'], keranjang['idMenu']))
        db.commit()

    return jsonify({'message': 'Pesanan berhasil dibuat', 'totalHarga': totalHarga})

@app.route('/pesanan/<int:user_id>', methods=['GET'])
@login_required
def lihat_pesanan(user_id):
    if user_id != session['user']['id']:
        return jsonify({'message': 'Forbidden'}), 403

    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT p.*, m.namaMenu, m.harga, k.jumlah
            FROM pesanan p
            JOIN keranjang k ON p.keranjang_id = k.idKeranjang
            JOIN menu m ON k.menu_id = m.idMenu
            WHERE k.user_id=%s
        """, (user_id,))
        return jsonify(cursor.fetchall())

@app.route('/gambar/bukti/<filename>')
def get_bukti(filename):
    return send_from_directory(app.config['UPLOAD_BUKTI_FOLDER'], filename)

@app.route('/admin/pesanan', methods=['GET'])
@admin_required
def admin_pesanan():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT p.*, u.nama, m.namaMenu, k.jumlah, m.harga FROM pesanan p
            JOIN keranjang k ON p.keranjang_id = k.idKeranjang
            JOIN user u ON k.user_id = u.id
            JOIN menu m ON k.menu_id = m.idMenu
        """)
        return jsonify(cursor.fetchall())
    
@app.route('/admin/pesanan/<int:idPesanan>', methods=['PUT'])
@admin_required
def update_status_pesanan(idPesanan):
    data = request.get_json()
    status = data.get('status')
    if status not in ['Diproses', 'Selesai']:
        return jsonify({"message": "Status tidak valid"}), 400

    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute("UPDATE pesanan SET statusPemesanan=%s WHERE idPesanan=%s", (status, idPesanan))
            db.commit()
            if cursor.rowcount == 0:
                return jsonify({"message": "Pesanan tidak ditemukan"}), 404
            return jsonify({"message": "Status pesanan diperbarui"})
    except Exception as e:
        db.rollback()
        return jsonify({"message": str(e)}), 500
    finally:
        db.close()

@app.route('/reset-stok/<int:idMenu>', methods=['POST'])
@admin_required
def reset_stok(idMenu):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("UPDATE menu SET stok = 0 WHERE idMenu = %s", (idMenu,))  # default reset
        db.commit()
    return jsonify({'message': 'Stok berhasil di-reset'})

# Scheduler otomatis
scheduler = BackgroundScheduler()
scheduler.add_job(lambda: reset_stok(), 'cron', hour=8, minute=0)
scheduler.start()

# =================== CARD DASHBOARD ===================
@app.route('/dashboard', methods=['GET'])
def get_dashboard_data():
    db = get_db()
    cursor = db.cursor()  # sudah DictCursor dari get_db()

    try:
        cursor.execute("SELECT COUNT(*) as total_makanan, isActive FROM menu WHERE kategori = 'makanan' AND stok > 0")
        total_makanan = cursor.fetchone()['total_makanan']  # ← akses dict

        cursor.execute("SELECT COUNT(*) as total_minuman, isActive FROM menu WHERE kategori = 'minuman' AND stok > 0")
        total_minuman = cursor.fetchone()['total_minuman']

        cursor.execute("SELECT COUNT(*) as total_pesanan FROM pesanan WHERE statusPemesanan	= 'Diproses'")
        total_pesanan = cursor.fetchone()['total_pesanan']

        cursor.execute("SELECT SUM(totalHarga) as total_pendapatan FROM pesanan")
        result = cursor.fetchone()
        total_pendapatan = result['total_pendapatan'] if result['total_pendapatan'] else 0

        return jsonify({
            'total_makanan': total_makanan,
            'total_minuman': total_minuman,
            'total_pesanan': total_pesanan,
            'total_pendapatan': total_pendapatan
        })
    finally:
        cursor.close()
        db.close()

# =================== MAIN ===================
if __name__ == '__main__':
    app.run(debug=True, port=5000)