#!/usr/bin/env python3

import argparse
import os
from pathlib import Path
import subprocess

MAILDIR = str(Path.home() / 'maildir')

def get_dot_davmail_dot_properties(email):
    # email: e.g. marti.bolivar@nordicsemi.no

    mail_prefix = email.split('@')[0]
    return f'''\
#DavMail settings
#Tue Jun 04 13:58:03 MDT 2019

# Per-user config
davmail.url=https\://outlook.office365.com/owa/{mail_prefix}@nordicsemi.mail.onmicrosoft.com/EWS/Exchange.asmx
# davmail.url=https\://login.microsoftonline.com/common/oauth2/authorize?client_id=00000002-0000-0ff1-ce00-000000000000&amp;redirect_uri=https%3a%2f%2foutlook.office365.com%2fowa%2f&amp;resource=00000002-0000-0ff1-ce00-000000000000&amp;response_mode=form_post&amp;response_type=code+id_token&amp;scope=openid&amp;msafed=0&amp;client-request-id=758156d1-b57b-432a-a2ab-1227ab1714cd&amp;protectedtoken=true&amp;nonce=637157338580333381.38af221a-8092-4030-a3a1-b47644c6bff2&amp;state=DYvLDsIgEACpfg_PpQVvxtijJw-et1gsSWET2mg_XyaZuU3HGDs3T81OtTA3gNO9A_C9V9DwWoDHaIxG7tXFcKtAcQTUfLJusDYMU4yma-9d0g_lA-uexI3W9MV6LVTfKWxzTiJjWgWVnEKljeIuAmU5vp5yPMKC5TML3PLxBw

# Network ports:
davmail.caldavPort=1080
davmail.imapPort=1143
davmail.ldapPort=1389
davmail.smtpPort=1025
davmail.popPort=1110

# Logging:
log4j.logger.davmail=INFO
log4j.logger.httpclient.wire=WARN
log4j.logger.org.apache.commons.httpclient=WARN
log4j.rootLogger=INFO,fout

# Etc.:
davmail.allowRemote=false
davmail.bindAddress=
davmail.caldavAlarmSound=
davmail.caldavAutoSchedule=true
davmail.caldavEditNotifications=false
davmail.caldavPastDelay=0
davmail.carddavReadPhoto=true
davmail.clientSoTimeout=
davmail.defaultDomain=
davmail.disableGuiNotifications=false
davmail.disableUpdateCheck=false
davmail.enableKeepAlive=false
davmail.enableKerberos=false
davmail.enableProxy=false
davmail.folderSizeLimit=
davmail.forceActiveSyncUpdate=false
davmail.imapAlwaysApproxMsgSize=false
davmail.imapAutoExpunge=true
davmail.imapIdleDelay=
davmail.keepDelay=30
davmail.mode=EWS
davmail.noProxyFor=
davmail.oauth.clientId=
davmail.oauth.redirectUri=
davmail.popMarkReadOnRetr=false
davmail.proxyHost=
davmail.proxyPassword=
davmail.proxyPort=
davmail.proxyUser=
davmail.sentKeepDelay=0
davmail.server=true
davmail.server.certificate.hash=
davmail.showStartupBanner=true
davmail.smtpSaveInSent=true
davmail.ssl.clientKeystoreFile=
davmail.ssl.clientKeystorePass=
davmail.ssl.clientKeystoreType=
davmail.ssl.keyPass=
davmail.ssl.keystoreFile=
davmail.ssl.keystorePass=
davmail.ssl.keystoreType=
davmail.ssl.nosecurecaldav=false
davmail.ssl.nosecureimap=false
davmail.ssl.nosecureldap=false
davmail.ssl.nosecurepop=false
davmail.ssl.nosecuresmtp=false
davmail.ssl.pkcs11Config=
davmail.ssl.pkcs11Library=
davmail.useSystemProxies=false
'''

def get_dot_mbsyncrc(email, password, legacy_names=True):
    # legacy_names: if true, return old-style mbsync config format which uses
    #               the terms 'Master' and 'Slave' instead of 'Far' and 'Near'
    #               when configuring the channel between remote and local
    #               mail boxes. Required for Ubuntu 20.04's isync.

    if legacy_names:
        far = 'Master'
        near = 'Slave'
    else:
        far = 'Far'
        near = 'Near'

    return f'''\
IMAPAccount nordic
Host localhost
Port 1143
User {email}
# You can also set a command that will print your password. See:
# https://wiki.archlinux.org/index.php/Isync
# You will likely need to set up and use an application password. See:
# https://account.activedirectory.windowsazure.com/AppPasswords.aspx
Pass {password}
AuthMechs LOGIN
SSLType None
Timeout 0

IMAPStore nordic-remote
Account nordic

MaildirStore nordic-local
Subfolders Verbatim
Path {MAILDIR}/nordic/
Inbox {MAILDIR}/INBOX

Channel nordic
{far} :nordic-remote:
{near} :nordic-local:
Patterns *
Create {near}
Sync Pull
SyncState *
'''

def get_dot_notmuch_config(name, email):
    return f'''\
[database]
path={MAILDIR}

[user]
name={name}
primary_email={email}

[new]
tags=unread;inbox;
ignore=

[search]
exclude_tags=deleted;spam;

[maildir]
synchronize_flags=true
'''

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--name', required=True, help='Your Name')
    parser.add_argument('--email', required=True,
                        help='your.name@nordicsemi.no')
    parser.add_argument(
        '--password', required=True,
        help='''your application password for accessing email; see
        https://account.activedirectory.windowsazure.com/AppPasswords.aspx''')

    return parser.parse_args()

def get_dot_msmtprc(email, password):
    return f'''\
defaults
logfile /home/mbolivar/.msmtp.log

account nordic
host localhost
port 1025
protocol smtp
from {email}
auth login
user {email}
password {password}

account default : nordic
'''

def hline():
    try:
        print('-' * os.get_terminal_size()[0])
    except:
        pass

def main():
    args = parse_args()

    if args.name is not None:
        name = args.name
    else:
        name = subprocess.run('git config user.name', shell=True, capture_output=True, encoding='utf-8').stdout.strip()

    hline()
    sudo = 'sudo' if os.getuid() else ''
    install_deps = f'{sudo} apt-get install isync davmail notmuch msmtp-mta'
    print(f'Installing dependencies with:\n\n{install_deps}')
    hline()
    subprocess.run(install_deps, shell=True, check=True)
    hline()
    print('Dependencies set up!')
    hline()

    print('Writing configuration files...\n')
    mbsyncrc = Path.home() / '.mbsyncrc'
    print(f'- {mbsyncrc}')
    with open(mbsyncrc, 'w') as f:
        f.write(get_dot_mbsyncrc(args.email, args.password))
    davmail_properties = Path.home() / '.davmail.properties'
    print(f'- {davmail_properties}')
    with open(davmail_properties, 'w') as f:
        f.write(get_dot_davmail_dot_properties(args.email))
    notmuch_config = Path.home() / '.notmuch-config'
    print(f'- {notmuch_config}')
    with open(notmuch_config, 'w') as f:
        f.write(get_dot_notmuch_config(name, args.email))
    msmtprc = Path.home() / '.msmtprc'
    print(f'- {msmtprc}')
    with open(msmtprc, 'w') as f:
        f.write(get_dot_msmtprc(args.email, args.password))
    subprocess.run(f'chmod go-rw {msmtprc}', shell=True, check=True)
    print('\ndone!')
    hline()

    print('''\
Next step: create your initial local email index:

  davmail &
  mkdir -p ~/maildir/nordic
  mbsync nordic
  notmuch new

This first run will take a long time. The "Password is being sent in the clear"
warning is safe to ignore.

Test your index is working:

  time notmuch search from:marti.bolivar@nordicsemi.no

Select your email front-end client:

  all: https://notmuchmail.org/frontends/
  vim: https://github.com/felipec/notmuch-vim

Leave davmail running. Run 'mbsync nordic && notmuch new' periodically
to update your local index.

More docs:

  https://notmuchmail.org/
''')

if __name__ == '__main__':
    main()
