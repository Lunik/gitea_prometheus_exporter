#!/usr/bin/env python3

import os

from api import App


def setup():
  app = App(config_file=os.path.join(os.getcwd(), 'config.yml'))

  app.setup()

  return app

if __name__ == "__main__":
  app = setup()

  app.start()
