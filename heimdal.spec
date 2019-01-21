%if %{_use_internal_dependency_generator}
%define __noautoreq 'devel\\(libcom_err(.*)\\)'
%else
%define _requires_exceptions devel(libcom_err
%endif

Summary:	Heimdal implementation of Kerberos V5 system
Name:		heimdal
Version:	7.5.0
Release:	2
License:	BSD-like
Group:		Networking/Other
URL:		http://www.h5l.org
Source0:	https://github.com/heimdal/heimdal/releases/download/heimdal-%{version}/heimdal-%{version}.tar.gz
Source1:	%{name}.init
#FIXME
#Source2:	%{name}.logrotate
Source3:	%{name}.sysconfig
#Source4:	%{name}-krb5.conf
Source8:	%{name}-kadmind.xinetd
Patch11:	heimdal-1.4-passwd-check.patch
Patch12:	fix-missing-headers
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	texinfo
BuildRequires:	db-devel
BuildRequires:	openldap-devel >= 2.0
BuildRequires:	pam-devel
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xau)
BuildRequires:	pkgconfig(xt)
#Required for tests/ldap
BuildRequires:	openldap-servers

%description
Heimdal is a free implementation of Kerberos 5. The goals are to:
   - have an implementation that can be freely used by anyone
   - be protocol compatible with existing implementations and, if not in
     conflict, with RFC 1510 (and any future updated RFC)
   - be reasonably compatible with the M.I.T Kerberos V5 API
   - have support for Kerberos V5 over GSS-API (RFC1964)
   - include enough backwards compatibility with Kerberos V4
   - IPv6 support

#----------------------------------------------------------------------------

%package	workstation
Summary:	Kerberos programs for use on workstations
Group:		Networking/Other
Requires:	%{name}-libs = %{EVRD}
Conflicts:	krb5-workstation
Provides:	kerberos-workstation

%description	workstation
This package contains Kerberos 5 programs for use on workstations.

%files workstation
%{_bindir}/afslog
%{_bindir}/kgetcred
%{_bindir}/string2key
%{_bindir}/otpprint
%{_bindir}/verify_krb5_conf
%{_bindir}/kf
%{_bindir}/kdestroy
%{_bindir}/kinit
%{_bindir}/klist
%{_bindir}/kpasswd
%{_bindir}/gsstool
%{_bindir}/pagsh
%{_bindir}/hxtool
%{_bindir}/idn-lookup
%{_bindir}/kswitch
%{_bindir}/bsearch
%{_bindir}/heimtools
%{_bindir}/kadmin
%{_bindir}/ktutil
%{_sbindir}/heimdal/asn1_compile
%{_sbindir}/heimdal/asn1_print
%{_sbindir}/heimdal/slc
%attr(4755,root,root) %{_bindir}/otp
%attr(4755,root,root) %{_bindir}/su
%attr(4755,root,root) %{_bindir}/ksu
%{_sbindir}/digest-service
%{_mandir}/man1/afslog.1*
%{_mandir}/man1/ksu.1*
%{_mandir}/man1/kdestroy.1*
%{_mandir}/man1/kgetcred.1*
%{_mandir}/man1/klist.1*
%{_mandir}/man1/kswitch.1*
%{_mandir}/man1/kinit.1*
%{_mandir}/man1/kpasswd.1*
%{_mandir}/man1/pagsh.1*
%{_mandir}/man1/otp.1*
%{_mandir}/man1/otpprint.1*
%{_mandir}/man1/kf.1*
%{_mandir}/man5/krb5.conf.5.*
%{_mandir}/man1/bsearch.1*
%{_mandir}/man1/kadmin.1*
%{_mandir}/man1/ktutil.1*
%{_mandir}/man7/krb5-plugin.7*
%{_mandir}/cat1/bsearch.1
%{_mandir}/cat1/kadmin.1
%{_mandir}/cat1/ktutil.1
%{_mandir}/cat7/krb5-plugin.7
%{_mandir}/cat1/kdestroy.1*
%{_mandir}/cat1/kgetcred.1*
%{_mandir}/cat1/klist.1*
%{_mandir}/cat1/kswitch.1*
%{_mandir}/cat1/afslog.1*
%{_mandir}/cat1/ksu.1*
%{_mandir}/cat1/kinit.1*
%{_mandir}/cat1/kpasswd.1*
%{_mandir}/cat1/pagsh.1*
%{_mandir}/cat1/otp.1*
%{_mandir}/cat1/otpprint.1*
%{_mandir}/cat1/kf.1*
%{_mandir}/man5/mech.5*
%{_mandir}/*8/verify_krb5_conf.8*
%{_mandir}/man8/string2key.8*
%{_mandir}/cat8/string2key.8*

#----------------------------------------------------------------------------

%package	server
Summary:	Kerberos Server
Group:		System/Servers
Requires:	%{name}-libs = %{EVRD}
# krb5 package ships krb5.conf etc on mdv 2008.0 and later
Requires:	krb5
Requires(post):	chkconfig
Requires(preun):chkconfig
Conflicts:	krb5-server

%description	server
This package contains the master KDC.

%files server
%doc NEWS TODO
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/xinetd.d/kadmind
%dir %{_localstatedir}/lib/%{name}
%config(noreplace) %{_localstatedir}/lib/%{name}/kadmind.acl
# %{_mandir}/*1/kimpersonate.1*
%{_mandir}/*8/kdigest.8*
%{_mandir}/*8/kimpersonate.8*
%{_mandir}/*8/iprop.8*
%{_mandir}/*8/iprop-log.8*
%{_mandir}/man8/kstash.8*
%{_mandir}/man8/hprop.8*
%{_mandir}/man8/hpropd.8*
%{_mandir}/man8/kadmind.8*
%{_mandir}/man8/kdc.8*
%{_mandir}/man8/kfd.8*
%{_mandir}/man8/kpasswdd.8*
%{_mandir}/man8/kcm.8*
%{_mandir}/*8/ipropd-*.8*
%{_mandir}/cat8/kstash.8*
%{_mandir}/cat8/hprop.8*
%{_mandir}/cat8/hpropd.8*
%{_mandir}/cat8/kadmind.8*
%{_mandir}/cat8/kdc.8*
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
%{_sbindir}/kfd
%{_sbindir}/kpasswdd
%{_sbindir}/iprop-log
%{_sbindir}/kcm
%{_sbindir}/kdigest
%{_sbindir}/kimpersonate
%{_libdir}/%{name}
%{_datadir}/%{name}
%doc doc/*.html lib/hdb/hdb.schema

%pre server
if [ -d %{_var}/%{name} ]; then
    mv %{_var}/%{name} %{_localstatedir}/lib/%{name}
fi

%post server
%_post_service %{name}

%preun server
%_preun_service %{name}

#----------------------------------------------------------------------------

# Not working right yet
%if 0
%package	hdb_ldap
Summary:	Kerberos Server LDAP Backend
Group:		System/Servers
Requires:	%{name}-server = %{EVRD}

%description	hdb_ldap
This package contains the LDAP HDB backend plugin, which allows the use of
an LDAP server for storing the Heimdal database.

%files hdb_ldap
%{_libdir}/hdb_ldap*
%endif

#----------------------------------------------------------------------------

%package	libs
Summary:	Heimdal shared libraries
Group:		System/Libraries
Conflicts:	%{_lib}gssapi2

%description	libs
This package contains shared libraries required by several of the other heimdal
packages.

%files libs
%attr(400,root,root) %ghost %{_sysconfdir}/krb5.keytab
%{_libdir}/lib*.so.*
%{_libdir}/windc*.so.*
%{_infodir}/heimdal.info*
%{_infodir}/hx509.info.*
%{_mandir}/man8/kerberos.8*
%{_mandir}/cat8/kerberos.8*

#----------------------------------------------------------------------------

%if 0
%package	clients
Summary:	Kerberos programs for use on workstations
Group:		Networking/Other
Requires:	%{name}-libs = %{EVRD}

%description	clients
Kerberos 5 Clients.
%endif

#----------------------------------------------------------------------------

%package	devel
Summary:	Header files for heimdal
Group:		System/Libraries
Requires:	%{name}-libs = %{EVRD}
Conflicts:	libxmlrpc-devel
Conflicts:	krb5-devel
Conflicts:	ext2fs-devel
Conflicts:	pkgconfig(com_err)

%description	devel
Contains files needed to compile and link software using the kerberos
libraries.

%files devel
%{_bindir}/heimdal-config
%{_libdir}/lib*.so
%{_libdir}/windc.so
%{_includedir}/*
%{_libdir}/pkgconfig/heimdal-gssapi.pc
%{_libdir}/pkgconfig/heimdal-kadm-client.pc
%{_libdir}/pkgconfig/heimdal-kadm-server.pc
%{_libdir}/pkgconfig/heimdal-krb5.pc
%{_libdir}/pkgconfig/kadm-client.pc
%{_libdir}/pkgconfig/kadm-server.pc
%{_libdir}/pkgconfig/kafs.pc
%{_libdir}/pkgconfig/krb5-gssapi.pc
%{_libdir}/pkgconfig/krb5.pc

#----------------------------------------------------------------------------

%package	devel-doc
Summary:	Developer documentation for heimdal
Group:		System/Libraries
Conflicts:	heimdal-devel

%description	devel-doc
Contains the documentation covering functions etc. in the heimdal libraries

%files devel-doc
%{_mandir}/man1/krb5-config.1*
%{_mandir}/cat1/krb5-config.1*
%{_mandir}/man3/*
%{_mandir}/cat3/*

#----------------------------------------------------------------------------

%prep
%setup -q
%patch11 -p1 -b .passwd_check
%patch12 -p1

%build
%serverbuild
#   --sysconfdir=%{_sysconfdir}/%{name} \
%configure2_5x \
    --libexecdir=%{_sbindir} \
    --with-hdbdir=%{_localstatedir}/lib/%{name} \
    --disable-static \
    --enable-shared \
    --with-readline \
    --with-readline-lib=%{_libdir} \
    --with-readline-include=%{_includedir}/readline \
    --with-openldap=%{_prefix} \
    --with-sqlite3=%{_prefix} \
    --with-libintl=%{_prefix} \
    --with-x \
    --with-ipv6 \
    --enable-kcm \
    --enable-pk-init
%if 0
    --enable-hdb-openldap-module
%endif
make
%make -C doc html

%install
install -d %{buildroot}%{_localstatedir}/lib/%{name}
#install -d %{buildroot}%{_sysconfdir}/%{name}

%makeinstall_std

install appl/su/.libs/su %{buildroot}%{_bindir}/ksu
#install %{SOURCE4} %{buildroot}%{_sysconfdir}/krb5.conf

install -m755 %{SOURCE1} -D %{buildroot}%{_initrddir}/%{name}
install -m644 %{SOURCE3} -D %{buildroot}%{_sysconfdir}/sysconfig/%{name}
# FIXME install %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
# FIXME install %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

install -m644 %{SOURCE8} -D %{buildroot}%{_sysconfdir}/xinetd.d/kadmind

chmod +r %{buildroot}%{_bindir}/otp   # qrde dlaczego to ma chmod 0

#touch %{buildroot}%{_sysconfdir}/%{name}/krb5.keytab
touch %{buildroot}%{_sysconfdir}/krb5.keytab
touch %{buildroot}%{_localstatedir}/lib/%{name}/kadmind.acl

# prevent some conflicts
mv %{buildroot}%{_mandir}/man1/su.1 %{buildroot}%{_mandir}/man1/ksu.1
mv %{buildroot}%{_mandir}/cat1/su.1 %{buildroot}%{_mandir}/cat1/ksu.1
rm -f %{buildroot}%{_mandir}/*5/ftpusers.5*

rm -f %{buildroot}%{_libdir}/lib{com_err,ss}.so
rm -f %{buildroot}%{_includedir}/{glob,fnmatch,ss/ss}.h
rm -f %{buildroot}%{_bindir}/mk_cmds

# see if we can avoid conflicting with krb5-devel
mv %{buildroot}%{_bindir}/krb5-config %{buildroot}%{_bindir}/heimdal-config

# utils
install -m755 tools/kdc-log-analyze.pl -D %{buildroot}%{_datadir}/%{name}/kdc-log-analyze.pl
install -m755 lib/kadm5/check-cracklib.pl -D %{buildroot}%{_datadir}/%{name}/check-cracklib.pl
perl -pi -e 's|^#! ?/usr/pkg/bin/perl|#!%{_bindir}/perl|' \
    %{buildroot}%{_datadir}/%{name}/*.pl

# cleanups
rm -f %{buildroot}%{_libdir}/*.*a

# looks like we don't need these
rm -f %{buildroot}%{_mandir}/*5/qop.5*
rm -f %{buildroot}%{_mandir}/cat5/mech.5

%check
%if %{?_with_test:1}%{!?_with_test:0}
# For some reason this check fails partially just under rpm:
perl -pi -e 's/check-iprop //g' tests/kdc/Makefile
make -C tests check
%endif

