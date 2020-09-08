
import tkinter.ttk as ttk
import tkinter as tk


class App(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.master.title(u'持ち越し計算機')
        self.master.minsize(255, 130)
        self.master.maxsize(255, 265)
        self.bosshp = tk.IntVar()
        self.bosshp.set('')
        self.damege = tk.IntVar()
        self.damege.set('')
        self.create_widgets()
        self.hp_entry.focus_set()

    def attack(self):
        try:
            x = self.damege.get()
            y = self.bosshp.get()
        except tk.TclError:
            t = 'Error!'
        else:
            if y - x > 0 or x == 0:  # 討伐に至らない場合
                t = '残りHP: {}'.format(y-x)
                self.bosshp.set(y-x)
            else:  # 討伐した場合
                t = '持ち越し時間は{:.1f}秒です'.format((1-y/x)*90+20)
        self.result.configure(state='normal')
        self.result.delete('1.0', 'end')
        self.result.insert('1.0', t)
        self.result.configure(state='disabled')

    def create_widgets(self):
        # Text
        self.result = tk.Text(self, font=('MeiryoUI', 13), height=1, width=26)
        self.result.insert('1.0', u'ここに結果が表示されます')
        self.result.configure(state='disabled')
        self.result.grid(row=0, column=0, columnspan=2, pady=10)
        # Label
        ttk.Label(self, text=u'ボス残り体力').grid(column=0, row=1, padx=5)
        ttk.Label(self, text=u'推定ダメージ').grid(column=0, row=2, padx=5)
        # Entry
        self.hp_entry = ttk.Entry(self, textvariable=self.bosshp, width=10)
        self.hp_entry.bind('<Return>', lambda *o: self.dmg_entry.focus_set())
        self.hp_entry.grid(column=1, row=1, padx=10, pady=5)
        self.dmg_entry = ttk.Entry(self, textvariable=self.damege, width=10)
        self.dmg_entry.bind('<Return>', lambda *o: self.attack())
        self.dmg_entry.grid(column=1, row=2, padx=10, pady=5)
        # self.toggle_softkey = ttk.Button(self, text='ソフトキー切り替え',
        #                                  command=self.toggle)


class Softkey(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        ttk.Button(master, text='ソフトキー切り替え',
                   command=self.toggle).grid(column=0, row=3, columnspan=2)
        self.a = master
        self.softkey = ttk.Frame(borderwidth=5, width=260,
                                 height=100, relief='groove')
        self.st = False
        self.tgl = False
        self.create_widgets()

    def toggle(self):
        self.tgl = not self.tgl
        if self.tgl:
            self.softkey.pack(fill='y', expand=True)
        else:
            self.softkey.pack_forget()

    def ins(self, n):
        if self.st:
            try:
                self.a.damege.set(self.a.damege.get()*10+n)
            except tk.TclError:
                self.a.damege.set(n)
        else:
            try:
                self.a.bosshp.set(self.a.bosshp.get()*10+n)
            except tk.TclError:
                self.a.bosshp.set(n)

    def back(self):
        try:
            if self.st:
                self.a.damege.set(self.a.damege.get()//10)
            else:
                self.a.bosshp.set(self.a.bosshp.get()//10)
        except tk.TclError:
            pass

    def tens(self):
        try:
            if self.st:
                self.a.damege.set(self.a.damege.get()*10000)
            else:
                self.a.bosshp.set(self.a.bosshp.get()*10000)
        except tk.TclError:
            pass

    def state(self):
        if self.st:
            self.sbutton['text'] = u'ボス残り体力'
        else:
            self.sbutton['text'] = u'推定ダメージ'
        self.st = not self.st

    def reset(self):
        self.a.bosshp.set('')
        self.a.damege.set('')
        self.a.result.configure(state='normal')
        self.a.result.delete('1.0', 'end')
        self.a.result.configure(state='disabled')
        return

    def create_widgets(self):
        # tenkey1-9
        for i in range(1, 10):
            column = (i+2) % 3
            row = -((i-1)//3)+2
            ttk.Button(self.softkey, text=f'{i}', command=lambda index=i:
                       self.ins(index)).grid(column=column, row=row)
        # 1万倍
        ttk.Button(self.softkey, text=u'万',
                   command=self.tens).grid(column=0, row=3)
        # 0
        ttk.Button(self.softkey, text='0',
                   command=lambda: self.ins(0)).grid(column=1, row=3)
        # backspace
        ttk.Button(self.softkey, text='Backspace',
                   command=self.back).grid(column=2, row=3)
        # reset
        ttk.Button(self.softkey, text='Reset',
                   command=self.reset).grid(column=0, row=4)
        # change state
        self.sbutton = ttk.Button(self.softkey, text=u'ボス残り体力',
                                  command=self.state)
        self.sbutton.grid(column=1, row=4)
        # attack
        ttk.Button(self.softkey, text='Attack',
                   command=lambda: App.attack(self.a)).grid(column=2, row=4)


if __name__ == '__main__':
    root = tk.Tk()
    style = ttk.Style()
    style.configure('TLabel', font=('游ゴシック', 13))
    app = App(master=root)
    Softkey(master=app)
    root.mainloop()
