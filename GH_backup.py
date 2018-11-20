import os
import sys
import json
import time
import subprocess

import pycurl

def token(filename='token'):

    with open(filename, 'r') as f:
        aux = f.read().strip()

    return aux

def request(url, multipage=True):
    # Request information to GitHub API

    dump = []
    page = 1

    while True:
        c = pycurl.Curl()

        c.setopt(c.USERPWD, ':'.join([__user__, __token__]))
        c.setopt(c.URL, url + '&page=%d' %page if multipage else url)

        # Load the output as a JSON object
        aux = json.loads(c.perform_rb())

        c.close()
        page += 1

        dump.extend(aux)

        if not aux or not multipage:
            break

    return dump

if __name__ == '__main__':
    start = time.time()
    print 'Session started @ %s\n' % time.strftime('%a %d %b %Y - %H:%M')

    __user__ = sys.argv[1]
    __token__ = token(filename=sys.argv[2])

    repos = request('https://api.github.com/%s/repos?type=all' % sys.argv[3])

    for repo in repos:
        name = repo['name']

        msg = 'Working on %s repository' % name
        print msg
        print '=' * len(msg) + '\n'

        if os.path.exists(name): # Repository already cloned
            print '- Directory "%s/" already exists' % name

            cloned = False

        else: # Clone the repository
            print '- Directory "%s/" not found' % name
            print '- Cloning repository "%s"' % name

            subprocess.call(('git clone --mirror %s %s/.git'
                             % (repo['ssh_url'], name)).split(' '),
                            stdout=sys.stdout)
            cloned = True

        print '>>> Entering subdirectory "%s/"' % name
        os.chdir(name)

        if cloned:
            subprocess.call('git config --bool core.bare false'.split(' '),
                            stdout=sys.stdout)

        print '- Checking branches...'
        # Check remote branches
        branch_url = repo['branches_url'].split('{')[0]
        aux = request(branch_url, multipage=False)
        remote = set([n['name'] for n in aux])

        if not cloned:
            # Check local branches
            aux = subprocess.check_output('git branch'.split(' '))
            local = set([r.strip('* ') for r in aux.strip().split('\n')])

            common = remote & local
            local_only = local - remote
            remote_only = remote - local

            #print 'REMOTE:', remote
            #print 'LOCAL:', local
            #print 'COMMON:', common

            for branch in remote_only:
                print '- Found new branch in remote: %s' % branch
                subprocess.call(('git checkout --track origin/%s'
                                 % branch).split(' '), stdout=sys.stdout)

            for branch in local_only:
                print '- Local branch %s not in remote anymore' % branch
                a = raw_input('Do you want to delete local branch %s?\n'
                              % branch)

                if a.lower()[0] == 'y':
                    print '- Deleting branch %s' % branch
                    subprocess.call(('git branch -d %s' % branch).split(' '),
                                    stdout=sys.stdout)

                else:
                    print '- Branch %s is has been kept locally' % branch

        if cloned:
            common = remote

        # Always keep master last:
        common = list(common)
        common.remove(u'master')
        common.append(u'master')

        for branch in common:
            print '- Checking out branch %s' % branch
            subprocess.call(('git checkout %s' % branch).split(' '),
                            stdout=sys.stdout)
            if not cloned:
                print '- Pulling branch %s' % branch
                subprocess.call(('git pull origin %s' % branch).split(' '),
                                stdout=sys.stdout)

        print '<<< Leaving subdirectory "%s/"' % name
        os.chdir('..')
        print '\n'

    print 'Backed up %d repositories' % len(repos)
    print 'Time elapsed %d sec.' %(time.time() - start)
    msg = 'Backup finished!'
    print '\n' + msg
    print '=' * len(msg)
