import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import sqlite3
import numpy as np
import pandas as pd
import datetime
from datetime import date
import modul_beasiswa
import pickle

st.set_page_config(layout="wide")

# Membuat Session Login
if 'login_user' not in st.session_state:
    st.session_state['login_user'] = ''

if 'login_admin' not in st.session_state:
    st.session_state['login_admin'] = ''        

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)
   
page_bg_img = """
<style>
[class="block-container css-18e3th9 egzxvld2"] {
background: "Images/background.png";
height: 100%;
width: 100%;
background-size: cover;
background-repeat: no-repeat;
background-position: center;
background-attachment: fixed;
height: auto;
}

# @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');

# html, body, [class*="css"]  {
#     font-family: 'Montserrat', sans-serif;
# }


[data-testid="stHeader"]{
background-color : rgba(0, 0, 0, 0);
}

[data-testid="column"]{
background-color : rgba(0, 0, 0, 0);
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown("""
<style>
.header-font {
    font-size:47px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.text-title {
    font-size:25px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.text-font {
    font-size:18px !important;
    allign='justify';
}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="header-font">Sistem Pendukung Keputusan Beasiswa</p>', unsafe_allow_html=True)
st.markdown('<p class="text-title">Sistem ini menggunakan metode <strong><em>Support Vector Machine </em></strong> (SVM) <em><strong> dan Simple Multi Attribute Rating</em></strong> (SMART)</p>', unsafe_allow_html=True)

          
data_menu = modul_beasiswa.menu()

selected = option_menu(
    menu_title = None,
    options = data_menu[0],
    icons = data_menu[1],
    menu_icon = 'cast',
    orientation = "horizontal",
    styles={
     "container" : {"background-color" : '#eee', 'color' : 'white'},#fafafa
     "nav-link-selected": {"background-color": '#fafafa', 'color' : 'rgb(10,21,29)'},
     "nav-link" : {"--hover-color": "#eee"}
    }
)

if selected == "Beranda":

    buffer, col1, col2 = st.columns([.6, 4, 4], gap='large')
    buffer_2, col1_2, col2_2 = st.columns([1, 4, 1])
    with col1:
        st.write("")

        st.write("# SMP Negeri 3 Mlati Yogyakarta")
        st.write("")
        st.markdown('''<p class="text-font", align='justify'>
            SMP Negeri 3 Mlati merupakan salah satu Sekolah Menengah Pertama yang berada di Sleman DI Yogyakarta. Memasuki akhir tahun 2022, SMP Negeri 3 Mlati berencana memberikan beasiswa kepada siswa yang layak menerima nya. Pemberian beasiswa dilakukan dengan cara pihak sekolah menentukan siswa mana yang berhak mendapatkan beasiswa. Tujuan pemberian beasiswa ini tentu saja untuk meringankan beban biaya pendidikan siswa SMP Negeri 3 Mlati. Karena kita ketahui bahwa pandemi covid yang sudah berjalan 2 tahun ini masih belum memberikan dampak positif perekonomian masyarakat terutama di wilayah DI Yogyakarta.</p>''', unsafe_allow_html=True)


        
    with col1_2:
        st.write("")
        st.markdown("<hr style='width:100%';>", unsafe_allow_html=True)
        st.markdown("<h1 class='header-font', align='center'>Beasiswa SMP Negeri 3 Mlati Yogyakarta</h1>", unsafe_allow_html=True)
        data_list_beasiswa = modul_beasiswa.get_beasiswa()
        data_list = modul_beasiswa.biodata(st.session_state['login_user'])
        list_Subject, list_open_date, list_close_date, list_Body= [], [], [], []
        num_list = 1
        if data_list_beasiswa != False:
            for i in range(len(data_list_beasiswa)):
                data_pendaftar = modul_beasiswa.get_pendaftaran(st.session_state['login_user'], data_list_beasiswa[i][0])
                st.write("# {}. {}".format(num_list, data_list_beasiswa[i][0]))
                html_str = f"""
                <p style="font-size:18px;">{data_list_beasiswa[i][3]}</p>
                """

                st.markdown(html_str, unsafe_allow_html=True)
                # st.write(data_list_beasiswa[i][3])
                with st.expander("Selengkapnya .."):
                    html_str_2 = f"""
                    <p style="font-size:18px;">Beasiswa ini dibuka dari tanggal {data_list_beasiswa[i][1]} hingga {data_list_beasiswa[i][2]}</p>
                    """
                    st.markdown(html_str_2, unsafe_allow_html=True)
                    # st.write("""
                    # Beasiswa ini dibuka dari tanggal {} hingga {}
                    # """.format(data_list_beasiswa[i][1], data_list_beasiswa[i][2]))

                    today = datetime.datetime.today().strftime('%Y-X%m-X%d').replace('X0','X').replace('X','')
                    if  today >= data_list_beasiswa[i][1] and today <= data_list_beasiswa[i][2] and st.session_state['login_user'] != '' and data_pendaftar == True:
                        name_btn = "Daftar {}".format(data_list_beasiswa[i][0])
                        exec('button_{} = st.button(name_btn)'.format(i+1))
                        if eval('button_{}'.format(i + 1)):
                            cek_insert = modul_beasiswa.insert_pendaftaran(data_list[0], data_list_beasiswa[i][0])
                            if cek_insert == True:
                                st.success("Berhasil Mendaftar")
                            else:
                                st.error("Gagal Mendaftar")
                    else:
                        name_btn = "Daftar {}".format(data_list_beasiswa[i][0])
                        exec('button_{} = st.button(name_btn, disabled= True)'.format(i+1))

                num_list += 1
    
    with col2:
        st.write("")
        st.write("")
        # img = Image.open("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse3.mm.bing.net%2Fth%3Fid%3DOIP.rru55RFI1xkznxeLn2aJxAHaFP%26pid%3DApi&f=1&ipt=6f35fc860613bf2392e992d2835117527e084738279e137edaedad7fb81042a8&ipo=images")
        st.image("Images/remove.png", width=475)
    
if selected == "SMART & SVM":
    smart = False
    buffer_2, col2_2, col3_2 = st.columns([2,6,2])
    with col2_2:
        option = st.selectbox(
            '',
            ('SMART', 'SVM')
        )
        if option == "SMART":
            smart = True
            image = Image.open("Images/smart.jpg")
            st.image(image)
        else:
            image = Image.open("Images/svm.jpg")
            st.image(image)

    if smart == True:
        buffer, col2, col3 = st.columns([1.5,7,1.5])
        with col2:
            st.markdown('##')

            st.markdown("<p class='text-font', align='justify'>SMART (Simple Multi Attribute Rating Technique) merupakan metode pengambilan keputusan yang multi-atribut yang dikembangkan oleh Edward pada tahun 1971 (Filho 2005). Pendekatan ini dirancang pada awalnya untuk memberikan cara mudah untuk menerapkan teknik MAUT (Multi-Attribute Utility Theory). Selama bertahun-tahun, kegagalan dalam metode ini telah diidentifikasi, dan telah diperbaiki (Edwards and Barron, 1994) yang menciptakan metode SMARTS dan SMARTER, menyajikan dua bentuk berbeda untuk memperbaiki kekurangan ini (Filho, 2005)</p>", unsafe_allow_html=True)
            st.write("")
            st.markdown("<p class='text-font', align='justify'>SMART menggunakan linier adaptif model untuk meramal nilai setiap alternatif. SMART lebih banyak digunakan karena kesederhanaannya dalam merespon kebutuhan pembuat keputusan dan caranya menganalisa respon. Analisis yang terbaik adalah transparan sehingga metode ini memberikan pemahaman masalah yang tinggi dan dapat diterima oleh pembuat keputusan. Pembobotan pada SMART menggunakan skala 0 sampai 1, sehingga mempermudah perhitungan dan perbandingan nilai pada masing-masing alternatif.</p>", unsafe_allow_html=True)
            st.write("")
            
            st.write("## Tahapan Metode SMART")
            st.write("### 1. Menentukan Kriteria")
            st.markdown("<p class='text-font', align='justify'>Menentukan kriteria yang digunakan dalam menyelesaikan masalah pengambilan keputusan. Untuk menentukan kriteria-kriteria apa saja yang digunakan dalam sistem pengambilan keputusan ini diperlukan data-data dari pengambil keputusan atau pihak yang berwenang/kompeten terhadap masalah yang akan diselesaikan.</p>", unsafe_allow_html=True)
            
            st.write("### 2. Menentukan Bobot Kriteria")
            st.markdown("<p class='text-font', align='justify'>Memberikan bobot kriteria pada masing-masing kriteria dengan menggunakan interval 1-100 untuk masing-masing kriteria dengan prioritas terpenting.</p>", unsafe_allow_html=True)
            
            st.write("### 3. Normalisasi Bobot Kriteria")
            st.markdown("<p class='text-font', align='justify'>Menghitung normalisasi bobot dari setiap kriteria dengan membandingkan nilai bobot kriteria dengan jumlah bobot kriteria</p>", unsafe_allow_html=True)
            image_bobot = Image.open("Images/rumus_bobot.jpg")
            st.image(image_bobot)
            st.write("###### Keterangan : ")
            st.write("""
            * wi : Bobot kriteria ternormalisasi untuk kriteria ke-I
            * Wi : Bobot kriteria ke-I
            * Wj : Bobot kriteria ke-J
            * j  :1,2,3...m jumlah kriteria
            """)

            
            st.write("### 4. Memberikan Parameter untuk Setiap Kriteria")
            st.markdown("<p class='text-font', align='justify'>Memberikan nilai kriteria untuk setiap alternatif, nilai kriteria untuk setiap alternatif ini dapat berbentuk data kuantitatif (angka) ataupun berbentuk data kualitatif, misalkan nilai untuk kriteria harga sudah dapat dipastikan berbentuk kuantitatif sedangkan nilai untuk kriteria fasilitas bisa jadi berbentuk kualitatif (sangat lengkap, lengkap, kurang lengkap). Apabila nilai kriteria berbentuk kualitatif maka kita perlu mengubah ke data kuantitatif dengan membuat parameter nilai kriteria, misalkan sangat lengkap artinya 3, lengkap artinya 2 dan tidak lengkap artinya 1.</p>", unsafe_allow_html=True)

            st.write("### 5. Menentukan Nilai Utility")
            st.markdown("<p class='text-font', align='justify'>Menentukan nilai utility dengan mengkonversikan nilai kriteria pada masing-masing kriteria menjadi nilai kriteria data baku. Nilai utility ini tergantung pada sifat kriteria itu sendiri.</p>", unsafe_allow_html=True)
            
            st.write("#### 1) Kriteria Biaya (Cost)")
            st.markdown("<p class='text-font', align='justify'>Kriteria yang bersifat “lebih diinginkan nilai yang lebih kecil” kriteria seperti ini biasanya dalam bentuk biaya yang harus dikeluarkan (misalkan kriteria harga, kriteria penggunaan bahan bakar per kilometer untuk pembelian mobil, periode pengembalian modal dalam suatu usaha, kriteria waktu pengiriman) dapat dihitung dengan menggunakan persamaan:</p>", unsafe_allow_html=True)
            image_cost = Image.open("Images/rumus_cost.jpg")
            st.image(image_cost)
            st.write("##### Keterangan : ")
            st.write("""
            * ui(ai) : nilai utility kriteria ke-i untuk alternatif ke-i
            * cmax : nilai kriteria maksimal
            * cmin : nilai kriteria minimal
            * cout : nilai kriteria ke-i
            """)

            
            st.write("#### 2) Kriteria Keuntungan (Benefit)")
            st.markdown("<p class='text-font', align='justify'>Kriteria yang bersifat “lebih diinginkan nilai yang lebih besar”, kriteria seperti ini biasanya dalam bentuk keuntungan (misalkan kriteria kapasitas tangki untuk pembelian mobil, kriteria kualitas dan lainnya)</p>", unsafe_allow_html=True)
            image_benefit = Image.open("Images/rumus_benefit.jpg")
            st.image(image_benefit)
            st.write("##### Keterangan : ")
            st.write("""
            * uj(ai) : nilai utility kriteria ke-j untuk alternatif ke-i
            * cmax : nilai kriteria maksimal
            * cmin : nilai kriteria minimal
            * cout : nilai kriteria alternatif ke-i
            """)
            
            st.write("### 6. Menentukan Nilai Akhir")
            st.markdown("<p class='text-font', align='justify'>Menentukan nilai akhir dari masing-masing dengan mengalikan nilai yang didapat dari normalisasi nilai kriteria data baku dengan nilai normalisasi bobot kriteria</p>", unsafe_allow_html=True)
            rumus_akhir = Image.open("Images/rumus_akhir.jpg")
            st.image(rumus_akhir)
            st.write("##### Keterangan : ")
            st.write("""
            * u(ai)  : nilai ttal untuk alternatid ke-I
            * Wj     : nilai bobot kriteria ke-j yang sudah ternormalisasi
            * uj(ai) : nilai utility kriteria ke-j untuk alternatif ke-i
            * cout   : nilai kriteria alternatif ke-i
            """)
            
            st.write("### 7. Perangkingan")
            st.markdown("<p class='text-font', align='justify'>Hasil dari perhitungan Nilai akhir kemudian diurutkan dari nilai yang terbesar hingga yang terkecil, alternatif dengan nilai akhir yang terbesar menunjukkan alternatif yang terbaik</p>", unsafe_allow_html=True)
       
    else:
        buffer, col2, col3 = st.columns([1.5,7,1.5])
        with col2:
            st.markdown('##')

            st.markdown("<p class='text-font', align='justify'><strong>Vladimir N Vapnik</strong>, seorang Professor dari Columbia, Amerika Serikat pada tahun 1992 memperkenalkan sebuah algoritma training yang bertujuan untuk memaksimalkan margin antara pola pelatihan dan batas keputusan (decision boundary) [10]. Algoritma ini kemudian dikenal luas sebagai Support Vector Machine (SVM).</p>", unsafe_allow_html=True)
            st.write("")
            st.markdown("<p class='text-font', align='justify'><strong>Support Vector Machine (SVM)</strong> merupakan salah satu metode dalam supervised learning yang biasanya digunakan untuk klasifikasi (seperti Support Vector Classification) dan regresi (Support Vector Regression). Dalam pemodelan klasifikasi, SVM memiliki konsep yang lebih matang dan lebih jelas secara matematis dibandingkan dengan teknik-teknik klasifikasi lainnya. SVM juga dapat mengatasi masalah klasifikasi dan regresi dengan linear maupun non linear.</p>", unsafe_allow_html=True)
            st.write("")
            st.markdown("<p class='text-font', align='justify'>Tujuan dari algoritma SVM adalah untuk menemukan hyperplane terbaik dalam ruang berdimensi-N (ruang dengan N-jumlah fitur) yang berfungsi sebagai pemisah yang jelas bagi titik-titik data input.</p>", unsafe_allow_html=True)
            st.write("")

            st.write("## Beberapa keunggulan Support Vector Machine antara lain : ")
            st.write("")
            st.markdown("<p class='text-font', align='justify'>1. SVM efektif pada data berdimensi tinggi (data dengan jumlah fitur atau atribut yang sangat banyak).</p>", unsafe_allow_html=True)
            st.write("")
            st.markdown("<p class='text-font', align='justify'>2. SVM efektif pada kasus di mana jumlah fitur pada data lebih besar dari jumlah sampel.</p>", unsafe_allow_html=True)
            st.write("")
            st.markdown("<p class='text-font', align='justify'>3. SVM menggunakan subset poin pelatihan dalam fungsi keputusan (disebut support vector) sehingga membuat penggunaan memori menjadi lebih efisien.</p>", unsafe_allow_html=True)
            st.write("")

            st.write("## Data Training Support Vector Machine Sebagai Berikut : ")
            with st.expander("Selengkapnya .."):
                df = pd.read_csv("dataset/Data Real SVM Beasiswa.csv")
                df = df.iloc[:, 1:]
                st.table(df)

if selected == "Pengumuman":
    buffer, col2, col3 = st.columns([2.5,5.5,2])
    
    with col2:
        data_list_beasiswa = modul_beasiswa.get_beasiswa()
        if data_list_beasiswa != False:
            list_Subject, list_open_date, list_close_date, list_Body= [], [], [], []
            for i in range(len(data_list_beasiswa)):
                list_Subject.append(data_list_beasiswa[i][0])
                list_open_date.append(data_list_beasiswa[i][1])
                list_close_date.append(data_list_beasiswa[i][2])
                list_Body.append(data_list_beasiswa[i][3])

            data_df ={
                'Subject' : list_Subject,
                'open_date' : list_open_date,
                'close_date' : list_close_date,
                'Body' : list_Body
            }

            df = pd.DataFrame(data_df)
            
            # for i in df.iterrows():
            #     st.write(i[1])
            #     st.write(i[1][0])
            #     st.write(i[1][1])
            #     st.write(i[1][2])
            
            for i in df.iterrows():
                subject = i[1][0]
                st.markdown("<h1 style='text-align:center'; color: black;'>{}</h1>".format(subject), unsafe_allow_html=True)
                close_date = str(i[1][2]).split('-')
                close_date = date(int(close_date[0]), int(close_date[1]), int(close_date[2]))
                today = datetime.datetime.now().strftime('%Y-%m-%d')
                today = str(today).split('-')
                today = date(int(today[0]), int(today[1]), int(today[2]))
                if today >= close_date:
                    with st.expander("Selengkapnya .."):
                        data_list_pendaftar = modul_beasiswa.cek_pendaftar(subject)
                        list_id_pendaftar, list_subject_beasiswa, list_nisn_siswa = [], [], []
                        if data_list_pendaftar != False:
                            st.markdown("<h1 style='text-align:center'; color: black;'>Data Pendaftar</h1>", unsafe_allow_html=True)
                            for j in range(len(data_list_pendaftar)):
                                list_id_pendaftar.append(data_list_pendaftar[j][0])
                                list_subject_beasiswa.append(data_list_pendaftar[j][1])
                                list_nisn_siswa.append(data_list_pendaftar[j][2])


                            data_df ={
                                'Id Pendaftar' : list_id_pendaftar,
                                'Subject Beasiswa' : list_subject_beasiswa,
                                'Nisn Siswa' : list_nisn_siswa
                            }

                            df = pd.DataFrame(data_df)
                            st.table(df)
                            
                            modul_beasiswa.sistem_smart(df)
                else:
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")
                    st.write("")


            # for num, i in enumerate(df.Subject):
            #     st.markdown("<h1 style='text-align:center'; color: black;'>{}</h1>".format(i), unsafe_allow_html=True)
            #     data = df.iloc[num, :]
            #     close_date = data['close_date']
            #     today = datetime.today().strftime('%Y-X%m-X%d').replace('X0','X').replace('X','')
            #     if today > close_date:
            #         with st.expander("Selengkapnya .."):
            #             data_list_pendaftar = modul_beasiswa.cek_pendaftar(i)
            #             list_id_pendaftar, list_subject_beasiswa, list_nisn_siswa = [], [], []
            #             if data_list_pendaftar != False:
            #                 st.markdown("<h1 style='text-align:center'; color: black;'>Data Pendaftar</h1>", unsafe_allow_html=True)
            #                 for j in range(len(data_list_pendaftar)):
            #                     list_id_pendaftar.append(data_list_pendaftar[j][0])
            #                     list_subject_beasiswa.append(data_list_pendaftar[j][1])
            #                     list_nisn_siswa.append(data_list_pendaftar[j][2])


            #                 data_df ={
            #                     'Id Pendaftar' : list_id_pendaftar,
            #                     'Subject Beasiswa' : list_subject_beasiswa,
            #                     'Nisn Siswa' : list_nisn_siswa
            #                 }

            #                 df = pd.DataFrame(data_df)
            #                 st.table(df)
                            
            #                 modul_beasiswa.sistem_smart(df)
                # else:
                #     st.write("")
                #     st.write("")
                #     st.write("")
                #     st.write("")
                #     st.write("")
                #     st.write("")
        
if selected == "Akun":
    buffer, col2, col3 = st.columns([3,4,3])

    with col2:
        option = st.selectbox(
            '',
            ('Login', 'Signup')
        )
        select_bg = """
        <style>
        div[data-baseweb="select"] > div {
            background-color: #eee;
        }
        
        div[role="listbox"] ul {
            background-color: #eee;
        }
        
        div[data-baseweb="input"] > div {
            background-color: #eee;
            -webkit-text-fill-color: black;
        }

        div[data-baseweb="submit"] > div {
            background-color: #eee;
            -webkit-text-fill-color: black;
        }
        
        .stTextArea [data-baseweb=base-input]{
            background-color: #eee;
            -webkit-text-fill-color: black;
        }
        </style>
    """

        st.markdown(select_bg, unsafe_allow_html=True)
        if option == "Login" :
#             m = st.markdown("""
#                 <style>
#                 div.stButton > button:first-child {
#                     background-color: rgb(204, 49, 49);
#                     color: white;
#                 }
#                 </style>""", unsafe_allow_html=True)

#             b = st.button("test")
            placeholder_1 = st.empty()

            with placeholder_1.form("login"):
                st.markdown("### Login Form")
                nisn = st.number_input(label="Nisn", max_value=9999999999, step = 1)
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login")

            if submit:
                placeholder_1.empty()
                cek_login = modul_beasiswa.login(nisn, password)
                if cek_login == ['Siswa', True] or cek_login == ['Admin', True]:
                    menu_new = modul_beasiswa.menu()
        
        if option == "Signup":
            placeholder_2 = st.empty()

            with placeholder_2.form("signup"):
                st.markdown("### Signup Form")
                nisn = st.number_input("Nisn", max_value=9999999999, step = 1)
                password = st.text_input("Password", type="password")
                nama = st.text_input('Nama Lengkap')
                opsi_kelas = st.selectbox(
                    'Kelas',
                    ('VII','VIII','IX')
                )
                alamat = st.text_area('Alamat Lengkap')
                opsi_status = st.selectbox(
                    'Status Orang Tua Siswa',
                    ('Lengkap','Yatim', 'Piatu', 'Yatim Piatu')
                )
                opsi_pendapatan = st.selectbox(
                    'Penghasilan Orang Tua / wali',
                    ('Kurang dari Rp. 500.000','Rp. 500.000 - Rp. 999,999', 'Tidak berpenghasilan', 'Diatas Rp 1.000.000'),
                )
                opsi_kip = st.selectbox(
                    'Kartu Program Indonesia Pintar',
                    ('Ada','Tidak ada')
                )
                submit_signup = st.form_submit_button("Submit")

                if submit_signup:
                    if opsi_kip == "Ada" and opsi_pendapatan == "Diatas Rp 1.000.000":
                        st.warning("KIP hanya dimiliki oleh siswa yang pendapatan dibawah Rp 1.000.000 !")
                    elif alamat == '' or nama == '' or password == '':
                        st.warning("Data Harus Lengkap !")
                    else:
                        cek_insert = modul_beasiswa.insert_data_siswa(nisn, password, nama, opsi_kelas, alamat, opsi_status, opsi_pendapatan, opsi_kip)
                        if cek_insert == ['Insert_data', 'True']:
                            st.success("Insert Data Berhasil")
                            
                        elif cek_insert == ['Insert_data', 'False']:
                            st.error("Insert Data Gagal !")
                        
 

if selected == st.session_state['login_user']:
    data_list = modul_beasiswa.biodata(st.session_state['login_user'])
    buffer, col2, col3 = st.columns([2,4,2])
    with col2:
        option = st.selectbox(
            '',
            ('Biodata', 'Edit')
        )
        if option == "Biodata" :
            placeholder_3 = st.empty()
            with placeholder_3.form("biodata_diri"):
                st.markdown("### Biodata Form")
                nisn = st.number_input("Nisn", max_value=9999999999, step = 1, value=data_list[0], disabled=True)
                password = st.text_input("Password", type="password", value=data_list[1], disabled=True)
                nama = st.text_input('Nama Lengkap', value=data_list[2], disabled=True)
                
                if data_list[3] == "VII":
                    index_kelas = 0
                    
                if data_list[3] == "VIII":
                    index_kelas = 1
                    
                if data_list[3] == "IX":
                    index_kelas = 2
                
                opsi_kelas = st.selectbox(
                    'Kelas',
                    ('VII','VIII','IX'),
                    index = index_kelas,
                    disabled=True
                )
                alamat = st.text_area('Alamat Lengkap', value=data_list[4], disabled=True)
                
                if data_list[5] == "Lengkap":
                    index_status = 0
                    
                if data_list[5] == "Yatim":
                    index_status = 1
                
                if data_list[5] == "Piatu":
                    index_status = 2
                
                if data_list[5] == "Yatim Piatu":
                    index_status = 3
                        
                opsi_status = st.selectbox(
                    'Status Orang Tua Siswa',
                    ('Lengkap','Yatim', 'Piatu', 'Yatim Piatu'),
                    index = index_status,
                    disabled=True
                )
                
                if data_list[6] == "Kurang dari Rp. 500.000":
                    index_pendapatan = 0
                if data_list[6] == 'Rp. 500.000 - Rp. 999,999':
                    index_pendapatan = 1
                if data_list[6] == 'Diatas Rp 1.000.000':
                    index_pendapatan = 3
                else:
                    index_pendapatan = 2
                    
                opsi_pendapatan = st.selectbox(
                    'Penghasilan Orang Tua',
                    ('Kurang dari Rp. 500.000','Rp. 500.000 - Rp. 999,999', 'Tidak berpenghasilan', 'Diatas Rp 1.000.000'),
                    index=index_pendapatan,
                    disabled=True
                )
                
                if data_list[7] == "Ada":
                    index_kip = 0
               
                if data_list[7] == "Tidak ada":
                    index_kip = 1
                    
                opsi_kip = st.selectbox(
                    'Kartu Program Indonesia Pintar',
                    ('Ada','Tidak ada'),
                    index = index_kip,
                    disabled=True
                )
                
                st.write("Status Dinas Sosial")
                if data_list[8] == None:
                    st.error("Belum Ada")
                
                else:
                    st.success("Tergolong {}".format(data_list[8]))
                
                
                
                submit_signup = st.form_submit_button("Submit")
                
        if option == "Edit" :
            placeholder_4 = st.empty()
            with placeholder_4.form("edit_data"):
                st.markdown("### Biodata Form")
                nisn = st.number_input("Nisn", max_value=9999999999, step = 1, value=data_list[0])
                password = st.text_input("Password", type="password", value=data_list[1])
                nama = st.text_input('Nama Lengkap', value=data_list[2])
                
                if data_list[3] == "VII":
                    index_kelas = 0
                    
                if data_list[3] == "VIII":
                    index_kelas = 1
                    
                if data_list[3] == "IX":
                    index_kelas = 2
                
                opsi_kelas = st.selectbox(
                    'Kelas',
                    ('VII','VIII','IX'),
                    index = index_kelas
                )
                alamat = st.text_area('Alamat Lengkap', value=data_list[4])
                
                if data_list[5] == "Lengkap":
                    index_status = 0
                    
                if data_list[5] == "Yatim":
                    index_status = 1
                
                if data_list[5] == "Piatu":
                    index_status = 2
                
                if data_list[5] == "Yatim Piatu":
                    index_status = 3
                        
                opsi_status = st.selectbox(
                    'Status Orang Tua Siswa',
                    ('Lengkap','Yatim', 'Piatu', 'Yatim Piatu'),
                    index = index_status
                )
                if data_list[6] == "Kurang dari Rp. 500.000":
                    index_pendapatan = 0
                if data_list[6] == 'Rp. 500.000 - Rp. 999,999':
                    index_pendapatan = 1
                if data_list[6] == 'Diatas Rp 1.000.000':
                    index_pendapatan = 3
                else:
                    index_pendapatan = 2
                    
                opsi_pendapatan = st.selectbox(
                    'Penghasilan Orang Tua',
                    ('Kurang dari Rp. 500.000','Rp. 500.000 - Rp. 999,999', 'Tidak berpenghasilan', 'Diatas Rp 1.000.000'),
                    index=index_pendapatan
                )
                
                if data_list[7] == "Ada":
                    index_kip = 0
               
                if data_list[7] == "Tidak ada":
                    index_kip = 1
                    
                opsi_kip = st.selectbox(
                    'Kartu Program Indonesia Pintar',
                    ('Ada','Tidak ada'),
                    index = index_kip
                )
                
                submit = st.form_submit_button("Submit")
                if submit:
                    modul_beasiswa.edit_data(nisn, password, nama, opsi_kelas, alamat, opsi_status, opsi_pendapatan, opsi_kip, data_list[0])
            

if selected == 'Data Beasiswa':
    col1, col2, col3= st.columns([.1, 5, 4])
    
    with col2:
        data_list_beasiswa = modul_beasiswa.get_beasiswa()
        list_Subject, list_open_date, list_close_date, list_Body= [], [], [], []
        if data_list_beasiswa != False:
            for i in range(len(data_list_beasiswa)):
                list_Subject.append(data_list_beasiswa[i][0])
                list_open_date.append(data_list_beasiswa[i][1])
                list_close_date.append(data_list_beasiswa[i][2])
                list_Body.append(data_list_beasiswa[i][3])

        data_df ={
            'Subject' : list_Subject,
            'open_date' : list_open_date,
            'close_date' : list_close_date,
            'Body' : list_Body
        }

        df = pd.DataFrame(data_df)
        st.write("# Database Beasiswa")
        st.table(df)
    
    with col3 :
        option_data = st.selectbox(
            '',
            ('Tambah Data', 'Ubah Data', 'Hapus Data')
        )
        if option_data == 'Ubah Data':
            option = st.selectbox("Subject Beasiswa", df.Subject, 0)
            selected_body = df.loc[df.Subject == option]["Body"].iloc[0]
            selected_star = pd.to_datetime((df.loc[df.Subject == option]["open_date"].iloc[0]))
            selected_end = pd.to_datetime((df.loc[df.Subject == option]["close_date"].iloc[0]))
            placeholder_5 = st.empty()
            with placeholder_5.form("update_beasiswa"):
                st.markdown("### Beasiswa Form")
                subject = st.text_input("Subject", value=option)
                start_date = st.date_input("Start Date", selected_star)
                end_date = st.date_input("Close Date", selected_end)
                body = st.text_area("Body", value=selected_body, height = 250)
                submit = st.form_submit_button("Edit")
                if submit:
                    cek_insert = modul_beasiswa.edit_beasiswa(option, start_date, end_date, body, subject)
                    if cek_insert == True:
                        st.success("Update Berhasil !")
                    else:
                        st.error("Update Gagal !")
        
        if option_data == 'Tambah Data':
            placeholder_8 = st.empty()
            with placeholder_8.form("insert_beasiswa"):
                st.markdown("### Beasiswa Form")
                subject = st.text_input("Subject")
                start_date = st.date_input("Start Date")
                end_date = st.date_input("Close Date")
                body = st.text_area("Body", height = 250)
                submit = st.form_submit_button("Submit")
                if submit:
                    cek_insert = modul_beasiswa.insert_beasiswa(subject, start_date, end_date, body)
                    if cek_insert == True:
                        st.success("Insert Berhasil !")
                    else:
                        st.error("Insert Gagal !")
                    
            
        if option_data == 'Hapus Data':
            option = st.selectbox("Subject Beasiswa", df.Subject, 0)
            btn_delete = st.button('Delete')
            if btn_delete:
                cek_delete = modul_beasiswa.delete_beasiswa(option)
                if cek_delete == True:

                    st.success("Delete Success")
                else:
                    st.error("Delete Failed")

if selected == 'Data Siswa':
    col1, col2, col3= st.columns([.1, 5, 4])
    
    with col2:
        data_list_siswa = modul_beasiswa.biodata()
        list_nisn_siswa, list_password_siswa, list_nama_siswa, list_kelas_siswa, list_alamat_siswa, list_status_siswa, list_pendapatan_ortu, list_pip_siswa, list_data_dinas_siswa = [], [], [], [], [], [], [], [], []
        for i in range(len(data_list_siswa)):
            list_nisn_siswa.append(data_list_siswa[i][0])
            list_password_siswa.append(data_list_siswa[i][1])
            list_nama_siswa.append(data_list_siswa[i][2])
            list_kelas_siswa.append(data_list_siswa[i][3])
            list_alamat_siswa.append(data_list_siswa[i][4])
            list_status_siswa.append(data_list_siswa[i][5])
            list_pendapatan_ortu.append(data_list_siswa[i][6])
            list_pip_siswa.append(data_list_siswa[i][7])
            list_data_dinas_siswa.append(data_list_siswa[i][8])
        
            
        data_df ={
            'Nisn' : list_nisn_siswa,
            'Password' : list_password_siswa,
            'Nama Lengkap' : list_nama_siswa,
            'Kelas' : list_kelas_siswa,
            'Alamat Lengkap' : list_alamat_siswa,
            'Status Siswa' : list_status_siswa,
            'Pendapatan Orang Tua' : list_pendapatan_ortu,
            'Kartu Indonesia Pintar' : list_pip_siswa,
            'Data Dinas Sosial' : list_data_dinas_siswa
        }
        
        df = pd.DataFrame(data_df)
        st.write("# Database Siswa")
        st.table(df)
    
    with col3 :
        option_data = st.selectbox(
            '',
            ('Tambah Data', 'Ubah Data', 'Hapus Data', 'Input Data Dinas Sosial')
        )
        if option_data == 'Ubah Data':
            option = st.selectbox("Nisn", df.Nisn, 0)
            selected_password = df.loc[df.Nisn == option]["Password"].iloc[0]
            selected_nama = df.loc[df.Nisn == option]["Nama Lengkap"].iloc[0]
            selected_kelas = df.loc[df.Nisn == option]["Kelas"].iloc[0]
            if selected_kelas == "VII":
                kelas_index = 0
            
            if selected_kelas == "VIII":
                kelas_index = 1
            
            if selected_kelas == "IX":
                kelas_index = 2
                
            selected_alamat = df.loc[df.Nisn == option]["Alamat Lengkap"].iloc[0]
            selected_status = df.loc[df.Nisn == option]["Status Siswa"].iloc[0]
            if selected_status == "Lengkap":
                status_index = 0

            if selected_status == "Yatim":
                status_index = 1
            
            if selected_status == "Piatu":
                status_index = 2
            
            if selected_status == "Yatim Piatu":
                status_index = 3
                
            selected_kip = df.loc[df.Nisn == option]["Kartu Indonesia Pintar"].iloc[0]
            if selected_kip == "Ada":
                kip_index = 0
                
            if selected_kip == "Tidak ada":
                kip_index = 1
            
            
            selected_penghasilan = df.loc[df.Nisn == option]["Pendapatan Orang Tua"].iloc[0]
            
            if selected_penghasilan == "Kurang dari Rp. 500.000":
                index_pendapatan = 0
            if selected_penghasilan == 'Rp. 500.000 - Rp. 999,999':
                index_pendapatan = 1
            if selected_penghasilan == 'Diatas Rp 1.000.000':
                index_pendapatan = 3
            else:
                index_pendapatan = 2
                
            selected_dinas = df.loc[df.Nisn == option]["Data Dinas Sosial"].iloc[0]
            
            if selected_dinas == "Normal":
                index_dinas = 0
            
            if selected_dinas == "Rentan Miskin":
                index_dinas = 1
            
            if selected_dinas == "Miskin":
                index_dinas = 2
            else:
                index_dinas = 0
                
            placeholder_6 = st.empty()
            with placeholder_6.form("Data_siswa"):
                st.markdown("### Data_siswa")
                nisn = st.number_input("Nisn", max_value=9999999999, step = 1, value = option)
                password = st.text_input("Password", type="password", value=selected_password)
                nama = st.text_input('Nama Lengkap', value=selected_nama)
                opsi_kelas = st.selectbox(
                    'Kelas',
                    ('VII','VIII','IX'),
                    index = kelas_index
                )
                alamat = st.text_area('Alamat Lengkap', value=selected_alamat)
                opsi_status = st.selectbox(
                    'Status Orang Tua Siswa',
                    ('Lengkap','Yatim', 'Piatu', 'Yatim Piatu'),
                    index = status_index
                )
                opsi_pendapatan = st.selectbox(
                    'Penghasilan Orang Tua',
                    ('Kurang dari Rp. 500.000','Rp. 500.000 - Rp. 999,999', 'Tidak berpenghasilan', 'Diatas Rp 1.000.000'),
                    index=index_pendapatan
                )
                opsi_kip = st.selectbox(
                    'Kartu Program Indonesia Pintar',
                    ('Ada','Tidak ada'),
                    index = kip_index
                )
                
                option_data_dinas = st.selectbox(
                    'Data Status Sosial Siswa',
                    ('Normal', 'Rentan Miskin', 'Miskin'),
                    index = index_dinas
                )
                submit_signup = st.form_submit_button("Submit")

                if submit_signup:
                    modul_beasiswa.edit_data_siswa_admin(nisn, password, nama, opsi_kelas, alamat, opsi_status, opsi_pendapatan, opsi_kip, option, option_data_dinas)
                
                
        if option_data == 'Tambah Data':
            placeholder_7 = st.empty()
            with placeholder_7.form("insert"):
                nisn = st.number_input("Nisn", max_value=9999999999, step = 1)
                password = st.text_input("Password", type="password")
                nama = st.text_input('Nama Lengkap')
                opsi_kelas = st.selectbox(
                    'Kelas',
                    ('VII','VIII','IX')
                )
                alamat = st.text_area('Alamat Lengkap')
                opsi_status = st.selectbox(
                    'Status Orang Tua Siswa',
                    ('Lengkap','Yatim', 'Piatu', 'Yatim Piatu')
                )
                opsi_pendapatan = st.selectbox(
                    'Penghasilan Orang Tua',
                    ('Kurang dari Rp. 500.000','Rp. 500.000 - Rp. 999,999', 'Tidak berpenghasilan', 'Diatas Rp 1.000.000')
                )
                opsi_kip = st.selectbox(
                    'Kartu Program Indonesia Pintar',
                    ('Ada','Tidak ada')
                )
                submit_signup = st.form_submit_button("Submit")

                if submit_signup:
                    cek_insert = modul_beasiswa.insert_data_siswa(nisn, password, nama, opsi_kelas, alamat, opsi_status, opsi_pendapatan, opsi_kip)
                    if cek_insert == ['Insert_data', 'True']:
                        st.success("Insert Data Berhasil")
                        
                    elif cek_insert == ['Insert_data', 'False']:
                        st.error("Insert Data Gagal !")
                        
        
        if option_data == 'Hapus Data':
            option = st.selectbox("Id_siswa", df.Nisn, 0)
            btn_delete = st.button('Delete')
            if btn_delete:
                cek_delete = modul_beasiswa.delete(option)
                if cek_delete == True:
                    st.success("Delete Success")
                else:
                    st.error("Delete Failed")
        
        if option_data == 'Input Data Dinas Sosial':
            placeholder_10 = st.empty()
            with placeholder_10.form("biodata_diri"):
                option = st.selectbox("Nisn", df.Nisn, 0)
                option_data = st.selectbox(
                    'Data Status Sosial Siswa',
                    ('Normal', 'Rentan Miskin', 'Miskin')
                )
                submit_btn = st.form_submit_button("Submit")
            
                if submit_btn:
                    modul_beasiswa.update_data_status_siswa(option, option_data)
            
                
if selected == "Data Pendaftar":
    buffer, col2, col3 = st.columns([2,6,2])
    
    with col2:
        data_list_pendaftar = modul_beasiswa.data_pendaftar()
        list_id_pendaftar, list_subject_beasiswa, list_nisn_siswa = [], [], []
        for i in range(len(data_list_pendaftar)):
            list_id_pendaftar.append(data_list_pendaftar[i][0])
            list_subject_beasiswa.append(data_list_pendaftar[i][1])
            list_nisn_siswa.append(data_list_pendaftar[i][2])
        
            
        data_df ={
            'Id Pendaftar' : list_id_pendaftar,
            'Subject Beasiswa' : list_subject_beasiswa,
            'Nisn Siswa' : list_nisn_siswa,
        }
        
        df = pd.DataFrame(data_df)
        st.markdown("<h1 style='text-align:center'; color: black;'>Database Pendaftar</h1>", unsafe_allow_html=True)
        st.table(df)
        
    
            
if selected == 'Logout':
    del st.session_state['login_user']
    del st.session_state['login_admin']
    st.success("Logout Berhasil !")
