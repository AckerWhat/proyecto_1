import os
import hashlib
import json
from datetime import datetime
from staging import StagingArea
from commit import Commit

class Repository:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.branches = {'main': None}  # Rama principal apunta a None (primer commit)
        self.current_branch = 'main'
        self.staging_area = StagingArea()
        self.commits = {}  # Diccionario de commits (hash: commit)
        self.head = None   # Commit actual

    def add_file(self, filename):
        self.staging_area.add_file(filename)

    def commit(self, message, author_email):
        if not self.staging_area.files:
            return "No hay archivos en el área de staging para hacer commit."
            
        commit_hash = self._generate_hash(message + author_email + str(datetime.now()))
        parent_hash = self.head.hash if self.head else None
        
        new_commit = Commit(
            commit_hash,
            datetime.now(),
            author_email,
            message,
            parent_hash,
            self.staging_area.get_files(),
            self.current_branch
        )
        
        self.commits[commit_hash] = new_commit
        self.branches[self.current_branch] = commit_hash
        self.head = new_commit
        self.staging_area.clear()
        
        return f"Commit [{commit_hash[:6]}] creado en rama '{self.current_branch}'"

    def _generate_hash(self, data):
        return hashlib.sha1(data.encode()).hexdigest()

    def to_dict(self):
        return {
            'name': self.name,
            'path': self.path,
            'branches': self.branches,
            'current_branch': self.current_branch,
            'head': self.head.hash if self.head else None,
            'commits': {hash: commit.to_dict() for hash, commit in self.commits.items()}
        }

    @classmethod
    def from_dict(cls, data):
        repo = cls(data['name'], data['path'])
        repo.branches = data['branches']
        repo.current_branch = data['current_branch']
        repo.commits = {hash: Commit.from_dict(commit_data) 
                       for hash, commit_data in data['commits'].items()}
        repo.head = repo.commits.get(data['head'])
        return repo

class RepositoryManager:
    def __init__(self):
        self.repositories = []  # Lista enlazada de repositorios

    def create_repository(self, name, path):
        repo = Repository(name, path)
        self.repositories.append(repo)
        return repo

    def get_repository(self, name):
        for repo in self.repositories:
            if repo.name == name:
                return repo
        return None

    def list_repositories(self):
        return [repo.name for repo in self.repositories]

    def load_repositories(self, data):
        self.repositories = [Repository.from_dict(repo_data) for repo_data in data]

    def to_dict(self):
        return [repo.to_dict() for repo in self.repositories]