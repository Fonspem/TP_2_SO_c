
from enum import Enum


class State(Enum):
    NUEVO = 1  # se a creado el proceso
    LISTO = 2  # listo para ejecutarse
    EJECUTANDO = 3  # el manager de prosesos tiene control
    BLOQUEADO = 4  # proceso esperando
    TERMINADO = 5  # proceso termino


class Process:
    def __init__(
        self, id: int, size_memory: int, execution_time: float, priority: int = 1
    ) -> None:
        self._id: int = id
        self._size_memory: int = size_memory
        self._execution_time: float = execution_time
        self._priority: int = priority
        self._state: State = State.NUEVO

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        if value < 0:
            raise ValueError("El ID del proceso no puede ser negativo.")
        self._id = value

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


import sys
import random
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
    QLabel,
)
from PyQt5.QtCore import QTimer

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
import time  # Para simular una tarea de larga duración


class ProcessWorkerThread(QThread):
    finished = pyqtSignal(Process)  # Señal para emitir cuando un proceso ha terminado
    process_updated = pyqtSignal(
        Process
    )  # Señal para actualizar el proceso en ejecución

    def __init__(self, process_manager, parent=None):
        super().__init__(parent)
        self.process_manager = process_manager

    def run(self):
        self.process_updated.emit(self.process_manager.ready_queue[0])
        if self.process_manager.ready_queue:
            process = self.process_manager.run_processes()
            if process:
                self.process_updated.emit(process)  # Actualiza el proceso en ejecución
                self.finished.emit(process)
            time.sleep(0.01)  # Ajusta este tiempo según sea necesario


class ProcessSimulatorGUI(QMainWindow):
    def __init__(self, process_manager):
        super().__init__()
        self.process_manager = process_manager
        self.finished_processes = []
        self.current_thread = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Simulador de Procesos")

        # Layout principal
        main_layout = QVBoxLayout()

        # Sección de tablas
        tables_layout = QHBoxLayout()

        # Ready Queue Section
        ready_queue_layout = QVBoxLayout()
        ready_label = QLabel("Ready Queue")
        self.ready_table = QTableWidget(0, 5)
        self.ready_table.setHorizontalHeaderLabels(
            ["ID", "Memoria", "Tiempo", "Prioridad", "Estado"]
        )
        ready_queue_layout.addWidget(ready_label)
        ready_queue_layout.addWidget(self.ready_table)

        # Waiting Queue Section
        waiting_queue_layout = QVBoxLayout()
        waiting_label = QLabel("Waiting Queue")
        self.waiting_table = QTableWidget(0, 5)
        self.waiting_table.setHorizontalHeaderLabels(
            ["ID", "Memoria", "Tiempo", "Prioridad", "Estado"]
        )
        waiting_queue_layout.addWidget(waiting_label)
        waiting_queue_layout.addWidget(self.waiting_table)

        # Añadir las dos secciones a la interfaz
        tables_layout.addLayout(ready_queue_layout)
        tables_layout.addLayout(waiting_queue_layout)
        main_layout.addLayout(tables_layout)

        # Sección del proceso en ejecución
        self.current_memory_label = QLabel(
            f"Memoria actual: {self.process_manager.available_memory}"
        )
        self.current_process_label = QLabel("Proceso en ejecución: Ninguno")
        self.algorithm_label = QLabel(
            f"Algoritmo usado: {self.process_manager.algorithm.name}"
        )

        main_layout.addWidget(self.current_memory_label)
        main_layout.addWidget(self.current_process_label)
        main_layout.addWidget(self.algorithm_label)

        # Tabla de Procesos Terminados
        finished_label = QLabel("Procesos Terminados")
        self.finished_table = QTableWidget(0, 4)
        self.finished_table.setHorizontalHeaderLabels(
            ["ID", "Memoria", "Prioridad", "Estado"]
        )
        main_layout.addWidget(finished_label)
        main_layout.addWidget(self.finished_table)

        # Botón para agregar procesos
        self.add_process_button = QPushButton("Agregar Proceso")
        self.add_process_button.clicked.connect(self.add_process)
        main_layout.addWidget(self.add_process_button)

        # Configuración de la ventana principal
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Temporizador para actualizar la interfaz
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_interface)
        self.timer.start(100)  # Actualizar cada 100 ms

    def add_process(self):
        # Genera valores aleatorios para el proceso

        id = (
            len(self.process_manager.ready_queue)
            + len(self.process_manager.waiting_queue)
            + len(self.finished_processes)
        )
        size_memory = random.randint(
            50, 200
        )  # Cambia los límites aquí según lo necesites
        execution_time = random.randint(1, 5)
        priority = random.randint(-10, 10)

        # Crea el nuevo proceso y lo agrega al ProcessManager
        new_process = Process(id, size_memory, execution_time, priority)
        self.process_manager.add_process(new_process)

        self.update_interface()

    def start_process_thread(self):
        # Verifica si hay procesos en la ready_queue y si no hay un hilo en ejecución
        if (self.process_manager.ready_queue) and (
            self.current_thread is None or not self.current_thread.isRunning()
        ):
            self.current_thread = ProcessWorkerThread(self.process_manager)
            self.current_thread.process_updated.connect(
                self.update_current_process_from_thread
            )
            self.current_thread.finished.connect(self.add_to_finished_processes)
            self.current_thread.process_updated.connect(
                self.update_current_process_from_thread
            )
            self.current_thread.start()

    def update_interface(self):
        # Actualiza las tablas con los procesos actuales
        self.start_process_thread()
        self.update_table(self.ready_table, self.process_manager.ready_queue)
        self.update_table(self.waiting_table, self.process_manager.waiting_queue)
        self.update_current_memory()
        self.update_finished_table()

    def update_table(self, table, queue):
        table.setRowCount(len(queue))
        for row, process in enumerate(queue):
            table.setItem(row, 0, QTableWidgetItem(str(process.id)))
            table.setItem(row, 1, QTableWidgetItem(str(process.size_memory)))
            table.setItem(row, 2, QTableWidgetItem(str(process.execution_time)))
            table.setItem(row, 3, QTableWidgetItem(str(process.priority)))
            table.setItem(row, 4, QTableWidgetItem(str(process.state)))

    def update_current_memory(self):
        current_memory = self.process_manager.available_memory
        self.current_memory_label.setText(f"Memoria actual: {current_memory}")

    def update_current_process(self):
        if self.process_manager.ready_queue:
            current_process = self.process_manager.ready_queue[0]
            self.current_process_label.setText(
                f"Proceso en ejecución: ID:{current_process.id}, Tamaño:{current_process.size_memory} B, Tiempo:{current_process.execution_time}, Prioridad:{current_process.priority}"
            )
        else:
            self.current_process_label.setText("Proceso en ejecución: Ninguno")

    @pyqtSlot(Process)
    def update_current_process_from_thread(self, process):
        self.current_process_label.setText(
            f"Proceso en ejecución: ID:{process.id}, Tamaño:{process.size_memory} B, Tiempo:{process.execution_time}, Prioridad:{process.priority}"
        )
        self.update_interface()

    def update_finished_table(self):
        # Actualiza la tabla de procesos terminados
        self.finished_table.setRowCount(len(self.finished_processes))
        for row, process in enumerate(self.finished_processes):
            self.finished_table.setItem(row, 0, QTableWidgetItem(str(process.id)))
            self.finished_table.setItem(
                row, 1, QTableWidgetItem(str(process.size_memory))
            )
            self.finished_table.setItem(row, 2, QTableWidgetItem(str(process.priority)))
            self.finished_table.setItem(row, 3, QTableWidgetItem(str(process.state)))

    def add_to_finished_processes(self, process):
        self.finished_processes.append(process)
        self.update_finished_table()


MEMORIA = 1000
ALGORITMO = Algorithm.SJF


if __name__ == "__main__":
    app = QApplication(sys.argv)

    manager = ProcessManager(MEMORIA, ALGORITMO)

    gui = ProcessSimulatorGUI(manager)
    gui.show()

    sys.exit(app.exec_())
