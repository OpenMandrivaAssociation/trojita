%define _disable_lto 1

Name:		trojita
Version:	0.5
Release:	9
Group:		Networking/Mail
License:	GPLv2 or GPLv3
Summary:	Qt IMAP e-mail client
Url:		http://trojita.flaska.net
Source0:	http://sourceforge.net/projects/trojita/files/src/%{name}-%{version}.tar.bz2
Patch1:		trojita-0.5-fix_Qt5.5_build.patch

BuildRequires:	qmake5
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Sql)
BuildRequires:	pkgconfig(Qt5WebKit)
BuildRequires:	pkgconfig(Qt5WebKitWidgets)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Test)
BuildRequires:	cmake(Qt5Keychain)
BuildRequires:	qt5-linguist
BuildRequires:	qt5-linguist-tools
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	ragel
# For tests
BuildRequires:  x11-server-xvfb

%description
%{summary}

* A pure Qt application with no additional dependencies
* Robust IMAP core implemented using Qt's Model-View framework
* Standards compliance is a design goal
* Support for bandwidth-saving mode aimed at mobile users 
  with expensive connection
* IMAP over SSH -- in addition to usual SSL/TLS connections, 
  the server could be accessed via SSH
* On-demand body part loading
* Offline IMAP support (you can access data you already have; 
  there's no complete "offline mail access" yet, though)
* Safe dealing with HTML mail (actually more robust than Thunderbird's)

%prep
%setup -q
# Evil workaround for build failure
echo 'add_definitions(-fvisibility=default)' >>CMakeLists.txt
%apply_patches
%cmake \
        -DWITH_TESTS=ON \
        -DWITH_QT5=ON \
        -DWITH_ZLIB=ON \
        -DWITH_RAGEL=ON \
        -DWITH_SHARED_PLUGINS=ON

%build
%make -C build

%install
%makeinstall_std -C build

#mkdir -p %{buildroot}%{_libdir}
#for i in AbookAddressbook AppVersion Common DesktopGui Composer Imap MSA Streams qwwsmtpclient; do
#	cp -a build/lib$i.so %{buildroot}%{_libdir}/
#done

%check
%define X_display ":98"
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}${LD_LIBRARY_PATH:+:}%{buildroot}%{_libdir}"
export DISPLAY=%{X_display}
Xvfb %{X_display} &
trap "kill $! || true" EXIT
cd build
ctest --output-on-failure || echo "whoops"

%files
%{_bindir}/%{name}
%{_bindir}/be.contacts
%{_datadir}/appdata/*xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/%{name}/locale/*.qm
%{_libdir}/*.so
