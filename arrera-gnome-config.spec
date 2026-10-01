Name:           arrera-gnome-config
Version:        2026.beta.1
Release:        3%{?dist}
Summary:        Default GNOME configuration and tweaks for Arrera Linux
License:        GPL-3.0-or-later
URL:            https://github.com/Arrera-Blue/arrera-gnome-config
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

%description
Default GNOME desktop environment settings, window management preferences,
enabled extensions, Firefox policies, and dconf local database for Arrera Linux.

# ==============================================================================
# Edition: Home
# ==============================================================================
%package home
Summary:        Default GNOME configuration for Arrera Linux Home
RemovePathPostfixes: .home

Requires:       dconf
Requires:       gnome-shell
Requires:       gnome-shell-extension-appindicator
Requires:       gnome-shell-extension-forge
Requires:       gnome-shell-extension-gpaste
Requires:       gnome-shell-extension-background-logo
Requires:       gnome-shell-extension-arrera-dock
Requires:       arrera-branding
Requires:       arrera-wallpapers

Provides:       %{name} = %{version}-%{release}
Conflicts:      %{name}-education
Conflicts:      %{name}-enterprise

%description home
Default GNOME desktop environment settings, window management preferences,
enabled extensions, Firefox policies, and dconf local database for Arrera Linux Home edition.

# ==============================================================================
# Edition: Education
# ==============================================================================
%package education
Summary:        Default GNOME configuration for Arrera Linux Education
RemovePathPostfixes: .education

Requires:       dconf
Requires:       gnome-shell
Requires:       gnome-shell-extension-appindicator
Requires:       gnome-shell-extension-forge
Requires:       gnome-shell-extension-gpaste
Requires:       gnome-shell-extension-background-logo
Requires:       gnome-shell-extension-arrera-dock
Requires:       arrera-branding
Requires:       arrera-wallpapers

Provides:       %{name} = %{version}-%{release}
Conflicts:      %{name}-home
Conflicts:      %{name}-enterprise

%description education
Default GNOME desktop environment settings, window management preferences,
enabled extensions, Firefox policies, and dconf local database for Arrera Linux Education edition.

# ==============================================================================
# Edition: Enterprise
# ==============================================================================
%package enterprise
Summary:        Default GNOME configuration for Arrera Linux Enterprise
RemovePathPostfixes: .enterprise

Requires:       dconf
Requires:       gnome-shell
Requires:       gnome-shell-extension-appindicator
Requires:       gnome-shell-extension-forge
Requires:       gnome-shell-extension-gpaste
Requires:       gnome-shell-extension-background-logo
Requires:       gnome-shell-extension-arrera-dock
Requires:       arrera-branding
Requires:       arrera-wallpapers

Provides:       %{name} = %{version}-%{release}
Conflicts:      %{name}-home
Conflicts:      %{name}-education

%description enterprise
Default GNOME desktop environment settings, window management preferences,
enabled extensions, Firefox policies, and dconf local database for Arrera Linux Enterprise edition.

%prep
%autosetup

%build
# Aucune compilation binaire requise

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/dconf/db/local.d
mkdir -p %{buildroot}%{_sysconfdir}/firefox/policies

for edition in home education enterprise; do
    # 1. Base de règles dconf locales
    for f in src/${edition}/dconf/db/local.d/*; do
        if [ -f "$f" ]; then
            fname=$(basename "$f")
            cp "$f" "%{buildroot}%{_sysconfdir}/dconf/db/local.d/${fname}.${edition}"
        fi
    done

    # 2. Politique Firefox par défaut
    if [ -f "src/${edition}/firefox/policies.json" ]; then
        cp "src/${edition}/firefox/policies.json" "%{buildroot}%{_sysconfdir}/firefox/policies/policies.json.${edition}"
    fi
done

%post home
if [ -x /usr/bin/dconf ]; then
    /usr/bin/dconf update &>/dev/null || :
fi
if [ -f %{_sysconfdir}/firefox/policies/policies.json ]; then
    for dist_dir in /usr/lib64/firefox/distribution /usr/lib/firefox/distribution; do
        if [ -d "$dist_dir" ]; then
            cp -f %{_sysconfdir}/firefox/policies/policies.json "$dist_dir/policies.json" 2>/dev/null || :
        fi
    done
fi

%postun home
if [ -x /usr/bin/dconf ]; then
    /usr/bin/dconf update &>/dev/null || :
fi

%post education
if [ -x /usr/bin/dconf ]; then
    /usr/bin/dconf update &>/dev/null || :
fi
if [ -f %{_sysconfdir}/firefox/policies/policies.json ]; then
    for dist_dir in /usr/lib64/firefox/distribution /usr/lib/firefox/distribution; do
        if [ -d "$dist_dir" ]; then
            cp -f %{_sysconfdir}/firefox/policies/policies.json "$dist_dir/policies.json" 2>/dev/null || :
        fi
    done
fi

%postun education
if [ -x /usr/bin/dconf ]; then
    /usr/bin/dconf update &>/dev/null || :
fi

%post enterprise
if [ -x /usr/bin/dconf ]; then
    /usr/bin/dconf update &>/dev/null || :
fi
if [ -f %{_sysconfdir}/firefox/policies/policies.json ]; then
    for dist_dir in /usr/lib64/firefox/distribution /usr/lib/firefox/distribution; do
        if [ -d "$dist_dir" ]; then
            cp -f %{_sysconfdir}/firefox/policies/policies.json "$dist_dir/policies.json" 2>/dev/null || :
        fi
    done
fi

%postun enterprise
if [ -x /usr/bin/dconf ]; then
    /usr/bin/dconf update &>/dev/null || :
fi

# ==============================================================================
# Files
# ==============================================================================
%files home
%license LICENSE
%config(noreplace) %{_sysconfdir}/dconf/db/local.d/*.home
%config(noreplace) %{_sysconfdir}/firefox/policies/policies.json.home

%files education
%license LICENSE
%config(noreplace) %{_sysconfdir}/dconf/db/local.d/*.education
%config(noreplace) %{_sysconfdir}/firefox/policies/policies.json.education

%files enterprise
%license LICENSE
%config(noreplace) %{_sysconfdir}/dconf/db/local.d/*.enterprise
%config(noreplace) %{_sysconfdir}/firefox/policies/policies.json.enterprise

%changelog
* Thu Oct 01 2026 Arrera Software <contact@arrera.org> - 2026.beta.1-3
- Split package into 3 edition subpackages: home, education, enterprise

* Sat Sep 19 2026 Arrera Software <contact@arrera.org> - 2026.beta.1-2
- Add clean default Firefox policy in /etc/firefox/policies/policies.json

* Sun Sep 06 2026 Arrera Software <contact@arrera.org> - 1.0.2-1
- Add gnome-shell-extension-arrera-dock to default enabled extensions

* Thu Aug 27 2026 Arrera Software <contact@arrera.org> - 1.0.1-1
- Remove /etc/dconf/profile/user to prevent file conflict with standard dconf package
