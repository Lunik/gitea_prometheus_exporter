import yaml
import os
import shutil
import threading

from prometheus_client import start_http_server

from api.gitea import module as GiteaModule


class App:
  def __init__(self, config_file=""):
    self.cache = dict()

    if config_file is not None and config_file != "":
      self.config = self._parseConfig(config_file)

  def _parseConfig(self, config_file):
    with open(config_file, 'r') as file:
      config = yaml.full_load(file)

    if config is None:
      raise Exception("Config file is empty: {}".format(config_file))

    return config

  def setup(self):
    pass

  def start(self):
    start_http_server(int(self.config['LISTEN_PORT']), self.config['LISTEN_HOST'])
    print("Prometheus exporter started.")

    threading.Thread(target=GiteaModule, args=(self,)).start()
