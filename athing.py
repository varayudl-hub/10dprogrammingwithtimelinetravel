import sys
import re
import os
import subprocess
import time

class Dimension:
    def __init__(self):
        self.number = 0
        self.console = []

class Timeline:
    def __init__(self):
        self.dimensions = [Dimension() for _ in range(10)]
        self.current_dim_index = 0

    @property
    def current_dimension(self):
        return self.dimensions[self.current_dim_index]

def run_10d_program(source_code):
    clean_code = re.sub(r'#.*', '', source_code)
    dimensions_code = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', clean_code)
    
    if not dimensions_code:
        print("\n[Sistema] Error: No se encontró código válido dentro de comillas \"\".")
        return

    # El multiverso arranca con la Línea Temporal 0
    timelines = [Timeline()]
    current_t_index = 0

    for block_idx, code_block in enumerate(dimensions_code):
        code_block = code_block.replace(" ", "").replace("\n", "").replace("\t", "")
        if not code_block:
            continue

        ptr = 0
        while ptr < len(code_block):
            char = code_block[ptr]
            t = timelines[current_t_index]

            # === CONDICIONALES ===
            if char == ')':
                match = re.match(r'\)(-?\d+)\((\d+)', code_block[ptr:])
                if match:
                    target_value = int(match.group(1))
                    target_dim = int(match.group(2)) % 10
                    if t.current_dimension.number == target_value:
                        t.current_dim_index = target_dim
                    ptr += len(match.group(0))
                    continue
            elif char == ']':
                match = re.match(r'\](-?\d+)\[(\d+)', code_block[ptr:])
                if match:
                    target_value = int(match.group(1))
                    target_dim = int(match.group(2)) % 10
                    if t.current_dimension.number != target_value:
                        t.current_dim_index = target_dim
                    ptr += len(match.group(0))
                    continue

            # === NUEVO COMANDO CUÁNTICO: g ===
            # g: Trae/clona el valor de esta misma dimensión desde la línea de tiempo anterior (si existe)
            elif char == 'g':
                if current_t_index > 0:
                    prev_t = timelines[current_t_index - 1]
                    t.current_dimension.number = prev_t.dimensions[t.current_dim_index].number
                else:
                    print(f"[Bloque {block_idx}] Error: No hay una línea de tiempo anterior para copiar con 'g'.")

            # === COMANDOS GLOBALES Y LOCALES ===
            elif char == 'i':
                for tl in timelines:
                    tl.current_dimension.number += 1
            elif char == 'j':
                for tl in timelines:
                    tl.current_dimension.number -= 1
            elif char == 'u':
                t.current_dimension.number += 1
            elif char == 'd':
                t.current_dimension.number -= 1
            
            # === VIAJE TEMPORAL Y ESPACIAL ===
            elif char == 'a':
                timelines.append(Timeline())
            elif char == 'b':
                current_t_index = (current_t_index + 1) % len(timelines)
            elif char == 'c':
                if len(timelines) > 1:
                    old_index = current_t_index
                    current_t_index = (current_t_index + 1) % len(timelines)
                    timelines.pop(old_index)
                    if current_t_index >= len(timelines):
                        current_t_index = 0
                else:
                    print(f"[Bloque {block_idx}] Error: No podés borrar la única línea de tiempo.")
            elif char == 'f':
                t.current_dim_index = (t.current_dim_index + 1) % 10
            elif char == 'l':
                t.current_dim_index = (t.current_dim_index - 1) % 10

            ptr += 1

        current_timeline = timelines[current_t_index]
        curr_d = current_timeline.current_dimension
        log_msg = f"[Acción {block_idx}] Dimensión {current_timeline.current_dim_index} -> Valor: {curr_d.number}"
        curr_d.console.append(log_msg)

    # OUTPUT FINAL EN PANTALLA
    print("\n" + "="*50)
    print("      OUTPUT DE LAS CONSOLAS MULTIDIMENSIONALES")
    print("="*50)
    
    any_output = False
    for t_idx, t in enumerate(timelines):
        has_activity = any(len(d.console) > 0 for d in t.dimensions)
        if has_activity:
            any_output = True
            print(f"\n🌍 LÍNEA TEMPORAL {t_idx}")
            print("-" * 40)
            for d_idx, d in enumerate(t.dimensions):
                if d.console:
                    print(f"  🔹 Dimensión {d_idx}:")
                    for line in d.console:
                        print(f"    {line}")
                    barra = "⭐" * max(0, d.number) if d.number > 0 else f"({d.number})"
                    print(f"    [VALOR FINAL]: {d.number} {barra}\n")
                    
    if not any_output:
        print("\nNinguna dimensión registró cambios.")
    print("="*50)

def open_editor_and_run(filename="code.10d"):
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('"aab"\n# Tu código va acá')
    
    print(f"[Sistema] Abriendo '{filename}' para programar...")
    time.sleep(0.5)

    try:
        if sys.platform == "win32":
            subprocess.run(["notepad.exe", filename], check=True)
        elif sys.platform == "darwin":
            subprocess.run(["open", "-a", "TextEdit", filename], check=True)
        else:
            try:
                subprocess.run(["nano", filename], check=True)
            except FileNotFoundError:
                subprocess.run(["xdg-open", filename], check=True)
    except Exception as e:
        print(f"Error al abrir el editor: {e}")
        return

    print("[Sistema] Calculando dimensiones alternativas...\n")
    with open(filename, 'r', encoding='utf-8') as f:
        run_10d_program(f.read())

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        try:
            with open(sys.argv, 'r', encoding='utf-8') as f:
                run_10d_program(f.read())
        except FileNotFoundError:
            print(f"Error: El archivo '{sys.argv}' no existe.")
    else:
        open_editor_and_run()
