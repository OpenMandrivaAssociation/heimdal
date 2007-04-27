Name:		heimdal
Version:	0.8.1
Release:	%mkrel 1
Summary:	Heimdal implementation of Kerberos V5 system
License:	Free
Group:		Networking/Other
Source0:	ftp://ftp.pdc.kth.se/pub/heimdal/src/%{name}-%{version}.tar.bz2
Source1:	%{name}.init
#FIXME
#Source2:	%{name}.logrotate
#Source3:	%{name}.sysconfig
#Source4:	%{name}-krb5.conf
Source5:	%{name}-ftpd.xinetd
Source6:	%{name}-rshd.xinetd
Source7:	%{name}-telnetd.xinetd
Source8:    %{name}-kadmind.xinetd
Patch7:		heimdal-0.6.3-fix-readline-detection.patch
Patch8:		heimdal-0.7.2-fix-database-location.patch
URL:		http://www.pdc.kth.se/heimdal/
BuildRequires:	XFree86-devel
BuildRequires:	db-devel >= 4.1.25
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	libtool
BuildRequires:	ncurses-devel >= 5.3
BuildRoot:	    %{_tmppath}/%{name}-%{version}

%define		_libexecdir	%{_sbindir}
%define _fortify_cflags %nil

%description
Heimdal is a free implementation of Kerberos 5. The goals are to:
   - have an implementation that can be freely used by anyone
   - be protocol compatible with existing implementations and, if not in
     conflict, with RFC 1510 (and any future updated RFC)
   - be reasonably compatible with the M.I.T Kerberos V5 API
   - have support for Kerberos V5 over GSS-API (RFC1964)
   - include the most important and useful application programs (rsh,
     telnet, popper, etc.)
   - include enough backwards compatibility with Kerberos V4
   - IPv6 support

%package workstation
Summary:	Kerberos programs for use on workstations
Group:		Networking/Other
Requires:	%{name}-libs = %{version}-%{release}
Conflicts:  krb5-workstation
Conflicts:  openafs
Provides:   kerberos-workstation
Obsoletes:  %{name}

%description workstation
This package contains Kerberos 5 programs for use on workstations.

%package server
Summary:	Kerberos Server
Group:		System/Servers
Requires:	%{name}-libs = %{version}-%{release}
Requires(post):	/sbin/chkconfig
Requires(preun):/sbin/chkconfig
Conflicts:  krb5-server

%description server
This package contains the master KDC.

%package libs
Summary:	Heimdal shared libraries
Group:		System/Libraries

%description libs
This package contains shared libraries required by several of the other heimdal
packages.

%package login
Summary:	login is used when signing onto a system
Group:		Networking/Other
Requires:	%{name}-libs = %{version}-%{release}
Provides:	login

%description login
login is used when signing onto a system. It can also be used to
switch from one user to another at any time (most modern shells have
support for this feature built into them, however). This package
contain kerberized version login program.

%package ftp
Summary:	The standard UNIX FTP (file transfer protocol) client
Group:		Networking/Other
Requires:	%{name}-libs = %{version}-%{release}

%description ftp
The ftp package provides the standard UNIX command-line FTP client
with kerberos authentication support. FTP is the file transfer
protocol, which is a widely used Internet protocol for transferring
files and for archiving files.

%package rsh
Summary:	Clients for remote access commands (rsh, rlogin, rcp)
Group:		Networking/Other
Requires:	%{name}-libs = %{version}-%{release}

%description rsh
The rsh package contains a set of programs which allow users to run
commands on remote machines, login to other machines and copy files
between machines (rsh, rlogin and rcp). All three of these commands
use rhosts style authentication. This package contains the clients
needed for all of these services.

%package telnet
Summary:	Client for the telnet remote login
Group:		Networking/Other
Requires:	%{name}-libs = %{version}-%{release}

%description telnet
Telnet is a popular protocol for remote logins across the Internet.
This package provides a command line telnet client.

%package ftpd
Summary:	The standard UNIX FTP (file transfer protocol) server
Group:		System/Servers
Requires(pre):	xinetd
Requires:	    %{name}-libs = %{version}-%{release}
Conflicts:      ftp-server-krb5

%description ftpd
FTP is the file transfer protocol, which is a widely used Internet
protocol for transferring files and for archiving files.

%package rshd
Summary:	Server for remote access commands (rsh, rlogin, rcp)
Group:		System/Servers
Requires(pre):	xinetd
Requires:	    %{name}-libs = %{version}-%{release}

%description rshd
The rsh package contains a set of programs which allow users to run
commmands on remote machines, login to other machines and copy files
between machines (rsh, rlogin and rcp). All three of these commands
use rhosts style authentication. This package contains servers needed
for all of these services.

%package telnetd
Summary:	Server for the telnet remote login
Group:		System/Servers
Requires(pre):	xinetd
Requires:	    %{name}-libs = %{version}-%{release}
Conflicts:      telnet-server-krb5

%description telnetd
Telnet is a popular protocol for remote logins across the Internet.
This package provides a telnet daemon which allows remote logins into
the machine it is running on.

%package clients
Summary:	Kerberos programs for use on workstations
Group:		Networking/Other
Requires:	%{name}-libs = %{version}-%{release}

%description clients
Kerberos 5 Clients.

%package daemons
Summary:	Kerberos daemons programs for use on servers
Group:		System/Servers
Requires:	%{name}-libs = %{version}-%{release}

%description daemons
Kerberos Daemons.

%package devel
Summary:	Header files for heimdal
Group:		System/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
contains files needed to compile and link software using the kerberos
libraries.

%prep
%setup -q
%patch7 -p1 -b .readline
%patch8 -p1 -b .database
autoconf

%build
%configure2_5x \
	--sysconfdir=%{_sysconfdir}/%{name} \
	--localstatedir=%{_localstatedir}/%{name} \
	--disable-static \
	--enable-new-des3-code \
	--enable-shared \
	--with-readline \
    --with-readline-lib=%{_libdir} \
    --with-readline-include=%{_includedir}/readline \
	--with-x \
	--with-ipv6 \
	--with-openldap=%{_prefix}
%{__make}

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_localstatedir}/%{name}
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_sysconfdir}/xinetd.d
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}%{_initrddir}

%makeinstall_std

install appl/su/.libs/su %{buildroot}%{_bindir}/ksu
#install %{SOURCE4} %{buildroot}%{_sysconfdir}/krb5.conf

install -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
# FIXME install %{SOURCE2} %{buildroot}/etc/logrotate.d/%{name}
# FIXME install %{SOURCE3} %{buildroot}/etc/sysconfig/%{name}

install -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/xinetd.d/ftpd
install -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/xinetd.d/rshd
install -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/xinetd.d/telnetd
install -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/xinetd.d/kadmind

rm -rf	%{buildroot}%{_libdir}/lib{com_err,ss}.so \
%{buildroot}%{_includedir}/{glob,fnmatch,ss/ss}.h

chmod +r %{buildroot}%{_bindir}/otp   # qrde dlaczego to ma chmod 0

touch %{buildroot}%{_sysconfdir}/%{name}/krb5.keytab
touch %{buildroot}%{_localstatedir}/%{name}/kadmind.acl

# prevent some conflicts
mv %{buildroot}/%{_mandir}/man1/su.1 %{buildroot}/%{_mandir}/man1/ksu.1
mv %{buildroot}/%{_mandir}/cat1/su.1 %{buildroot}/%{_mandir}/cat1/ksu.1

%multiarch_binaries %{buildroot}/%{_bindir}/krb5-config

%clean
rm -rf %{buildroot}

%pre server
if [ -d %{_var}/%{name} ]; then
    mv %{_var}/%{name} %{_localstatedir}/%{name}
fi

%post server
%_post_service %{name}

%preun server
%_preun_service %{name}

%post ftpd
service xinetd condreload

%postun ftpd
service xinetd condreload

%post rshd
service xinetd condreload

%postun rshd
service xinetd condreload

%post telnetd
service xinetd condreload

%postun telnetd
service xinetd condreload

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig

%files server
%defattr(-,root,root)
%doc NEWS TODO
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/xinetd.d/kadmind
%dir %{_localstatedir}/%{name}
%config(noreplace) %{_localstatedir}/%{name}/kadmind.acl
%{_mandir}/man1/kimpersonate.1*
%{_mandir}/man8/iprop.8*
%{_mandir}/man8/iprop-log.8*
%{_mandir}/man8/kstash.8*
%{_mandir}/man8/hprop.8*
%{_mandir}/man8/hpropd.8*
%{_mandir}/man8/kadmind.8*
%{_mandir}/man8/kdc.8*
%{_mandir}/man8/kxd.8*
%{_mandir}/man8/kfd.8*
%{_mandir}/man8/kpasswdd.8*
%{_mandir}/man8/kcm.8*
%{_mandir}/cat8/kstash.8*
%{_mandir}/cat8/hprop.8*
%{_mandir}/cat8/hpropd.8*
%{_mandir}/cat8/kadmind.8*
%{_mandir}/cat8/kdc.8*
%{_mandir}/cat8/kxd.8*
%{_mandir}/cat8/kfd.8*
%{_mandir}/cat8/kpasswdd.8*
%{_mandir}/cat8/kcm.8*
%{_sbindir}/kstash
%{_sbindir}/hprop
%{_sbindir}/hpropd
%{_sbindir}/ipropd-master
%{_sbindir}/ipropd-slave
%{_sbindir}/kadmind
%{_sbindir}/kdc
%{_sbindir}/kxd
%{_sbindir}/kfd
%{_sbindir}/kpasswdd
%{_sbindir}/iprop-log
%{_sbindir}/kcm
%{_sbindir}/kdigest
%{_sbindir}/kimpersonate

%files libs
%defattr(-,root,root)
%dir %{_sysconfdir}/%{name}
%attr(400,root,root) %ghost %{_sysconfdir}/%{name}/krb5.keytab
%{_libdir}/lib*.so.*
%{_libdir}/windc*.so.*
%{_infodir}/heimdal.info*
%{_infodir}/hx509.info.*
%{_mandir}/man8/kerberos.8*
%{_mandir}/cat8/kerberos.8*

%files login
%defattr(-,root,root)
%{_bindir}/login
%{_mandir}/man1/login.1*
%{_mandir}/cat1/login.1*
%{_mandir}/man5/login.access.5*
%{_mandir}/cat5/login.access.5*

%files ftp
%defattr(-,root,root)
%{_bindir}/ftp
%{_mandir}/man1/ftp.1*
%{_mandir}/cat1/ftp.1*

%files rsh
%defattr(-,root,root)
%{_bindir}/rsh
%{_bindir}/rcp
%{_mandir}/man1/rsh.1*
%{_mandir}/cat1/rsh.1*

%files telnet
%defattr(-,root,root)
%{_bindir}/telnet
%{_mandir}/man1/telnet.1*
%{_mandir}/cat1/telnet.1*

%files ftpd
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/xinetd.d/ftpd
%{_sbindir}/ftpd
%{_mandir}/man5/ftpusers.5*
%{_mandir}/cat5/ftpusers.5*
%{_mandir}/man8/ftpd.8*
%{_mandir}/cat8/ftpd.8*

%files rshd
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/xinetd.d/rshd
%{_sbindir}/rshd
%{_mandir}/man8/rshd.8*
%{_mandir}/cat8/rshd.8*

%files telnetd
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/xinetd.d/telnetd
%{_sbindir}/telnetd
%{_mandir}/man8/telnetd.8*
%{_mandir}/cat8/telnetd.8*

%files workstation
%defattr(-,root,root)
%{_bindir}/afslog
%{_bindir}/kauth
%{_bindir}/kgetcred
%{_bindir}/kx
%{_bindir}/pfrom
%{_bindir}/rxtelnet
%{_bindir}/rxterm
%{_bindir}/string2key
%{_bindir}/tenletxr
%{_bindir}/otpprint
%{_bindir}/verify_krb5_conf
%{_bindir}/xnlock
%{_bindir}/kf
%{_bindir}/kdestroy
%{_bindir}/kinit
%{_bindir}/klist
%{_bindir}/kpasswd
%{_bindir}/pagsh
%{_bindir}/compile_et
%{_bindir}/gss
%{_bindir}/hxtool
%attr(4755,root,root) %{_bindir}/otp
%attr(4755,root,root) %{_bindir}/su
%attr(4755,root,root) %{_bindir}/ksu
%{_sbindir}/kadmin
%{_sbindir}/ktutil
%{_mandir}/man1/afslog.1*
%{_mandir}/man1/ksu.1*
%{_mandir}/man1/kauth.1*
%{_mandir}/man1/kdestroy.1*
%{_mandir}/man1/kgetcred.1*
%{_mandir}/man1/kinit.1*
%{_mandir}/man1/klist.1*
%{_mandir}/man1/kpasswd.1*
%{_mandir}/man1/pagsh.1*
%{_mandir}/man1/otp.1*
%{_mandir}/man1/otpprint.1*
%{_mandir}/man1/kf.1*
%{_mandir}/man1/kx.1*
%{_mandir}/man1/pfrom.1*
%{_mandir}/man1/rxtelnet.1*
%{_mandir}/man1/rxterm.1*
%{_mandir}/man1/tenletxr.1*
%{_mandir}/man1/xnlock.1*
%{_mandir}/cat1/afslog.1*
%{_mandir}/cat1/ksu.1*
%{_mandir}/cat1/kauth.1*
%{_mandir}/cat1/kinit.1*
%{_mandir}/cat1/kpasswd.1*
%{_mandir}/cat1/pagsh.1*
%{_mandir}/cat1/otp.1*
%{_mandir}/cat1/otpprint.1*
%{_mandir}/cat1/kf.1*
%{_mandir}/cat1/kx.1*
%{_mandir}/cat1/pfrom.1*
%{_mandir}/cat1/rxtelnet.1*
%{_mandir}/cat1/rxterm.1*
%{_mandir}/cat1/tenletxr.1*
%{_mandir}/cat1/xnlock.1*
%{_mandir}/man5/krb5.conf.5*
%{_mandir}/cat5/krb5.conf.5*
%{_mandir}/man8/verify_krb5_conf.8*
%{_mandir}/man8/string2key.8*
%{_mandir}/man8/kadmin.8*
%{_mandir}/man8/ktutil.8*
%{_mandir}/cat8/string2key.8*
%{_mandir}/cat8/kadmin.8*
%{_mandir}/cat8/ktutil.8*

%files daemons
%defattr(-,root,root)
%{_sbindir}/popper
%{_sbindir}/push
%{_mandir}/man8/popper.8*
%{_mandir}/man8/push.8*
%{_mandir}/cat8/popper.8*
%{_mandir}/cat8/push.8*

%files devel
%defattr(-,root,root)
%_bindir/krb5-config
%multiarch_bindir/krb5-config
%{_bindir}/mk_cmds
%{_libdir}/lib*.la
%{_libdir}/lib*.so
%{_libdir}/windc.la
%{_libdir}/windc.so
%{_includedir}/*
%{_mandir}/man1/krb5-config.1*
%{_mandir}/cat1/krb5-config.1*
%{_mandir}/man3/*
%{_mandir}/cat3/*
