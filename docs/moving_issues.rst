Moving Your Bugs, Blueprints and Milestones to GitHub
=====================================================

This document will give you a detailed account of how to transfer your bugs,
blueprints and milestones from Launchpad to GitHub and explain what to do once
you've moved.


You'll Be Using
---------------
- python-github3 (included in the lp2gh tree)
- launchpadlib (http://launchpad.net/launchpadlib)
- most of the files in the bin directory
- a launchpad account that has access to your project's branches (actually the
  code only handles anonymous access at the moment)
- a github account
- if you want to be cool, a mapping of your project members' Launchpad
  usernames to their GitHub usernames


Overview
--------

The import process works by first exporting the current content of the bugs,
blueprints and milestones associated with your project, and then feeding those
files into the import tools.

The import tools will push them to GitHub while translating some of their
content to point to the new issue numbers and adding a summary to the
description that shows some additional history of the issue and a link to the
original Launchpad bug or blueprint.

They will all be imported as GitHub issues and tagged appropriately.


Exporting Your Bugs
-------------------

Bugs are so Launchpad, we want to make some Issues, but the first step is
getting all the data.

To begin the export run the following::

  # <your_project_name> is the part after 'lp:', e.g. nova instead of lp:nova
  $ bin/lp2gh-export-bugs <your_project_name> > my_bugs.json

That will export the bugs from Launchpad and dump a JSON file that looks a bit
like::

  [
    {
      "status": "Fix Released",
      "security_related": false,
      "description": "nova/objectstore/handler.py\nimageResoure#render_GET\n\nYou can call image.is_authorized(context, True)",
      "tags": [],
      "duplicates": [],
      "assignee": "xtoddx",
      "milestone": "austin",
      "owner": "xtoddx",
      "id": 653344,
      "duplicate_of": null,
      "title": "Image downloading should check project membership and publicity settings",
      "comments": [
        {
          "owner": "dendrobates",
          "content": "what is the status if this fix",
          "date_created": "2010-10-19T16:12:08Z"
        },
        {
          "owner": "xtoddx",
          "content": "Fix in lp:~xtoddx/nova/imagedownload, proposing now",
          "date_created": "2010-10-19T23:42:40Z"
        }
      ],
      "importance": "Critical",
      "lp_url": "https://bugs.launchpad.net/bugs/653344",
      "date_created": "2010-10-01T23:50:09Z"
    }
  ]

It may take a while for big projects, but should give you some progress updates
as it moves along.

Keep track of that file, you are going to use it again later.


Exporting Your Milestones
-------------------------

Pretty much the same process here as for exporting bugs::

  # <your_project_name> is the part after 'lp:', e.g. nova instead of lp:nova
  $ bin/lp2gh-export-milestones <your_project_name> > my_milestones.json

Which will result in a `my_milestones.json` that looks like::

  [
    {
      "active": false,
      "date_targeted": null,
      "name": "2010.1-rc2",
      "summary": "Austin Release Candidate 2"
    },
    {
      "active": true,
      "date_targeted": "2011-09-10T00:00:00Z",
      "name": "diablo-integrated-freeze",
      "summary": ""
    }
  ]


Exporting Your Blueprints
-------------------------

The same process here as for exporting bugs::

  # <your_project_name> is the part after 'lp:', e.g. nova instead of lp:nova
  $ bin/lp2gh-export-blueprints <your_project_name> > my_blueprints.json

Which will result in a `my_blueprints.json` that looks like::

  [
    {
      "whiteboard": "Setting this to diablo-4 because it is vital to have for our next release, but we haven't fully defined all of the functions needed.  Some of this can be informed by the effort to move dashboard over.  --vish",
      "name": "admin-account-actions",
      "title": "Admin API: Actions to perform on accounts",
      "url": "http://wiki.openstack.org/NovaAdminAPI#A.2BAC8-accounts.2BAC8.7Baccount_id.7D.2BAC8-action",
      "milestone": "diablo-4",
      "bugs": [],
      "definition_status": "Approved",
      "priority": "Essential",
      "assignee": "rackspace-titan",
      "dependencies": [
        "api-additions"
      ],
      "lp_url": "https://blueprints.launchpad.net/nova/+spec/admin-account-actions",
      "drafter": "glen-campbell",
      "lifecycle_status": "Not started",
      "date_created": "2011-04-13T18:59:40Z",
      "summary": "As a service provider, Rackspace needs to perform certain actions on a per-account basis. For example, an account needs to be suspended for violations of terms of service or non-payment. This specification is for a set of actions that can be performed on an account, which usually translates to actions performed on all the servers belonging to an account. ",
      "implementation_status": "Not started"
    }
  ]


Getting All That Stuff On To GitHub
-----------------------------------

This part starts getting a bit more complicated because the order you do things
in will matter more. While it is possible to import only bugs or only blueprints or only milestones this guide will focus on the more involved process of
importing all three.

The general way of the importers is that as they are run they produce an output
that is a mapping of the old Launchpad identifiers to the new GitHub
identifiers. Those mappings will be used by other importers to support the
translation of content in the bugs, etcetera.


--------------------
Importing Milestones
--------------------

Milestones don't have any other dependencies so we'll import those first.

You'll need to have your `my_milestones.json` file around::

  $ ./bin/lp2gh-import-milestones --username=<your_github_username> \
                                  --password=<your_github_password> \
                                  --repo_user=<target_github_repo_user> \
                                  --repo_name=<target_github_repo_name> \
                                  my_milestones.json > my_milestones_map.json

Which will output a `my_milestones_map.json` that looks like::

  {
    "diablo-4": 3,
    "cactus-gamma": 9,
    "diablo-1": 6,
    "diablo-2": 5,
    "diablo-3": 4,
    "bexar-gamma": 13,
    "2010.1-rc2": 1,
    "2011.1.1": 10,
    "austin-final-freeze": 17,
    "2010.1": 15,
    "2011.2": 7,
    "austin-feature-freeze": 18,
    "2011.1": 11,
    "bexar-rc": 12,
    "austin-rc": 16,
    "austin": 14,
    "cactus-rc": 8,
    "diablo-integrated-freeze": 2
  }

And will result in a a variety of empty milestones, preserving any targeted
dates.

--------------
Importing Bugs
--------------

Similar to importing the milestones, but will make use of the mapping file
created earlier to allow attaching bugs to milestones::

  $ ./bin/lp2gh-import-bugs --username=<your_github_username> \
                            --password=<your_github_password> \
                            --repo_user=<target_github_repo_user> \
                            --repo_name=<target_github_repo_name> \
                            --milestones_map=my_milestones_map.json
                            my_bugs.json > my_bugs_map.json

This will output a `my_bugs_map.json` file that looks similar to::

  [INSERT BUGS OUTPUT]

And will result in all the issues being created over three passes, the first
pass will generate all the labels (tags in Launchpad) that are being used by
any bug. The second pass will create the basic content of the issue as it
existed on Launchpad. Finally, the third pass will use the new bug mapping
to translate autolinks from the Launchpad bug numbers to the GitHub issue
numbers, add a summary to the issue description that includes additional
information from the launchpad history of the project, and finally add all
the comments made so far on the issue.

The summary will currently look similar to::

  Imported from Launchpad using lp2gh.

  date created: 2011-04-04T17:52:50Z
  owner: tpatil
  assignee: mihgen
  the launchpad url was https://bugs.launchpad.net/bugs/750544

The comments will look similar to::

  (by blamar)
  What version of glance are you running? Although snapshotting doesn't work for me in nova trunk, this looks to be a glance issue?

