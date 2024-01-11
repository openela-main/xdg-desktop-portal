%global pipewire_version 0.2.90
%global geoclue_version 2.5.2
%global glib_version 2.68.3-5
%global low_memory_monitor_version 2.0

Name:    xdg-desktop-portal
Version: 1.12.4
Release: 1%{?dist}
Summary: Portal frontend service to flatpak

License: LGPLv2+
URL:     https://github.com/flatpak/xdg-desktop-portal/
Source0: https://github.com/flatpak/xdg-desktop-portal/releases/download/%{version}/%{name}-%{version}.tar.xz

BuildRequires: gcc
BuildRequires: make
BuildRequires: systemd-rpm-macros
BuildRequires: pkgconfig(flatpak)
BuildRequires: pkgconfig(fuse)
BuildRequires: pkgconfig(gio-unix-2.0) >= %{glib_version}
BuildRequires: pkgconfig(json-glib-1.0)
BuildRequires: pkgconfig(libgeoclue-2.0) >= %{geoclue_version}
BuildRequires: pkgconfig(libpipewire-0.3) >= %{pipewire_version}
BuildRequires: /usr/bin/xmlto

Requires:      dbus
# Required version for icon validator.
Recommends:    flatpak >= 1.2.0
Requires:      geoclue2 >= %{geoclue_version}
Requires:      glib2%{?_isa} >= %{glib_version}
Recommends:    pipewire >= %{pipewire_version}
Requires:      pipewire-libs%{?_isa} >= %{pipewire_version}
# Required for the document portal.
Requires:      /usr/bin/fusermount
# Required for the GMemoryMonitor GIO API
Requires:      low-memory-monitor >= %{low_memory_monitor_version}

# https://github.com/flatpak/xdg-desktop-portal/pull/613
Patch0: power-profiles-daemon-gnome-40-backport.patch

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
* Wed Apr 20 2022 Debarshi Ray <rishi@fedoraproject.org> - 1.12.4-1
- Update to 1.12.4
Resolves: #2068448, #2076812

* Mon Apr 04 2022 Debarshi Ray <rishi@fedoraproject.org> - 1.12.3-1
- Update to 1.12.3
Resolves: #2068448, #2069328

* Fri Mar 25 2022 Debarshi Ray <rishi@fedoraproject.org> - 1.12.2-1
- Update to 1.12.2
- Explicit library Requires should be arch-specific
Resolves: #2068448

* Tue Feb 08 2022 Debarshi Ray <rishi@fedoraproject.org> - 1.12.1-1
- Rebase to 1.12.1
Resolves: #2051488

* Tue Aug 24 2021 Bastien Nocera <bnocera@redhat.com> - 1.8.1-6
+ xdg-desktop-portal-1.8.1-6
- Add PowerProfileMonitor portal
- Resolves: rhbz#1994468

* Tue Aug 10 2021 Mohan Boddu <mboddu@redhat.com> - 1.8.1-5
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 1.8.1-4
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Thu Apr 15 2021 Tomas Popela <tpopela@redhat.com> - 1.8.1-3
- Drop PipeWire 0.2 requirement as Chrom[e|ium] 90 now depends on PipeWire 0.3
- Resolves: rhbz#1929237

* Wed Feb 17 2021 David King <amigadave@amigadave.com> - 1.8.1-2
- Drop unused fontconfig BuildRequires

* Wed Feb 17 2021 Kalev Lember <klember@redhat.com> - 1.8.1-1
- Update to 1.8.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Sep 14 2020 Kalev Lember <klember@redhat.com> - 1.8.0-1
- Update to 1.8.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 25 2020 Tomas Popela <tpopela@redhat.com> - 1.7.2-2
- Start to require pipewire0.2-libs so screen sharing works out of the box in Chrome and Chromium.

* Fri Apr 03 2020 David King <amigadave@amigadave.com> - 1.7.2-1
- Update to 1.7.2 (#1820660)

* Sat Mar 28 2020 Kalev Lember <klember@redhat.com> - 1.7.1-1
- Update to 1.7.1

* Sat Mar 14 2020 David King <amigadave@amigadave.com> - 1.7.0-1
- Update to 1.7.0 (#1813534)

* Tue Mar 10 2020 Kalev Lember <klember@redhat.com> - 1.6.0-4
- Backport PipeWire 0.3 support

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 03 2020 Bastien Nocera <bnocera@redhat.com> - 1.6.0-2
+ xdg-desktop-portal-1.6.0-2
- Add requires to implement GMemoryMonitor

* Fri Dec 20 2019 David King <amigadave@amigadave.com> - 1.6.0-1
- Update to 1.6.0

* Thu Dec 12 2019 David King <amigadave@amigadave.com> - 1.5.4-1
- Update to 1.5.4

* Thu Nov 28 2019 David King <amigadave@amigadave.com> - 1.5.3-1
- Update to 1.5.3

* Tue Oct 29 2019 David King <amigadave@amigadave.com> - 1.5.2-1
- Update to 1.5.2 (#1766780)

* Tue Oct 22 2019 David King <amigadave@amigadave.com> - 1.5.1-1
- Update to 1.5.1 (#1714704)

* Fri Oct 04 2019 David King <amigadave@amigadave.com> - 1.5.0-1
- Update to 1.5.0

* Mon Sep 16 2019 Kalev Lember <klember@redhat.com> - 1.4.2-3
- Avoid a hard dep on pipewire daemon

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 28 2019 Kalev Lember <klember@redhat.com> - 1.4.2-1
- Update to 1.4.2

* Thu Feb 14 2019 David King <amigadave@amigadave.com> - 1.2.0-3
- Drop icon validator Requires to Recommends

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 26 2019 David King <amigadave@amigadave.com> - 1.2.0-1
- Update to 1.2.0 (#1669552)

* Wed Jan 16 2019 Kalev Lember <klember@redhat.com> - 1.1.1-1
- Update to 1.1.1

* Tue Oct 09 2018 David King <amigadave@amigadave.com> - 1.0.3-1
- Update to 1.0.3

* Mon Sep 03 2018 David King <amigadave@amigadave.com> - 1.0.2-1
- Update to 1.0.2

* Mon Aug 20 2018 David King <amigadave@amigadave.com> - 1.0-1
- Update to 1.0

* Wed Aug 01 2018 Jan Grulich <jgrulich@redhat.com> - 0.99-2
- Rebuild PipeWire 0.2.2

* Tue Jul 24 2018 David King <amigadave@amigadave.com> - 0.99-1
- Update to 0.99

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

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
