import random
import matplotlib.pyplot as plt

class MemoryManager:
    def __init__(self, total_memory, page_size=None):
        self.total_memory = total_memory
        self.page_size = page_size
        self.memory = [None] * total_memory  # None represents free space

    def allocate_program(self, program_id, size):
        if self.page_size:
            return self._allocate_paging(program_id, size)
        else:
            return self._allocate_compaction(program_id, size)

    def deallocate_program(self, program_id):
        for i in range(self.total_memory):
            if self.memory[i] == program_id:
                self.memory[i] = None

    def _allocate_paging(self, program_id, size):
        num_pages = (size + self.page_size - 1) // self.page_size
        allocated = 0

        for i in range(0, self.total_memory, self.page_size):
            if allocated >= num_pages:
                break
            if all(self.memory[j] is None for j in range(i, min(i + self.page_size, self.total_memory))):
                for j in range(i, min(i + self.page_size, self.total_memory)):
                    if allocated < num_pages:
                        self.memory[j] = program_id
                        allocated += 1

        if allocated < num_pages:
            print(f"Not enough memory for program {program_id}")
            return False
        return True

    def _allocate_compaction(self, program_id, size):
        free_space = self.memory.count(None)
        if free_space < size:
            print(f"Not enough memory for program {program_id}")
            return False

        free_index = 0
        for i in range(self.total_memory):
            if self.memory[i] is None:
                free_index = i
                break

        for i in range(size):
            self.memory[free_index + i] = program_id

        return True

    def compact_memory(self):
        compacted = [block for block in self.memory if block is not None]
        self.memory = compacted + [None] * (self.total_memory - len(compacted))

    def display_memory(self):
        plt.bar(range(self.total_memory), [1 if x is not None else 0 for x in self.memory])
        plt.title('Memory Layout')
        plt.xlabel('Memory Blocks')
        plt.ylabel('Usage (1=Used, 0=Free)')
        plt.show()


# Ejemplo de uso
total_memory = 100
page_size = 10

# Instanciamos el gestor de memoria
manager = MemoryManager(total_memory, page_size=page_size)

# Elegimos paginación
print("Usando Paginación")
manager.allocate_program("A", 15)  # Alocar programa A con 15 unidades de memoria
manager.allocate_program("B", 35)  # Alocar programa B con 35 unidades de memoria
manager.display_memory()

# Deasignamos un programa y mostramos la memoria
manager.deallocate_program("A")
manager.display_memory()

# Elegimos compactación
print("Usando Compactación")
manager = MemoryManager(total_memory)  # Sin paginación, solo compactación
manager.allocate_program("C", 20)
manager.allocate_program("D", 30)
manager.display_memory()

# Compactamos y mostramos la memoria
manager.compact_memory()
manager.display_memory()
