import random


# Definir el estado inicial para los postes
def initial_state(num_discs):
    A = list(range(num_discs, 0, -1))
    B = []
    C = []
    return A, B, C


# Función heurística que calcula cuántos discos están en el poste "C" en el orden correcto
def heuristic(state):
    _, _, C = state
    count = 0
    for i in range(1, len(C) + 1):
        if C[-i] == i:
            count += 1
        else:
            break
    return count


# Genera un estado aleatorio para reiniciar el proceso de Hill Climbing
def random_state(num_discs):
    A, B, C = [], [], []
    for disc in range(num_discs, 0, -1):
        peg = random.choice([A, B, C])
        peg.append(disc)
    return A, B, C


# Genera vecinos del estado actual al mover un disco entre los postes
def get_neighbors(state):
    A, B, C = state
    neighbors = []

    # Lista de movimientos posibles entre postes con sus nombres
    possible_moves = [(A, B, "A", "B"), (A, C, "A", "C"),
                      (B, A, "B", "A"), (B, C, "B", "C"),
                      (C, A, "C", "A"), (C, B, "C", "B")]

    # Genera los estados vecinos aplicando cada movimiento posible
    for source, target, source_name, target_name in possible_moves:
        if source and (not target or source[-1] < target[-1]):  # Regla de discos
            # Copiar el estado actual
            new_A, new_B, new_C = A[:], B[:], C[:]
            new_state = (new_A, new_B, new_C)

            # Ejecutar el movimiento en la copia
            disk = source.pop()
            target.append(disk)
            neighbors.append((new_A[:], new_B[:], new_C[:], disk, source_name, target_name))

            # Revertir el movimiento en el estado original
            target.pop()
            source.append(disk)

    return neighbors


# Implementa el algoritmo Hill Climbing con retroceso y reinicio aleatorio
def hill_climbing_hanoi(num_discs, max_backtracks=3, max_restarts=3):
    current_state = initial_state(num_discs)
    current_heuristic = heuristic(current_state)
    steps = []
    backtracks = 0  # Contador de retrocesos
    restarts = 0  # Contador de reinicios aleatorios

    while current_heuristic < num_discs:
        # Obtener todos los vecinos del estado actual
        neighbors = get_neighbors(current_state)

        # Seleccionar el mejor vecino
        best_neighbor = None
        best_neighbor_heuristic = -1

        for neighbor in neighbors:
            state_only = neighbor[:3]
            heuristic_value = heuristic(state_only)

            # Solo selecciona el vecino si mejora la heurística
            if heuristic_value > best_neighbor_heuristic:
                best_neighbor = neighbor
                best_neighbor_heuristic = heuristic_value

        # Si no encontramos un vecino que mejore, realiza retroceso o reinicio
        if best_neighbor is None or best_neighbor_heuristic <= current_heuristic:
            backtracks += 1
            print(f"Retroceso: {backtracks}")
            if backtracks > max_backtracks:
                restarts += 1
                if restarts > max_restarts:
                    print("No se puede mejorar más el estado actual. Se alcanzó el límite de reinicios.")
                    break
                print(f"Reinicio aleatorio {restarts} de {max_restarts}")
                current_state = random_state(num_discs)
                current_heuristic = heuristic(current_state)
                backtracks = 0
                steps.append(("Reinicio aleatorio", current_state))
            continue  # Realizar retroceso o reinicio

        # Imprimir el movimiento realizado
        disk, origen, destino = best_neighbor[3], best_neighbor[4], best_neighbor[5]
        print(f"Mueve el disco {disk} de {origen} a {destino}")

        # Actualizar el estado actual y la heurística
        current_state = best_neighbor[:3]
        current_heuristic = best_neighbor_heuristic
        steps.append((disk, origen, destino))
        backtracks = 0  # Reiniciar contador de retrocesos

    return steps


# Número de discos
num_discs = 4

# Ejecutar el algoritmo de Hill Climbing con retroceso y reinicio aleatorio
hill_climbing_hanoi(num_discs, max_backtracks=3, max_restarts=3)
