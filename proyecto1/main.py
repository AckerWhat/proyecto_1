import json
import os
from datetime import datetime
from repository import Repository, RepositoryManager
from commands import Command, GitInitCommand, GitStatusCommand, GitLogCommand

import os
import sys
import json
from pathlib import Path

class GitSimulator:
    def __init__(self):
        # Obtener el directorio base donde se encuentra el script
        self.base_dir = Path(__file__).parent.resolve()
        self.repo_manager = RepositoryManager()
        self.current_repo = None
        self.commands = self._initialize_commands()
        self._load_data()

    def _get_config_path(self):
        """Devuelve la ruta completa al archivo de configuración"""
        return self.base_dir / 'config.json'

    def _get_data_dir(self):
        """Devuelve la ruta completa al directorio de datos"""
        return self.base_dir / 'data'

    def _initialize_commands(self):
        # Configuración por defecto
        default_config = {
            "commands": {
                "init": True,
                "add": True,
                "commit": True,
                "status": True,
                "log": True,
                "branch": True,
                "checkout": True,
                "merge": True,
                "pr": True
            }
        }
        
        config_path = self._get_config_path()
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            # Si no existe el archivo, crear uno con configuración por defecto
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=4)
            config = default_config
        except json.JSONDecodeError:
            print(f"Error: El archivo de configuración {config_path} está corrupto.")
            config = default_config
        
        commands = {
            'init': GitInitCommand(self),
            'status': GitStatusCommand(self),
            'log': GitLogCommand(self),
            # Agregar más comandos aquí...
        }
        
        # Habilitar/deshabilitar comandos según configuración
        for cmd_name, enabled in config['commands'].items():
            if cmd_name in commands:
                commands[cmd_name].enabled = enabled
                
        return commands

    def _load_data(self):
        data_dir = self._get_data_dir()
        repos_path = data_dir / 'repos.json'
        
        if repos_path.exists():
            try:
                with open(repos_path, 'r') as f:
                    data = json.load(f)
                    self.repo_manager.load_repositories(data)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error cargando datos: {str(e)}")

    def save_data(self):
        data_dir = self._get_data_dir()
        data_dir.mkdir(exist_ok=True)  # Crear directorio si no existe
        
        repos_path = data_dir / 'repos.json'
        try:
            with open(repos_path, 'w') as f:
                json.dump(self.repo_manager.to_dict(), f)
        except IOError as e:
            print(f"Error guardando datos: {str(e)}")

    def execute_command(self, command_name, *args):
        if command_name in self.commands and self.commands[command_name].enabled:
            return self.commands[command_name].execute(*args)
        else:
            return f"Comando '{command_name}' no disponible."

    def run(self):
        print("Bienvenido al Simulador de Git")
        while True:
            try:
                user_input = input("git> ").strip()
                if not user_input:
                    continue
                    
                parts = user_input.split()
                command = parts[0]
                args = parts[1:] if len(parts) > 1 else []
                
                if command == 'exit':
                    self.save_data()
                    break
                    
                result = self.execute_command(command, *args)
                print(result)
                
            except Exception as e:
                print(f"Error: {str(e)}")

if __name__ == "__main__":
    simulator = GitSimulator()
    simulator.run()