Virtualenv Application Manager
==============================

Install Python applications into their own virtual environments automatically.

Have you ever tried to install two applications from PyPI which have conflicting requirements?
The usual answer to this is using virtualenvs which provide a sandboxed environment to install the packages into.
However, virtualenvs are not really designed for installing *applications* into,
they are designed for installing libraries into against which you write your application.

``vam`` provides a way to install as many Python applications as you wish alongside each other without them interfering with in any way.

For example, running:

.. code-block:: bash

    vam install pss
    vam install pytest

will install each of these into their own virtualenvs so that any dependencies they have will not interfere.
A launcher script will be installed into ``~/.local/bin/`` to start any applications they may have installed.
