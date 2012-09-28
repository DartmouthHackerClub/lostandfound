#!/usr/bin/env python
from shutil import copyfile
# copy default settings
copyfile("default_settings.py", "local_settings.py")

# setup development database
from app import db
db.create_all()
