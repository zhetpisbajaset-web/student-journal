import tkinter as tk
from tkinter import ttk,messagebox
from datetime import date
from db.database import init_db,connect
from models.person import Student,ExamGrade,ControlGrade
class App(tk.Tk):
 def __init__(self):
  super().__init__(); init_db(); self.title('Электрондық студенттер журналы'); self.geometry('850x540'); self.tabs=ttk.Notebook(self); self.tabs.pack(fill='both',expand=True,padx=8,pady=8)
  self.st=ttk.Frame(self.tabs); self.gr=ttk.Frame(self.tabs); self.at=ttk.Frame(self.tabs); self.tabs.add(self.st,text='Студенттер'); self.tabs.add(self.gr,text='Бағалар'); self.tabs.add(self.at,text='Қатысу'); self.students_ui(); self.grades_ui(); self.att_ui(); self.refresh_all()
 def tree(self,parent,cols,heads):
  t=ttk.Treeview(parent,columns=cols,show='headings',height=16)
  for c,h in zip(cols,heads): t.heading(c,text=h); t.column(c,width=130,anchor='center')
  t.pack(fill='both',expand=True,padx=5,pady=5); return t
 def students_ui(self):
  f=ttk.Frame(self.st); f.pack(fill='x',padx=5,pady=5); self.search=tk.StringVar(); ttk.Label(f,text='Іздеу:').pack(side='left'); e=ttk.Entry(f,textvariable=self.search); e.pack(side='left'); e.bind('<KeyRelease>',lambda _ : self.refresh_students())
  f2=ttk.Frame(self.st); f2.pack(fill='x',padx=5); self.n=tk.StringVar(); self.g=tk.StringVar(value='25-12'); self.num=tk.StringVar()
  for label,var in [('Аты-жөні',self.n),('Тобы',self.g),('№',self.num)]: ttk.Label(f2,text=label).pack(side='left'); ttk.Entry(f2,textvariable=var,width=15).pack(side='left',padx=3)
  ttk.Button(f2,text='Қосу',command=self.add_student).pack(side='left',padx=3); ttk.Button(f2,text='Өңдеу',command=self.edit_student).pack(side='left',padx=3); ttk.Button(f2,text='Өшіру',command=self.delete_student).pack(side='left')
  self.stree=self.tree(self.st,('id','name','group','number'),('ID','Аты-жөні','Тобы','Студент №'))
 def grades_ui(self):
  f=ttk.Frame(self.gr); f.pack(fill='x',padx=5,pady=6); self.gs=tk.StringVar(); self.gsub=tk.StringVar(); self.gv=tk.StringVar(); self.gt=tk.StringVar(value='Exam')
  for label,var in [('Студент ID',self.gs),('Пән ID',self.gsub),('Баға',self.gv)]: ttk.Label(f,text=label).pack(side='left'); ttk.Entry(f,textvariable=var,width=8).pack(side='left',padx=3)
  ttk.Combobox(f,textvariable=self.gt,values=['Exam','Control'],state='readonly',width=9).pack(side='left'); ttk.Button(f,text='Баға енгізу',command=self.add_grade).pack(side='left',padx=3)
  self.gtree=self.tree(self.gr,('id','student','subject','score','type','date'),('ID','Студент','Пән','Баға','Түрі','Күні'))
 def att_ui(self):
  f=ttk.Frame(self.at); f.pack(fill='x',padx=5,pady=6); self.asid=tk.StringVar(); self.asub=tk.StringVar(); self.astatus=tk.StringVar(value='Present')
  for label,var in [('Студент ID',self.asid),('Пән ID',self.asub)]: ttk.Label(f,text=label).pack(side='left'); ttk.Entry(f,textvariable=var,width=8).pack(side='left',padx=3)
  ttk.Combobox(f,textvariable=self.astatus,values=['Present','Absent','Late'],state='readonly',width=10).pack(side='left'); ttk.Button(f,text='Белгілеу',command=self.add_att).pack(side='left',padx=3)
  self.atree=self.tree(self.at,('id','student','subject','date','status'),('ID','Студент','Пән','Күні','Қатысу'))
 def refresh_all(self): self.refresh_students(); self.refresh_grades(); self.refresh_att()
 def refresh_students(self):
  if not hasattr(self,'stree'): return
  self.stree.delete(*self.stree.get_children()); q=f'%{self.search.get()}%'
  with connect() as c: rows=c.execute('SELECT students.id,full_name,group_name,student_number FROM students JOIN groups ON group_id=groups.id WHERE full_name LIKE ? OR group_name LIKE ? OR student_number LIKE ?',(q,q,q)).fetchall()
  for r in rows:self.stree.insert('', 'end',values=r)
 def add_student(self):
  try:
   obj=Student(self.n.get(),self.g.get(),self.num.get())
   with connect() as c:
    c.execute('INSERT OR IGNORE INTO groups(group_name) VALUES(?)',(obj.group_name,)); gid=c.execute('SELECT id FROM groups WHERE group_name=?',(obj.group_name,)).fetchone()[0]
    c.execute('INSERT INTO students(full_name,group_id,student_number) VALUES(?,?,?)',(obj.full_name,gid,obj.student_number or None))
   self.n.set('');self.num.set('');self.refresh_students()
  except Exception as ex:messagebox.showerror('Қате',str(ex))

 def edit_student(self):
  sel=self.stree.selection()
  if not sel: messagebox.showinfo('Ескерту','Өңдейтін студентті таңдаңыз'); return
  vals=self.stree.item(sel[0],'values'); sid=vals[0]
  win=tk.Toplevel(self); win.title('Студентті өңдеу'); win.geometry('320x220')
  name=tk.StringVar(value=vals[1]); group=tk.StringVar(value=vals[2]); number=tk.StringVar(value=vals[3] or '')
  for i,(label,var) in enumerate([('Аты-жөні',name),('Тобы',group),('№',number)]):
   ttk.Label(win,text=label).grid(row=i,column=0,padx=8,pady=6); ttk.Entry(win,textvariable=var).grid(row=i,column=1,padx=8,pady=6)
  def save():
   try:
    obj=Student(name.get(),group.get(),number.get())
    with connect() as c:
     c.execute('INSERT OR IGNORE INTO groups(group_name) VALUES(?)',(obj.group_name,))
     gid=c.execute('SELECT id FROM groups WHERE group_name=?',(obj.group_name,)).fetchone()[0]
     c.execute('UPDATE students SET full_name=?,group_id=?,student_number=? WHERE id=?',(obj.full_name,gid,obj.student_number or None,sid))
    win.destroy(); self.refresh_students()
   except Exception as ex: messagebox.showerror('Қате',str(ex))
  ttk.Button(win,text='Сақтау',command=save).grid(row=3,column=0,columnspan=2,pady=10)

 def delete_student(self):
  sel=self.stree.selection()
  if not sel:messagebox.showinfo('Ескерту','Студентті таңдаңыз');return
  sid=self.stree.item(sel[0],'values')[0]
  if messagebox.askyesno('Растау','Өшіру керек пе?'):
   with connect() as c:c.execute('DELETE FROM students WHERE id=?',(sid,))
   self.refresh_all()
 def add_grade(self):
  try:
   sid=int(self.gs.get()); sub=int(self.gsub.get()); obj=ExamGrade(self.gv.get()) if self.gt.get()=='Exam' else ControlGrade(self.gv.get())
   with connect() as c:c.execute('INSERT INTO grades(student_id,subject_id,grade_value,grade_type,grade_date) VALUES(?,?,?,?,?)',(sid,sub,obj.value,obj.grade_type(),date.today().isoformat()))
   self.gv.set('');self.refresh_grades()
  except Exception as ex:messagebox.showerror('Қате','Мәліметтерді тексеріңіз: '+str(ex))
 def refresh_grades(self):
  if not hasattr(self,'gtree'):return
  self.gtree.delete(*self.gtree.get_children())
  with connect() as c:rows=c.execute('SELECT grades.id,full_name,subject_name,grade_value,grade_type,grade_date FROM grades JOIN students ON student_id=students.id JOIN subjects ON subject_id=subjects.id ORDER BY grades.id DESC').fetchall()
  for r in rows:self.gtree.insert('', 'end',values=r)
 def add_att(self):
  try:
   sid=int(self.asid.get()); sub=int(self.asub.get())
   with connect() as c:c.execute('INSERT INTO attendance(student_id,subject_id,lesson_date,status) VALUES(?,?,?,?)',(sid,sub,date.today().isoformat(),self.astatus.get()))
   self.refresh_att()
  except Exception as ex:messagebox.showerror('Қате','ID дұрыс па? '+str(ex))
 def refresh_att(self):
  if not hasattr(self,'atree'):return
  self.atree.delete(*self.atree.get_children())
  with connect() as c:rows=c.execute('SELECT attendance.id,full_name,subject_name,lesson_date,status FROM attendance JOIN students ON student_id=students.id JOIN subjects ON subject_id=subjects.id ORDER BY attendance.id DESC').fetchall()
  for r in rows:self.atree.insert('', 'end',values=r)
if __name__=='__main__':App().mainloop()
