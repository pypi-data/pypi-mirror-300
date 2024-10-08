from tkinter import Tk,Text,Canvas,Button,INSERT,messagebox,END,filedialog,Toplevel,Label,PhotoImage,Listbox,Scrollbar
import os,threading,time,subprocess
import pyperclip
Lk=None
carpets=None
nameFile=None
scrolls=None
def wait():
        messagebox.showinfo("Espera","Espera mientras se ejecuta tu programa...")
def resize_canvas(event,canvas):
  
    global Lk,scrolls
    x=A.geometry()
    x=x.split("+")[0]
    x=x.split("x")[0]
    
    canvas2.config(width=int(x))
    canvas.place(x=-2,y=0,height=int(A.winfo_height()+20))
    scrolly.config(command=B.yview)
    B.config(yscrollcommand=scrolly.set)
    scrolly.place(x=(int(x)-20),y=50,height=int(int(str(A.winfo_height()))//1.1))
    ButtonPlay.place(x=int(x)-200,y=15)
    if Lk!=None:
            
            
            
            canvas.config(width=150)
            
            Lk.config(height=int(int(str(A.winfo_height())[:-1])//2))
            scrolls.place(x=130,y=0,height=int(str(A.winfo_height())))
            Lk.config(yscrollcommand=scrolls.set)
x=False
def xs():
    global x
    x=True
xzc=True
w=None
hh=0
def seleccion(event,carpeta,B):
    global nameFile
    click=event.widget
    index=click.curselection()
    if index:
            val=click.get(index)
            nameFile=val
            with open(carpeta+f"/{val}","r") as f:
                    B.delete("1.0",END)
                    B.insert("1.0",f.read())
def BC():
    global x,Lk,scrolls,carpets
    
    while True:
            carpeta=filedialog.askdirectory()
            if carpeta:
                    carpets=carpeta
                    print(os.listdir(carpeta))
                    canvas.delete("all")
                    listaCarp=os.listdir(carpeta)
                    Button2.pack(side="bottom",padx=0,pady=(0,25))
                    Button3.pack(side="bottom",padx=0,pady=(0,10))
                    Lista=Listbox(canvas,width=20,height=int(int(str(A.winfo_height())[:-1])//2))
                    Lista.place(x=0,y=0)
                    Lista.bind("<<ListboxSelect>>",lambda event:seleccion(event,carpeta,B))
                    scroll=Scrollbar(canvas,orient="vertical",command=Lista.yview)
                    scroll.place(x=130,y=0,height=int(str(A.winfo_height())))
                    for i in listaCarp:
                        Lista.insert(END,i)
                    Lk=Lista
                    scrolls=scroll
                    Lista.config(yscrollcommand=scroll.set)
                    break
            else:
                    path3="KomiPensativa.png"
                    a=Toplevel()
                    a.attributes("-toolwindow",True)
                    a.attributes("-topmost",True)
                    a.title("¿SEGURO?")
                    a.focus()
                    a.bell()
                    a.grab_set()
                    a.geometry("300x200")
                    a.resizable(0,0)
                    imagen=PhotoImage(file=path3)
                    lab_img=Label(a,image=imagen)
                    lab_img.image=imagen
                    lab_img.place(x=0,y=100)
                    L1=Label(a,text="¿Estás seguro de cancelar?")
                    L1.pack(pady=(20,10))
                    B1=Button(a,text="Si",command=lambda:[a.destroy(),xs()],width=20)
                    B2=Button(a,text="No",command=lambda:a.destroy(),width=20)
                    B1.place(x=150,y=100)
                    B2.place(x=150,y=150)
                    a.wait_window()
            if x==True:
                    x=False
                    break
def h():
    pid=os.getpid()
    os.system(f"taskkill /f /pid {pid}")
def GD():
    global carpets,nameFile,Lk,gg,gg2
    if carpets!=None and nameFile !=None and Lk!=None:
            with open(carpets+f"/{nameFile}","w") as f:
                    LLS=Lk.get("1.0",END)
                    lls=LLS.replace(" » ","      ")
                    f.write(lls)
    else:
            archivo=filedialog.asksaveasfilename(
                    title="¿Guardar como?",
                    defaultextension=".txt"
            )
            
            if archivo:
                    gg2=archivo
                    gg=archivo.split("/")[-1]
                    print(archivo)
                    with open(archivo,"w") as f:
                        LLS=B.get("1.0",END)
                        lls=LLS.replace(" » ","      ")
                        f.write(lls)
def K(event,B):
    CTRL=event.state & 0x0004
    if CTRL and event.keysym.lower()=="g" or CTRL and event.keysym.lower()=="s":
            GD()
    elif CTRL and event.keysym.lower()=="o":
            AD(B)
    elif CTRL and event.keysym.lower()=="f":
            BC()
    elif CTRL and event.keysym.lower()=="n":
            ND()
CXX=50
CXXX=120
gg=None
gg2=None
def comando(xs,names,B):
    global gg,gg2    
    gg2=names    
    gg=names.split("/")[-1]    
    print("boton en la pocision ",xs)
    print("El archivo es: ",names)
    with open(names,"r") as f:
            s=f.read()
            s=s.replace("     "," » ")
            B.delete("1.0",END)
            B.insert("1.0",s)
datosList=[]
def hh(BB,A):
    BB.grab_release()
    BB.destroy()
dic={}
def comandc(names,names_cls,B):
    global dic,CXX,CXXX,datosList,nbotones,gg,gg2
    for i in range(0,len(datosList)):
            if datosList[i] ==names:
                    print(datosList)
                    datosList.pop(i)
                    print(datosList)
                    break
    if names_cls in dic:
        CXX-=150
        CXXX-=150
        with open(names,"w") as f:
            LLS=B.get("1.0",END)
            lls=LLS.replace(" » ","      ")
            f.write(lls)
        names_cls1=names_cls.split("_")[0]
        dic[names_cls1].destroy()
        dic[names_cls].destroy()
        del dic[names_cls1]
        del dic[names_cls]
        B.delete("1.0",END)
        CXXn=50
        CXXXn=120
        print(nbotones)
        if nbotones>0:
            for i in list(dic.keys()):
                if "_cerrar" in i:
                        
                        dic[i].place(x=CXXXn,y=15)
                        CXXn+=150
                        CXXXn+=150
                else:
                        dic[i].place(x=CXXn,y=15)

                        
                
            nbotones-=1
        
        if dic!={}:
            for i in range(0,len(datosList)):
                if datosList[i]==list(dic.keys())[0]:
                    gg2=datosList[i]    
                    datz=datosList[i].split("/")[-1]
                    gg2=datz
                    with open(datosList[i],"r") as f:
                        s=f.read()
                        s=s.replace("     "," » ")
                        B.delete("1.0",END)
                        B.insert("1.0",s)
                    break
        else:
            gg=None
            gg2=None    
            datosList.clear()
nbotones=0            
xll=True
def AD(B):
    global CXX,CXXX,dic,datosList,nbotones,xll,gg,gg2
    archivoz=filedialog.askopenfilename(title="Abrir un archivo")
    
    if archivoz:
        
        if archivoz in datosList:
                xll=False
                BB=Toplevel(A)
                BB.geometry("350x350")
                AA=PhotoImage(file="komiTriste.png")
                Label3=Label(BB,image=AA)
                Label3.image=AA
                BT1=Button(BB,text="OK",command=lambda:hh(BB,A))
                label2=Label(BB,text="El archivo ya esta en uso")
                label2.pack()
                Label3.pack(pady=10)
                BT1.pack()
                BB.attributes("-toolwindow",True)
                BB.resizable(0,0)
                BB.attributes("-topmost",True)
                BB.grab_set()
                BB.focus()
                BB.bell()
                BB.protocol("WM_DELETE_WINDOW",lambda:hh(BB,A))
                BB.wait_window()

        else:
                namesValue=archivoz.split("/")[-1]
                if namesValue.split(".")[-1] in ("png","jpg","jfif"):
                        BB=Toplevel(A)
                        BB.geometry("350x350")
                        AA=PhotoImage(file="komiTriste.png")
                        Label3=Label(BB,image=AA)
                        Label3.image=AA
                        BT1=Button(BB,text="OK",command=lambda:hh(BB,A))
                        label2=Label(BB,text="Todavia no aceptamos imagenes espera a la proxima version")
                        label2.pack()
                        Label3.pack(pady=10)
                        BT1.pack()
                        BB.attributes("-toolwindow",True)
                        BB.resizable(0,0)
                        BB.attributes("-topmost",True)
                        BB.grab_set()
                        BB.focus()
                        BB.bell()
                        BB.protocol("WM_DELETE_WINDOW",lambda:hh(BB,A))
                else:
                        gg2=archivoz
                        gg=namesValue
                        datosList.append(archivoz)
                try:
                        with open(archivoz,"r") as f:
                                s=f.read()
                                s=s.replace("     "," » ")
                                B.delete("1.0",END)
                                B.insert("1.0",s)
                        arch=archivoz.split("/")[-1]
                        if len(arch)>8:
                                sd=arch
                                arch=""
                                for i in range(0,len(sd)):
                                        
                                        if i>8:
                                                break
                                        else:
                                                arch+=sd[i]
                                arch+="..."
                        names=archivoz
                        
                        
                        if CXX>=450:
                                BB=Toplevel(A)
                                BB.geometry("350x350")
                                AA=PhotoImage(file="komiTriste.png")
                                Label3=Label(BB,image=AA)
                                Label3.image=AA
                                BT1=Button(BB,text="OK",command=lambda:hh(BB,A))
                                label2=Label(BB,text="Son muchos archivos por favor cierra alguno")
                                label2.pack()
                                Label3.pack(pady=10)
                                BT1.pack()
                                BB.attributes("-toolwindow",True)
                                BB.resizable(0,0)
                                BB.attributes("-topmost",True)
                                BB.grab_set()
                                BB.focus()
                                BB.bell()
                                BB.protocol("WM_DELETE_WINDOW",lambda:hh(BB,A))
                        else:
                                nbotones+=1
                                B2=Button(canvas2,text=arch,command=lambda CXX=CXX,names=names:comando(CXX,names,B),borderwidth=0,fg="white",bg="black",font=("Arial",10))
                                B2.place(x=CXX,y=15)
                                dic[names]=B2                          
                                xcerrar=names+"_cerrar"        
                                Bcloses=Button(canvas2,text="x",command=lambda names=names,names_cls=xcerrar:comandc(names,names_cls,B),borderwidth=0,fg="white",bg="black",font=("Arial",10))
                                Bcloses.place(x=CXXX,y=15)
                                dic[names+"_cerrar"]=Bcloses
                                
                                CXX+=150
                                CXXX+=150
                except:
                        BB=Toplevel(A)
                        BB.title("")
                        BB.geometry("350x350")
                        AA=PhotoImage(file="komiTriste.png")
                        Label3=Label(BB,image=AA)
                        Label3.image=AA
                        BT1=Button(BB,text="OK",command=lambda:hh(BB,A))
                        label2=Label(BB,text="Hubo un error intentando abrir el archivo\npor favor elije otro o revisalo")
                        label2.pack()
                        Label3.pack(pady=10)
                        BT1.pack()
                        BB.attributes("-toolwindow",True)
                        BB.resizable(0,0)
                        BB.attributes("-topmost",True)
                        BB.grab_set()
                        BB.focus()
                        BB.bell()
                        BB.protocol("WM_DELETE_WINDOW",lambda:hh(BB,A))
                    
tam=10
def td(B):
    inx="1.0"
    while True:
            
            dat=B.index("insert")
            #print(dat)
            #print(inx)
            
            if "print" in B.get("1.0",dat):
                    strs=B.search("print",inx,END)
                    if strs:
                        B.tag_add("colored",strs,str(strs.split(".")[0])+"."+str(len("print")))
                        B.tag_configure("colored", foreground="red")
                        inx=dat.split(".")[0]+".0"
            
def keys(event,B):
    global tam
    CTRL=event.state & 0x0004
    dat=B.index("insert")
    
            
    print(event.keysym)
    if event.keysym.lower()=="braceleft":
            if "}" in B.get(dat,str(float(dat)+1)):
                    B.insert(dat,"{")
            else:
                    B.insert(dat,"{}")
            return "break"
    elif event.keysym.lower()=="parenleft":
            if ")" in B.get(dat,str(float(dat)+1)):
                    B.insert(dat,"(")
            else:
                    B.insert(dat,"()")
            return "break"
    elif event.keysym.lower()=="tab":
            B.insert(dat," » ")
            return "break"
    elif event.keysym.lower()=="bracketleft":
            if "]" in B.get(dat,str(float(dat)+1)):
                    B.insert(dat,"[")
            else:
                    B.insert(dat,"[]")
            return "break"
    elif event.keysym.lower()=="quotedbl":
            if "\"" in B.get(dat,str(float(dat)+1)):
                    B.insert(dat,"\"")
            else:
                    B.insert(dat,"\"\"")
            return "break"        
    elif event.keysym.lower()=="less":
            if ">" in B.get(dat,str(float(dat)+1)):
                    B.insert(dat,"<")
            else:
                    B.insert(dat,"<>")
            return "break"
    elif CTRL and event.keysym.lower()=="v":
            datosP=pyperclip.paste()
            datosP=datosP.replace("      "," » ")
            B.insert("insert",datosP)
            return "break"
    elif CTRL and event.keysym.lower()=="plus":
            
            if tam<=100:
                    tam+=10
            B.config(font=("Arial",tam))
            print(tam)
            rez()
    elif CTRL and event.keysym.lower()=="minus":
            
            if tam>=10:
                    tam-=10
            B.config(font=("Arial",tam))
            print(tam)
            rez()
    if "*htm" in B.get("1.0",END):
            varD=B.search("*htm","1.0",END)
            B.delete(varD,f"{varD}+5c")
            B.insert("insert","<!DOCTYPE html>\n<html lang=\"es\">\n<head>\n<meta charset=\"UTF-8\">\n<title>\n\n</title>\n</head>\n<body>\n<center>\n<p>Hola mundo</p>\n</center>\n<style>\n\n<style>\n<script>\n\n</script>\n</body>\n</html>")
            return "break"
    

def rez():
    f=A.geometry()
    f=f.split("+")[0]
    f=f.split("x")
    A.geometry(f"{f[0]}x{f[1]}")
def ayuda():
    G=Toplevel()
    G.geometry("500x500")
    G.title("Ayuda")
    Ls1=Label(G,text="combinaciones con teclas:\nabrir un documento:\n\"CTRL\" + \"o\"\nguardar un documento:\n\"CTRL\" + \"s\" o \"CTRL\" + \"g\"\nabrir o cambiar de carpeta:\n\"CTRL\" + \"f\"\nNuevo documento:\nCTRL + \"n\"",font=("Arial",20))
    Ls2=Label(G,text="Ayuda de texto:\n*html\ngenera la sintaxis basica\n",font=("Arial",20))
    Ls1.pack()
    Ls2.pack()
def buttonPlay(B):
    global gg,gg2,CXX,CXXX,dic,datosList,nbotones
    print("valor de ",gg)
    if gg==None:
        BB=Toplevel(A)
        BB.title("")
        BB.geometry("350x350")
        AA=PhotoImage(file="komiFeliz.png")
        Label3=Label(BB,image=AA)
        Label3.image=AA
        BT1=Button(BB,text="OK",command=lambda:hh(BB,A))
        label2=Label(BB,text="primero guarda tu archivo")
        label2.pack()
        Label3.pack(pady=10)
        BT1.pack()
        BB.attributes("-toolwindow",True)
        BB.resizable(0,0)
        BB.attributes("-topmost",True)
        BB.grab_set()
        BB.focus()
        BB.bell()
        BB.protocol("WM_DELETE_WINDOW",lambda:hh(BB,A))
        BB.wait_window()
        GD()
        
    if gg!=None:
        ff=gg.split("/")[-1]
        ff=ff.split(".")[-1]
        with open(gg2,"w") as f:
                LLS=B.get("1.0",END)
                lls=LLS.replace(" » ","      ")
                f.write(lls)
        if ff.lower() in ("py","pyw"):                
                try:
                        print("val ",gg)
                        if not(gg2) in datosList:
                                names=gg
                                datosList.append(gg2)
                                nbotones+=1
                                B2=Button(canvas2,text=gg,command=lambda CXX=CXX,names=names:comando(CXX,names,B),borderwidth=0,fg="white",bg="black",font=("Arial",10))
                                B2.place(x=CXX,y=15)
                                dic[names]=B2                          
                                xcerrar=names+"_cerrar"        
                                Bcloses=Button(canvas2,text="x",command=lambda names=names,names_cls=xcerrar:comandc(names,names_cls,B),borderwidth=0,fg="white",bg="black",font=("Arial",10))
                                Bcloses.place(x=CXXX,y=15)
                                dic[names+"_cerrar"]=Bcloses
                                CXX+=150
                                CXXX+=150
                        subprocess.Popen(["cmd.exe","/c",f"python {gg}"])
                        
                except:
                        print("no tienes python")       
        elif ff.lower()=="c":
                try:
                        threading.Thread(target=wait).start()
                        vvc=gg.split(".")[:-1]
                        print("valor de vvc ",vvc[0])
                        comandoa=f"gcc -o {vvc[0]} {gg}"
                        cvvv=os.path.dirname(gg2)
                        print(cvvv)
                        os.chdir(cvvv)
                        print(os.getcwd())
                        gg3=gg.replace(".c",".exe")
                        if not(gg2) in datosList:
                                names=gg
                                datosList.append(gg2)
                                nbotones+=1
                                B2=Button(canvas2,text=gg,command=lambda CXX=CXX,names=names:comando(CXX,names,B),borderwidth=0,fg="white",bg="black",font=("Arial",10))
                                B2.place(x=CXX,y=15)
                                dic[names]=B2                          
                                xcerrar=names+"_cerrar"        
                                Bcloses=Button(canvas2,text="x",command=lambda names=names,names_cls=xcerrar:comandc(names,names_cls,B),borderwidth=0,fg="white",bg="black",font=("Arial",10))
                                Bcloses.place(x=CXXX,y=15)
                                dic[names+"_cerrar"]=Bcloses
                                CXX+=150
                                CXXX+=150
                        subprocess.Popen(["cmd.exe","/c",comandoa])
                        
                        time.sleep(5)
                        
                        if os.path.exists(gg3):
                                cmds=f"start {gg3}"
                                print(gg3)
                                subprocess.Popen(["cmd.exe","/c",cmds])
                        else:
                                print("el archivo no existe")
                except Exception as e:
                        print("no tienes c ",e)
        elif ff.lower()=="html":
                try:
                        if not(gg2) in datosList:
                                names=gg
                                datosList.append(gg2)
                                nbotones+=1
                                B2=Button(canvas2,text=gg,command=lambda CXX=CXX,names=names:comando(CXX,names,B),borderwidth=0,fg="white",bg="black",font=("Arial",10))
                                B2.place(x=CXX,y=15)
                                dic[names]=B2                          
                                xcerrar=names+"_cerrar"        
                                Bcloses=Button(canvas2,text="x",command=lambda names=names,names_cls=xcerrar:comandc(names,names_cls,B),borderwidth=0,fg="white",bg="black",font=("Arial",10))
                                Bcloses.place(x=CXXX,y=15)
                                dic[names+"_cerrar"]=Bcloses
                                CXX+=150
                                CXXX+=150
                        #gg=gg.split("/")[-1]
                        print(gg2)
                        program="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                        subprocess.Popen([program,gg2])
                except:
                        print("no hay chrome")
        else:
                BB=Toplevel(A)
                BB.title("")
                BB.geometry("350x350")
                AA=PhotoImage(file="komiTriste.png")
                Label3=Label(BB,image=AA)
                Label3.image=AA
                BT1=Button(BB,text="OK",command=lambda:hh(BB,A))
                label2=Label(BB,text="no se encontro la forma de ejecutar el archivo    ")
                label2.pack()
                Label3.pack(pady=10)
                BT1.pack()
                BB.attributes("-toolwindow",True)
                BB.resizable(0,0)
                BB.attributes("-topmost",True)
                BB.grab_set()
                BB.focus()
                BB.bell()
                BB.protocol("WM_DELETE_WINDOW",lambda:hh(BB,A))
                BB.wait_window()
def ND():
        global dic,CXX,CXXX,datosList,nbotones,gg,gg2
        gg=None
        gg2=None
        B.delete("1.0",END)
        

A=Tk()
A.protocol("WM_DELETE_WINDOW",h)
A.minsize(500,500)
A.title("IDE")
B=Text(A)
B.pack(padx=(150,0),pady=(50,0),expand=True,fill="both")
canvas=Canvas(A,width=150,bg="black")
canvas.place(x=-2,y=0,height=int(A.winfo_height()+20))
scrolly=Scrollbar(A,orient="vertical",bg="blue")
scrolly.place(x=0,y=0,height=int(str(A.winfo_height())))
canvas2=Canvas(A,width=int(A.winfo_width()+20),bg="blue")
canvas2.place(x=150,y=0,height=50)
Button1=Button(A,text="¿Deseas agregar\nuna carpeta?",command=BC,font=("Arial",10))
Button2=Button(canvas,text="¿Deseas cambiar\nde carpeta?",command=BC,width=17,borderwidth=0,fg="white",bg="black",font=("Arial",10))
btnid=canvas.create_window(70, 50, window=Button1)
Button2.pack_forget()
ButtonPlay=Button(canvas2,text="➤",bg="blue",command=lambda:buttonPlay(B))
ButtonPlay.place(x=0,y=0)
Button0=Button(canvas,text="¿Guardar documento?",command=GD,font=("Arial",10))
btnid2=canvas.create_window(70, 150, window=Button0)
Button3=Button(canvas,text="¿Guardar documento?",command=GD,width=17,borderwidth=0,fg="white",bg="black",font=("Arial",10))
Button3.pack_forget()
Button42=Button(canvas,text="Documento Nuevo",command=ND,width=17,font=("Arial",10))
btnida=canvas.create_window(70, 350, window=Button42)
Button4=Button(canvas,text="Abrir documento",command=lambda:AD(B),width=17,font=("Arial",10))
btnid3=canvas.create_window(70, 250, window=Button4)
Button6=Button(canvas,text="ayuda",command=ayuda,width=17,font=("Arial",10))
btnid6=canvas.create_window(70, 400, window=Button6)
B.bind("<KeyPress>",lambda event:keys(event,B))
A.bind("<KeyPress>",lambda event:K(event,B))
A.bind("<Configure>",lambda event:resize_canvas(event,canvas))
A.mainloop()

