import requests
from config import GITHUB_TOKEN, OWNER, REPO


class GitHubClient:

    BASE_URL = "https://api.github.com"

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

    def get_workflow_runs(self):

        url = (
            f"{self.BASE_URL}/repos/"
            f"{OWNER}/{REPO}/actions/runs"
            "?per_page=100"
        )

        response = requests.get(
            url,
            headers=self.headers
        )

        response.raise_for_status()

        return response.json()


    def get_commits(self):
        pass


    def get_deployments(self):
        pass


    def get_workflow_run(self, run_id):
        pass