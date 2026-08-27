Name:           arrera-gnome-config
Version:        1.0.1
Release:        1%{?dist}
Summary:        Default GNOME configuration and tweaks for Arrera Linux
License:        GPL-3.0-or-later
URL:            https://arrera.org/
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

Requires:       dconf
Requires:       gnome-shell
Requires:       gnome-shell-extension-appindicator
Requires:       gnome-shell-extension-forge
Requires:       gnome-shell-extension-gpaste
Requires:       gnome-shell-extension-background-logo
Requires:       arrera-branding
Requires:       arrera-wallpapers

%description
Default GNOME desktop environment settings, window management preferences,
enabled extensions, and dconf local database for Arrera Linux.

%prep
%autosetup

%build
# Aucune compilation binaire requise

%install
rm -rf %{buildroot}

# Base de règles dconf locales uniquement
mkdir -p %{buildroot}%{_sysconfdir}/dconf/db/local.d
cp src/dconf/db/local.d/* %{buildroot}%{_sysconfdir}/dconf/db/local.d/

%post
if [ -x /usr/bin/dconf ]; then
    /usr/bin/dconf update &>/dev/null || :
fi

%postun
if [ -x /usr/bin/dconf ]; then
    /usr/bin/dconf update &>/dev/null || :
fi

%files
%license LICENSE
%config(noreplace) %{_sysconfdir}/dconf/db/local.d/*

%changelog
* Thu Aug 27 2026 Arrera Software <contact@arrera.org> - 1.0.1-1
- Remove /etc/dconf/profile/user to prevent file conflict with standard dconf package
