from abc import ABC, abstractmethod

class Command(ABC):
    def __init__(self, simulator):
        self.simulator = simulator
        self.enabled = True

    @abstractmethod
    def execute(self, *args):
        pass

class GitInitCommand(Command):
    def execute(self, *args):
        if not args:
            return "Uso: git init <nombre_repositorio>"
            
        repo_name = args[0]
        if self.simulator.repo_manager.get_repository(repo_name):
            return f"El repositorio '{repo_name}' ya existe."
            
        repo = self.simulator.repo_manager.create_repository(repo_name, f"./{repo_name}")
        self.simulator.current_repo = repo
        return f"Repositorio vacío '{repo_name}' inicializado."

class GitStatusCommand(Command):
    def execute(self, *args):
        if not self.simulator.current_repo:
            return "No hay repositorio seleccionado. Use 'git init' o seleccione un repositorio."
            
        status = f"En la rama {self.simulator.current_repo.current_branch}\n"
        
        if self.simulator.current_repo.staging_area.files:
            status += "\nArchivos en staging:\n"
            for file in self.simulator.current_repo.staging_area.files:
                status += f"  {file['status']}: {file['filename']}\n"
        else:
            status += "\nNo hay archivos en staging\n"
            
        return status

class GitLogCommand(Command):
    def execute(self, *args):
        if not self.simulator.current_repo:
            return "No hay repositorio seleccionado."
            
        if not self.simulator.current_repo.commits:
            return "No hay commits aún en este repositorio."
            
        log = f"Historial de commits (rama {self.simulator.current_repo.current_branch}):\n"
        current = self.simulator.current_repo.head
        
        while current:
            log += f"\n{current}"
            current = self.simulator.current_repo.commits.get(current.parent_hash) if current.parent_hash else None
            
        return log

