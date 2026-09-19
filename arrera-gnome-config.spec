Name:           arrera-gnome-config
Version:        2026.beta.1
Release:        2%{?dist}
Summary:        Default GNOME configuration and tweaks for Arrera Linux
License:        GPL-3.0-or-later
URL:            https://github.com/Arrera-Blue/arrera-gnome-config
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

Requires:       dconf
Requires:       gnome-shell
Requires:       gnome-shell-extension-appindicator
Requires:       gnome-shell-extension-forge
Requires:       gnome-shell-extension-gpaste
Requires:       gnome-shell-extension-background-logo
Requires:       gnome-shell-extension-arrera-dock
Requires:       arrera-branding
Requires:       arrera-wallpapers

%description
Default GNOME desktop environment settings, window management preferences,
enabled extensions, Firefox policies, and dconf local database for Arrera Linux.

%prep
%autosetup

%build
# Aucune compilation binaire requise

%install
rm -rf %{buildroot}

# 1. Base de règles dconf locales
mkdir -p %{buildroot}%{_sysconfdir}/dconf/db/local.d
cp src/dconf/db/local.d/* %{buildroot}%{_sysconfdir}/dconf/db/local.d/

# 2. Politique Firefox par défaut
mkdir -p %{buildroot}%{_sysconfdir}/firefox/policies
cp src/firefox/policies.json %{buildroot}%{_sysconfdir}/firefox/policies/policies.json

%post
if [ -x /usr/bin/dconf ]; then
    /usr/bin/dconf update &>/dev/null || :
fi

# Déploiement de secours dans les répertoires de distribution Firefox si présents
if [ -f %{_sysconfdir}/firefox/policies/policies.json ]; then
    for dist_dir in /usr/lib64/firefox/distribution /usr/lib/firefox/distribution; do
        if [ -d "$dist_dir" ]; then
            cp -f %{_sysconfdir}/firefox/policies/policies.json "$dist_dir/policies.json" 2>/dev/null || :
        fi
    done
fi

%postun
if [ -x /usr/bin/dconf ]; then
    /usr/bin/dconf update &>/dev/null || :
fi

%files
%license LICENSE
%config(noreplace) %{_sysconfdir}/dconf/db/local.d/*
%config(noreplace) %{_sysconfdir}/firefox/policies/policies.json

%changelog
* Sat Sep 19 2026 Arrera Software <contact@arrera.org> - 2026.beta.1-2
- Add clean default Firefox policy in /etc/firefox/policies/policies.json

* Sun Sep 06 2026 Arrera Software <contact@arrera.org> - 1.0.2-1
- Add gnome-shell-extension-arrera-dock to default enabled extensions

* Thu Aug 27 2026 Arrera Software <contact@arrera.org> - 1.0.1-1
- Remove /etc/dconf/profile/user to prevent file conflict with standard dconf package
