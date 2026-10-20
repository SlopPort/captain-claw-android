"""Small bilingual frontend for the existing local-data packer; never downloads Claw.

LLM-authored adaptation work; see docs/DEVELOPMENT-NOTES.md for provenance.
The worker owns subprocesses only. All Tk updates stay on the UI thread.
"""
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

PORT = Path(__file__).resolve().parents[1]


def main():
    root = tk.Tk()
    root.title('Kapitan Pazur / Claw — game-data.zip')
    root.geometry('680x420')
    lang = tk.StringVar(value='PL')
    messages = queue.Queue()
    busy = False
    text = {
        'PL': ('Przygotuj dane gry',
               'Wybierz CLAW.REZ ze swojej instalacji gry na komputerze.\n'
               'Powstanie osobny game-data.zip. Oryginał nie zostanie zmieniony.\n'
               'Potrzebny jest Git i internet do pobrania otwartych zależności.\n'
               'Program nie pobiera gry Claw.',
               'Wybierz CLAW.REZ i przygotuj ZIP', 'Przygotowywanie…',
               'Gotowe. Skopiuj ten plik na telefon do Pobranych:\n',
               'Brakuje Git. Zainstaluj Git, zamknij i otwórz ponownie ten program.'),
        'EN': ('Prepare game data',
               'Select CLAW.REZ from your own PC game installation.\n'
               'A separate game-data.zip is created; original files stay unchanged.\n'
               'Git and internet are needed to fetch open-source dependencies.\n'
               'This tool does not download the Claw game.',
               'Select CLAW.REZ and prepare ZIP', 'Preparing…',
               'Done. Copy this file into Downloads on your phone:\n',
               'Git is missing. Install Git, then close and reopen this tool.')}
    tk.OptionMenu(root, lang, 'PL', 'EN').pack(anchor='e', padx=16, pady=8)
    description = tk.Label(root, justify='left', wraplength=640)
    description.pack(fill='x', padx=16, pady=8)
    output = tk.Text(root, height=10, wrap='word', state='disabled')

    def append(value):
        output.configure(state='normal')
        output.insert('end', value + '\n')
        output.see('end')
        output.configure(state='disabled')

    def refresh(*_):
        description.configure(text=text[lang.get()][1])
        if not busy:
            button.configure(text=text[lang.get()][2])

    def worker(game_root):
        try:
            # Reuse the pinned bootstrap and packer rather than duplicating archive logic.
            for args in ([sys.executable, '-u', str(PORT/'tools/bootstrap.py')],
                         [sys.executable, '-u', str(PORT/'tools/pack_assets.py'),
                          '--game-root', str(game_root)]):
                with subprocess.Popen(args, cwd=PORT, stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT, text=True,
                                      encoding='utf-8', errors='replace') as process:
                    for line in process.stdout:
                        messages.put(('line', line.rstrip()))
                    if process.wait():
                        raise RuntimeError('Preparation failed. See output above. / Przygotowanie nie powiodło się.')
            messages.put(('done', str(PORT/'build/game-data.zip')))
        except Exception as error:
            messages.put(('error', str(error)))

    def start():
        nonlocal busy
        if not shutil.which('git'):
            messagebox.showerror('Git', text[lang.get()][6])
            return
        path = filedialog.askopenfilename(title='Select / Wybierz CLAW.REZ',
                                          filetypes=[('CLAW.REZ', '*.REZ *.rez'), ('All files', '*')])
        if not path:
            return
        selected = Path(path)
        if selected.name.lower() != 'claw.rez':
            messagebox.showerror('CLAW.REZ', 'Select / Wybierz CLAW.REZ')
            return
        busy = True
        button.configure(state='disabled', text=text[lang.get()][3])
        threading.Thread(target=worker, args=(selected.parent,), daemon=True).start()

    button = tk.Button(root, command=start)
    button.pack(fill='x', padx=16, pady=8)
    output.pack(fill='both', expand=True, padx=16, pady=8)
    lang.trace_add('write', refresh)

    def poll():
        nonlocal busy
        while not messages.empty():
            kind, value = messages.get_nowait()
            append(value)
            if kind in ('done', 'error'):
                busy = False
                button.configure(state='normal')
                refresh()
                if kind == 'done':
                    messagebox.showinfo('game-data.zip', text[lang.get()][5] + value)
                else:
                    messagebox.showerror('Error / Błąd', value)
        root.after(100, poll)

    def close():
        # Avoid leaving a half-written archive by closing the UI during packaging.
        if busy:
            messagebox.showinfo('Please wait / Poczekaj', text[lang.get()][3])
        else:
            root.destroy()

    root.protocol('WM_DELETE_WINDOW', close)
    refresh()
    poll()
    root.mainloop()


if __name__ == '__main__':
    main()
