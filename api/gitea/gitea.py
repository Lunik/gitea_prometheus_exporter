from lib.gitea import Gitea

def gitea_export(app):
  metrics = dict()

  print("========== Scraping Start ==========")

  try:
    gitea = Gitea(app.config['MODULE_CONFIG']['url'], app.config['MODULE_CONFIG']['auth']['token'])
    print(gitea.get_version())
  except Exception as e:
    print(e)
    print("[WARNING] Unable to initiate connection with gitea.")
    return metrics

  try:
    metrics['users'] = gitea.get_users()
  except Exception as e:
    print(e)
    print("[WARNING] Unable to retrieve 'Gitea Users'.")
    metrics['users'] = dict()

  try:
    metrics['orgs'] = gitea.get_orgs()
  except Exception as e:
    print(e)
    print("[WARNING] Unable to retrieve 'Gitea Users'.")
    metrics['orgs'] = dict()

  metrics['repos'] = []

  try:
    for user in metrics['users']:
      metrics['repos'] += user.get_repositories()
  except Exception as e:
    print(e)
    print("[WARNING] Unable to retrieve 'Gitea Users repos'.")

  try:
    for org in metrics['orgs']:
      metrics['repos'] += org.get_repositories()
  except Exception as e:
    print(e)
    print("[WARNING] Unable to retrieve 'Gitea Orgs repos'.")

  try:
    for repo in metrics['repos']:
      repo.branches_count = len(repo.get_branches()) if not repo.empty else 0
      repo.commits_count = repo.get_commit_count() if not repo.empty else 0
  except Exception as e:
    print(e)
    print("[WARNING] Unable to retrieve 'Gitea repos git infos'.")

  return metrics
