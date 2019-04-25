#!/usr/bin/env bash

# Check root
if [[ `id -u` -ne 0 ]]; then
	echo "Setup must be run as root user."
	exit 1
fi

if [[ -z "$1" ]]; then
    echo "Input domain is required."
    exit 1
fi

# Constants
appdir=$(realpath "$(dirname $0)")
project="syllabus"
username="$project"
sysfile="/etc/systemd/system/${project}.service"
destination="/opt/${project}"
domain="$1"
httpconf="/etc/nginx/sites-available/$domain"
PKGS=( "\
build-essential \
python3.5 \
python3-dev \
postgresql \
postgresql-contrib \
libssl-dev \
yarn \
nginx" )

# Add yarn repo
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
if [[ ! -f /etc/apt/sources.list.d/yarn.list ]]; then
    echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list
    apt-get update
fi

# Install missing packages
found_pkgs=""
for i in ${PKGS[@]}; do
    dpkg --list | grep $i &> /dev/null || found_pkgs="${found_pkgs} ${i}"
done
[[ -z "$found_pkgs" ]] || apt-get install -y $found_pkgs

# Check pip
if ! which pip3 &> /dev/null; then
    curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
    python3 /tmp/get-pip.py
    rm -f /tmp/get-pip.py
else
    pip3 install pip --upgrade
fi

# Check install requirements
pip3 install -r $appdir/requirements.txt --upgrade

# Check uwsgi existence
if ! which uwsgi &> /dev/null; then
    echo "uWSGI is not installed"
    exit 1
fi

# Backward compatibility for nodejs
test -f /usr/bin/node || ln -s `which nodejs` /usr/bin/node

# Create postgresql database & role
query="SELECT 1 FROM pg_roles WHERE rolname='$project'"
if [[ $(sudo -u postgres psql postgres -tAc "$query") -ne 1 ]]; then
    echo "Creating PostgreSQL user and database..."
    sudo -u postgres createuser -P -d $project && \
    sudo -u postgres createdb $project
fi

# Create user
id -u $username &> /dev/null || \
useradd -r -s /bin/false -M -d $destination $username

# Copy source
[[ -d "$destination" ]] || mkdir -p $destination
yes | cp -rf $appdir/* $destination/
chown -R $username:www-data $destination

# Install static libraries
curdir=`pwd`
cd $destination/app
yarn install
cd $curdir

# Create systemd service
if ! systemctl status $project &> /dev/null; then
    cat > $sysfile <<EOF
[Unit]
Description=uWSGI Server for $project
After=syslog.target

[Service]
User=$username
Group=www-data
ExecStart=$(which uwsgi) --ini $destination/app/wsgi.ini --chdir $destination
WorkingDirectory=$destination
Restart=always
KillSignal=SIGTERM
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
EOF

    # Reload and start service
    systemctl daemon-reload
    systemctl enable $project
    systemctl start $project
fi

# Configure nginx
test -f /etc/nginx/sites-enabled/default && \
rm -f /etc/nginx/sites-enabled/default

if [[ ! -f $httpconf ]]; then
    cat > $httpconf <<EOF
server {
    listen 80;
    server_name $domain www.$domain;

    location /static {
        alias $destination/app/static;
    }

    location / {
        include uwsgi_params;
        uwsgi_pass unix:///$destination/countpy.sock;
    }
}
EOF

    ln -s $httpconf /etc/nginx/sites-enabled/$domain
fi

# Restart nginx
systemctl enable nginx
systemctl restart nginx

# Finish
echo "Done!"
