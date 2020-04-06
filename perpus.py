import mysql.connector
import os

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="perpustakaan"
)

cursor = db.cursor()

def tambah_data(db):
	kode = input("ID Buku        : ")
	judul = input("Judul Buku     : ")
	nama = input("Nama Pengarang : ")
	sql = "INSERT INTO data_buku (id, judul, pengarang) VALUES (%s, %s, %s)"
	val = (kode, judul, nama)
	cursor.execute(sql, val)
	
	db.commit()
	
	os.system("clear")
	print("Data Berhasil Ditambahkan")
	
def cari_data(db):
	kata = input("Kata Kunci = ")
	sql = "SELECT * FROM data_buku WHERE id LIKE %s OR judul LIKE %s OR pengarang LIKE %s"
	val = ("%{}%".format(kata),"%{}%".format(kata), "%{}%".format(kata))
	cursor.execute(sql, val)
	result = cursor.fetchall()
	
	os.system("clear")
	print("Hasil Pencarian :")
	
	for data in result:
		print(data)
	print("")
	
def cari_anggota(db):
	kata = input("Kata Kunci = ")
	sql = "SELECT * FROM data_peminjam WHERE id LIKE %s OR nama LIKE %s"
	val = ("%{}%".format(kata),"%{}%".format(kata))
	cursor.execute(sql, val)
	result = cursor.fetchall()
	
	os.system("clear")
	print("Hasil Pencarian :")
	
	for data in result:
		print(data)
	print("")

def tambah_anggota(db):
	kode = input("ID Anggota	: ")
	nama = input("Nama Anggota	: ")
	sql = "INSERT INTO data_peminjam (id, nama) VALUES (%s, %s)"
	val = (kode, nama)
	cursor.execute(sql,val)
	
	db.commit()
	
	sql = """CREATE TABLE {}_{}(
				id VARCHAR(256) PRIMARY KEY,
				judul VARCHAR(256),
				pengarang VARCHAR(256)
				)"""
				
	cursor.execute(sql.format(kode,nama))
	
	os.system("clear")
	print("Penambahan Anggota Berhasil!")
	print("")

def peminjaman(db):
	kode_anggota = input("ID Anggota : ")
	kode_buku = input("ID Buku    : ")
	
	cursor.execute("SELECT * FROM data_peminjam WHERE id = '"+kode_anggota+"' ")
	obj = cursor.fetchall()
	for row in obj :
		nama_anggota = row[1]
	
	cursor.execute("SELECT * FROM data_buku WHERE id = '"+kode_buku+"' ")
	obj = cursor.fetchall()
	for row in obj :
		judul = row[1]
		pengarang = row[2]
	
	cursor.execute("INSERT INTO "+kode_anggota+"_"+nama_anggota+"(id, judul, pengarang) VALUES (%s, %s, %s)", (kode_buku, judul, pengarang))
	cursor.execute("DELETE FROM data_buku WHERE id = '"+kode_buku+"'")
	
	db.commit()
	
	print(nama_anggota+"("+kode_anggota+") telah meminjam buku "+judul+"("+kode_buku+") karya "+pengarang)
	print("")
	
def pengembalian(db):
	kode_anggota = input("ID Anggota : ")
	kode_buku = input("ID Buku    : ")
	
	cursor.execute("SELECT * FROM data_peminjam WHERE id = '"+kode_anggota+"' ")
	obj = cursor.fetchall()
	for row in obj :
		nama_anggota = row[1]
	
	cursor.execute("SELECT * FROM "+kode_anggota+"_"+nama_anggota+" WHERE id = '"+kode_buku+"' ")
	obj = cursor.fetchall()
	
	judul = "-"
	for row in obj :
		judul = row[1]
		pengarang = row[2]
	
	if judul != "-"	:
		cursor.execute("INSERT INTO data_buku(id, judul, pengarang) VALUES (%s, %s, %s)", (kode_buku, judul, pengarang))	
		cursor.execute("DELETE FROM "+kode_anggota+"_"+nama_anggota+" WHERE id = '"+kode_buku+"'")
	
	db.commit()
	if judul=="-" :
		print(nama_anggota+"("+kode_anggota+") mengembalikan buku dengan ID yang salah, mohon periksa ID yang benar di daftar tagihan")
	else :
		print(nama_anggota+"("+kode_anggota+") telah mengembalikan buku "+judul+"("+kode_buku+") karya "+pengarang)
	print("")
	
def tagihan(db):
	kode_anggota = input("ID Anggota : ")	
	
	cursor.execute("SELECT * FROM data_peminjam WHERE id = '"+kode_anggota+"' ")
	obj = cursor.fetchall()
	for row in obj :
		nama_anggota = row[1]
		
	cursor.execute("SELECT * FROM "+kode_anggota+"_"+nama_anggota)
	result = cursor.fetchall()
	
	for data in result:
		print(data)
	print("")
	
def beranda(db):
	print("=============================")
	print("===      Perpustakaan     ===")
	print("=============================")
	print("=== 1 Tambahkan Data Buku ===")
	print("=== 2 Cari Data Buku      ===")
	print("=== 3 Tambahkan Anggota   ===")
	print("=== 4 Cari Anggota        ===")
	print("=== 5 Peminjaman          ===")
	print("=== 6 Pengembalian        ===")
	print("=== 7 Tagihan Buku        ===")
	print("=== 0 Keluar              ===")
	print("=============================")
	print("===  Created By : Adivii  ===")
	print("=============================")
	print("")
	
	x=input("=>> ")
	
	os.system("clear")
	
	if x=="1" :
		tambah_data(db)
	elif x=="2" :
		cari_data(db)
	elif x=="3" :
		tambah_anggota(db)
	elif x=="4" :
		cari_anggota(db)
	elif x=="5" :
		peminjaman(db)
	elif x=="6":
		pengembalian(db)
	elif x=="7":
		tagihan(db)
	elif x=="0" :
		exit()
	else :
		print("Masukkan Salah")

if __name__=="__main__":
	while(True):
		beranda(db)
