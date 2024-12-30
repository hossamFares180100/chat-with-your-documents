import tkinter as tk
from tkinter import messagebox
from tkinter import*
from tkinter import ttk
from datetime import datetime

import sqlite3


class Ostaz:
    def __init__(self,root):
        self.root=root
        self.root.title("دفتر الاستاذ")
        # Dashboard background color
        self.root.configure(bg="#34495e")

        self.screenW = self.root.winfo_screenwidth()
        self.screenH = self.root.winfo_screenheight()
        taskbar_height = 40  # Assuming the taskbar height is 40 pixels (you should adjust this according to your system)
        self.root.geometry("%dx%d+%d+%d" % (self.screenW, self.screenH - taskbar_height, -12, 0))
        self.root.resizable(False, False)

        self.var_mden=StringVar()
        self.var_date_number=StringVar()
        self.var_date_number2=StringVar()
        ################title######
        lbl_title=Label(self.root,text="Student Support System",font=("times new roman",40,"bold"),bg="black",fg="silver",bd=4,relief=RIDGE)
        lbl_title.place(x=0,y=0,width=self.screenW,height=50)
        
        
        
        # Username Label and Entry
        self.askQuestion = tk.Label(self.root, text="Your Question:", font=("Helvetica", 16), bg="#2980b9", fg="white")
        self.askQuestion.pack()
        self.askQuestion_entry = tk.Entry(self.root, font=("Helvetica", 16))
        self.askQuestion_entry.pack(pady=5)

        def filterByDate(data,start_date_str,end_date_str):
            # Convert string dates to datetime objects
            start_date = datetime.strptime(start_date_str.get(), "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str.get(), "%Y-%m-%d")
            
            # Filter data based on date range
            filtered_data = [item for item in data if start_date <= datetime.strptime(item[1], "%Y-%m-%d") <= end_date]
            return filtered_data
            
        def filterByMdean(data,mdean):
            print(data)
            print(mdean)
            res=[]
            for i in data:
                mdeanA = ast.literal_eval(i[3])
                if(mdean in mdeanA):
                    res.append(i)
            return res
        
        def createDict(mdeanA,mdeanV,daenA,daenV):
            d = {}
            v=0
            for i in range(len(mdeanA)): 
                key=mdeanA[i] 
                l = []
                tot=0
                val = int(mdeanV[i])
                for j in range(v,len(daenA)):
                    v+=1
                    l.append(daenA[j])
                    tot+= int(daenV[j])
                    if(tot==val):
                        break
                d[key] = l
                if v==len(daenA):
                    v=v-1
                #print(v)
            return d
                
        def show():
            delete_buttonm.config(text = str(0))  
            delete_buttond.config(text = str(0))  
            self.Cust_Details_Table.delete(*self.Cust_Details_Table.get_children())
            db = DataBase()
            data= db.showAllFatoras()
            allData=[]
            for row in data:
                allData.append(row)
            res = filterByMdean(allData, self.var_mden.get())
            res = filterByDate(res, self.var_date_number,self.var_date_number2)
            print(res)
           
            su2=0
            su=0
            for r in res:
                mdeanA = ast.literal_eval(r[3])
                mdeanV = ast.literal_eval(r[4])
                daenA = ast.literal_eval(r[6])
                daenV = ast.literal_eval(r[7])
                dic = createDict(mdeanA,mdeanV,daenA,daenV)
                print(dic)
                daenVV=[]
                for key,val in dic.items():
                    
                    if key==self.var_mden.get():
                        print(val)                        
                        mkey=mdeanA.index(key)
                        su = su + int(mdeanV[mkey])
                        for i in range(len(val)):
                            dkey=daenA.index(val[i])
                            if(int(daenV[dkey])>int(mdeanV[mkey])):
                                daenVV.append(mdeanV[mkey])
                                su2=su2+int(mdeanV[mkey])
                            else:
                                daenVV.append(daenV[dkey])
                                su2=su2+int(daenV[dkey])     
                        self.Cust_Details_Table.insert('',END,values=(r[1],key,int(mdeanV[mkey]),str(val),str(daenVV)))
            
            delete_buttonm.config(text = str(su))  
            delete_buttond.config(text = str(su2))  
            print(su)
            print(su2)
                    
            
        btnShow=Button(self.root,command=show,text="عرض",bg="black",fg="gold",width=15,font=("times new roman",12,"bold"))
        btnShow.place(x=self.screenW/2+20,y=110)
        
        lblT=Label(self.root,bd=2,relief=RIDGE,text="نوع الحساب",font=("times new roman",15,"bold"),padx=2)
        lblT.place(x=self.screenW/2+240,y=72,width=135)        
        
        
        
        
        
        delete_buttonm = Label(self.root, text="0", bg="black",fg="gold",font=("times new roman",12,"bold"),width=25)
        delete_buttonm.place(x=self.screenW/2-260,y=5/8 * self.screenH)
        
        # Button to delete selected item
        delete_buttond = Label(self.root, text="0",bg="black",fg="gold",width=25,font=("times new roman",12,"bold"))
        delete_buttond.place(x=self.screenW/2+120,y=5/8 * self.screenH)
        lblT2=Label(self.root,bd=2,relief=RIDGE,text="الاجمالي",font=("times new roman",15,"bold"),padx=2)
        lblT2.place(x=self.screenW-350,y=5/8 * self.screenH,width=135)   
        
        
        
        
        
        details_table=Frame(self.root,bd=2,relief=RIDGE)
        
        details_table.place(x=self.screenW/16,y=170,width=self.screenW-450,height=300)
        scroll_x=ttk.Scrollbar(details_table,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(details_table,orient=VERTICAL)
        
        self.Cust_Details_Table=ttk.Entry(details_table,column=("التاريخ","مدين","المبلغ","دائن","القيمه"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

 

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)


        scroll_x.config(command=self.Cust_Details_Table.xview)
        scroll_y.config(command=self.Cust_Details_Table.yview)
       
             
        self.Cust_Details_Table.pack(fill=BOTH,expand=1)
        
        
        def back():
            self.root.destroy()
            root=Tk()
            obj=Dashboard(root)
            root.mainloop() 
        btnBack=Button(self.root,command=back,text="رجوع",bg="black",fg="gold",width=25,font=("times new roman",15,"bold"))
        btnBack.place(x=20,y=self.screenH-200)
        
        def logout():
            self.root.destroy()
            root=Tk()
            obj=LoginScreen(root)
            root.mainloop() 
        btnBack2=Button(self.root,command=logout,text="تسجيل الخروج",bg="black",fg="gold",width=25,font=("times new roman",15,"bold"))
        btnBack2.place(x=350,y=self.screenH-200)



class Dashboard:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("dashboard")

        self.screenW = self.parent.winfo_screenwidth()
        self.screenH = self.parent.winfo_screenheight()
        taskbar_height = 40  # Assuming the taskbar height is 40 pixels (you should adjust this according to your system)
        self.parent.geometry("%dx%d+%d+%d" % (self.screenW, self.screenH - taskbar_height, -12, 0))
        self.parent.resizable(False, False)


        # Dashboard background color
        self.parent.configure(bg="#34495e")

        # Dashboard Title
        self.title_label = tk.Label(self.parent, text="Student Support System", font=("Helvetica", 20, "bold"), bg="#34495e", fg="white")
        self.title_label.pack(pady=20)

        # Buttons Frame
        self.buttons_frame = tk.Frame(self.parent, bg="#34495e")
        self.buttons_frame.pack(expand=True)

        # Button 1
        self.button1 = tk.Button(self.buttons_frame, text="Ask PDF", command=self.AskPDFScreen, font=("Helvetica", 16), bg="#2ecc71", fg="white", padx=40, pady=20, bd=2, relief=tk.FLAT)
        self.button1.grid(row=0, column=0, padx=20, pady=20)

        # Button 2
        self.button2 = tk.Button(self.buttons_frame, text="Summarize PDF", command=self.summarizePDFScreen, font=("Helvetica", 16), bg="#3498db", fg="white", padx=40, pady=20, bd=2, relief=tk.FLAT)
        self.button2.grid(row=0, column=1, padx=20, pady=20)

        # Button 3
        self.button3 = tk.Button(self.buttons_frame, text="دفتر المراجعات", command=self.button3_clicked, font=("Helvetica", 16), bg="#e74c3c", fg="white", padx=40, pady=20, bd=2, relief=tk.FLAT)
        self.button3.grid(row=1, column=0, padx=20, pady=20)

        # Button 4
        self.button4 = tk.Button(self.buttons_frame, text="تسجيل خروج", command=self.button4_clicked, font=("Helvetica", 16), bg="#f39c12", fg="white", padx=40, pady=20, bd=2, relief=tk.FLAT)
        self.button4.grid(row=1, column=1, padx=20, pady=20)

    def AskPDFScreen(self):
        self.parent.destroy()
        root=Tk()
        obj=Cust_Win(root)
        root.mainloop() 

    def summarizePDFScreen(self):
        self.parent.destroy()
        root=Tk()
        obj=Ostaz(root)
        root.mainloop() 

    def button3_clicked(self):
        messagebox.showinfo("Button 3 Clicked", "You clicked Button 3!")

    def button4_clicked(self):
        self.parent.destroy()
        root=Tk()
        obj=LoginScreen(root)
        root.mainloop() 




if __name__ == "__main__":
    root=Tk()
    dashboard = Dashboard(root)
    dashboard.parent.mainloop()
