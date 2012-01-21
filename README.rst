How to add a cry?
=================

* Update your local tree with ``git pull`` or clone the repository with
  ``git clone`` if you don't have it already
* Add the cry or cries in `www/snd`. See the website FAQ
  (http://lolicri.es/faq.html) for more information on the format/codec
  restrictions and extraction.
* Add a kawaii 300x200 PNG picture in `www/img`
* Run ``git add`` on the just added sound and images files
* Edit `loli_list.py` and add/edit the loli entry
* Run ``make && firefox www/index.html`` and check if everything is fine
* Commit the new loli with ``git commit -a -m <commit message>``
* Request a merge (if you forked the project) or send a patch (``git
  format-patch -1``)
* Wait for a review from a developer

Eventually, a developer will run ``git push`` on the main server with your
patch.


How to edit a standard page?
============================

All the pages content are located in the `src/` directory. Just edit them and
follow the 3 last steps of the previous section.


How to change page information or the index page?
=================================================

Everything you need is in `gen.py`, just edit it and hack.


What is the setup of lolicri.es?
================================

We have a shared bare repository in
``GITROOT=/home/$COMMON_GROUP/lolicri.es.git``. This is the repository cloned
by the developers, `$COMMON_GROUP` being a shared group between them.

A cloned repository (from the `$GITROOT` bare one) is located in
``WWWROOT=/home/$ADMIN_DEV/lolicri.es``. The *DocumentRoot* of the httpd points
on `$WWWROOT/www`. This directory contains all the images, cries, generated
pages, etc. The web server is also configured to redirect any 404 to
`www/404.html`.

Each time a developer pushes something, the script
`$GITROOT/hooks/post-receive` is run. It contains the following code to update
the `$WWWROOT` repository::

    #!/bin/sh

    ADMIN_DEV=...
    WWWROOT=/home/$ADMIN_DEV/lolicri.es

    read oldrev newrev refname
    [ "$refname" != "refs/heads/master" ] && exit 0
    cd $WWWROOT
    unset GIT_DIR
    git pull
    make BASEURL=
