import hashlib
import os

class StagingArea:
    """Implementación del área de staging como una pila"""
    def __init__(self):
        self.files = []  # Pila de archivos preparados para commit

    def add_file(self, filename, status='A'):
        """Añade un archivo al área de staging"""
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Archivo '{filename}' no encontrado")
            
        with open(filename, 'rb') as f:
            content = f.read()
            checksum = hashlib.sha1(content).hexdigest()
            
        file_info = {
            'filename': filename,
            'status': status,
            'checksum': checksum,
            'metadata': {
                'size': os.path.getsize(filename),
                'last_modified': os.path.getmtime(filename)
            }
        }
        
        self.files.append(file_info)
        return f"Archivo '{filename}' añadido al área de staging"

    def remove_file(self, filename):
        """Elimina un archivo del área de staging"""
        for i, file_info in enumerate(self.files):
            if file_info['filename'] == filename:
                self.files.pop(i)
                return f"Archivo '{filename}' removido del área de staging"
        return f"Archivo '{filename}' no encontrado en staging"

    def get_files(self):
        """Obtiene todos los archivos en staging"""
        return [file['filename'] for file in self.files]

    def clear(self):
        """Limpia el área de staging"""
        self.files = []

    def status(self):
        """Muestra el estado del área de staging"""
        if not self.files:
            return "No hay archivos en el área de staging"
            
        status_msg = "Archivos en el área de staging:\n"
        for file in self.files:
            status_msg += f"{file['status']}: {file['filename']}\n"
        return status_msg