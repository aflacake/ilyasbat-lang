# helpers/parser.py

from helpers.fungsi import execute_line
from helpers.jika import evaluate_condition


def parse_buffer(lines):
    """
    Ubah list baris menjadi AST tree.
    Setiap node punya {type, header, children}.
    """
    stack = [{"type": "root", "children": []}]

    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        if line.startswith("jika") or line.startswith("jikalain") or line.startswith("lainnya"):
            node = {"type": "ifbranch", "header": line, "children": []}
            stack[-1]["children"].append(node)
            stack.append(node)

        elif line.startswith("ulangi"):
            node = {"type": "loop", "header": line, "children": []}
            stack[-1]["children"].append(node)
            stack.append(node)

        elif line == "selesai":
            if len(stack) > 1:
                stack.pop()
            else:
                raise ValueError("[Parser] 'selesai' tanpa pembuka")

        else:
            stack[-1]["children"].append({"type": "statement", "line": line})

    if len(stack) != 1:
        raise ValueError("[Parser] Blok tidak ditutup dengan benar")

    return stack[0]["children"]


def exec_tree(nodes, env):
    """
    Eksekusi tree hasil parse_buffer.
    """
    i = 0
    while i < len(nodes):
        node = nodes[i]

        if node["type"] == "statement":
            execute_line(node["line"], env)

        elif node["type"] == "ifbranch":
            executed = False
            branches = [node]
            j = i + 1
            while j < len(nodes) and nodes[j]["type"] == "ifbranch":
                branches.append(nodes[j])
                j += 1

            for branch in branches:
                header = branch["header"].split(maxsplit=1)
                cmd = header[0].lower()
                cond_expr = header[1] if len(header) > 1 else ""

                if cmd == "jika" and evaluate_condition(cond_expr.split(), env):
                    exec_tree(branch["children"], env)
                    executed = True
                    break
                elif cmd == "jikalain" and evaluate_condition(cond_expr.split(), env):
                    exec_tree(branch["children"], env)
                    executed = True
                    break
                elif cmd == "lainnya":
                    exec_tree(branch["children"], env)
                    executed = True
                    break

            i = j - 1

        elif node["type"] == "loop":
            header = node["header"].split()
            mode = header[1].lower()

            if mode.isdigit():
                count = int(mode)
                for _ in range(count):
                    exec_tree(node["children"], env)

            elif mode == "sampai":
                cond_expr = " ".join(header[2:])
                while not evaluate_condition(cond_expr.split(), env):
                    exec_tree(node["children"], env)

            elif mode == "untuk":
                try:
                    var = header[2]
                    eq = header[3]
                    rng = header[4]
                    start, end = map(int, rng.split(".."))
                    for v in range(start, end + 1):
                        env[var] = v
                        exec_tree(node["children"], env)
                except Exception as e:
                    print(f"[Kesalahan parsing ulangi untuk: {e}]")

            else:
                print(f"[Loop] Mode tidak dikenal: {mode}")

        i += 1


def parse_block(lines, i, end_token="selesai", alt_end_tokens=None):
    """
    Parse blok multiline (hidup/mati/jika/ulangi).
    end_token default 'selesai'.
    alt_end_tokens bisa dipakai untuk if-chain (jikalain/lainnya).
    """
    block = []
    i += 1
    while i < len(lines):
        line = lines[i].strip()

        if line == end_token or (alt_end_tokens and line in alt_end_tokens):
            return block, i

        node, next_i = parse_line(lines, i)
        block.append(node)
        i = next_i

    raise SyntaxError(f"Blok tidak ditutup dengan {end_token}")


def parse_line(lines, i):
    """Parse satu baris, bisa blok atau baris biasa."""
    line = lines[i].strip()

    if line.startswith("hidup("):
        block, next_i = parse_block(lines, i, end_token=")")
        return {"type": "hidup", "body": block}, next_i + 1

    if line.startswith("mati("):
        block, next_i = parse_block(lines, i, end_token=")")
        return {"type": "mati", "body": block}, next_i + 1

    if line.startswith("jika "):
        cond = line[4:].strip()
        body, next_i = parse_block(lines, i, end_token="selesai",
                                   alt_end_tokens={"jikalain", "lainnya"})
        node = {"type": "jika", "cond": cond, "body": body, "elifs": [], "else": []}

        while next_i < len(lines):
            line2 = lines[next_i].strip()
            if line2.startswith("jikalain "):
                cond2 = line2[8:].strip()
                body2, next_i = parse_block(lines, next_i, end_token="selesai",
                                            alt_end_tokens={"jikalain", "lainnya"})
                node["elifs"].append({"cond": cond2, "body": body2})
            elif line2 == "lainnya":
                body3, next_i = parse_block(lines, next_i, end_token="selesai")
                node["else"] = body3
                break
            else:
                break
        return node, next_i + 1

    if line.startswith("ulangi "):
        header = line.split(maxsplit=1)[1]
        body, next_i = parse_block(lines, i, end_token="selesai")
        node = {"type": "ulangi", "header": header, "body": body}
        return node, next_i + 1

    return line, i + 1


def parse(lines):
    """Parser utama: hasilkan tree nested nodes"""
    tree = []
    i = 0
    while i < len(lines):
        node, next_i = parse_line(lines, i)
        tree.append(node)
        i = next_i
    return tree
