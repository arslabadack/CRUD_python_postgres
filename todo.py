from tkinter import Tk, Button, Label, Scrollbar, Listbox, StringVar, Entry, W,E,N,S,END
from tkinter import ttk
from tkinter import messagebox
import psycopg2 as psy
from dbconfig import dbcon

con = psy.connect(**dbcon)
print(con)

cursor = con.cursor()

class TodoApp:
    def __init__(self):
        self.con = psy.connect(**dbcon)
        self.cursor = con.cursor()
        print("You have connected to the database")

    def __del__(self):
        self.con.close()
    
    def view(self):
        self.cursor.execute("SELECT * FROM todo")
        rows = self.cursor.fetchall()
        return rows

    def insert(self, title):
        sql = ("INSERT INTO todo(title)VALUES (%s)")
        values = [title]
        self.cursor.execute(sql,values)
        self.con.commit()
        messagebox.showinfo(title="Todolist Database", message="New task added")
    
    def update(self, id, title):
        tsql = 'UPDATE todo SET title = %s WHERE id=%s'
        self.cursor.execute(tsql, [title,id])
        self.con.commit()
        messagebox.showinfo(title="Todolist Database", message="Task Updated")
    
    def delete(self, id):
        delquery = 'DELETE FROM todo WHERE id = %s'
        self.cursor.execute(delquery, [id])
        self.con.commit()
        messagebox.showinfo(title="Todolist Database", message="Task Deleted")
    
db = TodoApp()

def get_selected_row(event):
    global selected_task
    index = list_bx.curselection()[0]
    selected_task = list_bx.get(index)
    title_entry.delete(0, 'end')
    title_entry.insert('end', selected_task[1])
    
def view_records():
    list_bx.delete(0, 'end')
    for row in db.view():
        list_bx.insert('end', row)
        
def add_task():
    db.insert(title_text.get())
    list_bx.delete(0, 'end')
    list_bx.insert('end', (title_text.get()))
    title_entry.delete(0, "end")
    con.commit()
    view_records()
    clear_screen()
    
def delete_task():
    db.delete(selected_task[0])
    con.commit()
    view_records()
    clear_screen()
    
def clear_screen():
    title_entry.delete(0, 'end')
    
def update_task():
    db.update(selected_task[0], title_text.get())
    title_entry.delete(0, "end")
    con.commit()
    view_records()
    clear_screen()
    
    
root = Tk()

root.title("Adam's Todo List App")
root.configure(background="light blue")
root.geometry ("600x600")
root.resizable(width=False, height=False)
title_label=ttk.Label(root,text="New Task",background="light blue",font=("Fira Code", 14))
title_label.grid(row=0, column=1, sticky=W)
title_text = StringVar()
title_entry = ttk.Entry(root,width=40, textvariable=title_text)
title_entry.grid(row=0, column=2, sticky=W)

add_btn = Button(root, text="Add Task", bg="purple", fg="white", font="helvetica 10 bold", command=add_task)
add_btn.grid(row=0, column=3, sticky=W)

list_bx = Listbox(root, height=16, width=40, font="helvetica 13", bg="white")
list_bx.grid(row=3, column=1, columnspan=14, sticky=W + E, pady=40, padx=15)
list_bx.bind('<<ListboxSelect>>', get_selected_row)

scroll_bar = Scrollbar(root)
scroll_bar.grid(row=1, column=8, rowspan=14, sticky=W)

list_bx.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=list_bx.yview)

modify_btn = Button(root, text="Modify Task", bg="purple", fg="white", font="helvetica 10 bold", command=update_task)
modify_btn.grid(row=15, column=1)

delete_btn = Button(root, text="Delete Task", bg="purple", fg="white", font="helvetica 10 bold", command=delete_task)
delete_btn.grid(row=15, column=2, padx=35)

exit_btn = Button(root, text="Exit Application", bg="purple", fg="white", font="helvetica 10 bold", command=root.destroy)
exit_btn.grid(row=15, column=3)

view_records()

root.mainloop()
