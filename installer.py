"""Contains functionality related to downloading and installing files."""

import os
import platform
import subprocess
from urllib import request
from pathlib import Path

MC_VERSION = '1.19.4'

FABRIC_INSTALLER_URL = 'https://maven.fabricmc.net/net/fabricmc/fabric-installer/0.11.2/fabric-installer-0.11.2.jar'  # noqa
FABRIC_INSTALLER_FILE_NAME = 'fabric-installer.jar'

MODS = {
    'fabric-api-1.19.4.jar': 'https://cdn.modrinth.com/data/P7dR8mSH/versions/Pz1hLqTB/fabric-api-0.76.0%2B1.19.4.jar',  # noqa
    'voicechat-fabric-1.19.4.jar': 'https://cdn.modrinth.com/data/9eGKb6K1/versions/pBGz0fqU/voicechat-fabric-1.19.4-2.3.28.jar'  # noqa
}

MOD_FOLDERS = {
    'Windows': f'{Path.home()}/AppData/Roaming/.minecraft/mods',
    'Darwin': f'{Path.home()}/Library/Application Support/minecraft/mods',
    'Linux': f'{Path.home()}/.minecraft/mods'
}


def run() -> str:
    """Downloads and installs everything necessary to use the Minecraft server.

    This first downloads the Fabric installer and runs it. Then all of the
    required mods are downloaded into the mods folder.

    Returns:
        A message with information about the outcome of the installation.
    """

    try:
        # Insert "legitimate" headers into http requests to not get blocked.
        opener = request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        request.install_opener(opener)

        # Download the Fabric installer.
        request.urlretrieve(FABRIC_INSTALLER_URL, FABRIC_INSTALLER_FILE_NAME)

        # Run the Fabric installer.
        subprocess.check_output(
            f'java -jar {FABRIC_INSTALLER_FILE_NAME} '
            f'client -mcversion {MC_VERSION}',
            shell=True
        )

        # Get the mods folder and create it if necessary.
        mods_folder = MOD_FOLDERS[platform.system()]
        Path(mods_folder).mkdir(parents=True, exist_ok=True)

        # Download the mod files to the mods folder.
        for file_name, url in MODS.items():
            file_path = os.path.join(mods_folder, file_name)
            request.urlretrieve(url, file_path)
    except Exception as e:
        return str(e)

    return 'Success!'
