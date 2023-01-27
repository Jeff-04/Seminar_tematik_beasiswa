import sqlite3

conn = sqlite3.connect('data_beasiswa_smp.db')
c = conn.cursor()

# Table Siswa
c.execute("""CREATE TABLE IF NOT EXISTS data_siswa(
                    Nisn_siswa INTEGER PRIMARY KEY,
                    Password_siswa VARCHAR(255) NOT NULL,
                    Nama_siswa VARCHAR(255) NOT NULL,
                    Kelas_siswa INTEGER NOT NULL,
                    Alamat_siswa TEXT NOT NULL,
                    Status_siswa VARCHAR(255) NOT NULL,
                    Pendapatan_ortu VARCHAR(255) NOT NULL,
                    Pip_siswa VARCHAR(255) NOT NULL,
                    Data_dinas_sosial_siswa VARCHAR(255));
            """)
conn.commit()


# Table Admin
c.execute("""CREATE TABLE IF NOT EXISTS admin(
                    Nisn_admin INTEGER PRIMARY KEY,
                    Password_admin VARCHAR(255) NOT NULL);
          """)
conn.commit()


# Table Pengumuman
c.execute("""CREATE TABLE IF NOT EXISTS pengumuman(
                    Id_pengumuman INTEGER PRIMARY KEY AUTOINCREMENT,
                    Nama_beasiswa VARCHAR(255) NOT NULL,
                    Nisn_siswa VARCHAR(255) NOT NULL,
                    Rangking INT NOT NULL,
                    FOREIGN KEY (Nisn_siswa) REFERENCES Persons(Nisn_siswa));
          """)
conn.commit()


# Table Beasiswa
c.execute("""CREATE TABLE IF NOT EXISTS beasiswa(
                    Subject VARCHAR(255) PRIMARY KEY,
                    open_date DATE NOT NULL,
                    close_date DATE NOT NULL,
                    Body TEXT NOT NULL);
          """)
conn.commit()

# Table Pendafataran
c.execute("""CREATE TABLE IF NOT EXISTS pendafaran(
                    Id_pendafaran INTEGER PRIMARY KEY AUTOINCREMENT,
                    Subject_beasiswa VARCHAR(255) NOT NULL,
                    Nisn_siswa INTEGER NOT NULL,
                    FOREIGN KEY (Subject_beasiswa) REFERENCES Persons(Subject),
                    FOREIGN KEY (Nisn_siswa) REFERENCES Persons(Nisn_siswa));
          """)
conn.commit()

c.execute("INSERT INTO admin VALUES(5190411609,'Kuningan123');")
conn.commit()

# c.execute("SELECT * FROM data_siswa;")
# one_result = c.fetchall()
# print(one_result)
c.close()
conn.close()
