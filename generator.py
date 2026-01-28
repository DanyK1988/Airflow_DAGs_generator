import os
import re
from jinja2 import Template
from datetime import datetime
import ast


SCRIPTS_DIR = "scripts"
TEMPLATES_DIR = "templates"
OUTPUT_DIR = "dags"


TEMPLATE_MAP = {
    ".sql": "sql_template.j2",
    ".py": "python_template.j2"
}

# Виды sql запроса, я решил отойти от DDL и расширил список команд
SQL_SPLIT = ["CREATE", "DROP", "ALTER", "TRUNCATE", "INSERT", "UPDATE", "DELETE", "SELECT"]

def split_sql_blocks(code):
    '''
    Разбиваем sql запрос на таски
    '''
    blocks = []
    current = []

    for line in code.splitlines():
        if any(line.upper().startswith(cmd) for cmd in SQL_SPLIT):
            if current:
                blocks.append("\n".join(current))
                current = []
        current.append(line)

    if current:
        blocks.append("\n".join(current))

    return [b.strip() for b in blocks if b.strip()]

def extract_schedule(code):
    '''
    Добавляем парсер, который будет вытягивать расписание DAG
    В начале каждого скрипта нужно прописать закомментированный кроновский интервал
    Например # 0 2 * * *
    '''
    match = re.search(r"schedule:\s*(.+)", code)
    return match.group(1).strip() if match else "@daily"

def mark_as_processed(filepath):
    '''
    Функция будет помечать отработанные скрипты как .processed
    таким образом при повторном запуске генератора они будут проигнорированы
    '''
    os.rename(filepath, filepath + ".processed")

def extract_python_functions(code):
    ''' Вытягиваем названия функций из скрипта'''
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []
    return [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]

def load_template(template_path):
    with open(template_path, encoding="utf-8") as f:
        return Template(f.read())

def generate_dag_file(script_name, code, template_name, functions=None, sql_blocks=None):
    file_base = os.path.splitext(script_name)[0]
    ext = os.path.splitext(script_name)[1]
    dag_id = f"generated_{ext[1:]}_{file_base}"

    template_path = os.path.join(TEMPLATES_DIR, template_name)
    template = load_template(template_path)

    # Получаем расписание и дату начала
    schedule = extract_schedule(code)
    start_date = datetime.today().strftime("%Y-%m-%d")

    rendered = template.render(
        dag_id=dag_id,
        schedule=schedule,
        start_date=start_date,
        python_code=code if ext == ".py" else "",
        functions=functions or [],
        sql_blocks=sql_blocks or [],
    )

    output_path = os.path.join(OUTPUT_DIR, f"{dag_id}.py")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"✅ Created DAG: {output_path}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for fname in os.listdir(SCRIPTS_DIR):
        if fname.endswith(".processed"):
            continue

        ext = os.path.splitext(fname)[1]
        if ext not in TEMPLATE_MAP:
            continue

        # Добавляем переменную полный путь, чтобы после создания DAG скрипт помечался отработанным
        full_path = os.path.join(SCRIPTS_DIR, fname)

        with open(full_path, encoding="utf-8") as f:
            code = f.read()

        code = re.sub(r"--\s*schedule:.*\n?", "", code)


        # В зависимости от типа файла будем разным способом разбивать скрипт на таски
        if ext == ".py":
            functions = extract_python_functions(code)
            generate_dag_file(fname, code, TEMPLATE_MAP[ext], functions=functions)

        elif ext == ".sql":
            sql_blocks = split_sql_blocks(code)
            generate_dag_file(fname, code, TEMPLATE_MAP[ext], sql_blocks=sql_blocks)


        # Помечаем отработанные скрипты
        mark_as_processed(full_path)

if __name__ == "__main__":
    main()