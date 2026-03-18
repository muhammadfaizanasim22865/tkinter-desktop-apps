import tkinter as tk

root=tk.Tk()
root.title("fizzy calculator")

entry_var=tk.StringVar()
entry=tk.Entry(root,textvariable=entry_var,font=("arial",20),justify="right",bg="#1e1e2f",fg="#f5f5f5",insertbackground="#00ffcc")
entry.grid(row=0,column=0,columnspan=4,ipadx=8,ipady=8)

def button_click(value):
    if value=="C":
        entry_var.set("")
    elif value=="=":
        try:
            result=str(eval(entry_var.get()))
            entry_var.set(result)
        except:
            entry_var.set("invalid!")
    else:
        entry_var.set(entry_var.get()+value)


buttons=[("7",1,0),("8",1,1),("9",1,2),("*",1,3),
         ("4",2,0),("5",2,1),("6",2,2),("/",2,3),
         ("1",3,0),("2",3,1),("3",3,2),("-",3,3),
         ("0",4,0),(".",4,1),("=",4,2),("+",4,3),
         ("C",5,0) ]


for (text,row,col) in buttons:
    color="#2d2d44"
    fg="white"
    if text in ("+","-","*","/"):
        color="#ff8c42"
        fg="black"
    elif text=="=":
        color="#4caf50"
        fg="white"
    elif text=="C":
        color="#e63946"
        fg="white"

    btn=tk.Button(root,text=text,bg=color,fg=fg,width=5,height=2)
    btn.grid(row=row,column=col,padx=3,pady=3)

    btn.config(command=lambda t=text : button_click(t))

root.mainloop()
































































