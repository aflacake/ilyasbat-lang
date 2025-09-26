# helpers/parser.py

from helpers.fungsi import execute_line

def parse_buffer(lines):
    stack = [{"type": "root", "children": []}]
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("ulangi"):
            node = {"type": "loop", "header": line, "children": []}
            stack[-1]["children"].append(node)
            stack.append(node)
        elif line.startswith("jika") or line.startswith("jikalain") or line.startswith("lainnya"):
            node = {"type": "if", "header": line, "children": []}
            stack[-1]["children"].append(node)
            stack.append(node)
        elif line == "selesai":
            stack.pop()
        else:
            stack[-1]["children"].append({"type": "statement", "line": line})
    return stack[0]["children"]

def exec_tree(nodes, env):
    for node in nodes:
        if node["type"] == "statement":
            execute_line(node["line"], env)
        elif node["type"] == "loop":
            parts = node["header"].split()
            count = int(parts[1])
            for _ in range(count):
                exec_tree(node["children"], env)
        elif node["type"] == "if":
            cond = " ".join(node["header"].split()[1:])
            if eval(cond, {}, env):
                exec_tree(node["children"], env)
