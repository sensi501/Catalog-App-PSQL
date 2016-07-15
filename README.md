Project 5 Linux Server Configuration
Jamal Pilgrim


Server SSH Port:
    2200


Server IP Address: 
    52.42.42.203


Server URL:
    http://ec2-52-42-42-203.us-west-2.compute.amazonaws.com/ 


Server Configuration Changes:
    -   Added a new user named "grader" assigned a password and sudo privilages
    -   Updated and upgraded all installed packages and declined grub boot loader upgrade
    -   Reconfiguration of timezone to UTC
    -   Blocked all incomming port communications and allowed all outgoing portcommunications
    -   Allowed incomming port communications on ports 2200, 80, and 123
    -   Installed python-pip, apache2, libapache2-mod-wsgi
    -   Installed PostgreSQL and PostgreSQL-contrib
    -   Added new limited privilage postgresql database role named 'catalog'
    -   Added a new non sudo user named catalog
    -   Installed git
    -   Installed python-dev
    -   Set-up python virtual environment
    -   Installed flask via python pip
    -   Installed sqlalchemy via python pip
    -   Installed oauth2client via python pip
    -   Installed python-psycopg2
    -   Installed libpq-dev
    -   Installed psycopg2 via python pip 
    -   Setup catalog application to run on virtual environment


Additional Software Installed:
    -   python-pip
    -   apache2 
    -   libapache2-mod-wsgi
    -   virtualenv (via - python pip install)
    -   PostgreSQL
    -   PostgreSQL-contrib
    -   git
    -   python-dev
    -   flask (via - python pip install)
    -   sqlalchemy (via python pip install)
    -   oauth2client (via python pip install)
    -   python-psycopg2
    -   libpq-dev
    -   psycopg2 (via python pip install)


Third Party Help/Tutorial/Information Resources:
    -   Add New User With Sudo Privilages
        -   https://www.digitalocean.com/community/tutorials/how-to-create-a-sudo-user-on-ubuntu-quickstart

    -   Update and Upgrade Ubuntu Software Packages
        -   https://www.digitalocean.com/community/tutorials/how-to-upgrade-to-ubuntu-16-04-lts

    -   Change Ubuntu Time Zone Data
        -   https://www.digitalocean.com/community/tutorials/how-to-set-up-timezone-and-ntp-synchronization-on-ubuntu-14-04-quickstart

    -   Change ssh daemon port configurations
        -   https://www.digitalocean.com/community/tutorials/how-to-tune-your-ssh-daemon-configuration-on-a-linux-vps

    -   Set-up Ubuntu UFW Firewall Ports And Rules
        -   https://www.digitalocean.com/community/tutorials/how-to-setup-a-firewall-with-ufw-on-an-ubuntu-and-debian-cloud-server

    -   Install Apache And mod_wsgi
        -   https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-16-04

    -   Install PostgreSQL
        -   https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04

    -   Configure And Secure PostgreSQL
        -   https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps

    -   Install Git
        -   https://www.digitalocean.com/community/tutorials/how-to-install-git-on-ubuntu-14-04

    -   Hosting Flask Application on Ubuntu
        -   https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps

    -   Setup psycopg2
        -   http://stackoverflow.com/questions/28253681/you-need-to-install-postgresql-server-dev-x-y-for-building-a-server-side-extensi


Notes
    -   Google account login authentication will only with updated Google App Engine Credentials


Contact:
<<<<<<< HEAD
    sensi501@gmail.com
=======
    sensi501@yahoo.com
>>>>>>> origin/master
