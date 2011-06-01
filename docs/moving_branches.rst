Moving Your Branches from Launchpad to GitHub
=============================================

This document will give you a detailed account of how to transfer your branches
from Launchpad to GitHub and explain what to do once you've moved.


You'll Be Using
---------------
- git-bzr-ng (http://github.com/termie/git-bzr-ng)
- python-github3 (included in the lp2gh tree)
- launchpadlib (http://launchpad.net/launchpadlib)
- bin/lp2gh-export-branches
- git and bzr, obviously
- a launchpad account that has access to your project's branches (actually the
  code only handles anonymous access at the moment)
- a github account


Overview
--------

The import process works by getting a list of all Launchpad branches associated
with your project, exporting them to a local git repository and then using a
normal git command to push to GitHub. The original owners of those branches
will then pull the changes in to their forks (example commands given below).

The exporter does some minor modifications along the way to ensure that branch
names will be git-compliant, specifically replacing the tilde '~' character
with a dash '-' character.


Exporting Your Branches
-----------------------

This process is easy to get started but will likely take a while if you have
a large project with many branches, you will effectively be making a bzr
checkout _and_ git checkout of each branch.

To begin the export run the following:

  $ bin/lp2gh-export-branches <your_project_name>

That will make a directory named <your_project_name> and begin importing all
of the branches associated with it. The branches will be named according to the
template <owner>_<branch_name> so that it will be easier for your project
members to find their branches afterwards.

You may want to take this chance to create the GitHub project you will import
to, if you haven't already.


Setting Up Your GitHub Project
------------------------------

Let's assume your project is named 'nova' and will be owned by an organization
named 'openstack' that you can create repositories in and your github user is
'termie'. To reduce the size of the main repository you aren't going to upload
all the branches to the fork owned by the organization, we're just going to
push master.

  $ cd nova
  $ git push git@github.com:openstack/nova master

This will push the 'base' code to the main repository. Once it is done, go to
that project on github.com, http://github.com/openstack/nova, and fork it. We
are going to upload the rest of the branches to your fork (thanks for taking
one for the team!) and you'll probably want to delete them all eventually.

  $ git push --all git@github.com:termie/nova

That will take a little while, though probably much less time than the import.


Getting Your Project Members On Board
-------------------------------------

Now that you've got all the code related to the project on to GitHub we still
need to get it into the hands of the original authors. Here's what each of them
should do:

  # First, go to http://github.com/openstack/nova and fork that project.
  $ git clone git@github.com:<your_name>/nova
  $ cd nova

  # This will import <export_branch_name> as <branch_name> in your repository
  # so you can remove your name from the branch.
  # Repeat for each branch you wish to import.
  $ git fetch http://github.com/termie/nova <export_branch_name>:<branch_name>

  # Push all your local branches to your GitHub fork.
  $ git push -a origin

Vwalla! Now you can work on any of those branches by doing:

  $ git checkout <branch_name>

And later pushing back to GitHub by:

  $ git push origin <branch_name>

Read on for some strategies for managing your project's forks and branches.


Continuing Your Development on GitHub
-------------------------------------

There are plenty of strategies teams use for developing with git, but this one
is geared at those of you making the Launchpad to GitHub transition.


--------------------------
Forks and Branches, Oh My!
--------------------------

Launchpad is a project-centric environment, so you will most likely have a
GitHub organization that owns the 'main' repository and encourage all members
and newcomers to fork from that. This means every developer should have a fork
of the organization's repository.

Within that fork, developers will make branches to support their feature work
and periodically, usually when about to issue a pull request -- GitHub's version
of a merge proposal, pull down changes from the upstream organization master
into their master. Since this will happen relatively often it is easiest to add
an additional 'remote' target for it:

  $ git remote add openstack http://github.com/openstack/nova.git

To update your feature branches before issuing a pull request you will do
something like:

  $ git checkout master
  $ git pull openstack
  $ git checkout <branch_name>

  # If you prefer to merge
  $ git merge master

  # Or if you prefer to rebase (I do)
  $ git rebase master

  # And if you want to get fancy and use interactive rebase
  $ git rebase -i master

Either way, at the end you should be left with a branch that should merge
cleanly with master once your pull request is approved.


----------------------
Continuous Integration
----------------------

A popular pattern on Launchpad is one of automating merges into the main
repository and gating that automation on continuous integration testing. For
this Launchpad often uses Jenkins and Tarmac, and on GitHub for the moment I'd
recommend using Jenkins and Roundabout for similar results.

Roundabout is triggered off of keywords used in comments on pull requests,
combined with filters on group membership (and is generally easily to hack to
add additional filters). Typically this will be checking for some number of
comments with a single 'LGTM' made by a member of a given team in an
organization.

Roundabout will then attempt to perform the merge, run all the tests via
Jenkins and if the result passes, push that merge to the main repository. If
the tests fail it will update the pull requests with the output and refuse to
merge.
