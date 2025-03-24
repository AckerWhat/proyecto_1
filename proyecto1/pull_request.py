from datetime import datetime
import json

class PullRequest:
    def __init__(self, pr_id, title, description, author, source_branch, target_branch):
        self.id = pr_id
        self.title = title
        self.description = description
        self.author = author
        self.source_branch = source_branch
        self.target_branch = target_branch
        self.created_at = datetime.now()
        self.status = "open"  # open, in_review, approved, rejected, merged
        self.reviewers = []
        self.comments = []
        self.commits = []
        self.merged_at = None
        self.tags = []

    def add_reviewer(self, reviewer):
        self.reviewers.append(reviewer)

    def add_comment(self, comment):
        self.comments.append(comment)

    def approve(self):
        self.status = "approved"

    def reject(self):
        self.status = "rejected"

    def merge(self):
        self.status = "merged"
        self.merged_at = datetime.now()

    def add_tag(self, tag):
        self.tags.append(tag)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'author': self.author,
            'source_branch': self.source_branch,
            'target_branch': self.target_branch,
            'created_at': self.created_at.isoformat(),
            'status': self.status,
            'reviewers': self.reviewers,
            'comments': self.comments,
            'commits': self.commits,
            'merged_at': self.merged_at.isoformat() if self.merged_at else None,
            'tags': self.tags
        }

    @classmethod
    def from_dict(cls, data):
        pr = cls(
            data['id'],
            data['title'],
            data['description'],
            data['author'],
            data['source_branch'],
            data['target_branch']
        )
        pr.created_at = datetime.fromisoformat(data['created_at'])
        pr.status = data['status']
        pr.reviewers = data['reviewers']
        pr.comments = data['comments']
        pr.commits = data['commits']
        pr.merged_at = datetime.fromisoformat(data['merged_at']) if data['merged_at'] else None
        pr.tags = data['tags']
        return pr

class PullRequestQueue:
    """Implementación de cola para manejar pull requests"""
    def __init__(self):
        self.queue = []
        self.next_id = 1

    def create_pr(self, title, description, author, source_branch, target_branch):
        pr = PullRequest(
            f"PR-{self.next_id}",
            title,
            description,
            author,
            source_branch,
            target_branch
        )
        self.next_id += 1
        self.queue.append(pr)
        return pr

    def get_next_pr(self):
        if not self.queue:
            return None
        return self.queue[0]

    def process_next_pr(self):
        if not self.queue:
            return None
        return self.queue.pop(0)

    def get_pr_by_id(self, pr_id):
        for pr in self.queue:
            if pr.id == pr_id:
                return pr
        return None

    def list_prs(self, status=None):
        if status:
            return [pr for pr in self.queue if pr.status == status]
        return self.queue.copy()

    def clear_queue(self):
        self.queue = []

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump([pr.to_dict() for pr in self.queue], f)

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.queue = [PullRequest.from_dict(pr_data) for pr_data in data]
                if self.queue:
                    last_id = int(self.queue[-1].id.split('-')[1])
                    self.next_id = last_id + 1
        except FileNotFoundError:
            pass