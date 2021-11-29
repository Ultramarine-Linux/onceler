import sys
import pylorax.mount
import pylorax.buildstamp
import pylorax.creator as creator
import pylorax.base
import pylorax.cmdline
import os

def build_iso(ks, variant,product,bugurl,version, final=False, iso_only=False):
    """Build the ISO image"""
    #flatten the kickstart file
    try:
        os.system(f"ksflatten --config {ks} --output onceler-output.ks")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(0)
    # create a buildstamp file
    pylorax.buildstamp.BuildStamp(
        product=product,
        version=version,
        bugurl=bugurl,
        isfinal=final,
        variant=variant,
        buildarch='x86_64',
    ).write('.buildstamp-tmp')
    # now append a post script to the kickstart file
    with open('onceler-output.ks', 'a') as f:
        # buildstamp = content of .buildstamp-tmp
        f.write('\n\n%post\n')
        # write a heredoc to the kickstart file
        f.write('cat << EOF > /.buildstamp\n')
        f.write(open('.buildstamp-tmp', 'r').read())
        f.write('EOF\n')
        f.write('%end\n')
    # now create the ISO image
    args = pylorax.cmdline.lmc_parser().parse_args([
        '--ks', 'onceler-output.ks',
        '--make-iso',
        '--project', product,
        '--releasever', version,
        '--resultdir', f'build/{variant}',
        '--no-virt',
    ])
    if iso_only:
        #append the --iso-only flag to the argparse
        print('ISO only flag is set, will not output the build tree')
        args.iso_only = True
        args.iso_name = f'{product}-{product}-{variant}.iso'
    compose = creator.run_creator(args)
    return compose