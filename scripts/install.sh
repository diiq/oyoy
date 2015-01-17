mkvirtualenv oyoy
ln -s `pwd`/scripts/virtualenv/* $VIRTUAL_ENV/$VIRTUALENVWRAPPER_ENV_BIN_DIR
pip install -r requirements.txt
deactivate
workon oyoy
