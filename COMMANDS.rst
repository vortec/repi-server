Commands
========
The default channels are using the 'repi' namespace. To talk to all connected repi-clients, publish a command to 'repi:cluster' (you can change those names). To talk to a specific repi-client, publish to 'repi:client-name'.

Exchange a simple PING/PONG:

.. code-block:: json

    {
        "command": "PING",
        "client": "master",
        "data": null
    }

Get a list of all installed packages:

.. code-block:: json

    {
        "command": "PACKAGE_LIST",
        "client": "master",
        "data": null
    }

Install a package:

.. code-block:: json

    {
        "command": "INSTALL",
        "client": "master",
        "data": {
            "package": "BeautifulSoup",
            "version": null
        }
    }

Install a certain package version:

.. code-block:: json

    {
        "command": "INSTALL",
        "client": "master",
        "data": {
            "package": "BeautifulSoup",
            "version": "3.2.1"
        }
    }