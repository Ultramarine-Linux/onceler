import sys
import pylorax.mount
import pylorax.buildstamp
import pylorax.creator as creator
import pylorax.base
import pylorax.cmdline
import os
import onceler.kickstart as patch
import subprocess


def build_iso(variant,variant_name,compose,iso_only=False):
    """Build the ISO image"""
    #flatten the kickstart file
    kickstart = variant['kickstart']
    os.system(f'ksflatten --config {kickstart} --output .tmp/onceler-output.ks')
    #patch the kickstart file
    patch.buildstamp(variant=variant_name,compose=compose,ks='.tmp/onceler-output.ks')
    cli_args = [
    '--ks', '.tmp/onceler-output.ks',
    '--no-virt',
    '--make-iso',
    '--macboot',
    '--project', f"\"{compose['project']}\"",
    '--releasever', compose['releasever'],
    '--logfile', 'logs/build.log',
    '--resultdir', 'build',
    '--compression', 'zstd'
    ]
    if iso_only:
        cli_args.append('--iso-only')
        cli_args.append(f'--output {variant_name}.iso')
    # now run the build
    cmd = f"sudo /usr/sbin/livemedia-creator {' '.join(cli_args)}"
    # run the command in a subprocess and capture the output
    proc = subprocess.run(cmd, shell=True, check=True)
    # now return the output
    # wait for the process to finish while returning the output
    return proc.stdout.decode('utf-8')
    #os.system(cmd)