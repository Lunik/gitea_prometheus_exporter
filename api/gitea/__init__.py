import time
from prometheus_client import Gauge

from api.gitea.gitea import *


MODULE_NAME = "gitea"

GAUGES = {
  "user": Gauge("{}_extra_user".format(MODULE_NAME), "Gitea user", ['username', 'full_name']),
  "org": Gauge("{}_extra_org".format(MODULE_NAME), "Gitea org", ['username', 'full_name', 'visibility']),
  "repo": Gauge("{}_extra_repo".format(MODULE_NAME), "Gitea repo", ['name', 'owner']),
  "repo_size": Gauge("{}_extra_repo_size".format(MODULE_NAME), "Gitea repo size", ['name', 'owner', 'unit']),
  "repo_empty": Gauge("{}_extra_repo_empty".format(MODULE_NAME), "Gitea repo empty", ['name', 'owner']),
  "repo_archived": Gauge("{}_extra_repo_archived".format(MODULE_NAME), "Gitea repo archived", ['name', 'owner']),
  "repo_stars": Gauge("{}_extra_repo_stars".format(MODULE_NAME), "Gitea repo stars", ['name', 'owner']),
  "repo_commits": Gauge("{}_extra_repo_commits".format(MODULE_NAME), "Gitea repo commits", ['name', 'owner']),
  "repo_branches": Gauge("{}_extra_repo_branches".format(MODULE_NAME), "Gitea repo branches", ['name', 'owner']),
  "repo_forks": Gauge("{}_extra_repo_forks".format(MODULE_NAME), "Gitea repo forks", ['name', 'owner']),
  "repo_issues": Gauge("{}_extra_repo_issues".format(MODULE_NAME), "Gitea repo issues", ['name', 'owner']),
  "repo_pull_requests": Gauge("{}_extra_repo_pull_requests".format(MODULE_NAME), "Gitea repo pull_requests", ['name', 'owner'])
}

def module(app):
  try:
    interval = int(app.config['MODULE_CONFIG']['interval'])
  except:
    interval = 60

  while True:
    try:
      gitea_metrics = gitea_export(app)

      GAUGES['user']._metrics.clear()
      for user in gitea_metrics['users']:
        GAUGES['user'].labels(username=user.username, full_name=user.full_name).set(1)

      GAUGES['org']._metrics.clear()
      for org in gitea_metrics['orgs']:
        GAUGES['org'].labels(username=org.username, full_name=org.full_name, visibility=org.visibility).set(1)

      GAUGES['repo']._metrics.clear()
      GAUGES['repo_size']._metrics.clear()
      GAUGES['repo_empty']._metrics.clear()
      GAUGES['repo_archived']._metrics.clear()
      GAUGES['repo_stars']._metrics.clear()
      GAUGES['repo_commits']._metrics.clear()
      GAUGES['repo_branches']._metrics.clear()
      GAUGES['repo_forks']._metrics.clear()
      GAUGES['repo_issues']._metrics.clear()

      for repo in gitea_metrics['repos']:
        GAUGES['repo'].labels(name=repo.name, owner=repo.owner.username).set(1)
        GAUGES['repo_size'].labels(name=repo.name, owner=repo.owner.username, unit="bytes").set(repo.size)

        if repo.empty:
          GAUGES['repo_empty'].labels(name=repo.name, owner=repo.owner.username).set(1)

        if repo.archived:
          GAUGES['repo_archived'].labels(name=repo.name, owner=repo.owner.username).set(1)

        if repo.stars_count > 0:
          GAUGES['repo_stars'].labels(name=repo.name, owner=repo.owner.username).set(repo.stars_count)

        if repo.commits_count > 0:
          GAUGES['repo_commits'].labels(name=repo.name, owner=repo.owner.username).set(repo.commits_count)

        if repo.branches_count > 0:
          GAUGES['repo_branches'].labels(name=repo.name, owner=repo.owner.username).set(repo.branches_count)

        if repo.forks_count > 0:
          GAUGES['repo_forks'].labels(name=repo.name, owner=repo.owner.username).set(repo.forks_count)

        if repo.open_issues_count > 0:
          GAUGES['repo_issues'].labels(name=repo.name, owner=repo.owner.username).set(repo.open_issues_count)

        if repo.open_pr_counter > 0:
          GAUGES['repo_pull_requests'].labels(name=repo.name, owner=repo.owner.username).set(repo.open_pr_counter)


    except Exception as e:
      print(e)
      print("[WARNING] Unable to retrieve 'Gitea' metrics.")

    time.sleep(interval)