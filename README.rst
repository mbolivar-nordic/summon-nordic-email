A helper script for setting up a local email workflow for Nordic Semiconductor
accounts using `davmail <http://davmail.sourceforge.net/>`_ to interface with
Exchange, `isync <https://wiki.archlinux.org/title/Isync>`_ to fetch email,
`msmtp <https://wiki.archlinux.org/title/Msmtp>`_ to send mail, and `notmuch
<https://notmuchmail.org/>`_ to index and search email.

From there, you have to pick a front-end program to read the email that can
interface with notmuch. See here for a list:
https://notmuchmail.org/frontends/.

Recommended front-end for emacs users: https://notmuchmail.org/notmuch-emacs/.

LWN articles on notmuch:

- `A year with Notmuch mail <https://lwn.net/Articles/705856/>`_ (2016)
- `A Notmuch mail update <https://lwn.net/Articles/586992/>`_ (2014)
- `Not much of an email review <https://lwn.net/Articles/380073/>`_ (2010)

.. code-block:: none

   usage: summon_nordic_email_ubuntu.py [-h] --name NAME --email EMAIL --password PASSWORD

   options:
     -h, --help           show this help message and exit
     --name NAME          Your Name
     --email EMAIL        your.name@nordicsemi.no
     --password PASSWORD  your application password for accessing email; see
                          https://account.activedirectory.windowsazure.com/AppPasswords.aspx
