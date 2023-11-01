%global pipewire_version 0.2.90
%global geoclue_version 2.5.2

Name:    xdg-desktop-portal
Version: 1.8.1
Release: 1%{?dist}
Summary: Portal frontend service to flatpak

License: LGPLv2+
URL:     https://github.com/flatpak/xdg-desktop-portal/
Source0: https://github.com/flatpak/xdg-desktop-portal/releases/download/%{version}/%{name}-%{version}.tar.xz

BuildRequires: make
BuildRequires: gcc
BuildRequires: pkgconfig(flatpak)
BuildRequires: pkgconfig(fuse)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(json-glib-1.0)
BuildRequires: pkgconfig(libgeoclue-2.0) >= %{geoclue_version}
BuildRequires: pkgconfig(libpipewire-0.3) >= %{pipewire_version}
BuildRequires: /usr/bin/xmlto
%{?systemd_requires}
BuildRequires: systemd

Requires:      dbus
# Required version for icon validator.
Recommends:    flatpak >= 1.2.0
Requires:      geoclue2 >= %{geoclue_version}
Recommends:    pipewire >= %{pipewire_version}
Requires:      pipewire-libs%{?_isa} >= %{pipewire_version}
# Required for the document portal.
Requires:      /usr/bin/fusermount

%description
xdg-desktop-portal works by exposing a series of D-Bus interfaces known as
portals under a well-known name (org.freedesktop.portal.Desktop) and object
path (/org/freedesktop/portal/desktop). The portal interfaces include APIs for
file access, opening URIs, printing and others.

%package  devel
Summary:  Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The pkg-config file for %{name}.


%prep
%autosetup -p1


%build
%configure --enable-docbook-docs --disable-libportal
%make_build


%install
%make_install
install -dm 755 %{buildroot}/%{_pkgdocdir}
install -pm 644 README.md %{buildroot}/%{_pkgdocdir}
# This directory is used by implementations such as xdg-desktop-portal-gtk.
install -dm 755 %{buildroot}/%{_datadir}/%{name}/portals

%find_lang %{name}


%post
%systemd_user_post %{name}.service
%systemd_user_post xdg-document-portal.service
%systemd_user_post xdg-permission-store.service


%preun
%systemd_user_preun %{name}.service
%systemd_user_preun xdg-document-portal.service
%systemd_user_preun xdg-permission-store.service


%files -f %{name}.lang
%doc %{_pkgdocdir}
%license COPYING
%{_datadir}/dbus-1/interfaces/org.freedesktop.portal.*.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.impl.portal.*.xml
%{_datadir}/dbus-1/services/org.freedesktop.portal.Desktop.service
%{_datadir}/dbus-1/services/org.freedesktop.portal.Documents.service
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.PermissionStore.service
%{_datadir}/%{name}
%{_libexecdir}/xdg-desktop-portal
%{_libexecdir}/xdg-document-portal
%{_libexecdir}/xdg-permission-store
%{_userunitdir}/%{name}.service
%{_userunitdir}/xdg-document-portal.service
%{_userunitdir}/xdg-permission-store.service

%files devel
%{_datadir}/pkgconfig/xdg-desktop-portal.pc


%changelog
* Tue Oct 12 2021 Tomas Popela <tpopela@redhat.com> - 1.8.1-1
- Rebase to 1.8.1
- Explicit library Requires should be arch-specific
Resolves: #2062430

* Tue Oct 12 2021 Tomas Popela <tpopela@redhat.com> - 1.6.0-6
- Rebuild to recover from broken binutils
  Resolves: #1954457

* Thu Apr 15 2021 Tomas Popela <tpopela@redhat.com> - 1.6.0-5
- Drop PipeWire 0.2 requirement as Chrom[e|ium] 90 now depends on PipeWire 0.3
- Resolves: rhbz#1949809

* Thu Feb 18 2021 Tomas Pelka <tpelka@redhat.com> - 1.6.0-4
- Bump version and rebuild due to z-stream release with the same version

* Fri Oct 09 2020 David King <dking@redhat.com> - 1.6.0-3
- Fix OpenURI crash (#1886025)

* Wed Jul 15 2020 Jonas Ådahl <jadahl@redhat.com> - 1.6.0-2
- Require pipewire0.2-libs for legacy application support.
  Resolves: #1854734

* Mon May 25 2020 Jonas Ådahl <jadahl@redhat.com> - 1.6.0-1
- Rebase to 1.6.0 (#1775345)
- Backport PipeWire 0.3 support (#1775345)
- Backport fixes (#1775345)

* Wed Oct 09 2019 David King <dking@redhat.com> - 1.4.2-1
- Rebase to 1.4.2 (#1748296)

* Tue Oct 09 2018 David King <amigadave@amigadave.com> - 1.0.3-1
- Update to 1.0.3

* Tue Sep 18 2018 Kalev Lember <klember@redhat.com> - 1.0.2-1
- Update to 1.0.2 (#1630249)

* Wed Aug 01 2018 Jan Grulich <jgrulich@redhat.com> - 0.99-2
- Rebuild PipeWire 0.2.2

* Tue Jul 31 2018 David King <dking@redhat.com> - 0.99-1
- Update to 0.99

* Wed Apr 25 2018 David King <amigadave@amigadave.com> - 0.11-1
- Update to 0.11 (#1545225)

* Wed Feb 14 2018 David King <amigadave@amigadave.com> - 0.10-1
- Update to 0.10 (#1545225)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Nov 19 2017 David King <amigadave@amigadave.com> - 0.9-1
- Update to 0.9 (#1514774)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 David King <amigadave@amigadave.com> - 0.8-1
- Update to 0.8 (#1458969)

* Fri Mar 31 2017 David King <amigadave@amigadave.com> - 0.6-1
- Update to 0.6

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 18 2017 David King <amigadave@amigadave.com> - 0.5-1
- Update to 0.5

* Thu Dec 01 2016 David King <amigadave@amigadave.com> - 0.4-1
- Update to 0.4

* Fri Sep 02 2016 David King <amigadave@amigadave.com> - 0.3-1
- Update to 0.3

* Fri Jul 29 2016 David King <amigadave@amigadave.com> - 0.2-1
- Update to 0.2 (#1361575)

* Tue Jul 12 2016 David King <amigadave@amigadave.com> - 0.1-2
- Own the portals directory

* Mon Jul 11 2016 David King <amigadave@amigadave.com> - 0.1-1
- Initial Fedora packaging
