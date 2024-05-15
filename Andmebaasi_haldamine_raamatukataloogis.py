from tkinter import * 
from tkinter import tk
from sqlite3 import *
from sqlite3 import Error
from os import *
from tkinter import ttk, messagebox

def create_connect(path:str):
    connection=None
    try:
        connection=connect(path)
        print("Ühendus on olemas!")
    except Error as e:
        print(f"Tekkis viga: {e}")
    return connection


def execute_query(connection,query):
    try:
        cursor=connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Tabel on loodud või andmed on sisestatud")
    except Error as e:
        print(f"Tekkis viga: {e}")


def execute_read_query(connection,query):
    cursor=connection.cursor()
    result=None
    try:
        cursor.execute(query)
        result=cursor.fetchall()
        return result
    except Error as e:
        print(f"Tekkis viga: {e}")
   

create_autorid_table="""
CREATE TABLE IF NOT EXISTS Autorid(
autor_id INTEGER PRIMARY KEY AUTOINCREMENT,
autor_nimi TEXT NOT NULL,
sünnikuupäev  DATE  NOT NULL
)
"""


create_zanrid_table="""
CREATE TABLE IF NOT EXISTS Zanrid(
zanr_id INTEGER PRIMARY KEY AUTOINCREMENT,
zanri_nimi TEXT NOT NULL
)
"""


create_raamatud_table="""
CREATE TABLE IF NOT EXISTS Raamatud(
raamat_id INTEGER PRIMARY KEY AUTOINCREMENT,
pealkiri TEXT NOT NULL,
väljaandmise_kuupäev DATE  NOT NULL,
autor_nimi INTEGER,
zanri_nimi INTEGER,
FOREIGN KEY (autor_nimi) REFERENCES Autorid (autor_nimi),
FOREIGN KEY (zanri_nimi) REFERENCES Zanrid (zanri_nimi)
)
"""

insert_autorid="""
INSERT INTO
Autorid(autor_nimi,sünnikuupäev)
VALUES
("Andrei Platonov","1899-08-28"),
("Aleksander Green","1932-07-08"),
("Mayne Reid","1818-04-04"),
("Rafael Sabatini","1875-04-29"),
("Mihhail Bulgakov","1891-05-15")
"""

insert_zanrid="""
INSERT INTO
Zanrid(zanri_nimi)
VALUES
("Lugu"),
("Seiklusromaan"),
("Seikluskirjandus"),
("Romaanid"),
("Fantastiline")
"""

insert_raamatud="""
INSERT INTO
Raamatud(pealkiri, väljaandmise_kuupäev, autor_nimi, zanri_nimi)
VALUES
("Scarlet Sails","2024-04-28", "Aleksander Green", "Seikluskirjandus"),
("Juska","2024-03-08", "Andrei Platonov", "Lugu"),
("Peata ratsanik","2024-02-15", "Mayne Reid", "Romaanid"),
("Kapten Bloodi odüsseia","2023-07-23", "Rafael Sabatini", "Fantastiline"),
("Meister ja Margarita","2024-02-12", "Mihhail Bulgakov", "Seiklusromaan")
"""


def create_tables(conn):
    execute_query(conn, create_autorid_table)
    execute_query(conn, create_zanrid_table)
    execute_query(conn, create_raamatud_table)
    messagebox.showinfo("Tabelid on loodud!")


def insert_tables(conn):
    execute_query(conn, insert_autorid)
    execute_query(conn, insert_zanrid)
    execute_query(conn, insert_raamatud)
    messagebox.showinfo("Tabelid on täidetud!")


filename=path.abspath(__file__)
dbdir=filename.rstrip('Andmebaasi_haldamine_raamatukataloogis.py')
dbpath=path.join(dbdir,"data.db")
conn=create_connect(dbpath) 


aken=Tk() 
aken.geometry("1000x1000") 
aken.title("Raamatukataloog") 
aken ["bg"]="#cfbaf0" 


def table_autorid(conn):
    aken_autorid = Tk() 
    aken_autorid.title("Autorite tabel") 
    tree =ttk.Treeview(aken_autorid)
    tree=ttk.Treeview(aken_autorid, column=("autor_id", "autor_nimi", "sünnikuupäev"), show="headings")
    tree.column("autor_id", anchor=CENTER)
    tree.heading("autor_id", text="autor_id")
    tree.column("autor_nimi", anchor=CENTER)
    tree.heading("autor_nimi", text="autor_nimi")
    tree.column("sünnikuupäev", anchor=CENTER)
    tree.heading("sünnikuupäev", text="sünnikuupäev")
    try:
        read=execute_read_query(conn, "SELECT * FROM Autorid")
        for row in read:
            tree.insert("", END, values=row)    
    except Exception as e:
        print(f"Viga tabelis autorid: {e}")
    tree.pack() 
    aken_autorid.mainloop()


def table_zanr(conn):
    aken_zanr = Tk() 
    aken_zanr.title("Žanrite tabel") 
    tree =ttk.Treeview(aken_zanr)
    tree=ttk.Treeview(aken_zanr, column=("zanr_id", "zanri_nimi"), show="headings")
    tree.column("zanr_id", anchor=CENTER)
    tree.heading("zanr_id", text="zanr_id")
    tree.column("zanri_nimi", anchor=CENTER)
    tree.heading("zanri_nimi", text="zanri_nimi")
    try:
        read=execute_read_query(conn, "SELECT * FROM Zanrid")
        for row in read:
            tree.insert("", END, values=row)    
    except Exception as e:
        print(f"Viga tabelis zanrid: {e}") 
    tree.pack()
    aken_zanr.mainloop()


def table_raamatud(conn): 
    aken_raamatud = Tk() 
    aken_raamatud.title("Raamatute tabel") 
    tree =ttk.Treeview(aken_raamatud)
    tree =ttk.Treeview(aken_raamatud)
    tree=ttk.Treeview(aken_raamatud, column=("raamat_id", "pealkiri", "väljaandmise_kuupäev", "autor_nimi", "zanri_nimi"), show="headings")
    tree.column("raamat_id", anchor=CENTER)
    tree.heading("raamat_id", text="raamat_id")
    tree.column("pealkiri", anchor=CENTER)
    tree.heading("pealkiri", text="pealkiri") 
    tree.column("väljaandmise_kuupäev", anchor=CENTER)
    tree.heading("väljaandmise_kuupäev", text="väljaandmise_kuupäev") 
    tree.column("autor_nimi", anchor=CENTER)
    tree.heading("autor_nimi", text="autor_nimi") 
    tree.column("zanri_nimi", anchor=CENTER)
    tree.heading("zanri_nimi", text="zanri_nimi") 
    try:
        read=execute_read_query(conn, "SELECT * FROM Raamatud ")
        for row in read:
            tree.insert("", END, values=row)    
    except Exception as e:
        print(f"Viga raamatu tabelis: {e}") 
    tree.pack()
    aken_raamatud.mainloop()  

def add_raamat(conn, pealkiri, väljaandmise_kuupäev, autor_nimi, zanri_nimi):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Raamatud (pealkiri, väljaandmise_kuupäev, autor_nimi, zanri_nimi) VALUES (?, ?, ?, ?)", (pealkiri, väljaandmise_kuupäev, autor_nimi, zanri_nimi,))
        conn.commit() 
        messagebox.showinfo("Raamat on lisatud")
    except Exception as e:
        messagebox.showerror("Viga", f"Viga tabeli sordimisel: {e}")



def add_zanr(conn, zanri_nimi):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Zanrid (zanri_nimi) VALUES (?)", (zanri_nimi,))
        conn.commit() 
        messagebox.showinfo("Zanr on lisatud")
    except Exception as e:
        messagebox.showerror(f"Viga {e}") 

def add_autor(conn, autor_nimi ,sünnikuupäev):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Autorid(autor_nimi,sünnikuupäev) VALUES (?, ?)", (autor_nimi, sünnikuupäev))
        conn.commit() 
        messagebox.showinfo("Autor on lisatud")
    except Exception as e:
        messagebox.showerror(f"Viga {e}")


def delete_raamat(conn, pealkiri):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Raamatud WHERE pealkiri=?", (pealkiri,))
        conn.commit()
        messagebox.showinfo("Pealkiri raamatud on kustutatud")
    except Exception as e:
        messagebox.showerror(f"Viga {e}")


def delete_raamat_autorNimi(conn, autor_nimi):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Raamatud WHERE autor_nimi=?", (autor_nimi,))
        conn.commit()
        messagebox.showinfo("Autor nimi raamatud on kustutatud")
    except Exception as e:
        messagebox.showerror(f"Viga {e}")


def add_zanr_aken():
    add_aken = Toplevel(aken)
    add_aken.title("Žanrite lisamine") 
    zanri_nimi_label = Label(add_aken, 
                             text="Zanri_nimi: ", 
                             font=("Algerian", 30), 
                             fg="#FA7070")
    zanri_nimi_label.grid(row=0, column=0, padx=10, pady=15)
    zanri_nimi_entry = Entry(add_aken, 
                           bg="#FBECB2",
                           fg="#FF70AB", 
                           font="Georgia 25",
                           width=15)
    zanri_nimi_entry.grid(row=0, column=1, padx=20, pady=15)
    def add_zanr_close():
        zanri_nimi = zanri_nimi_entry.get()
        add_zanr(conn,  zanri_nimi)
        add_aken.destroy()

    add_button = Button(add_aken, 
                        text="Lisa žanr",
                        fg="#642ca9",  
                        bg="#ff74d4",
                        font=("Times New Roman", 30),  
                        command=add_zanr_close)
    add_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)


def add_autor_aken():
    add_aken = Toplevel(aken)
    add_aken.title("Autorite lisamine") 
    autor_nimi_label = Label(add_aken, 
                             text="Autor_nimi: ", 
                             font=("Algerian 30"), 
                             fg="#FF6500")
    autor_nimi_label.grid(row=0, column=0, padx=10, pady=15)
    autor_nimi_entry = Entry(add_aken, 
                           bg="#FFC100",
                           fg="#C40C0C", 
                           font="Georgia 25",
                           width=15)
    autor_nimi_entry.grid(row=0, column=1, padx=20, pady=15)
    sünnikuupäev_label = Label(add_aken, 
                               text="Sünnikuupäev: ", 
                               font=("Algerian 30"), 
                               fg="#FF6500")
    sünnikuupäev_label.grid(row=1, column=0, padx=10, pady=15)
    sünnikuupäev_label_entry = Entry(add_aken, 
                                        bg="#FFC100",
                                        fg="#C40C0C", 
                                        font="Georgia 25",
                                        width=15)
    sünnikuupäev_label_entry.grid(row=1, column=1, padx=20, pady=15)
    def add_autor_close():
        autor_nimi = autor_nimi_entry.get()
        sünnikuupäev_label = sünnikuupäev_label_entry.get()
        add_autor(conn, autor_nimi, sünnikuupäev_label)
        add_aken.destroy()

    add_button = Button(add_aken, 
                        text="Autor lisatud", 
                        fg="#642ca9",  
                        bg="#ff74d4",
                        font=("Times New Roman", 30),  
                        command=add_autor_close)
    add_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)


def add_raamat_aken():
    add_aken = Toplevel(aken)
    add_aken.title("Raamatute lisamine") 
    pealkiri_label = Label(add_aken, 
                           text="Pealkiri: ", 
                           font=("Algerian 30"), 
                           fg="#A91D3A")
    pealkiri_label.grid(row=0, column=0, padx=10, pady=15)
    pealkiri_entry = Entry(add_aken, 
                           bg="#F3D0D7",
                           fg="#FF204E", 
                           font="Georgia 25",
                           width=15)
    pealkiri_entry.grid(row=0, column=1, padx=20, pady=15)
    väljaandmise_kuupäev_label = Label(add_aken, 
                                       text="Väljaandmise kuupäev: ", 
                                       font=("Algerian 30"), 
                                       fg="#A91D3A")
    väljaandmise_kuupäev_label.grid(row=1, column=0, padx=10, pady=15)
    väljaandmise_kuupäev_entry = Entry(add_aken, 
                                        bg="#F3D0D7",
                                        fg="#FF204E", 
                                        font="Georgia 25",
                                        width=15)
    väljaandmise_kuupäev_entry.grid(row=1, column=1, padx=20, pady=15)
    autor_nimi_label = Label(add_aken, 
                           text="Autor_nimi: ", 
                           font=("Algerian 30"), 
                           fg="#A91D3A")
    autor_nimi_label.grid(row=2, column=0, padx=10, pady=15)
    autor_nimi_entry = Entry(add_aken, 
                           bg="#F3D0D7",
                           fg="#FF204E", 
                           font="Georgia 25",
                           width=15)
    autor_nimi_entry.grid(row=2, column=1, padx=20, pady=15)
    zanr_nimi_label = Label(add_aken, 
                          text="Zanri_nimi: ", 
                          font=("Algerian 30"), 
                          fg="#A91D3A")
    zanr_nimi_label.grid(row=3, column=0, padx=20, pady=15)
    zanr_nimi_entry = Entry(add_aken, 
                           bg="#F3D0D7",
                           fg="#FF204E", 
                           font="Georgia 25",
                           width=15)
    zanr_nimi_entry.grid(row=3, column=1, padx=10, pady=15)

    def add_raamat_close():
        pealkiri = pealkiri_entry.get()
        väljaandmise_kuupäev = väljaandmise_kuupäev_entry.get()
        autor_nimi = autor_nimi_entry.get()
        zanri_nimi = zanr_nimi_entry.get()
        add_raamat(conn, pealkiri, väljaandmise_kuupäev, autor_nimi, zanri_nimi)
        add_aken.destroy()

    add_button = Button(add_aken, 
                        text="Lisa raamat",
                        fg="#642ca9",  
                        bg="#ff74d4", 
                        font=("Times New Roman", 30),  
                        command=add_raamat_close)
    add_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)


def delete_raamat_autor_nimi_aken():
    delete_aken = Toplevel(aken)
    delete_aken.title("Raamatute kustutamine autori nime järgi")
    autor_nimi_label = Label(delete_aken, 
                             text="Autor_nimi: ", 
                             font=("Algerian  30"), 
                             fg="#C65BCF")
    autor_nimi_label.grid(row=0, column=0, padx=10, pady=5)
    autor_nimi_entry = Entry(delete_aken,
                           bg="#F27BBD",
                           fg="#10439F", 
                           font="Georgia 25",
                           width=15)
    autor_nimi_entry.grid(row=0, column=1, padx=10, pady=5)

    def delete_raamat_autor_nimi_close():
        autor_nimi = autor_nimi_entry.get()
        delete_raamat_autorNimi(conn, autor_nimi)
        delete_aken.destroy()

    delete_button = Button(delete_aken, 
                           text="Kustuta",
                           bg="#d9d0de",
                           fg="#ed2c34",
                           font="Algerian 25",  
                           command=delete_raamat_autor_nimi_close)
    delete_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)


def delete_raamat_pealkiri_aken():
    delete_aken = Toplevel(aken)
    delete_aken.title("Pealkirjaraamatute kustutamine ")
    pealkiri_label = Label(delete_aken, 
                           text="Pealkiri: ", 
                           font=("Algerian 30"), 
                           fg="#41B06E")
    pealkiri_label.grid(row=0, column=0, padx=10, pady=5)
    pealkiri_entry = Entry(delete_aken,
                           bg="#8DECB4",
                           fg="#141E46", 
                           font="Georgia 25",
                           width=15)
    pealkiri_entry.grid(row=0, column=1, padx=10, pady=5)

    def delete_raamat_pealkiri_close():
        pealkiri = pealkiri_entry.get()
        delete_raamat(conn, pealkiri)
        delete_aken.destroy()

    delete_button = Button(delete_aken, 
                           text="Kustuta",
                           bg="#d9d0de",
                           fg="#ed2c34",
                           font=("Algerian 25"),  
                           command=delete_raamat_pealkiri_close)
    delete_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10) 

def dropTable(table_name, conn):
    try:
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE {table_name}")
        conn.commit()
        messagebox.showinfo(f"Tabel {table_name} on kustutatud!")
    except Exception as e:
        messagebox.showerror(f"Tekkis väga: {e}")

def drop_table_aken(conn):
    drop_aken = Toplevel()
    drop_aken.geometry("600x300") 
    drop_aken.title("Kustuta tabel")
    btn_drop_autorid = Button(drop_aken, 
                              text="Autorite tabeli kustutamine",
                              bg="#c77dff",
                              fg="#ffff00",
                              font=("Times New Roman", 30),                  
                              command=lambda: dropTable("Autorid", conn))
    btn_drop_autorid.pack(pady=5)
    btn_drop_zanrid = Button(drop_aken, 
                             text="Žanritabeli kustutamine",
                             bg="#fff3b0",
                             fg="#ff00cc",
                             font=("Times New Roman", 30),  
                             command=lambda: dropTable("Zanrid", conn))
    btn_drop_zanrid.pack(pady=5)
    btn_drop_raamatud = Button(drop_aken, 
                               text="Kustuta raamatu tabel",
                               bg="#ff74d4",
                               fg="#9a031e",
                               font=("Times New Roman", 30), 
                               command=lambda: dropTable("Raamatud", conn))
    btn_drop_raamatud.pack(pady=5)


btn_fill_tables = Button(aken, 
                         text="Tabeli kustutamine",
                         bg="#ffc4d6",
                         fg="#d1495b",
                         font=("Forte 25"), 
                         width=30,
                         command=lambda:drop_table_aken(conn))
btn_fill_tables.pack()


btn_create_tables = Button(aken, 
                           text="Tabelite loomine", 
                           bg="#8eecf5",
                           fg="#27187e",
                           font=("Forte 25"), 
                           width=25,
                           command=lambda:create_tables(conn))
btn_create_tables.pack()

btn_fill_tables = Button(aken, 
                         text="Tabeli täitmine",
                         bg="#8eecf5",
                         fg="#27187e",
                         font=("Forte 25"),
                         width=25,
                         command=lambda:insert_tables(conn))
btn_fill_tables.pack()

btn_autorid=Button(aken,
                   text="Autorite tabel", 
                   bg="#fbf8cc",
                   fg="#ff7d00",
                   font=("Forte 25"), 
                   width=22, 
                   command=lambda: table_autorid(conn)) 
btn_autorid.pack() 

btn_zanrid=Button(aken,
                  text="Žanrite tabel", 
                  bg="#fbf8cc",
                  fg="#ff7d00",
                  font=("Forte 25"), 
                  width=22, 
                  command=lambda: table_zanr(conn)) 
btn_zanrid.pack() 

btn_raamatud=Button(aken,
                    text="Raamatute tabel",
                    bg="#fbf8cc",
                    fg="#ff7d00",
                    font=("Forte 25"), 
                    width=22, 
                    command=lambda: table_raamatud(conn)) 
btn_raamatud.pack() 

btn_add_zanr = Button(aken, 
                      text="Žanrite lisamine",
                      bg="#b9fbc0",
                      fg="#0a9396",
                      font=("Forte 25"),
                      width=20, 
                      command=add_zanr_aken)
btn_add_zanr.pack()

btn_add_raamat = Button(aken, 
                        text="Raamatute lisamine", 
                        bg="#b9fbc0",
                        fg="#0a9396",
                        font=("Forte 25"), 
                        width=20, 
                        command=add_raamat_aken)
btn_add_raamat.pack()

btn_add_autor = Button(aken, 
                       text="Autoride lisamine",
                       bg="#b9fbc0",
                       fg="#0a9396",
                       font=("Forte 25"), 
                       width=20, 
                       command=add_autor_aken)
btn_add_autor.pack()

btn_delete_raamat = Button(aken, 
                           text="Raamatute kustutamine autori nime järgi",
                           bg="#f7d1cd",
                           fg="#b56576",
                           font=("Forte 25"),
                           width=38, 
                           command=delete_raamat_autor_nimi_aken)
btn_delete_raamat.pack()

btn_delete_raamat = Button(aken, 
                           text="Pealkirjaraamatute kustutamine",
                           bg="#f7d1cd",
                           fg="#b56576",
                           font=("Forte 25"), 
                           width=35, 
                           command=delete_raamat_pealkiri_aken)
btn_delete_raamat.pack() 


aken.mainloop()
