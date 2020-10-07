
import tkinter.ttk as ttk
import tkinter as tk


class App(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.master.title('Overkill_calcurator')
        self.master.minsize(255, 130)
        self.master.maxsize(255, 265)
        # Define Variables
        self.bosshp = tk.StringVar()
        self.damage = tk.StringVar()
        self.st = tk.BooleanVar(False)
        self.tgl = False
        # Criate Widgets
        self.create_widgets()
        self.hp_entry.focus_set()
        self.softkey = ttk.Frame(borderwidth=5, width=260,
                                 height=100, relief='groove')
        self.create_softkey()
        # Bind Key events
        self.master.bind_all("<Return>", lambda *o: self.attack())
        self.master.bind_all("<equal>", lambda *o: self.attack())
        self.master.bind_all("<Delete>", lambda *o: self.reset())
        self.master.bind_all("<period>", lambda *o: self.reset())
        self.master.bind_all("<Escape>", lambda *o: self.reset())
        self.master.bind_all("<Button-1>", self.click_entry)
        self.master.bind_all("<Tab>", self.state_key)
        self.master.bind_all("<slash>", self.state_key)
        self.master.bind_all("<asterisk>", self.state_key)
        self.master.bind_all("<minus>", self.state_key)
        self.master.bind_all("<plus>", self.state_key)

    def attack(self):
        try:
            x = int(self.damage.get())
            y = int(self.bosshp.get())
        except Exception:
            t = 'Error!'
        else:
            if y - x > 0 or x == 0:  # 討伐に至らない場合
                t = f'Enemy HP: {y-x}'
                self.bosshp.set(str(y-x))
                self.damage.set('')
            else:  # 討伐した場合
                r = int((1-y/x)*90+20)
                if r > 90:
                    t = 'Carry-over time is 90 seconds'
                else:
                    t = f'Carry-over time is {r} seconds'
        self.result.configure(state='normal')
        self.result.delete('1.0', 'end')
        self.result.insert('1.0', t)
        self.result.configure(state='disabled')

    def create_widgets(self):
        # Text
        self.result = tk.Text(self, font=('MeiryoUI', 13), height=1, width=26)
        self.result.insert('1.0', 'The result is displayed here')
        self.result.configure(state='disabled')
        self.result.grid(row=0, column=0, columnspan=2, pady=10)
        # Label
        ttk.Label(self, text='Enemy HP', font=('游ゴシック', 13)
                  ).grid(column=0, row=1, padx=5)
        ttk.Label(self, text='Damage', font=('游ゴシック', 13)
                  ).grid(column=0, row=2, padx=5)
        # Entry
        self.hp_entry = ttk.Entry(self, textvariable=self.bosshp, width=10)
        self.hp_entry.grid(column=1, row=1, padx=10, pady=5)
        self.dmg_entry = ttk.Entry(self, textvariable=self.damage, width=10)
        self.dmg_entry.grid(column=1, row=2, padx=10, pady=5)
        ttk.Button(self, text='Toggle Softkey',
                   command=self.toggle).grid(column=0, row=3, columnspan=2)

    def click_entry(self, event):
        focus = self.focus_get()
        if focus == self.hp_entry:
            self.st.set(False)
            self.sbutton['text'] = 'Enemy HP'
        elif focus == self.dmg_entry:
            self.st.set(True)
            self.sbutton['text'] = 'Damage'

    def toggle(self):
        self.tgl = not self.tgl
        if self.tgl:
            self.softkey.pack(fill='y', expand=True)
        else:
            self.softkey.pack_forget()

    def ins(self, n):
        if self.st.get():
            try:
                m = int(self.damage.get())
                self.damage.set(str(m*10+n))
            except Exception:
                self.damage.set(str(n))
        else:
            try:
                m = int(self.bosshp.get())
                self.bosshp.set(str(m*10+n))
            except Exception:
                self.bosshp.set(str(n))

    def tens(self):
        try:
            if self.st.get():
                m = int(self.damage.get())
                self.damage.set(str(m*10000))
            else:
                m = int(self.bosshp.get())
                self.bosshp.set(str(m*10000))
        except Exception:
            pass

    def back(self):
        try:
            if self.st.get():
                m = self.damage.get()
                self.damage.set(m[0:-1])
            else:
                m = self.bosshp.get()
                self.bosshp.set(m[0:-1])
        except Exception:
            pass

    def reset(self):
        self.bosshp.set('')
        self.damage.set('')
        self.result.configure(state='normal')
        self.result.delete('1.0', 'end')
        self.result.configure(state='disabled')

    def state_button(self):
        st = self.st.get()
        if self.st.get():
            self.hp_entry.focus_set()
            self.sbutton['text'] = 'Enemy HP'
        else:
            self.dmg_entry.focus_set()
            self.sbutton['text'] = 'Damage'
        self.st.set(not st)

    def state_key(self, event):
        st = self.st.get()
        if not event.keysym == 'Tab':
            if st:
                self.damage.set(self.damage.get().rstrip('+-*/'))
            else:
                self.bosshp.set(self.bosshp.get().rstrip('+-*/'))
        if st:
            self.hp_entry.focus_set()
            self.sbutton['text'] = 'Enemy HP'
        else:
            self.dmg_entry.focus_set()
            self.sbutton['text'] = 'Damage'
        self.st.set(not st)

    def create_softkey(self):
        # Tenkey1-9
        for i in range(1, 10):
            column = (i+2) % 3
            row = -((i-1)//3)+2
            ttk.Button(self.softkey, text=f'{i}', command=lambda index=i:
                       self.ins(index)).grid(column=column, row=row)
        # 1万倍
        ttk.Button(self.softkey, text='x10000',
                   command=self.tens).grid(column=0, row=3)
        # 0
        ttk.Button(self.softkey, text='0',
                   command=lambda: self.ins(0)).grid(column=1, row=3)
        # Backspace
        ttk.Button(self.softkey, text='Backspace',
                   command=self.back).grid(column=2, row=3)
        # Reset
        ttk.Button(self.softkey, text='Reset',
                   command=self.reset).grid(column=0, row=4)
        # State
        self.sbutton = ttk.Button(self.softkey, text='Enemy HP',
                                  command=self.state_button)
        self.sbutton.grid(column=1, row=4)
        # Attack
        ttk.Button(self.softkey, text='Attack',
                   command=self.attack).grid(column=2, row=4)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(master=root)
    app.mainloop()
