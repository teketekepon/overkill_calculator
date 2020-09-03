
import tkinter.ttk as ttk
from tkinter import *

class MotikosiCalc(ttk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.pack()
        self.st = False
        self.bosshp = IntVar().set('')
        self.damege = IntVar().set('')
        self.master.title(u'持ち越し計算機')
        self.master.geometry('255x245')
        self.master.resizable(0,0)
        self.create_widgets()
        self.create_softkey()
        self.hp_entry.focus_set()

    def ins(self,n):
        if self.st:
            try:
                self.damege.set(self.damege.get()*10+n)
            except TclError:
                self.damege.set(n)
        else:
            try:
                self.bosshp.set(self.bosshp.get()*10+n)
            except TclError:
                self.bosshp.set(n)

    def back(self):
        try:
            if self.st:
                self.damege.set(self.damege.get()//10)
            else:
                self.bosshp.set(self.bosshp.get()//10)
        except TclError:
            pass

    def tens(self):
        try:
            if self.st:
                self.damege.set(self.damege.get()*10000)
            else:
                self.bosshp.set(self.bosshp.get()*10000)
        except TclError:
            pass

    def state(self):
        if self.st:
            self.sbutton['text'] = u'ボス残り体力'
        else:
            self.sbutton['text'] = u'推定ダメージ'
        self.st = not self.st

    def reset(self):
        self.bosshp.set('')
        self.damege.set('')
        self.result.configure(state='normal')
        self.result.delete('1.0', 'end')
        self.result.configure(state='disabled')
        return

    def attack(self):
        try:
            x = self.damege.get()
            y = self.bosshp.get()
        except TclError:
            t = 'Error!'
        else:
            if y - x > 0 or x == 0:  # 討伐に至らない場合
                t = '残りHP: {}'.format(y-x)
                self.bosshp.set(y-x)
            else:  # 討伐した場合
                t = '持ち越し時間は{:.1f}秒です'.format((1-y/x)*90+20)

        self.result.configure(state='normal')
        self.result.delete('1.0','end')
        self.result.insert('1.0',t)
        self.result.configure(state='disabled')

    def create_widgets(self):
        # Text
        self.result = Text(self,font=('MeiryoUI',13),height=1,width=26)
        self.result.insert('1.0',u'ここに結果が表示されます')
        self.result.configure(state='disabled')
        self.result.grid(row=0,column=0,columnspan=2,pady=10)
        # Label
        ttk.Label(self,text=u'ボス残り体力').grid(column=0,row=1,padx=5)
        ttk.Label(self,text=u'推定ダメージ').grid(column=0,row=2,padx=5)
        # Entry
        self.hp_entry = ttk.Entry(self,textvariable=self.bosshp,width=10)
        self.hp_entry.bind('<Return>',lambda *o:self.dmg_entry.focus_set())
        self.hp_entry.grid(column=1,row=1,padx=10,pady=5)
        self.dmg_entry = ttk.Entry(self,textvariable=self.damege,width=10)
        self.dmg_entry.bind('<Return>',lambda *o:self.attack())
        self.dmg_entry.grid(column=1,row=2,padx=10,pady=5)

    def create_softkey(self):
        softkey = ttk.Frame(borderwidth=5,width=260,height=100,relief='groove')
        # tenkey1-9
        for i in range(1,10):
            column = (i+2)%3
            row = -((i-1)//3)+2
            ttk.Button(softkey, text=f'{i}', command=lambda index=i:self.ins(
            index)).grid(column=column,row=row)
        # 1万倍
        ttk.Button(softkey,text=u'万',command=self.tens).grid(column=0,row=3)
        # 0
        ttk.Button(softkey,text='0',command=lambda:self.ins(0)).grid(column=1,row=3)
        # backspace
        ttk.Button(softkey,text='Backspace',command=self.back).grid(column=2,row=3)
        # reset
        ttk.Button(softkey,text='Reset',command=self.reset).grid(column=0,row=4)
        # change state
        self.sbutton = ttk.Button(softkey,text=u'ボス残り体力',command=self.state)
        self.sbutton.grid(column=1,row=4)
        # attack
        ttk.Button(softkey, text='Attack', command=self.attack).grid(column=2,row=4)
        softkey.pack()

if __name__ == '__main__':
    root = Tk()
    style = ttk.Style()
    style.configure('TLabel',font=('游ゴシック',13))
    MotikosiCalc(master=root)
    root.mainloop()
