import json
import os
import subprocess
import toml

from .util import MockBuild
from .config import load_config


from .log import get_logger

logger = get_logger(__name__)


def remove_dir(path: str):
    logger.info(f"Removing {path}")
    return subprocess.run(["rm", "-rf", path])

class Onceler:
    def __init__(self):
        self.config = load_config()

        if not self.config["image"]:
            logger.fatal("No image configration found!")

        self.image = self.config["image"]

        # pretty print config
        logger.debug(json.dumps(self.config, indent=4))
        # variants is all the keys with variant-* in the name, then remove the variant-
        self.variants = [
            variant[len("variant-"):]
            for variant in self.config.keys()
            if variant.startswith("variant-")
        ]

        if self.variants == []:
            logger.fatal("No variants found!")
        logger.debug(self.variants)

        self.mock = MockBuild()

        # pre included command line arguments to reduce boilerplate
        self.cli_args = [
            "livemedia-creator",
            "--no-virt",
            "--project",
            self.image["project"] if "project" in self.image else "Onceler-Image",
            "--releasever",
            str(self.image["releasever"]),
            "--resultdir",
            "/var/tmp/lmc",
            "--logfile",
            "/var/tmp/lmc-logs/livemedia-out.log",
        ]
        self.mock.delete("/var/tmp/lmc/")
        if "compression" in self.image:
            self.cli_args.extend([
                "--compression",
                self.image["compression"]
            ])

    def check_variant(self, variant):
        if variant not in self.variants:
            raise Exception(f"Variant {variant} not found in config")

    def build(self, variant):
        try:
            self.check_variant(variant)
        except Exception as e:
            logger.fatal(e)
            return 1
        var = self.config[f"variant-{variant}"]
        ks_output = f"onceler-{variant}.ks"

        if not var["kickstart"]:
            logger.fatal("No kickstart file found!")
            return 1

        # if path not exists
        if not os.path.isfile(var["kickstart"]):
            logger.fatal(f"Kickstart file {var['kickstart']} not found!")
            return 1

        logger.info("Compiling kickstart file")
        if not os.path.isdir("build"):
            try:
                os.mkdir("build")
            except Exception as e:
                logger.fatal(e)
                return 1
        # KSFlatten is indeed written in Python, but it's some argparse shit, so we'll run the system call ourselves
        subprocess.run(["ksflatten", "-c", var["kickstart"], "-o", f"build/{ks_output}"])

        logger.info("Preparing mock build")
        logger.info("Adding kickstart file to chroot")
        self.mock.add_file(f"build/{ks_output}")

        args = self.cli_args.copy()
        match var["type"]:
            case "iso":
                logger.info(f"Building ISO for {variant}")
                args.extend([
                    "--make-iso",
                    "--iso-only",
                    "--ks",
                    f"/{ks_output}",
                    "--iso-only",
                    "--iso-name",
                    "onceler-build-{variant}.iso",
                ])
                self.mock.run(args)
                # remove folder if already exists
                if os.path.exists(f"build/image/{variant}"):
                    remove_dir(f"build/image/{variant}")
                self.mock.export_file(f"/var/tmp/lmc", f"build/image/{variant}")
            case "docker":
                logger.info(f"Building Docker image for {variant}")
                args.extend([
                    "--make-tar",
                    "--ks",
                    f"/{ks_output}",
                    "--image-name",
                    f"onceler-build-{variant}.tar.xz",
                ])
                self.mock.run(args)
                # remove folder if already exists
                if os.path.exists(f"build/image/{variant}"):
                    remove_dir(f"build/image/{variant}")
                self.mock.export_file(f"/var/tmp/lmc", f"build/image/{variant}")
            case "podman":
                logger.info(f"Building Podman image for {variant}")
                args.extend([
                    "--make-tar",
                    "--ks",
                    f"/{ks_output}",
                    "--image-name",
                    f"onceler-build-{variant}.tar.xz",
                ])
                self.mock.run(args)
                # remove folder if already exists
                if os.path.exists(f"build/image/{variant}"):
                    remove_dir(f"build/image/{variant}")
                self.mock.export_file(f"/var/tmp/lmc", f"build/image/{variant}")
            case _:
                logger.critical(f"Unknown or unsupported variant type {variant}")
                return 1