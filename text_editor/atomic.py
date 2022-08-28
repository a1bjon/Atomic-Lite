import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkFont
import subprocess
import sys
import os
import pathlib
import datetime
import pyperclip
import time
import colorama

def main():
    start = time.time()
    WIDTH, HEIGHT = '784', '500'
    root = tk.Tk()
    root.title('Atomic Lite')
    root.geometry(f'{WIDTH}x{HEIGHT}')
    root.iconbitmap('app_addons/icon.ico')
    root.config(bg='grey12')

    class App():
        events_arr = []
        def __init__(self, master):
            self.ttl = tk.Label(master, text='[Atomic Lite]', font=('consolas', 15), fg='#9933ff', bg='grey12')
            self.ttl.pack(pady=5)

            self.menu_bar = tk.Frame(master, bg='grey', width=784, height=30)
            self.menu_bar.pack() # fill='x' when more buttons added
            self.menu_bar.pack_propagate(0)

            self.file_name_lbl_con = tk.Frame(master, highlightbackground='grey', highlightthickness=4)
            self.file_name_lbl_con.pack(fill='x')
            self.file_name_lbl = tk.Label(self.file_name_lbl_con,
                text='-- No File --', bg='grey12', fg='#9933ff', font=('consolas bold', 10))
            self.file_name_lbl.pack(fill='x')

            self.open_btn = tk.Button(self.menu_bar, text='Open File',
                bg='grey12', fg='grey', width=10, font=('consolas', 10), command=self.open_file, border=0)
            self.open_btn.pack(padx=4, side='left')

            self.save_btn = tk.Button(self.menu_bar, text='Save As',
                bg='grey12', fg='grey', width=10, font=('consolas', 10), command=self.save, border=0)
            self.save_btn.pack(padx=2, side='left')

            self.rm_file_btn = tk.Button(self.menu_bar, text='RM File',
                bg='grey12', fg='grey', width=10, font=('consolas', 10), command=self.remove_file, border=0)
            self.rm_file_btn.pack(padx=4, side='left')

            self.font_size_con = tk.Frame(self.menu_bar, bg='grey12')
            self.font_size_con.pack(padx=2, side='left')
            self.font_btn_up = tk.Button(self.font_size_con, text='▲',
                bg='grey12', fg='grey', width=3, font=('consolas', 10), border=0, command=self.font_size_up)
            self.font_btn_up.pack(side='left')
            self.font_size_cnt = tk.Label(self.font_size_con, text=12,
                bg='grey12', fg='grey', width=2, font=('consolas', 10))
            self.font_size_cnt.pack(side='left')
            self.font_btn_down = tk.Button(self.font_size_con, text='▼',
                bg='grey12', fg='grey', width=3, font=('consolas', 10), border=0, command=self.font_size_down)
            self.font_btn_down.pack(side='left')

            self.fonts = ['consolas',
                          'calibri',
                          'times',
                          'arial',
                          'verdana',
                          'terminal']
            self.font_option = tk.StringVar()
            self.font_option.set('Font')
            self.font_drop_menu = tk.OptionMenu(self.menu_bar, self.font_option, *self.fonts, command=self.set_font)
            self.font_drop_menu.config(bg='grey12', fg='grey', width=5, font=('consolas', 10), highlightthickness=0, border=0)
            self.font_drop_menu['menu'].config(bg='grey12', fg='grey', activeforeground='#9933ff', activebackground='grey12')
            self.font_drop_menu.pack(padx=4, pady=4, side='left')

            self.themes = ['Dark',
                           'Light',
                           'High Contrast',
                           'Matrix',
                           'Ubuntu']
            self.theme_option = tk.StringVar()
            self.theme_option.set('Theme')
            self.theme_drop_menu = tk.OptionMenu(self.menu_bar, self.theme_option, *self.themes, command=self.set_theme)
            self.theme_drop_menu.config(bg='grey12', fg='grey', width=5, font=('consolas', 10), highlightthickness=0, border=0)
            self.theme_drop_menu['menu'].config(bg='grey12', fg='grey', activeforeground='#9933ff', activebackground='grey12')
            self.theme_drop_menu.pack(pady=4, padx=2, side='left')

            self.copy_btn = tk.Button(self.menu_bar, text='Copy Text', width=10,
                bg='grey12', fg='grey', font=('consolas', 10), border=0, command=self.clipboard)
            self.copy_btn.pack(padx=4, side='left')

            self.reset_btn = tk.Button(self.menu_bar, text='Reset', width=10,
                bg='grey12', fg='grey', font=('consolas', 10), border=0, command=self.reset_settings)
            self.reset_btn.pack(padx=2, side='left')

            self.help_btn = tk.Button(self.menu_bar, text='Help', width=10,
                bg='grey12', fg='grey', font=('consolas', 10), border=0, command=self.help)
            self.help_btn.pack(padx=4, side='left')

            self.quit_btn = tk.Button(self.menu_bar, text='Quit', width=6,
                bg='grey12', fg='grey', font=('consolas', 10), border=0, command=master.destroy)
            self.quit_btn.pack(padx=2, side='left')

            self.scrollbar_con = tk.Frame(master, highlightbackground='grey', highlightthickness=2)
            self.scrollbar_con.pack(side='right', fill='y')
            self.scrollbar = tk.Scrollbar(self.scrollbar_con)
            self.scrollbar.pack(side='right', fill='y')

            self.text_box_con = tk.Frame(master, highlightbackground='grey', highlightthickness=3)
            self.text_box_con.pack()
            self.text_font = tkFont.Font(family='consolas', size=12)
            self.text_box = tk.Text(self.text_box_con, bg='grey12', fg='grey',  height=49, width=211, 
                font=self.text_font, insertbackground='#9933ff', selectbackground='#9933ff', 
                border=0, yscrollcommand=self.scrollbar.set)
            self.text_box.pack()
            self.scrollbar.config(command=self.text_box.yview)

            self.char_cnt = tk.Label(master, text=f'Total: [{0}]',
                bg='grey12', fg='#9933ff', font=('consolas bold', 10))
            self.char_cnt.place(x=0, y=-1)

            self.line_char_cnt = tk.Label(
                master, text=f'Line | Col: [{0}] [{0}]', bg='grey12',
                fg='#9933ff', font=('consolas bold', 10))
            self.line_char_cnt.place(x=0, y=17)

            self.text_box.bind('<KeyPress>', self.update_cnt)
            self.text_box.bind('<KeyRelease>', self.update_cnt)

        def update_cnt(self, event):
            text_length = len(self.text_box.get('1.0', 'end-1c').replace('\n', '')) # returns not counted
            current_line, current_col = self.text_box.index('insert').split('.') # '1.0' -> ['1', '0']

            self.char_cnt.config(text=f'Total: [{text_length}]')
            self.line_char_cnt.config(text=f'Line | Col: [{current_line}] [{current_col}]')

            App.events_arr.append(event)

        def open_file(self):
            try:
                open_file_path = filedialog.askopenfilename(initialdir='/', title='Select File')
                with open(open_file_path, 'r', encoding='utf-8') as file_choice:
                    content = file_choice.read()

                self.text_box.delete('1.0', 'end')
                self.text_box.insert('1.0', content)
                
                file_name = os.path.basename(open_file_path)
                file_timestamp = pathlib.Path(open_file_path).stat().st_mtime
                file_last_mod = datetime.datetime.fromtimestamp(file_timestamp).strftime('[%d-%m-%Y @ %H:%M]')
                self.file_name_lbl.config(text=f'{file_name} | Last modified: {file_last_mod}')

                text_length = len(self.text_box.get('1.0', 'end-1c').replace('\n', '')) # returns not counted
                current_line, current_col = self.text_box.index('insert').split('.') # '1.0' -> ['1', '0']

                self.char_cnt.config(text=f'Total: [{text_length}]')
                self.line_char_cnt.config(
                    text=f'Line | Col: [{current_line}] [{current_col}]')

            except FileNotFoundError:
                return None

            except UnicodeDecodeError:
                return tk.messagebox.showerror(
                 'File Error', 'Could not open selected file')

        def save(self):
            try:
                file_save_path = filedialog.asksaveasfilename(
                    initialdir='/', title='Select Save Destination',
                    initialfile='atomic_file.txt')
                with open(file_save_path, 'w') as new_file:
                    new_file.write(self.text_box.get('1.0','end-1c'))

                file_name = os.path.basename(file_save_path)
                file_timestamp = pathlib.Path(file_save_path).stat().st_mtime
                file_last_mod = datetime.datetime.fromtimestamp(file_timestamp).strftime('[%d-%m-%Y @ %H:%M]')
                self.file_name_lbl.config(text=f'{file_name} | Last modified: {file_last_mod}')

            except FileNotFoundError:
                if self.file_name_lbl['text'] != '-- No File --':
                    return tk.messagebox.showerror(
                     'File Save Error', 'Current file was not saved.')
                return None

        def remove_file(self):
            if self.file_name_lbl['text'] == '-- No File --':
                return tk.messagebox.showerror('File Error',
                    'Cannot remove file as no file is present in environment')
            self.text_box.delete('1.0','end')
            self.file_name_lbl.config(text='-- No File --')
            self.char_cnt.config(text=f'Total: [{0}]')
            self.line_char_cnt.config(text=f'Line | Col: [{0}] [{0}]')

        def set_font(self, font_option_choice):
            self.text_font.config(family=font_option_choice)
            self.font_option.set('Font')

        def font_size_up(self):
            self.text_font['size'] += 2
            if self.text_font['size'] > 100:
                self.text_font['size'] = 12
            self.font_size_cnt['text'] = self.text_font['size']

        def font_size_down(self):
            self.text_font['size'] -= 2
            if self.text_font['size'] < 12:
                self.text_font['size'] = 12
            self.font_size_cnt['text'] = self.text_font['size']

        def help(self):
            if sys.platform == 'win32':
                return subprocess.check_output('notepad.exe app_addons/help.txt', shell=True)

            elif sys.platform == 'darwin':
                return subprocess.check_output('open -a TextEdit app_addons/help.txt', shell=True)

            elif sys.platform == 'linux' or sys.platform == 'linux2':
                return subprocess.check_output('gedit app_addons/help.txt', shell=True)

            return tk.messagebox.showerror(
                 'OS Error', 'Current operating system not supported')

        def clipboard(self):
            text = self.text_box.get('1.0', 'end-1c')
            return pyperclip.copy(text)

        def set_theme(self, set_theme_choice):
            if set_theme_choice == 'Dark':
                root.config(bg='grey12')
                self.ttl.config(bg='grey12', fg='#9933ff')

                self.open_btn.config(bg='grey12', fg='grey')
                self.save_btn.config(bg='grey12', fg='grey')

                self.font_drop_menu.config(bg='grey12', fg='grey')
                self.font_drop_menu['menu'].config(bg='grey12', fg='grey', activeforeground='#9933ff', activebackground='grey12')

                self.theme_drop_menu.config(bg='grey12', fg='grey')
                self.theme_drop_menu['menu'].config(bg='grey12', fg='grey', activeforeground='#9933ff', activebackground='grey12')

                self.text_box.config(bg='grey12', fg='grey', insertbackground='#9933ff', selectbackground='#9933ff')

                self.font_size_con.config(bg='grey12')
                self.font_btn_up.config(bg='grey12', fg='grey')
                self.font_btn_down.config(bg='grey12', fg='grey')
                self.font_size_cnt.config(bg='grey12', fg='grey')

                self.reset_btn.config(bg='grey12', fg='grey')

                self.help_btn.config(bg='grey12', fg='grey')

                self.copy_btn.config(bg='grey12', fg='grey')

                self.quit_btn.config(bg='grey12', fg='grey')

                self.char_cnt.config(bg='grey12', fg='#9933ff')

                self.line_char_cnt.config(bg='grey12', fg='#9933ff')

                self.file_name_lbl.config(bg='grey12', fg='#9933ff')

                self.rm_file_btn.config(bg='grey12', fg='grey')

                self.theme_option.set('Theme')

            elif set_theme_choice == 'Light':
                root.config(bg='white')
                self.ttl.config(bg='white', fg='black')

                self.open_btn.config(bg='white', fg='black')
                self.save_btn.config(bg='white', fg='black')

                self.font_drop_menu.config(bg='white', fg='black')
                self.font_drop_menu['menu'].config(bg='grey', fg='black', activeforeground='black', activebackground='white')

                self.theme_drop_menu.config(bg='white', fg='black')
                self.theme_drop_menu['menu'].config(bg='grey', fg='black', activeforeground='black', activebackground='white')

                self.text_box.config(bg='white', fg='black', insertbackground='black', selectbackground='black')

                self.font_size_con.config(bg='white')
                self.font_btn_up.config(bg='white', fg='black')
                self.font_btn_down.config(bg='white', fg='black')
                self.font_size_cnt.config(bg='white', fg='black')

                self.reset_btn.config(bg='white', fg='black')

                self.help_btn.config(bg='white', fg='black')

                self.copy_btn.config(bg='white', fg='black')

                self.quit_btn.config(bg='white', fg='black')

                self.char_cnt.config(bg='white', fg='black')

                self.line_char_cnt.config(bg='white', fg='black')

                self.file_name_lbl.config(bg='white', fg='black')

                self.rm_file_btn.config(bg='white', fg='black')

                self.theme_option.set('Theme')

            elif set_theme_choice == 'High Contrast':
                root.config(bg='black')
                self.ttl.config(bg='black', fg='#00ffff')

                self.open_btn.config(bg='black', fg='yellow')
                self.save_btn.config(bg='black', fg='yellow')

                self.font_drop_menu.config(bg='black', fg='yellow')
                self.font_drop_menu['menu'].config(bg='black', fg='yellow', activeforeground='#00ffff', activebackground='black')

                self.theme_drop_menu.config(bg='black', fg='yellow')
                self.theme_drop_menu['menu'].config(bg='black', fg='yellow', activeforeground='#00ffff', activebackground='black')

                self.text_box.config(bg='black', fg='#00ffff', insertbackground='yellow', selectbackground='#00ffff')

                self.font_size_con.config(bg='black')
                self.font_btn_up.config(bg='black', fg='yellow')
                self.font_btn_down.config(bg='black', fg='yellow')
                self.font_size_cnt.config(bg='black', fg='yellow')

                self.reset_btn.config(bg='black', fg='yellow')

                self.help_btn.config(bg='black', fg='yellow')

                self.copy_btn.config(bg='black', fg='yellow')

                self.quit_btn.config(bg='black', fg='yellow')

                self.char_cnt.config(bg='black', fg='#00ffff')

                self.line_char_cnt.config(bg='black', fg='#00ffff')

                self.file_name_lbl.config(bg='black', fg='#00ffff')

                self.rm_file_btn.config(bg='black', fg='yellow')

                self.theme_option.set('Theme')

            elif set_theme_choice == 'Matrix':
                root.config(bg='black')
                self.ttl.config(bg='black', fg='#20C20E')

                self.open_btn.config(bg='black', fg='#20C20E')
                self.save_btn.config(bg='black', fg='#20C20E')

                self.font_drop_menu.config(bg='black', fg='#20C20E')
                self.font_drop_menu['menu'].config(bg='black', fg='#20C20E', activeforeground='grey', activebackground='black')

                self.theme_drop_menu.config(bg='black', fg='#20C20E')
                self.theme_drop_menu['menu'].config(bg='black', fg='#20C20E', activeforeground='grey', activebackground='black')

                self.text_box.config(bg='black', fg='#20C20E', insertbackground='#20C20E', selectbackground='#20C20E')

                self.font_size_con.config(bg='black')
                self.font_btn_up.config(bg='black', fg='#20C20E')
                self.font_btn_down.config(bg='black', fg='#20C20E')
                self.font_size_cnt.config(bg='black', fg='#20C20E')

                self.reset_btn.config(bg='black', fg='#20C20E')

                self.help_btn.config(bg='black', fg='#20C20E')

                self.copy_btn.config(bg='black', fg='#20C20E')

                self.quit_btn.config(bg='black', fg='#20C20E')

                self.char_cnt.config(bg='black', fg='#20C20E')

                self.line_char_cnt.config(bg='black', fg='#20C20E')

                self.file_name_lbl.config(bg='black', fg='#20C20E')

                self.rm_file_btn.config(bg='black', fg='#20C20E')

                self.theme_option.set('Theme')

            elif set_theme_choice == 'Ubuntu':
                root.config(bg='#2C001E')
                self.ttl.config(bg='#2C001E', fg='#e6e6e6')

                self.open_btn.config(bg='#2C001E', fg='#e6e6e6')
                self.save_btn.config(bg='#2C001E', fg='#e6e6e6')

                self.font_drop_menu.config(bg='#2C001E', fg='#e6e6e6')
                self.font_drop_menu['menu'].config(bg='#2C001E', fg='#e6e6e6', activeforeground='#80ff00', activebackground='#2C001E')

                self.theme_drop_menu.config(bg='#2C001E', fg='#e6e6e6')
                self.theme_drop_menu['menu'].config(bg='#2C001E', fg='#e6e6e6', activeforeground='#80ff00', activebackground='#2C001E')

                self.text_box.config(bg='#2C001E', fg='#e6e6e6', insertbackground='#80ff00', selectbackground='#e6e6e6')

                self.font_size_con.config(bg='#2C001E')
                self.font_btn_up.config(bg='#2C001E', fg='#e6e6e6')
                self.font_btn_down.config(bg='#2C001E', fg='#e6e6e6')
                self.font_size_cnt.config(bg='#2C001E', fg='#e6e6e6')

                self.reset_btn.config(bg='#2C001E', fg='#e6e6e6')

                self.help_btn.config(bg='#2C001E', fg='#e6e6e6')

                self.copy_btn.config(bg='#2C001E', fg='#e6e6e6')

                self.quit_btn.config(bg='#2C001E', fg='#e6e6e6')

                self.char_cnt.config(bg='#2C001E', fg='#e6e6e6')

                self.line_char_cnt.config(bg='#2C001E', fg='#e6e6e6')

                self.file_name_lbl.config(bg='#2C001E', fg='#80ff00')

                self.rm_file_btn.config(bg='#2C001E', fg='#e6e6e6')

                self.theme_option.set('Theme')


        def reset_settings(self):
            choice = tk.messagebox.askyesno(
             'Reset Settings', 'Are you sure you want to reset all settings to default?')

            if choice:
                root.config(bg='grey12')

                self.ttl.config(bg='grey12', fg='#9933ff')

                self.open_btn.config(bg='grey12', fg='grey')
                self.save_btn.config(bg='grey12', fg='grey')

                self.font_drop_menu.config(bg='grey12', fg='grey')
                self.font_drop_menu['menu'].config(bg='grey12', fg='grey', activeforeground='#9933ff', activebackground='grey12')

                self.theme_drop_menu.config(bg='grey12', fg='grey')
                self.theme_drop_menu['menu'].config(bg='grey12', fg='grey', activeforeground='#9933ff', activebackground='grey12')

                self.text_box.config(bg='grey12', fg='grey', insertbackground='#9933ff')

                self.font_size_con.config(bg='grey12')
                self.font_btn_up.config(bg='grey12', fg='grey')
                self.font_btn_down.config(bg='grey12', fg='grey')
                self.font_size_cnt.config(bg='grey12', fg='grey')

                self.reset_btn.config(bg='grey12', fg='grey')
                self.font_size_cnt['text'] = 12

                self.text_font.config(family='consolas', size= 12)

                self.help_btn.config(bg='grey12', fg='grey')

                self.copy_btn.config(bg='grey12', fg='grey')

                self.quit_btn.config(bg='grey12', fg='grey')

                self.char_cnt.config(bg='grey12', fg='#9933ff')

                self.line_char_cnt.config(bg='grey12', fg='#9933ff')

                self.file_name_lbl.config(bg='grey12', fg='#9933ff')

                self.rm_file_btn.config(bg='grey12', fg='grey')

            return None

    colorama.init(convert=True)
    with open('app_addons/atomic_loading.txt', 'r') as txt:
        cnt = txt.read()
    print(colorama.Fore.CYAN, colorama.Style.BRIGHT, cnt, colorama.Style.RESET_ALL)

    test = App(root)
    root.mainloop()

    end = time.time()
    print('------------------------------------------------')
    total_time = abs(round(start-end, 2))
    print(f'Editor Session Time: [{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}{total_time}s{colorama.Style.RESET_ALL}]')
    print(f'Total Keystrokes: [{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}{int(len(App.events_arr)/2)}{colorama.Style.RESET_ALL}]\n')

if __name__ == '__main__':
    main()
