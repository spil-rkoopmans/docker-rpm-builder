from __future__ import unicode_literals
import shutil
from unittest2 import TestCase
from drb.downloadsources import get_spec_with_resolved_macros, get_source_and_patches_urls, download_files
from tempfile import NamedTemporaryFile, mkdtemp
import os

TMUX_SPEC = """
Name:           tmux
Version:        1.6
Release:        3%{?dist}
Summary:        A terminal multiplexer

Group:          Applications/System
# Most of the source is ISC licensed; some of the files in compat/ are 2 and
# 3 clause BSD licensed.
License:        ISC and BSD
URL:            http://sourceforge.net/projects/tmux
Source0:        http://pkgs.fedoraproject.org/repo/%{rhel}/%{dist}/pkgs/tmux/tmux-%{version}.tar.gz/3e37db24aa596bf108a0442a81c845b3/tmux-1.6.tar.gz
BuildRequires:  ncurses-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
tmux is a "terminal multiplexer."  It enables a number of terminals (or
windows) to be accessed and controlled from a single terminal.  tmux is
intended to be a simple, modern, BSD-licensed alternative to programs such
as GNU Screen.

%prep
touch /tmp/sarcazzo_123
%setup -q

%build
%configure
make %{?_smp_mflags} LDFLAGS="%{optflags}"
"""

class TestMacroResolving(TestCase):
    def test_get_spec_with_resolved_macros(self):
        tmp = NamedTemporaryFile()
        tmp.write(TMUX_SPEC)
        tmp.flush()

        lines = get_spec_with_resolved_macros(tmp.name, "alanfranz/drb-epel-6-x86-64:latest")
        for line in lines:
            if line.startswith("Source0"):
                self.assertTrue("http://pkgs.fedoraproject.org/repo/6/.el6/pkgs/tmux/tmux-1.6.tar.gz/3e37db24aa596bf108a0442a81c845b3/tmux-1.6.tar.gz" in line)
                break
        else:
            self.fail("could not find source line")

    def test_get_source_and_patches_urls(self):
        lines = [
            "asd",
            "pippo",
            "forget",
            "Source: http://my.web.site/me.tar.gz",
            "Source37: https://your.web.site/you.tar.gz",
            "Source38: local.tar.gz",
            "Patch22: patch1.patch",
            "Patch: ftp://wonderful.world/my.patch",
            "",
            "%prep"
        ]
        out = get_source_and_patches_urls(lines)
        self.assertEquals(["http://my.web.site/me.tar.gz",
            "https://your.web.site/you.tar.gz",
            "ftp://wonderful.world/my.patch"],
                          out)

    def test_download_files(self):
        tmpdir = mkdtemp()
        try:
            download_files(["http://mirror.centos.org/centos/7.1.1503/os/x86_64/Packages/ElectricFence-2.2.2-39.el7.i686.rpm",
                        "http://mirror.centos.org/centos/7.1.1503/os/x86_64/Packages/GeoIP-devel-1.5.0-9.el7.x86_64.rpm"],
                       tmpdir)
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "ElectricFence-2.2.2-39.el7.i686.rpm")))
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "GeoIP-devel-1.5.0-9.el7.x86_64.rpm")))
        finally:
            shutil.rmtree(tmpdir)






