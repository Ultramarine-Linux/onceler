# Kickstart file injection options
# should be run as functions to inject each Kickstart patch before composition
import os
import sys
import shutil
import pylorax.buildstamp
import configparser

# read the compose file again
parser = configparser.ConfigParser()
config = parser.read('onceler.cfg')


def buildstamp(variant,compose,ks):
    """
    Injects the buildstamp into the kickstart file

    Variant is a string of the variant name
    Compose is the compose section of the Onceler config
    ks is the kickstart file to inject the buildstamp into
    """
    # create a buildstamp file
    pylorax.buildstamp.BuildStamp(
        product=compose['project'],
        version=compose['releasever'],
        bugurl=compose['bugurl'],
        isfinal=compose['final'],
        variant=variant,
        buildarch='x86_64',
    ).write('/tmp/buildstamp-tmp')
    # now append a post script to the kickstart file
    with open(ks, 'a') as f:
        # buildstamp = content of .buildstamp-tmp
        f.write('\n\n%post\n')
        # write a heredoc to the kickstart file
        f.write('cat << EOF > /.buildstamp\n')
        f.write(open('/tmp/buildstamp-tmp', 'r').read())
        f.write('EOF\n')
        f.write('%end\n')
    # remove the temporary file
    os.remove('/tmp/buildstamp-tmp')


def apply_patches(variant_data,ks):
    """
    Reads the list of patches from the Onceler config and applies them to the
    kickstart file

    variant_data is a dictionary of the Onceler config
    ks is the kickstart file to inject the patches into
    """

    ### REPO PATCHES ###
    # This will through the sections of the Onceler config that start with repo-
    
    for section in parser.sections():
        if section.startswith('repo-'):
            # get the repo name
            repo = section.split('-')[1]
            # get the repo url
            # check if whether a url or a mirrorlist is specified
            if parser.has_option(section, 'url'):
                url = parser.get(section, 'url')
            elif parser.has_option(section, 'mirrorlist'):
                mirror = parser.get(section, 'mirrorlist')
            # now patch in the repos
            with open(ks, 'a') as f:
                f.write('\n\nrepo ')
                f.write(f'--name={repo} ')
                if url:
                    f.write(f'--baseurl={url} ')
                elif mirror:
                    f.write(f'--mirrorlist={mirror} ')
    ### END REPO PATCHES ###

    ### PATCHES ###
    patches = variant_data['patches']
    if not patches:
        return
    # check the list of patches
    for patch in patches:
        pass #TODO add patch injection, im getting distracted ADHD moment