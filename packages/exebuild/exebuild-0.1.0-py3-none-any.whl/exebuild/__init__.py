# -*- coding: utf-8 -*-
# Copyright (c) 2024 IKUS Software
#
# This software is licensed under the MIT License.
# See the LICENSE file for more details.
import json
import os
import shutil
import subprocess
import tempfile

import requests

# Let define environment variable for some constants.
nuget_url = os.getenv("EXEBUILD_NUGET_URL", "https://dist.nuget.org/win-x86-commandline/latest/nuget.exe")


def get_env_var(var_name):
    value = os.getenv(var_name)
    if not value:
        raise EnvironmentError(f"Environment variable {var_name} is not set or is empty")
    return value


def check_donet_runtime():
    """Verify if dotnet runtime 6 is available."""
    dotnet_exe = shutil.which('dotnet.exe')
    if not dotnet_exe:
        path = os.environ.get("PATH", None)
        raise FileNotFoundError(
            f'Fail to find "dotnet.exe". Make sure to install ".NET Runtime 6.0" and verify you PATH environment variable: {path}'
        )
    output = subprocess.check_output(['dotnet.exe', '--list-runtimes'], text=1)
    if 'Microsoft.NETCore.App 6.0' not in output:
        raise FileNotFoundError(f'.NET Runtime 6.0 is not installed. Following runtime was found: {output}')


def find_or_download_nuget(dest):
    """Search for nuget on the path or download nuget.exe file from the web."""
    # Check if nuget.exe could be found in PATH
    nuget = shutil.which('nuget.exe')
    if nuget:
        return nuget
    try:
        # Otherwise, download it from our url
        nuget = os.path.join(dest, "nuget.exe")
        response = requests.get(nuget_url)
        response.raise_for_status()
        with open(nuget, 'wb') as file:
            file.write(response.content)
        print(f"Found nuget.exe at {nuget}")
        return nuget
    except Exception:
        raise FileNotFoundError("Failed find or download nuget.exe")


def nuget_install(nuget_exe, package, version, dest):
    try:
        subprocess.check_call([nuget_exe, "install", package, "-Version", version], cwd=dest)
    except Exception:
        raise RuntimeError(f"Failed to install dependencies {package} version {version}")


def signexe(exe_path):
    # Make sure we are on Windows
    if os.name != "nt":
        raise EnvironmentError('exebuild only work on Windows platform')

    # Check if the executable exists
    if not os.path.isfile(exe_path):
        raise FileNotFoundError(exe_path)

    check_donet_runtime()

    # Let work in a temporary location to avoid poluting current working directory
    with tempfile.TemporaryDirectory(prefix='exebuild-signexe-') as temp_dir:
        # Check if required environment variable are defined
        get_env_var('AZURE_TENANT_ID')
        get_env_var('AZURE_CLIENT_ID')
        get_env_var('AZURE_CLIENT_SECRET')
        metadata = {
            "Endpoint": get_env_var('AZURE_ENDPOINT'),
            "CodeSigningAccountName": get_env_var('AZURE_CODE_SIGNING_NAME'),
            "CertificateProfileName": get_env_var('AZURE_CERT_PROFILE_NAME'),
        }

        # First we need to get "nuget.exe"
        nuget_exe = find_or_download_nuget(dest=temp_dir)

        # Let install our dependencies
        nuget_install(nuget_exe, package="Microsoft.Windows.SDK.BuildTools", version="10.0.26100.1742", dest=temp_dir)
        nuget_install(nuget_exe, package="Microsoft.Trusted.Signing.Client", version="1.0.60", dest=temp_dir)

        # Get location required for our command line.
        signtool_exe = os.path.join(
            temp_dir, "Microsoft.Windows.SDK.BuildTools.10.0.26100.1742/bin/10.0.26100.0/x64/signtool.exe"
        )
        if not os.path.exists(signtool_exe):
            raise FileNotFoundError(signtool_exe)
        dlib_dll = os.path.join(temp_dir, "Microsoft.Trusted.Signing.Client.1.0.60/bin/x64/Azure.CodeSigning.Dlib.dll")
        if not os.path.exists(dlib_dll):
            raise FileNotFoundError(dlib_dll)

        # Create metadata.json
        metdata_json = os.path.join(temp_dir, 'metadata.json')
        with open(metdata_json, "w") as f:
            json.dump(metadata, f, indent=4)

        # Sign executable using signtool
        try:
            proc = subprocess.run(
                [
                    signtool_exe,
                    'sign',
                    '/v',
                    '/debug',
                    '/fd',
                    'SHA256',
                    '/tr',
                    'http://timestamp.digicert.com',
                    '/td',
                    'SHA256',
                    '/dlib',
                    dlib_dll,
                    '/dmdf',
                    metdata_json,
                    exe_path,
                ],
                stderr=subprocess.STDOUT,
            )
            print(proc.stdout)
        except subprocess.CalledProcessError as e:
            if 'Status: 403 (Forbidden)' in e.stdout:
                raise RuntimeError(
                    'Failed to sign executable: Access Forbidden. Make you your Client ID, Client Secret is valid. Make sure your App Ressource has the role Trusted Signing Certificate Profile Signer assigned.'
                )


def makensis(cmd, *args, **kwargs):
    # Make sure we are on Windows
    if os.name != "nt":
        raise EnvironmentError('exebuild only work on Windows platform')

    # Let work in a temporary location to avoid poluting current working directory
    with tempfile.TemporaryDirectory(prefix='exebuild-nsis-') as temp_dir:
        # First we need to get "nuget.exe"
        nuget_exe = find_or_download_nuget(dest=temp_dir)

        # Let install our dependencies
        nuget_install(nuget_exe, package="NSIS-Tool", version="3.10.0", dest=temp_dir)

        # Get path to makensis.exe
        makensis_exe = os.path.join(temp_dir, "NSIS-Tool.3.10.0/tools/makensis.exe")
        if not os.path.exists(makensis_exe):
            raise FileNotFoundError(makensis_exe)

        # Create the command
        cmd = [makensis_exe] + cmd
        p = subprocess.Popen(cmd, *args[1:], **kwargs)
        p.wait()
        if p.returncode != 0:
            raise subprocess.CalledProcessError(p.returncode, cmd)
