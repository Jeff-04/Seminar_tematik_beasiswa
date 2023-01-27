from datetime import datetime
import streamlit as st
import sqlite3
import pickle
import pandas as pd
import numpy as np

def change_date_to_db(data):
    data = data.replace('/','-')
    dt = datetime.strptime(f"{data}", '%Y-%m-%d')
    dt_new = "{}-{}-{}".format(dt.year, dt.month, dt.day)
    return dt_new

def menu():
    if st.session_state['login_user'] == '' and st.session_state['login_admin'] == '':
        menu = [["Beranda","SMART & SVM",'Pengumuman', "Akun"], ['house', 'info-circle', 'card-checklist', 'box-arrow-right']]
        return menu
    if st.session_state['login_user'] != '':
        menu = [["Beranda","SMART & SVM", st.session_state['login_user'],'Pengumuman', 'Logout'], ['house', 'info-circle', 'person', 'card-checklist', 'box-arrow-left']]
        return menu
    
    if st.session_state['login_admin'] != '':
        menu = [["Data Beasiswa","Data Siswa","Data Pendaftar", 'Logout'], ['card-checklist', 'person', 'card-checklist', 'box-arrow-left']]
        return menu
        
        
    
def insert_data_siswa(nisn_inp, pasword_inp, nama_inp, opsi_kelas_inp, alamat_inp, opsi_status_inp, penghasilan_inp, kip_inp):
    try:
        sqliteConnection = sqlite3.connect('database/data_beasiswa_smp.db')
        cursor = sqliteConnection.cursor()
        
        sqlite_insert_query = """INSERT INTO data_siswa
                               VALUES 
                              (?, ?, ?, ?, ?, ?, ?, ?, ?);
                              """
        data_tuple = (nisn_inp, pasword_inp, nama_inp, opsi_kelas_inp, alamat_inp, opsi_status_inp, penghasilan_inp, kip_inp, np.nan)
            
        cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        cursor.close()
        return ['Insert_data', 'True']
        
    except sqlite3.Error as error:
        st.write(error)
        return ['Insert_data', 'False']
    
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def edit_data_siswa_admin(nisn_inp, password_inp, nama_inp, opsi_kelas_inp, alamat_inp, opsi_status_inp, nilai_pendapatan_inp, opsi_kip_inp, nisn_ori, opti_dinas_inp):
    try:
        sqliteConnection = sqlite3.connect('database/data_beasiswa_smp.db')
        cursor = sqliteConnection.cursor()
        
        if nisn_inp != nisn_ori :
            data_tuple = (nisn_inp, password_inp, nama_inp, opsi_kelas_inp, alamat_inp, opsi_status_inp, nilai_pendapatan_inp, opsi_kip_inp, opti_dinas_inp, nisn_ori)
        
        else:
            data_tuple = (nisn_inp, password_inp, nama_inp, opsi_kelas_inp, alamat_inp, opsi_status_inp, nilai_pendapatan_inp, opsi_kip_inp, opti_dinas_inp, nisn_inp)

        sql = ''' UPDATE data_siswa
                  SET Nisn_siswa = ?,
                      Password_siswa = ?,
                      Nama_siswa = ?,
                      Kelas_siswa = ?,
                      Alamat_siswa = ?,
                      Status_siswa = ?,
                      Pendapatan_ortu = ?,
                      Pip_siswa = ?,
                      Data_dinas_sosial_siswa = ?
                  WHERE Nisn_siswa = ?;'''
        
        cursor.execute(sql, data_tuple)
        sqliteConnection.commit()
        st.success("Update Data Berhasil")
        cursor.close()
        
    except sqlite3.Error as error:
        st.write(error)
        st.error("Update Data Gagal !")
        
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            

def edit_data(nisn_inp, password_inp, nama_inp, opsi_kelas_inp, alamat_inp, opsi_status_inp, nilai_pendapatan_inp, opsi_kip_inp, nisn_ori):
    try:
        sqliteConnection = sqlite3.connect('database/data_beasiswa_smp.db')
        cursor = sqliteConnection.cursor()
        
        if nisn_inp != nisn_ori :
            data_tuple = (nisn_inp, password_inp, nama_inp, opsi_kelas_inp, alamat_inp, opsi_status_inp, nilai_pendapatan_inp, opsi_kip_inp, nisn_ori)
        
        else:
            data_tuple = (nisn_inp, password_inp, nama_inp, opsi_kelas_inp, alamat_inp, opsi_status_inp, nilai_pendapatan_inp, opsi_kip_inp, nisn_inp)

        sql = ''' UPDATE data_siswa
                  SET Nisn_siswa = ?,
                      Password_siswa = ?,
                      Nama_siswa = ?,
                      Kelas_siswa = ?,
                      Alamat_siswa = ?,
                      Status_siswa = ?,
                      Pendapatan_ortu = ?,
                      Pip_siswa = ?
                  WHERE Nisn_siswa = ?;'''
        
        cursor.execute(sql, data_tuple)
        sqliteConnection.commit()
        st.success("Update Data Berhasil")
        cursor.close()
        
    except sqlite3.Error as error:
        st.write(error)
        st.error("Update Data Gagal !")
        
    finally:
        if sqliteConnection:
            sqliteConnection.close()

            

def biodata(nama = ''):
    try:
        sqliteConnection = sqlite3.connect('database/data_beasiswa_smp.db')
        cursor = sqliteConnection.cursor()
        if nama != '':
            statement = f"SELECT * from data_siswa WHERE Nama_siswa='{nama}';"
            cursor.execute(statement)
            rows = cursor.fetchone()
            if not rows:  # An empty result evaluates to False.
                st.error("Data Eror")
            else:
                data_empty = []
                for i in range(9):
                    data_empty.append(rows[i])
                return data_empty
            
        if nama == '':
            statement = f"SELECT * from data_siswa;"
            cursor.execute(statement)
            rows = cursor.fetchall()
            data_empty = []
            for row in rows:
                data_empty.append(row)
            return data_empty
            
                    
    except sqlite3.Error as error:
        st.error("Data Eror")
        return False
    
    finally:
        if sqliteConnection:
            sqliteConnection.close()       

def login(nisn, password):
    try:
        sqliteConnection = sqlite3.connect('database/data_beasiswa_smp.db')
        cursor = sqliteConnection.cursor()
        statement = f"SELECT Nisn_admin from admin WHERE Nisn_admin='{nisn}' AND Password_admin = '{password}';"
        row_count_admin = cursor.execute(statement)
        data_admin = cursor.fetchone()
        if not data_admin:  # An empty result evaluates to False.
            statement_new = f"SELECT Nama_siswa from data_siswa WHERE Nisn_siswa ='{nisn}' AND Password_siswa = '{password}';"
            row_count_siswa = cursor.execute(statement_new)
            data_siswa = cursor.fetchone()
            
            if not data_siswa: 
                st.error("Login Gagal")
                cursor.close()
                return ['Siswa',False]
            else:
                st.success("Login Berhasil Sebagai Siswa")
                st.session_state['login_user'] = data_siswa[0]
                cursor.close()
                return ['Siswa',True]
        else:
            st.success("Login Berhasil Sebagai Admin")
            st.session_state['login_admin'] = data_admin[0]
            cursor.close()
            return ['Admin',True]
            
    except sqlite3.Error as error:
        st.error("Insert Data Gagal !")
        return False
    
    finally:
        if sqliteConnection:
            sqliteConnection.close()

            
            
            
def delete(data_id):
    try:
        sqliteConnection = sqlite3.connect('database/data_beasiswa_smp.db')
        cursor = sqliteConnection.cursor()
        statement = f"DELETE FROM data_siswa WHERE Nisn_siswa={data_id};"
        cursor.execute(statement)
        sqliteConnection.commit()
        cursor.close()
        return True
            
    except sqlite3.Error as error:
        return False
    
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def delete_beasiswa(data_subject):
    try:
        sqliteConnection = sqlite3.connect('database/data_beasiswa_smp.db')
        cursor = sqliteConnection.cursor()
        statement = f"DELETE FROM beasiswa WHERE Subject='{data_subject}';"
        cursor.execute(statement)
        sqliteConnection.commit()
        cursor.close()
        return True
            
    except sqlite3.Error as error:
        return False
    
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def insert_beasiswa(subject_inp, start_date_inp, close_date_inp, body_inp):
    try:
        sqliteConnection = sqlite3.connect('database/data_beasiswa_smp.db')
        cursor = sqliteConnection.cursor()

        sqlite_insert_query = """INSERT INTO beasiswa
                           VALUES 
                          (?, ?, ?, ?);
                          """
        
        new_start_date = change_date_to_db(str(start_date_inp))
        new_end_date = change_date_to_db(str(close_date_inp))
        data_tuple = (subject_inp, new_start_date, new_end_date, body_inp)
        
        cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        return True
        cursor.close()
        
    except sqlite3.Error as error:
        return False
        
    finally:
        if sqliteConnection:
            sqliteConnection.close()
 

def edit_beasiswa(subject_inp, start_date_inp, close_date_inp, body_inp, data):
    try:   
        sqliteConnection = sqlite3.connect('database/data_beasiswa_smp.db')
        cursor = sqliteConnection.cursor()

        sql = ''' UPDATE beasiswa
                  SET Subject = ?,
                      open_date = ?,
                      close_date = ?,
                      Body = ?
                  WHERE Subject = ?;'''
        
        new_start_date = change_date_to_db(str(start_date_inp))
        new_end_date = change_date_to_db(str(close_date_inp))
        
        if data == subject_inp:
            data_tuple = (subject_inp, new_start_date, new_end_date, body_inp, subject_inp)
            
        if data != subject_inp:
            data_tuple = (subject_inp, new_start_date, new_end_date, body_inp, data)
        
        cursor.execute(sql, data_tuple)
        sqliteConnection.commit()
        return True
        cursor.close()
        
    except sqlite3.Error as error:
        return False
        
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        


def get_beasiswa():
    try:
        sqliteConnection = sqlite3.connect('database/data_beasiswa_smp.db')
        cursor = sqliteConnection.cursor()

        statement = f"SELECT * from beasiswa;"
        cursor.execute(statement)
        rows = cursor.fetchall()
        if not rows:
            return False
        else: 
            data_empty = []
            for row in rows:
                data_empty.append(row)
            return data_empty
        
    except sqlite3.Error as error:
        return False
        
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def insert_pendaftaran(id_siswa, subject_beasiswa):
    try:
        sqliteConnection = sqlite3.connect('database/data_beasiswa_smp.db')
        cursor = sqliteConnection.cursor()

        sqlite_insert_query = """INSERT INTO pendafaran
                           VALUES 
                          (?, ?, ?);
                          """
        
        data_tuple = (np.nan, subject_beasiswa, id_siswa)
        
        cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        return True
        cursor.close()
        
    except sqlite3.Error as error:
        return False
        
    finally:
        if sqliteConnection:
            sqliteConnection.close()
    

def get_pendaftaran(id_siswa, subject_beasiswa):
    try:
        sqliteConnection = sqlite3.connect('database/data_beasiswa_smp.db')
        cursor = sqliteConnection.cursor()

        statement = f"SELECT Nisn_siswa from data_siswa WHERE Nama_siswa = '{id_siswa}';"
        cursor.execute(statement)
        data_id = cursor.fetchone()
        if not data_id:
            return False
        else:  
            data_id_new = data_id[0]
            statement_new = f"SELECT * from pendafaran WHERE Nisn_siswa = {data_id_new} and Subject_beasiswa='{subject_beasiswa}';"
            cursor.execute(statement_new)
            rows = cursor.fetchone()
            if not rows:
                return True
            else:
                return False
            cursor.close()
        
    except sqlite3.Error as error:
        return False
        
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def data_pendaftar():
    try:
        sqliteConnection = sqlite3.connect('database/data_beasiswa_smp.db')
        cursor = sqliteConnection.cursor()

        statement = f"SELECT * from pendafaran;"
        cursor.execute(statement)
        rows = cursor.fetchall()
        data_empty = []
        for row in rows:
            data_empty.append(row)
        return data_empty
        
    except sqlite3.Error as error:
        return False
        
    finally:
        if sqliteConnection:
            sqliteConnection.close()
    
def update_data_status_siswa(nisn_inp, data_sosial_siswa_inp):
    try:
        sqliteConnection = sqlite3.connect('database/data_beasiswa_smp.db')
        cursor = sqliteConnection.cursor()

        sql = ''' UPDATE data_siswa
                  SET Data_dinas_sosial_siswa = ?
                  WHERE Nisn_siswa = ?;'''
        
        data_tuple = (data_sosial_siswa_inp, nisn_inp)
        cursor.execute(sql, data_tuple)
        sqliteConnection.commit()
        st.success("Insert Berhasil")
        cursor.close()
        
    except sqlite3.Error as error:
        st.write(error)
        st.error("Insert Gagal !")
        
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def cek_pendaftar(beasiswa_inp):
    try:
        sqliteConnection = sqlite3.connect('database/data_beasiswa_smp.db')
        cursor = sqliteConnection.cursor()

        statement = f"SELECT * from pendafaran WHERE Subject_beasiswa = '{beasiswa_inp}';"
        cursor.execute(statement)
        rows = cursor.fetchall()
        if not rows:
            return False
        else:
            data_empty = []
            for row in rows:
                data_empty.append(row)
            return data_empty
        
    except sqlite3.Error as error:
        return False
        
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def sistem_svm(df, df2):
    data = ['Rentan Miskin', 'Miskin', 'Normal']
    df = df.loc[df['Data Dinas Sosial'] > 0]
    df2 = df2.loc[df2['Data Dinas Sosial'].isin(data)]
    loaded_model = pickle.load(open('./model_beasiswa_svm.pkl', 'rb'))
    list_svm = []
    for i in range(len(df)):
        data = df.iloc[i, 1:].values
        predict = loaded_model.predict([data])

        if predict == 1:
            list_svm.append("Lolos Seleksi 1")
        else:
            list_svm.append("Tidak Lolos Seleksi 1")
        
    df['predict_svm'] = list_svm
    df2['predict-svm'] = list_svm

    # df_new = df.loc[df['predict_svm'] == "Lolos Seleksi 1"]

    # st.write("#KLASIFIKASI SVM")
    st.markdown("<h1 style='text-align:center'; color: black;'>Klasifikasi SVM</h1>", unsafe_allow_html=True)
    st.table(df2)
    df_new = df.loc[df['predict_svm'] == "Lolos Seleksi 1"]
    return df_new

def sistem_smart(df):
    # st.table(df)
    
    list_nisn, list_kip, list_penghasilan, list_status, list_data_kemiskinan = [], [], [], [], []
    
    for i in df['Nisn Siswa']:
        sqliteConnection = sqlite3.connect('database/data_beasiswa_smp.db')
        cursor = sqliteConnection.cursor()

        statement = f"SELECT * from data_siswa WHERE Nisn_siswa = {i};"
        cursor.execute(statement)
        rows = cursor.fetchone()
        if rows is None:
            pass
        else:
            list_nisn.append(rows[0])
            list_kip.append(rows[7])
            list_penghasilan.append(rows[6])
            list_status.append(rows[5])
            list_data_kemiskinan.append(rows[8])

    data_df ={
            'Nisn' : list_nisn,
            'Kartu Indonesia Pelajar' : list_kip,
            'Status Orang Tua' : list_status,
            'Penghasilan Orang Tua' : list_penghasilan,
            'Data Dinas Sosial' : list_data_kemiskinan
    }
    df_new = pd.DataFrame(data_df)
    # KONVERSI KE NUMERIK
    df_new_2 = df_new
    df_new_2["Kartu Indonesia Pelajar"].replace({"Ada": "4", "Tidak ada": "0"}, inplace=True)
    df_new_2 = df_new_2.astype({'Kartu Indonesia Pelajar' : int})

    df_new_2["Penghasilan Orang Tua"].replace({
        "Kurang dari Rp. 500.000" : "0.75",
        "Rp. 500.000 - Rp. 999,999" : "0.5",
        'Diatas Rp 1.000.000' : "0.25",
        "Tidak berpenghasilan" : "1"
    },
        inplace=True)
    
    df_new_2 = df_new_2.astype({'Penghasilan Orang Tua' : float})

    df_new_2["Status Orang Tua"].replace({"Yatim": "0.75", "Piatu": "0.75", "Yatim Piatu" : "1", "Lengkap" : "0.5"}, inplace=True)
    df_new_2 = df_new_2.astype({'Status Orang Tua' : float})

    df_new_2["Data Dinas Sosial"].replace({"Miskin": "1", "Rentan Miskin": "0.75", "Pemegang PKH/KPS/KKS" : "1", "Normal" : "0.5"}, inplace=True)
    df_new_2 = df_new_2.astype({'Data Dinas Sosial' : float})
    

    # Sistem SVM
    df_svm_first = sistem_svm(df_new_2, df_new)
    df_svm = df_svm_first.iloc[:, :-1]
    # option = ['Rentan Miskin', 'Miskin', 'Normal']
    # df_svm = df_svm.loc[df_svm['Data Dinas Sosial'].isin(option)]
    # df_svm = df_svm.dropna()

    # SISTEM SMART
    df_svm['Kartu Indonesia Pelajar'] = df_svm['Kartu Indonesia Pelajar'].apply(lambda x: int((x - 0) / 1))
    df_svm['Penghasilan Orang Tua'] = df_svm['Penghasilan Orang Tua'].apply(lambda x: float((x - 0.5) / 0.5))
    df_svm['Status Orang Tua'] = df_svm['Status Orang Tua'].apply(lambda x: float((x - 0.5) / 0.5))
    df_svm['Data Dinas Sosial'] = df_svm['Data Dinas Sosial'].apply(lambda x: float((x - 0.5) / 0.5))
    
    
    df_new_3 = df_svm.astype(float)
    df_new_3 = df_new_3.astype({"Nisn": int, 'Kartu Indonesia Pelajar' : float})
    df_new_3['Kartu Indonesia Pelajar'] = df_new_3['Kartu Indonesia Pelajar'].apply(lambda x: float(x * 0.4))
    df_new_3['Penghasilan Orang Tua'] = df_new_3['Penghasilan Orang Tua'].apply(lambda x: float(x * 0.1))
    df_new_3['Status Orang Tua'] = df_new_3['Status Orang Tua'].apply(lambda x: float(x * 0.3))
    df_new_3['Data Dinas Sosial'] = df_new_3['Data Dinas Sosial'].apply(lambda x: float(x * 0.2))
    
    column_list = list(df_new_3)
    column_list.remove("Nisn")
    
    df_new_3["Total"] = df_new_3[column_list].sum(axis=1)
    
    
    df_new_3['Ranking'] = df_new_3['Total'].rank(ascending = 0, method='dense')
    df_new_3 = df_new_3.astype({'Ranking' : int})
    th_props = [
    ('font-size', '14px'),
    ('text-align', 'center'),
    ('font-weight', 'bold'),
    # ('color', '#6d6d6d'),
    ('background-color', '#f0f1f6')
    ]
                                
    td_props = [
    ('font-size', '18px')
    ]
                                    
    styles = [
    dict(selector="th", props=th_props),
    dict(selector="td", props=td_props)
    ]

    df_new['Status SVM'] = df_svm_first['predict_svm']
    df_new['ranking'] = df_new_3['Ranking']
    df_new = df_new.sort_values(by=['ranking'])
    df_new = df_new.loc[df_new['ranking'] > 0]
    df_new['ranking'] = df_new['ranking'].astype(int)

    # df_svm['Data Dinas Sosial'] = df_svm['Data Dinas Sosial'].astype(int)
    # df_svm['Penghasilan Orang Tua'] = df_svm['Penghasilan Orang Tua'].astype(int)
    # df_svm['Status Orang Tua'] = df_svm['Status Orang Tua'].astype(int)
    # table
    st.write("")
    st.write("")
    df2=df_new.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles)
    st.markdown("<h1 style='text-align:center'; color: black;'>SISTEM SMART</h1>", unsafe_allow_html=True)
    st.table(df2)
