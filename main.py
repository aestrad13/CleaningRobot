import threading
import random
import time

class Habitacion:
    def __init__(self, M, N, dirty_percentage):
        self.M = M
        self.N = N
        self.grid = [[random.random() < dirty_percentage for _ in range(N)] for _ in range(M)]
        self.lock = threading.Lock()

    def esta_sucia(self, x, y):
        return self.grid[x][y]

    def limpiar(self, x, y, agent_id):
        with self.lock:
            if self.grid[x][y]:
                self.grid[x][y] = False
                print(f"Agente {agent_id} limpió la celda ({x+1},{y+1})")  # Imprime la acción de limpieza
                return True
        return False

    def porcentaje_limpio(self):
        with self.lock:
            clean_cells = sum(row.count(False) for row in self.grid)
            total_cells = self.M * self.N
            return (clean_cells / total_cells) * 100

class Agente(threading.Thread):
    def __init__(self, agent_id, habitacion, max_moves):
        threading.Thread.__init__(self)
        self.agent_id = agent_id
        self.habitacion = habitacion
        self.pos_x, self.pos_y = 1, 1
        self.moves = 0
        self.max_moves = max_moves
        self.active = True

    def run(self):
        while self.active and self.moves < self.max_moves:
            if self.habitacion.esta_sucia(self.pos_x, self.pos_y):
                self.habitacion.limpiar(self.pos_x, self.pos_y, self.agent_id)
            else:
                self.moverse()
            self.moves += 1
            time.sleep(0.01)

    def moverse(self):
        dx, dy = random.choice([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])
        new_x, new_y = self.pos_x + dx, self.pos_y + dy
        if 0 <= new_x < self.habitacion.M and 0 <= new_y < self.habitacion.N:
            self.pos_x, self.pos_y = new_x, new_y

def simulacion(M, N, num_agentes, dirty_percentage, tiempo_maximo):
    habitacion = Habitacion(M, N, dirty_percentage)
    agentes = [Agente(i + 1, habitacion, tiempo_maximo * 100) for i in range(num_agentes)]

    start_time = time.time()
    for agente in agentes:
        agente.start()

    while time.time() - start_time < tiempo_maximo:
        if habitacion.porcentaje_limpio() == 100:
            break
        time.sleep(0.1)

    for agente in agentes:
        agente.active = False
    for agente in agentes:
        agente.join()

    tiempo_transcurrido = time.time() - start_time
    porcentaje_limpio = habitacion.porcentaje_limpio()
    movimientos_totales = sum(agente.moves for agente in agentes)

    print(f"Tiempo necesario hasta que todas las celdas estén limpias: {tiempo_transcurrido:.2f} segundos")
    print(f"Porcentaje de celdas limpias después de la simulación: {porcentaje_limpio:.2f}%")
    print(f"Número total de movimientos realizados: {movimientos_totales}")

# Parámetros de la simulación
M = 10  # Filas
N = 10  # Columnas
num_agentes = 3
dirty_percentage = 0.3
tiempo_maximo = 10  # segundos

simulacion(M, N, num_agentes, dirty_percentage, tiempo_maximo)

