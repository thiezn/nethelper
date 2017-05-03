Running NetHelper through systemd
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Test if this actually works...!

Here we have a prepared service file for running the NetHelper web application through UNIX systemd. 


The service file
================

The file nethelper.service contains all the things. Here's an overview of the more interesting fields

- After=network.target          indicates when the machine boots up it should wait until the main network functionality is available.
- Environment=SERVER_PORT       This allows you to provide environmental variables
- User=ubuntu                   Indicates the user the service should run as
- ExecStart=                    Is the actual CLI command to launch the application
- Restart=on-failure            Instructs systemd to restart the service if it sees it crashed. Does not restart when the application gracefully shut down
- Install section               Not sure ut just do what is says on the tin

There's a lot more you can do with this, rtfman page...!


copy the file to /lib/systemd/system/

systemctl to control the application
====================================

First run the following command. This needs to happen every time the service file has changed:

    sudo systemctl daemon-reload

Next, launch the application:

    sudo systemctl start nethelper

After this the application should be up and running.

To check the status of the application do:

    sudo systemctl status nethelper

Stopping application:

    sudo systemctl stop nethelper

Restarting the application:

    sudo systemctl restart nethelper

Ensure the application starts when the machine boots up

    sudo systemctl enable nethelper

Disabe the application from starting when the machine boots up

    sudo systemctl disable nethelper

Load balancing and other stuff through nginx
============================================

Python's (in)famous GIL limits standard applications to a single thread so doesn't allow you to utilise multiple CPUs of the machine. In order to fully
utilise the server's hardware we want to run multiple instances of the application.


systemd multiple instances
--------------------------

Each application instance will run on localhost and a seperate TCP port for this to work. The application clients will connect to nginx which load balances traffic between the various processes.
nginx also has good support for caching of static content which will offload the application processes.

systemd allows you to run multiple instances of your applications. To allow this we will have to rename our service file to nethelper@.service. This will tell systemd that you want to run multiple instances.
Next edit the Environment= directive as follows:

    Environment=SERVER_PORT=%i

Now you can launch multiple instances on different ports using the systemctl command:

    sudo systemctl start nethelper@4001
    sudo systemctl start nethelper@4002
    sudo systemctl start nethelper@4003

or if you want a oneliner:

    for port in $(seq 4001 4003); do sudo systemctl start nethelper@$port; done

Please note that each instance will have to be enabled as before:

    sudo systemctl enable nethelper#4001
    sudo systemctl enable nethelper#4002
    sudo systemctl enable nethelper#4003

You could also do the same trick as above using different configuration files. For instance if you edit the service file to look like this:

    ExecStart=/usr/bin/env python3 run.py --config %i

and then start the instances like this:

    sudo systemctl start nethelper@config/file1.json
    sudo systemctl start nethelper@config/file2.json
    ...


nginx configuration
-------------------

first install nginx and remove all the default configs

    sudo apt-get update
    sudo apt-get -y install nginx-full
    sudo rm -fv /etc/nginx/sites-enabled/default

Next create a load balancing configuration file in as root user:

    sudo vi /etc/nginx/sites-enabled/nethelper.conf

Add the followong to the configuration file:

    upstream nethelper {
        server 127.0.0.1:4001
        server 127.0.0.1:4002
        server 127.0.0.1:4003
    }

    server {
        listen 80 default_server;
        server_name _;

        location / {
            proxy_pass http://nethelper;
            proxy_set_header Host $host;
       }
    }

This is all thats required. nginx will use round-robin load balancing by default. Check http://nginx.org/en/docs/http/load_balancing.html for more details

Now go and start nginx using systemd and browse to the nginx defined server to see your application running in full, load-balanced, high-perfomant bliss...

    sudo systemctl restart nginx
