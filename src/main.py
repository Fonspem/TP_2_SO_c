import time
from enum import Enum


class Memoria:
    def __init__(self, size: int):
        self._size: int = size
        self.memoria = ['-' for _ in range(size)]

    def add_to_memory(self, size_in_memory: int, indice_memoria: int) -> None:
        if size_in_memory > self._size:
            raise ValueError("Tamaño superior al esperado")
        if indice_memoria > self._size:
            raise ValueError("indice fuera de limites")




class State(Enum):
    NUEVO = 1  # se a creado el proceso
    LISTO = 2  # listo para ejecutarse
    EJECUTANDO = 3  # el manager de prosesos tiene control
    BLOQUEADO = 4  # proceso esperando
    TERMINADO = 5  # proceso terminó y listo para quitar de memoria


class Process:
    ids: list[int] = list

    def __init__(self, size_in_memory: int, execution_time: float, priority: int = 1) -> None:
        self._id: int = -1
        self.__set_id__()
        self._size_memory: int = size_in_memory
        self.size_memory = size_in_memory
        self._execution_time: float
        self.execution_time = execution_time
        self._priority: int
        self.priority = priority
        self._state: State
        self.state = State.NUEVO

    @property
    def id(self) -> int:
        return self._id

    def __set_id__(self) -> None:
        if len(Process.ids) > 0:
            self._id = max(Process.ids) + 1
        else:
            self._id = 0

    @property
    def size_memory(self) -> int:
        return self._size_memory

    @size_memory.setter
    def size_memory(self, value: int) -> None:
        if value < 0:
            raise ValueError("El espacio en memoria no puede ser negativo.")
        self._size_memory = value

    @property
    def execution_time(self) -> float:
        return self._execution_time

    @execution_time.setter
    def execution_time(self, value: float) -> None:
        if value < 0:
            raise ValueError("El tiempo de ejecución debe ser 0 o mayor.")
        self._execution_time = value

    @property
    def priority(self) -> int:
        return self._priority

    @priority.setter
    def priority(self, value: int) -> None:
        self._priority = value

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, value: State) -> None:
        if not isinstance(value, State):
            raise ValueError("El estado no es válido.")
        self._state = value


from collections import deque


class Algorithm(Enum):
    FIFO = 1  # Los procesos se ejecutan en el orden en que llegan.
    SJF = 2  # (Shortest Job First) - El proceso con el menor tiempo de ejecución se ejecuta primero.
    ROUND_ROBIN = 3  # Cada proceso recibe un tiempo fijo (time_quantum) para ejecutar, después de lo cual se pasa al siguiente proceso en la cola.
    PRIORITY = 4  # Los procesos se ejecutan según su prioridad, siendo el proceso con la mayor prioridad el primero en ejecutarse.


class ProcessManager:
    def __init__(self, memory_size: int, algorithm: Algorithm) -> None:
        self.memory_limit: int = memory_size
        self._available_memory: int = memory_size
        self.ready_queue: deque[Process] = deque()
        self.waiting_queue: deque[Process] = deque()
        self.algorithm: Algorithm = algorithm

    @property
    def available_memory(self) -> int:
        aux = self.memory_limit
        for x in self.ready_queue:
            aux -= x.size_memory
        self._available_memory = aux
        return self._available_memory

    def add_process(self, process: Process) -> None:
        process.state = State.LISTO
        if process.size_memory <= self.available_memory:
            self.ready_queue.append(process)
            print(f"Proceso {process.id} agregado a la cola de listos.")
        else:
            self.waiting_queue.append(process)
            print(
                f"Proceso {process.id} agregado a la cola de espera por falta de memoria."
            )
        self.order_queue()

    def order_queue(self) -> None:

        match self.algorithm:
            case Algorithm.SJF:
                for x in self.ready_queue:
                    self.waiting_queue.append(x)
                self.waiting_queue = deque(
                    sorted(self.waiting_queue, key=lambda p: p.execution_time)
                )
                self.ready_queue.clear()
            case Algorithm.PRIORITY:
                for x in self.ready_queue:
                    self.waiting_queue.append(x)
                self.waiting_queue = deque(
                    sorted(self.waiting_queue, key=lambda p: p.priority)
                )
                self.ready_queue.clear()
            case _:
                pass
        self.move_queue()

    def move_queue(self) -> None:
        while (
                len(self.waiting_queue) > 0
                and self.waiting_queue[0].size_memory <= self.available_memory
        ):
            self.ready_queue.append(self.waiting_queue.popleft())

    def finish_process(self, process: Process) -> Process:
        # retorna el proceso terminado, es para que poder visualizar mejor en la IG
        self.ready_queue.remove(process)
        process.state = State.TERMINADO
        print(f"Proceso {process.id} terminado")
        self.move_queue()
        return process

    def run_processes(self) -> Process | None:
        match self.algorithm:
            case Algorithm.FIFO:
                return self._run_fifo()
            case Algorithm.SJF:
                return self._run_fifo()
            case Algorithm.ROUND_ROBIN:
                return self._run_round_robin()
            case Algorithm.PRIORITY:
                return self._run_fifo()

    def _run_fifo(self) -> Process | None:
        if self.ready_queue:
            current_process = self.ready_queue.popleft()
            current_process.state = State.EJECUTANDO
            self.ready_queue.appendleft(current_process)
            print(f"Proceso {current_process.id} está ejecutándose.")
            time.sleep(current_process.execution_time)
            return self.finish_process(current_process)

    def _run_round_robin(self) -> Process | None:
        time_quantum: float = 3.0  # 3 segundos
        if self.ready_queue:
            current_process: Process = self.ready_queue.popleft()
            current_process.state = State.EJECUTANDO
            self.ready_queue.appendleft(current_process)

            print(f"Proceso {current_process.id} está ejecutándose.")

            execution_time = min(time_quantum, current_process.execution_time)
            time.sleep(execution_time)
            current_process.execution_time -= execution_time

            if current_process.execution_time > 0:
                current_process.state = State.LISTO
                self.ready_queue.remove(current_process)
                self.add_process(current_process)
                print(f"Proceso {current_process.id} retornado a la cola de listos.")
            else:
                return self.finish_process(current_process)


if __name__ == "__main__":
    pass
