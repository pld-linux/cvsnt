# TODO:
# - check server mode
# - verify when cvslockd is needed (in main or in pserver package)
Summary:	Concurrent Versioning System
Summary(pl.UTF-8):	Concurrent Versioning System
Name:		cvsnt
Version:	2.5.03.2382
Release:	0.1
License:	GPL v2+/LGPL v2+
Group:		Development/Version Control
Source0:	http://unifacecm.de/archive/%{name}-%{version}.tar.gz
# Source0-md5:	4f7d2e54c5529829a43b089f9b37c86e
Source1:	%{name}.inetd
Source2:	%{name}-cvslockd.init
URL:		http://www.cvsnt.org/
BuildRequires:	autoconf >= 2.58
BuildRequires:	automake >= 1:1.7.9
BuildRequires:	avahi-compat-libdns_sd-devel
BuildRequires:	docbook-style-xsl
BuildRequires:	expat-devel
BuildRequires:	krb5-devel
BuildRequires:	libstdc++-devel
BuildRequires:	mysql-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	pcre-devel
BuildRequires:	postgresql-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sqlite3-devel
BuildRequires:	texinfo
BuildRequires:	unixODBC-devel
BuildRequires:	xmlto
BuildRequires:	zlib-devel
Provides:	cvs-client = %{version}
Obsoletes:	cvs-client
Obsoletes:	cvs-nserver-client
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_cvs_root	/var/lib/cvs

%description
CVS means Concurrent Version System; it is a version control system
which can record the history of your files (usually, but not always,
source code). CVS only stores the differences between versions,
instead of every version of every file you've ever created. CVS also
keeps a log of who and when made some changes and why they occurred,
among other aspects.

CVSNT Server features include:
- Access control for securing projects and branches.
- Detailed audit and metrics recorded in an SQL database.
- Authentication with Active Directory.
- Tracking everything about the change - including whether it was
  merged from somewhere, belongs to a problem report or was part of a
  change set.
- A control panel to manage email notification of changes, defect
  tracking integration, and more.
- Integrated repository synchronisation (for fail-over servers).
- Change set support (group changes by defect number).
- Supports UNICODE UTF-8/UCS-2 files and multi-lingual filenames.
- When operating in UTF-8 (Unicode) mode it can automatically
  translate filename encoding for any client.
- Plug-ins for email notification.
- Helps make merging branches easier with its "Mergepoint" feature.
- Native servers available for Mac OS X, Windows, Linux, Solaris,
  HPUX.
- Supports reserved and unreserved versioning methodologies.
- CVSAPI for integration into 3rd party products.
- Script, COM and 3GL interface for triggers and integration into 3rd
  party tools (such as defect tracking)

%package pserver
Summary:	rc-inetd config files to run CVS pserver
Summary(pl.UTF-8):	Pliki konfiguracyjne rc-inetd do postawienia pservera CVS
Group:		Development/Version Control
Requires(post):	fileutils
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name} = %{version}-%{release}
Requires:	rc-inetd
Provides:	group(cvs)
Provides:	user(cvs)
Obsoletes:	cvs-nserver-common
Obsoletes:	cvs-nserver-nserver
Obsoletes:	cvs-nserver-pserver

%description pserver
Config files for rc-inetd that are necessary to run CVS in pserver
mode.

%prep
%setup -q

%build
%configure \
	--enable-mdns \
	--enable-sqlite \
	--enable-mysql \
	--enable-odbc \
	--enable-postgres \
	--enable-pam \
	--enable-server \
	--enable-lockserver \
	--enable-pserver \
	--enable-ext \
	--enable-rsh \
	--enable-gserver \
	--enable-sserver \
	--enable-sspi \
	--enable-enum \
	--disable-rcs

%{__make}

cd doc
sed "s/__VERSION__/%{version}/" < cvs.dbk > cvs2.dbk
sed "s/__VERSION__/%{version}/" < cvsclient.dbk > cvsclient2.dbk
xmlto --skip-validation -o html_cvs html cvs2.dbk
xmlto --skip-validation -o html_cvsclient html cvsclient2.dbk

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig/rc-inetd},%{_cvs_root}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/cvslockd

mv $RPM_BUILD_ROOT%{_sysconfdir}/cvsnt/PServer.example $RPM_BUILD_ROOT%{_sysconfdir}/cvsnt/PServer
mv $RPM_BUILD_ROOT%{_sysconfdir}/cvsnt/Plugins.example $RPM_BUILD_ROOT%{_sysconfdir}/cvsnt/Plugins

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%pre pserver
%groupadd -f -g 52 cvs
%useradd -g cvs -d %{_cvs_root} -u 52 -s /bin/false cvs

%post pserver
if [ "$1" = "1" ]; then
	# Initialise repository
	%{_bindir}/cvs -d :local:%{_cvs_root} init
	chown -R cvs:cvs %{_cvs_root}/CVSROOT
fi
%service -q rc-inetd reload

%postun pserver
if [ "$1" = "0" ]; then
	%userremove cvs
	%groupremove cvs
	%service -q rc-inetd reload
fi

%triggerpostun -- cvs-pserver < 1.1.13-1
echo "Warning: default cvsroot moved to %{_cvs_root}."
echo "Check your configration."

%files
%defattr(644,root,root,755)
%doc doc/html_cvsclient
%doc AUTHORS FAQ README
%dir %{_sysconfdir}/cvsnt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cvsnt/*
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/cvsnt
%dir %{_libdir}/cvsnt/*
%attr(755,root,root) %{_libdir}/cvsnt/*/*.so
%{_libdir}/cvsnt/*/*.la
%attr(755,root,root) %{_libdir}/lib*-*.so*
%{_mandir}/man[15]/*

%files pserver
%defattr(644,root,root,755)
%doc doc/html_cvs
%attr(770,root,cvs) %dir %{_cvs_root}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/cvsnt
%attr(754,root,root) /etc/rc.d/init.d/cvslockd
