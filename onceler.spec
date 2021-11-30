Name:           onceler
Version:        0.1.1
Release:        1%{?dist}
Summary:        A Lorax wrapper.

License:        MIT
Source0:        https://gitlab.ultramarine-linux.org/release-engineering/onceler/-/archive/main/onceler-main.tar.gz

BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
Requires:       python3-setuptools
Requires:       python3-typer
Requires:       python3-click-spinner
Requires:       pykickstart
Requires:       lorax

%description
The Onceler is a command line wrapper that turns long Live Media Creator (LMC) command line arguments into a simple, human readable config files, similar to the ones used by Pungi.

%prep
%autosetup -n onceler-main

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{python3_sitelib}
install onceler-build -m 755 %{buildroot}%{_bindir}/onceler
cp -rv onceler/ %{buildroot}%{python3_sitelib}

%files
%{_bindir}/onceler
%{python3_sitelib}/onceler

%changelog
* Mon Nov 29 2021 Cappy Ishihara <cappy@cappuchino.xyz>
- Init Commit
