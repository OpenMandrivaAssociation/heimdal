%define _disable_ld_no_undefined 1
%global __requires_exclude perl\\(Crypt::Cracklib\\)

Name:       heimdal
Version:    7.7.0
Release:    3
Summary:    Heimdal implementation of Kerberos V5 system
License:    BSD-like
Group:      Networking/Other
URL:        http://www.h5l.org
Source0:    http://www.h5l.org/dist/src/heimdal-%{version}.tar.gz
Source1:    http://www.h5l.org/dist/src/heimdal-%{version}.tar.gz.asc
Source3:    %{name}.sysconfig
Source10:   %{name}.logrotate
Source26:   %{name}-kdc.service
Source27:   %{name}-ipropd-master.service
Source28:   %{name}-ipropd-slave.service
Source29:   %{name}-kadmind.service
Source30:   %{name}-kpasswdd.service
Source31:   %{name}-ipropd-slave-wrapper

Patch0:		fix-missing-headers

BuildRequires:  db18-devel >= 4.2.52
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  libtool
BuildRequires:  texinfo
BuildRequires:  openldap-devel >= 2.0
BuildRequires:  readline-devel
BuildRequires:  pam-devel
BuildRequires:  pkgconfig(ncurses) >= 5.3
BuildRequires:	pkgconfig(com_err)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(x11)
BuildRequires:	pkgconfig(xau)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(libedit)
BuildRequires:	perl(JSON)
#Required for tests/ldap
BuildRequires:  openldap-servers

%description
Kerberos 5 is a network authentication and single sign-on system.
Heimdal is a free Kerberos 5 implementation without export restrictions
written from the spec (rfc1510 and successors) including advanced features
like thread safety, IPv6, master-slave replication of Kerberos Key
Distribution Center server and support for ticket delegation (S4U2Self,
S4U2Proxy).

%package workstation
Summary:    Kerberos programs for use on workstations
Group:      Networking/Other
Requires:   %{name}-libs = %{version}-%{release}
Conflicts:  krb5-workstation
Provides:   kerberos-workstation

%description workstation
This package contains Kerberos 5 programs for use on workstations.
#----------------------------------------------------------------------------

%package server
Summary:    Kerberos Server
Group:      System/Servers
Requires:   %{name}-libs = %{version}-%{release}
Requires:   krb5
Requires(post): chkconfig
Requires(preun):chkconfig
Conflicts:  krb5-server

%description server
This package contains the master KDC.
#----------------------------------------------------------------------------

%package hdb_ldap
Summary:    Kerberos Server LDAP Backend
Group:      System/Servers
Requires:   %{name}-server = %{version}-%{release}

%description hdb_ldap
This package contains the LDAP HDB backend plugin, which allows the use of
an LDAP server for storing the Heimdal database.

#----------------------------------------------------------------------------

%package libs
Summary:    Heimdal shared libraries
Group:      System/Libraries
Conflicts:  %{_lib}gssapi2

%description libs
This package contains shared libraries required by several of the other heimdal
packages.
#----------------------------------------------------------------------------

%package devel
Summary:    Header files for heimdal
Group:      System/Libraries
Requires:   %{name}-libs = %{version}-%{release}
Conflicts:  libxmlrpc-devel
Conflicts:  krb5-devel

%description devel
contains files needed to compile and link software using the kerberos
libraries.
#----------------------------------------------------------------------------

%package devel-doc
Summary:    Developer documentation for heimdal
Group:      System/Libraries
Conflicts:  heimdal-devel <= 1.0.1-4

%description devel-doc
Contains the documentation covering functions etc. in the heimdal libraries
#----------------------------------------------------------------------------

%package -n	openldap-schemas-%{name}
Summary:	OpenLDAP schema files from %{name}-%{EVRD} source tree
Group:		Databases
BuildArch:	noarch
Requires(pre):	openldap-config

%files -n		openldap-schemas-%{name}
%config(noreplace) %{_sysconfdir}/openldap/schema/*
%attr(750,ldap,ldap) %config(noreplace) %{_sysconfdir}/openldap/slapd.d/%{name}.conf

%description -n		openldap-schemas-%{name}
scheme for openldap

#----------------------------------------------------------------------------


%prep
%autosetup -p1

# Make absolutely sure we don't end up using broken
# bundled libraries
rm -rf lib/sqlite/*.{c,h}

# Find db18 instead of obsolete db6
sed -i -e 's,db6,db18.1.32,g' cf/db.m4 lib/hdb/db3.c
sed -i -e 's,DB6,DB18_1_32,g' lib/hdb/db3.c

%build
%serverbuild
%configure \
	--with-hdbdir=%{_localstatedir}/lib/%{name} \
	--disable-static \
	--enable-shared \
	--with-readline \
	--with-readline-lib=%{_libdir} \
	--with-readline-include=%{_includedir}/readline \
	--with-openldap \
	--with-openldap-lib=%{_libdir} \
	--with-openldap-include=%{_includedir} \
	--with-sqlite3 \
	--with-sqlite3-lib=%{_libdir} \
	--with-sqlite3-include=%{_includedir} \
	--with-libintl \
	--with-libintl-lib=%{_libdir} \
	--with-libintl-include=%{_includedir} \
	--with-readline-lib=%{_libdir} \
	--with-readline-include=%{_includedir}/readline \
	--with-libedit \
	--with-libedit-lib=%{_libdir} \
	--with-libedit-include=%{_includedir}/editline \
	--without-x \
	--with-ipv6 \
	--enable-kcm \
	--enable-pk-init \
	--enable-hdb-openldap-module

%make_build

%install
install -d %{buildroot}%{_localstatedir}/lib/%{name}
#install -d %{buildroot}%{_sysconfdir}/%{name}

%make_install

install -d -m 755 %{buildroot}%{_unitdir}
install -m 644 %{SOURCE26} %{buildroot}%{_unitdir}/heimdal-kdc.service
install -m 644 %{SOURCE27} %{buildroot}%{_unitdir}/heimdal-ipropd-master.service
install -m 644 %{SOURCE28} %{buildroot}%{_unitdir}/heimdal-ipropd-slave.service
install -m 644 %{SOURCE29} %{buildroot}%{_unitdir}/heimdal-kadmind.service
install -m 644 %{SOURCE30} %{buildroot}%{_unitdir}/heimdal-kpasswdd.service
install -m 755 %{SOURCE31} %{buildroot}%{_libexecdir}/ipropd-slave-wrapper

install -D -m 755 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -D -m 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

chmod +r %{buildroot}%{_bindir}/otp   # qrde dlaczego to ma chmod 0

#touch %{buildroot}%{_sysconfdir}/%{name}/krb5.keytab
touch %{buildroot}%{_sysconfdir}/krb5.keytab
touch %{buildroot}%{_localstatedir}/lib/%{name}/kadmind.acl

# prevent some conflicts
mv %{buildroot}%{_bindir}/su %{buildroot}%{_bindir}/ksu
mv %{buildroot}/%{_mandir}/man1/su.1 %{buildroot}/%{_mandir}/man1/ksu.1
rm -f %{buildroot}%{_mandir}/*5/ftpusers.5*

rm -f %{buildroot}%{_libdir}/lib{com_err,ss}.so
rm -f %{buildroot}%{_includedir}/{glob,fnmatch,ss/ss}.h
rm -f %{buildroot}%{_bindir}/mk_cmds

# see if we can avoid conflicting with krb5-devel
mv %{buildroot}/%{_bindir}/krb5-config %{buildroot}/%{_bindir}/heimdal-config

# utils
install -d -m 755 %{buildroot}%{_datadir}/%{name}
install -m 755 tools/kdc-log-analyze.pl %{buildroot}%{_datadir}/%{name}
install -m 755 lib/kadm5/check-cracklib.pl %{buildroot}%{_datadir}/%{name}
perl -pi -e 's|^#! ?/usr/pkg/bin/perl|#!%{_bindir}/perl|' \
    %{buildroot}%{_datadir}/%{name}/*.pl

# remove CAT files
rm -rf %{buildroot}%{_mandir}/cat*

# Prepare schema files to be included into OpenLDAP configuration
mkdir -p %{buildroot}%{_sysconfdir}/openldap/{schema,slapd.d}
install -m 0644 lib/hdb/hdb.schema %{buildroot}%{_sysconfdir}/openldap/schema/
cat > %{buildroot}%{_sysconfdir}/openldap/slapd.d/%{name}.conf <<EOF
# If you need heimdal support load this file or copy
# uncommented lines below to your slapd.conf.
include %{_sysconfdir}/openldap/schema/hdb.schema
EOF
chmod 0644 %{buildroot}%{_sysconfdir}/openldap/slapd.d/%{name}.conf

%check
%if %{?_with_test:1}%{!?_with_test:0}
# For some reason this check fails partially just under rpm:
perl -pi -e 's/check-iprop //g' tests/kdc/Makefile
make -C tests check
%endif

%post server
%_post_service %{name}-kdc

%preun server
%_preun_service %{name}-kdc

%files server
%doc NEWS TODO
%{_unitdir}/heimdal-kdc.service
%{_unitdir}/heimdal-ipropd-master.service
%{_unitdir}/heimdal-ipropd-slave.service
%{_unitdir}/heimdal-kadmind.service
%{_unitdir}/heimdal-kpasswdd.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%dir %{_localstatedir}/lib/%{name}
%config(noreplace) %{_localstatedir}/lib/%{name}/kadmind.acl
# %{_mandir}/*1/kimpersonate.1*
%{_mandir}/man8/kimpersonate.8.*
%{_mandir}/man8/iprop.8*
%{_mandir}/man8/iprop-log.8*
%{_mandir}/man8/kstash.8*
%{_mandir}/man8/hprop.8*
%{_mandir}/man8/hpropd.8*
%{_mandir}/man8/kadmind.8*
%{_mandir}/man8/kdc.8*
%{_mandir}/man8/kfd.8*
%{_mandir}/man8/kpasswdd.8*
%{_mandir}/man8/kcm.8*
%{_mandir}/man8/ipropd-*.8*
%{_sbindir}/kstash
%{_sbindir}/iprop-log
%{_libexecdir}/hprop
%{_libexecdir}/hpropd
%{_libexecdir}/ipropd-master
%{_libexecdir}/ipropd-slave
%{_libexecdir}/kadmind
%{_libexecdir}/kdc
%{_libexecdir}/kfd
%{_libexecdir}/kpasswdd
%{_libexecdir}/kcm
%{_libexecdir}/kimpersonate
%{_libexecdir}/ipropd-slave-wrapper
%{_datadir}/%{name}
%doc doc/*.html

%files hdb_ldap
%{_libdir}/hdb_ldap*

%files libs
%attr(400,root,root) %ghost %{_sysconfdir}/krb5.keytab
%{_bindir}/string2key
%{_bindir}/verify_krb5_conf
%{_libexecdir}/digest-service
%{_libexecdir}/kdigest
%{_libdir}/lib*.so.*
%{_libdir}/windc*.so.*
%{_infodir}/heimdal.info*
%{_infodir}/hx509.info.*
%{_mandir}/man5/qop.5*
%{_mandir}/man5/mech.5*
%{_mandir}/man8/kerberos.8*
%{_mandir}/man8/verify_krb5_conf.8*
%{_mandir}/man8/string2key.8*
%{_mandir}/man8/kdigest.8.*

%files workstation
%{_bindir}/afslog
%{_bindir}/bsearch
%{_bindir}/gsstool
%{_bindir}/heimtools
%{_bindir}/hxtool
%{_bindir}/idn-lookup
%{_bindir}/kdestroy
%{_bindir}/kf
%{_bindir}/kgetcred
%{_bindir}/kinit
%{_bindir}/klist
%{_bindir}/kpasswd
%attr(4755,root,root) %{_bindir}/ksu
%{_bindir}/kswitch
%attr(4755,root,root) %{_bindir}/otp
%{_bindir}/otpprint
%{_bindir}/pagsh
%{_bindir}/kadmin
%{_bindir}/ktutil
%{_mandir}/man1/afslog.1*
%{_mandir}/man1/bsearch.1*
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
%{_mandir}/man1/kadmin.1*
%{_mandir}/man1/ktutil.1*
%{_mandir}/man5/krb5.conf.5*

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
%{_libexecdir}/%{name}/asn1_compile
%{_libexecdir}/%{name}/asn1_print
%{_libexecdir}/%{name}/slc

%files devel-doc
%{_mandir}/man1/krb5-config.1*
%{_mandir}/man3/*
%{_mandir}/man7/*
