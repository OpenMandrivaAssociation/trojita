Name:		trojita
Version:	0.3.93
Release:	7
Group:		Networking/Mail
License:	GPLv2 or GPLv3
Summary:	Qt IMAP e-mail client
Url:		http://trojita.flaska.net
Source0:	http://sourceforge.net/projects/trojita/files/src/%{name}-%{version}.tar.bz2

BuildRequires:	qt4-devel
BuildRequires:	pkgconfig(QtWebKit)
BuildRequires:	qt4-linguist

%description
%{summary}

* A pure Qt4 application with no additional dependencies
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

%build
%qmake_qt4 PREFIX=%{_prefix}
%make

%install
make INSTALL_ROOT=%{buildroot} install

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/%{name}/locale/*.qm
