SafelySaveOnline
================

SafelySaveOnline is a python libary making it easy to save encrypted
dictionaries and store them in a git repository.

Installing
----------

You can install SafelySaveOnline with:

::

   pip install safelysaveonline

Usage
-----

Import SafelySaveOnline with:

::

   import safelysave

Create a SSO file with:

::

   key: bytes = safelysave.create_sso_file(file_path, 'git', git_repo_address)

Remember the returned key.

Create a instance with:

::

    sso = safelysave.sso(file_path, key)

Now add an dictionary with:

::

   sso.add_data(ictionary)

Push it to your repo with:

::

   sso.sync()

You can find out more at
https://codeberg.org/VisualXYW/safelysaveonline/wiki (WIP/Outdated).
