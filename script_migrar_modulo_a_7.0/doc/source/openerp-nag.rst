Openerp Nag
===========

Prerequisites
-------------

Python 2.7 is guaranteed to be supported.
Other versions of Python have not been tested.

The launchpadlib_ egg is required.

Usage
-----

See the usage of `openerp-nag` using::

  openerp-nag --help

Basically, for the OpenERP Community reviews,
you will mainly use::

  openerp-nag --projects-file projects
  openerp-nag -f projects  # short version

Or, if you want to target one or a few
specific project::

  openerp-nag --project account-financial-report
  openerp-nag -p account-financial-report  # short version
  openerp-nag -p account-financial-report banking-addons  # multiple projects


List of projects
----------------

The list of projects to watch is defined in
the `projects` file.

I did not find any means to build the list
of projects based on the launchpad team.

So each time a project is added in the
Community Reviewers pool, it has to be added there.

If someone can contribute to automatize the build of
the projects list (if that where possible),
that would be great.


Known issues
------------

SSL troubles
  If you encounter issues with the SSL certificate,
  try an update of the `httplib2` egg::

    pip install --upgrade httplib2

  On non Debian based systems you have to patch the `lazr.restfulclient`_
  library, see the `lazr.restfulclient bug report`_.


.. _launchpadlib: http://pypi.python.org/pypi/launchpadlib/1.10.2
.. _lazr.restfulclient: https://launchpad.net/lazr.restfulclient
.. _lazr.restfulclient bug report: https://bugs.launchpad.net/lazr.restfulclient/+bug/1094253
