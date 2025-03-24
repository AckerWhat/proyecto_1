from datetime import datetime

class Commit:
    def __init__(self, commit_hash, date, author_email, message, parent_hash, files, branch):
        self.hash = commit_hash
        self.date = date
        self.author_email = author_email
        self.message = message
        self.parent_hash = parent_hash
        self.files = files  # Lista de archivos modificados
        self.branch = branch

    def __str__(self):
        return (f"Commit: {self.hash[:6]}\n"
                f"Author: {self.author_email}\n"
                f"Date:   {self.date}\n"
                f"Branch: {self.branch}\n"
                f"\n    {self.message}\n")

    def to_dict(self):
        return {
            'hash': self.hash,
            'date': self.date.isoformat(),
            'author_email': self.author_email,
            'message': self.message,
            'parent_hash': self.parent_hash,
            'files': self.files,
            'branch': self.branch
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['hash'],
            datetime.fromisoformat(data['date']),
            data['author_email'],
            data['message'],
            data['parent_hash'],
            data['files'],
            data['branch']
        )

class CommitHistory:
    """Lista enlazada de commits"""
    def __init__(self):
        self.head = None  # Commit más reciente

    def add_commit(self, commit):
        commit.parent_hash = self.head.hash if self.head else None
        self.head = commit

    def get_history(self, max_commits=10):
        history = []
        current = self.head
        count = 0
        
        while current and count < max_commits:
            history.append(current)
            current = self.commits.get(current.parent_hash) if current.parent_hash else None
            count += 1
            
        return history