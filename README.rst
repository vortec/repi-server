RePi
===========

RePi manages your virtual environments, whether they're are all
on the same machine or not. You can remotely list installed PyPi
packages or install new ones. RePi does not, unlike Chef or Puppet,
require a SSH connection. All you need is a Redis server your machines
can connect to. If you want to go crazy, you can also use the nightly
Redis build which supports clustering. RePi will still work.


repi-server
===========

This module gives you a small web interface which establishes a
Websocket connection and lets you list PyPi packages or install new
ones. To connect your virtual environments, you need to install and run
`repi-client <http://github.com/vortec/repi-client>`_ in each of them.


Installation
------------

repi-server requires a running Redis server. See`Redis' quickstart
<http://redis.io/topics/quickstart>`_ for installation instructions.
repi-server is compatible with Redis clusters (which is an experimental
feature at this point).

.. code-block:: bash

    $ pip install repi-server

or from source:

.. code-block:: bash

    $ python setup.py install

Getting started
---------------

After installation, you can run the 'repi-server' script.

.. code-block:: bash

    $ repi-server

Now you can point your browser towards http://localhost:8888/ .

To connect to a Redis host different from 'localhost' or change the HTTP
port, you can see a list of all the available options by running:

.. code-block:: bash

    $ repi-server -h
