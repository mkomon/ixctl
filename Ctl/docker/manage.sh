IXCTL_HOME=/srv/ixctl

. $IXCTL_HOME/venv/bin/activate
cd $IXCTL_HOME/main

./manage.py $@
