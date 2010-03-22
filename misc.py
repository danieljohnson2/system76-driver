#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
## Installs Miscellaneous drivers

import os
import ubuntuversion
import jme_kernel_latest

WORKDIR = os.path.join(os.path.dirname(__file__), '.')
WIRELESS8187 = os.path.join(os.path.dirname(__file__), 'rtl8187B_linux_26.1052.0225.2009.release')
WIRELESS8187B = os.path.join(os.path.dirname(__file__), 'rtl8187B/rtl8187/')
JMEDIR = os.path.join(os.path.dirname(__file__), 'jme-1.0.5')

def piix():
    """Changes hard drive driver from ata_piix to piix"""

    a = os.popen('lsmod | grep ata_piix')
    try:
        ata_piix = a.readline().strip()
    finally:
        a.close()
    piix = ata_piix[0:8]
    
    if piix == "ata_piix":
        os.system("echo blacklist ata_piix | sudo tee -a /etc/modprobe.d/blacklist-ata")
        os.system("echo piix | sudo tee -a /etc/initramfs-tools/modules")
        os.system("sudo update-initramfs -u")
    else:
        return
    
def piix2():
    """Blacklist ata_piix and uses piix.  Required for the CDROM on
    Feisty Santa Rosa models.  Can render some models un-bootable.
    Test prior to applying to particular machines."""

    a = os.popen('lsmod | grep piix')
    try:
        ata_piix = a.readline().strip()
    finally:
        a.close()
    piix = ata_piix[0:4]
    
    if piix != "piix":
        os.system("echo blacklist ata_piix | sudo tee -a /etc/modprobe.d/blacklist-ata")
        os.system("echo piix | sudo tee -a /etc/initramfs-tools/modules")
        os.system("sudo update-initramfs -u")
    else:
        return
    
def linux_backports():
    """Install linux-backports-modules for the currently installed release"""
    
    os.system('sudo apt-get --assume-yes install linux-backports-modules-`lsb_release -c -s`')
    
def wireless8187b():
    
    version = ubuntuversion.release()
    
    """Install updated 8187b wireless driver"""
    if version == ('9.04'):
        # blacklist old rtl8187 driver
        os.system("sudo rm /etc/modprobe.d/rtl8187.conf")
        os.system("echo blacklist rtl8187 | sudo tee -a /etc/modprobe.d/rtl8187.conf")
    
        if os.path.exists(WIRELESS8187) == True:
            # Install kernel headers
            os.system("sudo apt-get --assume-yes install linux-headers-`uname -r`")
            # Configure and Install Driver
            os.chdir(WIRELESS8187)
            os.system("sudo make && sudo make install")
        elif os.path.exists(WIRELESS8187) == False:
            # Get the driver
            os.chdir(WORKDIR)
            os.system("sudo wget http://drivers76.com/drivers/laptops/star1/rtl8187B_linux_26.1052.0225.2009.release.tar.gz")
            os.system("tar -xf rtl8187B_linux_26.1052.0225.2009.release.tar.gz")
            # Install kernel headers
            os.system("sudo apt-get --assume-yes install linux-headers-`uname -r`")
            # Configure and Install Driver
            os.chdir(WIRELESS8187)
            os.system("sudo make && sudo make install")
    elif version == ('9.10'):
        # blacklist old rtl8187 driver
        os.system("sudo rm /etc/modprobe.d/rtl8187.conf")
        os.system("echo blacklist rtl8187 | sudo tee -a /etc/modprobe.d/rtl8187.conf")
        
        # Place files to run driver install after new headers install
        os.system('sudo cp /opt/system76/system76-driver/src/rtl8187b /etc/kernel/header_postinst.d/rtl8187b')
        os.system('sudo chmod +x /etc/kernel/header_postinst.d/rtl8187b')
    
        # Get the driver
        os.chdir(WORKDIR)
        os.system("sudo wget http://planet76.com/drivers/star1/rtl8187B.tar.gz")
        os.system("tar -xf rtl8187B.tar.gz")
        # Configure and Install Driver
        os.chdir(WIRELESS8187B)
        os.system("sudo make && sudo make install")
        os.chdir(WORKDIR)
        os.system('sudo rm -r rtl8187B.tar.gz rtl8187B/')
        
def jme_nic():
    """Install 1.0.5 jme driver - fixes 4GB mem lag"""
    
    # Place files to run driver install after new headers install
    os.system('sudo cp /opt/system76/system76-driver/src/jme /etc/kernel/header_postinst.d/jme')
    os.system('sudo chmod +x /etc/kernel/header_postinst.d/jme')
    
    # Install the driver
    if os.path.exists(JMEDIR) == True:
        # Install Driver
        jme_kernel_latest.makefile_kernel()
        os.chdir(JMEDIR)
        os.system("sudo make install")
    elif os.path.exists(JMEDIR) == False:
        # Extract the driver
        os.chdir(WORKDIR)
        os.system('sudo tar xf /opt/system76/system76-driver/src/jme-1.0.5.tar.gz')
        # Install Driver
        jme_kernel_latest.makefile_kernel()
        os.chdir(JMEDIR)
        os.system("sudo make install")
        
def rm_aticatalyst():
    """Remove Catalyst from the menu system (does not work well in Ubuntu 9.10)"""
    
    os.system('sudo rm /usr/share/applications/amdcccle.desktop /usr/share/applications/amdccclesu.desktop')
