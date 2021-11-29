# Kickstart file injection options
# should be run as functions to inject each Kickstart patch before composition
import os
import sys
import shutil
import pylorax.buildstamp

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