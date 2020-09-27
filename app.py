
import tkinter.ttk as ttk
import tkinter as tk
from tkinter.ttk import Widget


class App(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.master.title(u'持ち越し計算機')
        self.master.minsize(255, 130)
        self.master.maxsize(255, 265)
        # Define Variables
        self.bosshp = tk.StringVar()
        self.bosshp.set('')
        self.damege = tk.StringVar()
        self.damege.set('')
        self.st = tk.BooleanVar(False)
        # Criate Widgets
        self.create_widgets()
        self.hp_entry.focus_set()
        self.master.bind_all("<Return>", lambda *o: self.attack())
        self.master.bind_all("<equal>", lambda *o: self.attack())

    def attack(self):
        try:
            x = int(self.damege.get())
            y = int(self.bosshp.get())
        except Exception:
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
        self.hp_entry.grid(column=1, row=1, padx=10, pady=5)
        self.dmg_entry = ttk.Entry(self, textvariable=self.damege, width=10)
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
        self.tgl = False
        self.create_widgets()
        # Binding Keys
        master.bind_all("<Button-1>", self.on_click_entry)
        master.bind_all("<Delete>", lambda *o: self.reset())
        master.bind_all("<period>", lambda *o: self.reset())
        master.bind_all("<Tab>", self.state_key)
        master.bind_all("<slash>", self.state_key)
        master.bind_all("<asterisk>", self.state_key)
        master.bind_all("<minus>", self.state_key)
        master.bind_all("<plus>", self.state_key)

    def on_click_entry(self, event):
        focus = self.focus_get()
        if focus == self.a.hp_entry:
            self.a.st.set(False)
            self.sbutton['text'] = u'ボス残り体力'
        if focus == self.a.dmg_entry:
            self.a.st.set(True)
            self.sbutton['text'] = u'推定ダメージ'

    def toggle(self):
        self.tgl = not self.tgl
        if self.tgl:
            self.softkey.pack(fill='y', expand=True)
        else:
            self.softkey.pack_forget()

    def ins(self, n):
        st = self.a.st.get()
        if st:
            try:
                m = int(self.a.damege.get())
                self.a.damege.set(str(m*10+n))
            except Exception:
                self.a.damege.set(str(n))
        else:
            try:
                m = int(self.a.bosshp.get())
                self.a.bosshp.set(str(m*10+n))
            except Exception:
                self.a.bosshp.set(str(n))

    def back(self):
        st = self.a.st.get()
        try:
            if st:
                m = int(self.a.damege.get())
                self.a.damege.set(str(m//10))
            else:
                m = int(self.a.bosshp.get())
                self.a.bosshp.set(str(m//10))
        except Exception:
            pass

    def tens(self):
        st = self.a.st.get()
        try:
            if st:
                m = int(self.a.damege.get())
                self.a.damege.set(str(m*10000))
            else:
                m = int(self.a.bosshp.get())
                self.a.bosshp.set(str(m*10000))
        except Exception:
            pass

    def state_key(self, event):
        st = self.a.st.get()
        if not event.keysym == 'Tab':
            if st:
                self.a.damege.set(self.a.damege.get().rstrip('+-*/'))
            else:
                self.a.bosshp.set(self.a.bosshp.get().rstrip('+-*/'))
        if st:
            self.a.hp_entry.focus_set()
            self.sbutton['text'] = u'ボス残り体力'
        else:
            self.a.dmg_entry.focus_set()
            self.sbutton['text'] = u'推定ダメージ'
        self.a.st.set(not st)

    def state_button(self):
        st = self.a.st.get()
        if st:
            self.a.hp_entry.focus_set()
            self.sbutton['text'] = u'ボス残り体力'
        else:
            self.a.dmg_entry.focus_set()
            self.sbutton['text'] = u'推定ダメージ'
        self.a.st.set(not st)

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
                                  command=self.state_button)
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
