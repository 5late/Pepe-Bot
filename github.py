from git import Repo
from datetime import datetime

PATH_OF_GIT_REPO = r"/home/blackbox2/Desktop/PepeBot"
# COMMIT_MESSAGE = str('Auto push from python script.')


def git_push():
    now = datetime.now()
    formatted = now.strftime("%a, %B %d, %Y| %H:%M")

    repo = Repo(PATH_OF_GIT_REPO)
    repo.git.add("test.txt")
    repo.index.commit("This commit was automatically called at: " + formatted)
    origin = repo.remote(name="origin")
    origin.fetch()
    origin.push()


git_push()
