#!/bin/bash
# Running as root
##############################################
ADMIN_USER=vman

update_webroot(){
    cd /srv/www/simplyfound.com/pri/venv/webroot
    source /srv/www/simplyfound.com/pri/venv/bin/activate
    git pull
    git checkout production
    git pull
    pip install -r env/reqs/prod.txt
}
export -f update_webroot

update_seekrets(){
    cd /srv/www/seekrets/simplyfound-seekrets
    git pull
    git checkout production
    git pull
}
export -f update_seekrets

# Install unattended upgrade for security updates
echo '**** Run unattended upgrades ****'
apt-get install unattended-upgrades -y
unattended-upgrade

# Update source code and seekrets
echo '**** Update Webroot simplyfound ****'
su $ADMIN_USER -c "bash -c update_seekrets"

echo '**** Update seekrets simplyfound ****'
su $ADMIN_USER -c "bash -c update_webroot"

# Restart webserver
echo '**** Restart web server ****'
supervisorctl stop simplyfound.com
supervisorctl start simplyfound.com
