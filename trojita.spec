#define _disable_lto 1

# comment out when not a git snapshot
%define git 20200626
%define rel 3

Name:		trojita
Version:	0.7
Release:	2%{?git:1.git%git.}%{rel}
Group:		Networking/Mail
License:	GPLv2 or GPLv3
Summary:	Qt IMAP e-mail client
Url:		http://trojita.flaska.net
#Source0:        https://sourceforge.net/projects/trojita/files/src/%{name}-%{version}%{?git:-git%git}.tar.bz2
Source0:         https://invent.kde.org/pim/trojita/-/archive/master/trojita-master-20200626.tar.bz2

#Git taken from: https://invent.kde.org/pim/trojita

BuildRequires:	pkgconfig(zlib)
BuildRequires:	qmake5
BuildRequires:  cmake(KF5AkonadiContact)
#BuildRequires:  cmake(KF5Sonnet)
BuildRequires:  cmake(Gpgmepp)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5DBus)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Sql)
BuildRequires:	pkgconfig(Qt5WebKit)
BuildRequires:	pkgconfig(Qt5WebKitWidgets)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Test)
BuildRequires:	pkgconfig(Qt5Svg)
BuildRequires:	pkgconfig(Qt5Help)
BuildRequires:	cmake(Qt5Keychain)
BuildRequires:	qt5-linguist
BuildRequires:	qt5-linguist-tools
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	ragel
# For tests
BuildRequires:  x11-server-xvfb
Requires:	qt5-qtbase-database-plugin-sqlite

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
%setup -qn %{name}-master
%autopatch -p1
# Evil workaround for build failure
echo 'add_definitions(-fvisibility=default)' >>CMakeLists.txt

%cmake \
        -DWITH_TESTS=ON \
        -DWITH_QT5=ON \
        -DWITH_ZLIB=ON \
        -DWITH_RAGEL=ON \
        -DWITH_SHARED_PLUGINS=ON \
        -DWITH_QTKEYCHAIN_PLUGIN=ON

%build
%make_build -C build

%install
%make_install -C build

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
%{_datadir}/metainfo/org.kde.trojita.appdata.xml
%{_datadir}/applications/org.kde.trojita.desktop
%{_datadir}/icons/hicolor/*x*/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_libdir}/*.so
%{_libdir}/%{name}
