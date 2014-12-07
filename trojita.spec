Name:		trojita
Version:	0.4.1
Release:	2
Group:		Networking/Mail
License:	GPLv2 or GPLv3
Summary:	Qt IMAP e-mail client
Url:		http://trojita.flaska.net
Source0:	http://sourceforge.net/projects/trojita/files/src/%{name}-%{version}.tar.bz2

BuildRequires:	qt5-devel
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Sql)
BuildRequires:	pkgconfig(Qt5WebKit)
BuildRequires:	pkgconfig(Qt5WebKitWidgets)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	qt5-linguist
BuildRequires:	cmake
BuildRequires:	ninja

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

%cmake -DWITH_QT5:BOOL=ON

%build
%make -C build

%install
%makeinstall_std -C build

mkdir -p %{buildroot}%{_libdir}
for i in AbookAddressbook AppVersion Common DesktopGui Composer Imap MSA Streams qwwsmtpclient; do
	cp -a build/lib$i.so %{buildroot}%{_libdir}/
done

%files
%{_bindir}/%{name}
%{_bindir}/be.contacts
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/%{name}/locale/*.qm
%{_libdir}/*.so
