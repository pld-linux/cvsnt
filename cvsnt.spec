#
# Conditional build:
%bcond_without	kerberos		# build without krb5 support
#
# TODO:
# - commit -r BRANCH is rejected (contrary to manual)
#   you can commit new file to branch with this technique:
#    cvs add file.patch
#    cvs up -r BRANCH file.patch
#    cvs ci -m '- bleh' file.patch
#   or just install cvs client from cvsnt package.
# - the newline auto translation on text files should be disabled on .patch files (better for any!)
# - check server mode and default config
# - unpackaged:
#   /usr/lib/libcvsapi.la
#   /usr/lib/libcvsapi.so
#   /usr/lib/libcvstools.la
#   /usr/lib/libcvstools.so
#   /usr/lib/libmdnsclient.la
#   /usr/lib/libmdnsclient.so
Summary:	Concurrent Versioning System
Summary(pl.UTF-8):	Concurrent Versioning System
Name:		cvsnt
# http://www.cvsnt.org/archive/2.5_stable tell which version is stable
Version:	2.5.05.3744
Release:	13
License:	GPL v2+/LGPL v2+
Group:		Development/Version Control
Source0:	http://www.cvsnt.org/archive/%{name}-%{version}.tar.gz
# Source0-md5:	64aa0fc627893cc66182023b936260da
Source1:	%{name}.inetd
Source2:	%{name}-cvslockd.init
Source3:	%{name}.pam
Patch0:		%{name}-system-pcre.patch
Patch1:		%{name}-system-ntlm.patch
Patch2:		%{name}-build.patch
Patch3:		%{name}-nospam.patch
Patch4:		%{name}-fixes.patch
Patch5:		%{name}-gcc4.patch
Patch6:		format-security.patch
Patch7:		cxx.patch
Patch8:		openssl.patch
URL:		http://www.cvsnt.org/
BuildRequires:	autoconf >= 2.58
BuildRequires:	automake >= 1:1.7.9
BuildRequires:	docbook-style-xsl
BuildRequires:	avahi-compat-howl-devel
%{?with_kerberos:BuildRequires:	heimdal-devel}
BuildRequires:	libltdl-devel
BuildRequires:	libntlm-devel >= 0.3.6
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	mysql-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	pcre-devel
BuildRequires:	postgresql-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sqlite3-devel
BuildRequires:	unixODBC-devel
BuildRequires:	xmlto
BuildRequires:	zlib-devel
Requires(post):	/sbin/ldconfig
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
Requires:	%{name}-cvslockd = %{version}-%{release}
Requires:	rc-inetd
Provides:	group(cvs)
Provides:	user(cvs)
Obsoletes:	cvs-nserver-common
Obsoletes:	cvs-nserver-nserver
Obsoletes:	cvs-nserver-pserver

%description pserver
Config files for rc-inetd that are necessary to run CVS in pserver
mode.

%package cvslockd
Summary:	locking daemon
Group:		Development/Version Control

%description cvslockd
CVS locking daemon.

%package database-mysql
Summary:	MySQL Database support for CVSNT
Group:		Development/Version Control
Requires:	%{name} = %{version}-%{release}

%description database-mysql
MySQL Database support for CVSNT.

%package database-odbc
Summary:	ODBC support for CVSNT
Group:		Development/Version Control
Requires:	%{name} = %{version}-%{release}

%description database-odbc
ODBC support for CVSNT.

%package database-postgres
Summary:	PostgreSQL Database support for CVSNT
Group:		Development/Version Control
Requires:	%{name} = %{version}-%{release}

%description database-postgres
PostgreSQL Database support for CVSNT.

%package database-sqlite
Summary:	SQLite Database support for CVSNT
Group:		Development/Version Control
Requires:	%{name} = %{version}-%{release}

%description database-sqlite
SQLite Database support for CVSNT.

%package protocol-gserver
Summary:	gserver (Kerberos GSS) protocol support for CVSNT
Group:		Development/Version Control
Requires:	%{name} = %{version}-%{release}

%description protocol-gserver
gserver (Kerberos GSS) support for CVSNT.

%package protocol-sserver
Summary:	sserver (SSL) procotol support for for CVSNT
Group:		Development/Version Control
Requires:	%{name} = %{version}-%{release}

%description protocol-sserver
sserver (SSL) protocol support for CVSNT.

%package protocol-sspi
Summary:	SSPI procotol support for for CVSNT
Group:		Development/Version Control
Requires:	%{name} = %{version}-%{release}

%description protocol-sspi
SSPI protocol support for CVSNT.

%package protocol-sync
Summary:	sync procotol support for for CVSNT
Group:		Development/Version Control
Requires:	%{name} = %{version}-%{release}

%description protocol-sync
sync protocol support for CVSNT.

%package rcs
Summary:	CVSNT version of RCS tools
Group:		Development/Version Control
Requires:	%{name} = %{version}-%{release}
Provides:	rcs

%description rcs
CVSNT version of RCS tools.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

rm -r protocols/ntlm

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
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
	--%{?with_kerberos:en}%{!?with_kerberos:dis}able-gserver \
	--enable-sserver \
	--enable-sspi \
	--enable-enum \
	--enable-rcs

%{__make}

cd doc
sed "s/__VERSION__/%{version}/" < cvs.dbk > cvs2.dbk
sed "s/__VERSION__/%{version}/" < cvsclient.dbk > cvsclient2.dbk
xmlto --skip-validation -o html_cvs html cvs2.dbk
xmlto --skip-validation -o html_cvsclient html cvsclient2.dbk

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{pam.d,rc.d/init.d,sysconfig/rc-inetd},%{_cvs_root}}

%{__make} install -j1 \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/cvslockd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/cvsnt

mv $RPM_BUILD_ROOT%{_sysconfdir}/cvsnt/PServer{.example,}
mv $RPM_BUILD_ROOT%{_sysconfdir}/cvsnt/Plugins{.example,}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post cvslockd
/sbin/chkconfig --add cvslockd
%service cvslockd restart

%preun cvslockd
if [ "$1" = "0" ]; then
	%service cvslockd stop
	/sbin/chkconfig --del cvslockd
fi

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

%files
%defattr(644,root,root,755)
%doc doc/html_cvsclient
%doc AUTHORS README
%doc triggers/examples/*.txt
%dir %{_sysconfdir}/cvsnt
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/cvsnt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cvsnt/*
%attr(755,root,root) %{_bindir}/cvs
%attr(755,root,root) %{_bindir}/cvsnt
%attr(755,root,root) %{_bindir}/cvsscript
%dir %{_libdir}/cvsnt
%dir %{_libdir}/cvsnt/database
%dir %{_libdir}/cvsnt/mdns
%attr(755,root,root) %{_libdir}/cvsnt/mdns/*.so
%{_libdir}/cvsnt/mdns/*.la
%dir %{_libdir}/cvsnt/protocols
%attr(755,root,root) %{_libdir}/cvsnt/protocols/enum.so
%attr(755,root,root) %{_libdir}/cvsnt/protocols/ext.so
%attr(755,root,root) %{_libdir}/cvsnt/protocols/pserver.so
%attr(755,root,root) %{_libdir}/cvsnt/protocols/server.so
%{_libdir}/cvsnt/protocols/enum.la
%{_libdir}/cvsnt/protocols/ext.la
%{_libdir}/cvsnt/protocols/pserver.la
%{_libdir}/cvsnt/protocols/server.la
%dir %{_libdir}/cvsnt/triggers
%attr(755,root,root) %{_libdir}/cvsnt/triggers/*.so
%{_libdir}/cvsnt/triggers/*.la
%dir %{_libdir}/cvsnt/xdiff
%attr(755,root,root) %{_libdir}/cvsnt/xdiff/*.so
%{_libdir}/cvsnt/xdiff/*.la
%attr(755,root,root) %{_libdir}/lib*-*.so*
%{_mandir}/man[15]/*

%files pserver
%defattr(644,root,root,755)
%doc doc/html_cvs
%attr(770,root,cvs) %dir %{_cvs_root}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/cvsnt

%files cvslockd
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cvslockd
%attr(754,root,root) /etc/rc.d/init.d/cvslockd

%files database-mysql
%defattr(644,root,root,755)
%doc triggers/sql/*_mysql.sql
%attr(755,root,root) %{_libdir}/cvsnt/database/mysql.so
%{_libdir}/cvsnt/database/mysql.la

%files database-odbc
%defattr(644,root,root,755)
%doc triggers/sql/*_oracle.sql
%doc triggers/sql/*_mssql.sql
%attr(755,root,root) %{_libdir}/cvsnt/database/odbc.so
%{_libdir}/cvsnt/database/odbc.la

%files database-postgres
%defattr(644,root,root,755)
%doc triggers/sql/*_postgres.sql
%attr(755,root,root) %{_libdir}/cvsnt/database/postgres.so
%{_libdir}/cvsnt/database/postgres.la

%files database-sqlite
%defattr(644,root,root,755)
%doc triggers/sql/*_sqlite.sql
%attr(755,root,root) %{_libdir}/cvsnt/database/sqlite.so
%{_libdir}/cvsnt/database/sqlite.la

%if %{with kerberos}
%files protocol-gserver
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/cvsnt/protocols/gserver.so
%{_libdir}/cvsnt/protocols/gserver.la
%endif

%files protocol-sserver
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/cvsnt/protocols/sserver.so
%{_libdir}/cvsnt/protocols/sserver.la

%files protocol-sspi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/cvsnt/protocols/sspi.so
%{_libdir}/cvsnt/protocols/sspi.la

#%files protocol-sync
#%defattr(644,root,root,755)
#%attr(755,root,root) %{_libdir}/cvsnt/protocols/sync.so
#%{_libdir}/cvsnt/protocols/sync.la

%files rcs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/co
%attr(755,root,root) %{_bindir}/rcsdiff
%attr(755,root,root) %{_bindir}/rlog
