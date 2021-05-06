Intention
=========

Make it "easier" for people to work on encrypted documents remotely.
Using git-remote-gcrypt (OpenPGP encrypted Git repository) and Git for
version control on Github (as an example) using git-remote-gcrypt
(https://github.com/spwhitton/git-remote-gcrypt).

@Github
=======

Create user account at Github.
Add ssh key to the repository.

Create a private repository at Github (or elsewhere).
Don't clone this repository yet!

On your computer
================

Make sure you installed git-remote-crypt.

    sudo apt install git-remote-gcrypt

Configure locally to use that key:

    vi ~/.ssh/config

In the file add:

    Host github
    Hostname github.com
    Port 22
    IdentityFile ~/.ssh/id_rsa
    IdentitiesOnly=yes
    ForwardAgent yes

On your computer create folder with repository name.

    mkdir reponame
    cd reponame

Add the Github repo as a remote

    git remote add origin gcrypt::git@github.com:yourgithubusername/reponame.git

Add your own GPG key ID:

    git config gcrypt.participants EDE3F4443F34D2619514D790B14BB0C38D861CF1

Now create a file

    vi test.txt

Add & commit the file with Git:

    git add test.txt
    git commit test.txt

Now you can push to the remote repository and your file will be
encrypted to your OpenPGP key:

    git push -u origin master

Working with an encrypted repository
====================================

It's crucial to always pull from the repository first before pushing new
content!

    git pull origin master

work and commit your work

    git commit modifications.txt

new files need to be added first before they can be committed

    git add newfile.txt
    git commit newfile.txt

Now send all that to the server

    git push -u origin master

Working with several people on that repository
==============================================

@Github create a user account per person, add their ssh key and give
them access to the repository you initially created on Github.

Verify or change the users the content is encrypted to
------------------------------------------------------

You can see the participant list in

    reponame/.git/config

Participants' key are listed in a white space separated list, under
gcrypt.participants.

Adding participants
→ look for their long key ID, gpg --list-keys friend@example.org

    git config --add gcrypt.participants [longkeyid]

Note that ALL participants share the same git config file. If one of
them has a different participant configuration, it might be that what
they commit is not readable to every participant (for example, if they
forgot to add this participant).

There can be a README to make this known and list the key IDs that
should be in the file.
