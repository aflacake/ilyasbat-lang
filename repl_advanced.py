# repl_advanced.py

from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings
from pygments.lexer import RegexLexer
from pygments.token import Keyword, Name, Operator, Number, String, Text

from repl import run_module, env, fungsi_end, fungsi_append, in_fungsi_mode

in_jika_mode = False

class IlyasBatLexer(RegexLexer):
    name = "ilyasbat"
    tokens = {
        "root": [
            (r"\b(fungsi|gema|impor|kalku|kembalikan|masukkan|melompat|selesai|jalan|reset|keluar|lihat|variabel)\b", Keyword),
            (r"\b(jika|maka|tulis|menampilkan|mengembalikan|menyimpan|ulangi|berakhir)\b", Keyword),
            (r"[0-9]+", Number),
            (r"\".*?\"", String),
            (r"[a-zA-Z_][a-zA-Z0-9_]*", Name),
            (r"[\+\-\*/=]", Operator),
            (r"\s+", Text),
        ]
    }

keywords = [
    "fungsi", "selesai", "kembalikan", "kalku", "jalan", "reset",
    "keluar", "lihat", "variabel", "jika", "maka", "tulis", "menampilkan", "berakhir",
    "gema", "impor", "masukkan", "melompat", "mengembalikan", "menyimpan", "ulangi" 
]
completer = WordCompleter(keywords, ignore_case=True)

style = Style.from_dict({
    "prompt": "ansicyan bold",
})

def jika_append(line: str):
    buffer.append(line)

def jika_end():
    global buffer
    print("[Blok jika tersimpan]")
    for l in buffer:
        print("   ", l)
    buffer = []

def continuation(width, line_number, is_soft_wrap):
    if in_fungsi_mode or in_jika_mode:
        return "    "
    return ""

def main():
    print("== IlyasBat REPL Lanjutan ==")
    print("Tips:")
    print(" - Ketik 'keluar' untuk keluar")
    print(" - Tekan Shift+Enter untuk pindah baris")
    print(" - Tekan Enter untuk eksekusi blok input\n")

    history = InMemoryHistory()

    kb = KeyBindings()

    @kb.add("enter")
    def _(event):
        buff = event.app.current_buffer
        if buff.validate():
            event.app.exit(result=buff.text)
        else:
            buff.insert_text("\n")

    @kb.add("s-enter")
    def _(event):
        event.app.current_buffer.insert_text("\n")

    session = PromptSession(
        history=history,
        completer=completer,
        auto_suggest=AutoSuggestFromHistory(),
        lexer=PygmentsLexer(IlyasBatLexer),
        style=style,
        multiline=True,
        prompt_continuation=continuation,
        key_bindings=kb,
    )

    buffer = []

    while True:
        try:
            inp = session.prompt("[IlyasBat]> ", style=style).rstrip()
        except (EOFError, KeyboardInterrupt):
            print("\nKeluar.")
            break

        if in_fungsi_mode:
            if not inp.strip():
                fungsi_end()
                continue

            for line in inp.splitlines():
                if not line.startswith("    "):
                    line = "    " + line
                fungsi_append(line)
            continue

        if inp.startswith("jika "):
            in_jika_mode = True
            buffer = []
            print("[Mulai blok jika]")
            continue

        if inp.strip() == "selesai" and in_jika_mode:
            in_jika_mode = False
            jika_end()
            continue

        if in_jika_mode:
            if not inp.strip():
                jika_end()
                continue

            for line in inp.splitlines():
                if not line.startswith("    "):
                    line = "    " + line
                jika_append(line)
            continue

        if inp.lower() == "keluar":
            break
        elif inp.lower() == "reset":
            buffer.clear()
            print("[penyangga dikosongkan]")
        elif inp.lower() == "lihat variabel":
            if env:
                for k, v in env.items():
                    print(f"{k} = {v}")
            else:
                print("[belum ada variabel]")
        elif inp.lower() == "jalan":
            for line in buffer:
                parts = line.strip().split()
                if not parts:
                    continue
                cmd, args = parts[0], parts[1:]
                run_module(cmd, args)
        else:
            for line in inp.splitlines():
                buffer.append(line.strip())

if __name__ == "__main__":
    main()
