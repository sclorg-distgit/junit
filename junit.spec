%global pkg_name junit
%{?scl:%scl_package %{pkg_name}}
%{?java_common_find_provides_and_requires}

# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:           %{?scl_prefix}%{pkg_name}
Version:        4.11
Release:        8.15.bs1%{?dist}
Epoch:          0
Summary:        Java regression test package
License:        CPL
URL:            http://www.junit.org/
BuildArch:      noarch

# ./clean-tarball.sh %{version}
Source0:        %{pkg_name}-%{version}-clean.tar.gz
Source2:        junit-OSGi-MANIFEST.MF
Source3:        create-tarball.sh

# Removing hamcrest source jar references (not available and/or necessary)
Patch0:         %{pkg_name}-no-hamcrest-src.patch

BuildRequires:  %{?scl_prefix}ant
BuildRequires:  %{?scl_prefix_maven}ant-contrib
BuildRequires:  %{?scl_prefix}javapackages-tools
BuildRequires:  %{?scl_prefix}hamcrest
BuildRequires:  perl(Digest::MD5)
BuildRequires:  zip

Requires:       %{?scl_prefix}hamcrest


%description
JUnit is a regression testing framework written by Erich Gamma and Kent Beck. 
It is used by the developer who implements unit tests in Java. JUnit is Open
Source Software, released under the Common Public License Version 1.0 and 
hosted on GitHub.

%package manual
Summary:        Manual for %{pkg_name}
Requires:       %{?scl_prefix}runtime

%description manual
Documentation for %{pkg_name}.

%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
Javadoc for %{pkg_name}.

%package demo
Summary:        Demos for %{pkg_name}
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description demo
Demonstrations and samples for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-r%{version}
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%patch0 -p1

cp build/maven/junit-pom-template.xml pom.xml
# fix placeholder version in pom
%pom_xpath_set pom:project/pom:version "%{version}"

ln -s $(build-classpath hamcrest/core) lib/hamcrest-core-1.3.jar
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
ant dist -Dversion-status= || :

# inject OSGi manifest
mkdir -p META-INF
cp -p %{SOURCE2} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{pkg_name}%{version}/%{pkg_name}-%{version}.jar META-INF/MANIFEST.MF
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - <<"EOF"}
set -e -x
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 %{pkg_name}%{version}/%{pkg_name}-%{version}.jar %{buildroot}%{_javadir}/%{pkg_name}.jar
# Many packages still use the junit4.jar directly
ln -s %{_javadir}/%{pkg_name}.jar %{buildroot}%{_javadir}/%{pkg_name}4.jar

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -m 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{pkg_name}.pom
%add_maven_depmap

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr %{pkg_name}%{version}/javadoc/* %{buildroot}%{_javadocdir}/%{name}

# demo
install -d -m 755 %{buildroot}%{_datadir}/%{pkg_name}/demo/%{pkg_name} 

cp -pr %{pkg_name}%{version}/%{pkg_name}/* %{buildroot}%{_datadir}/%{pkg_name}/demo/%{pkg_name}
%{?scl:EOF}


%files -f .mfiles
%doc LICENSE README CODING_STYLE
%{_javadir}/%{pkg_name}4.jar

%files demo
%doc LICENSE
%{_datadir}/%{pkg_name}

%files javadoc
%doc LICENSE
%doc %{_javadocdir}/%{name}

%files manual
%doc LICENSE README CODING_STYLE
%doc junit%{version}/doc/*

%changelog
* Thu Jul 02 2015 Michael Simacek <msimacek@redhat.com> - 0:4.11-8.15
- Fix OSGi manifest metadata (rhbz#1238311)

* Wed Jan 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:4.11-8.14
- Add requires on SCL filesystem package

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 0:4.11-8.13
- Mass rebuild 2015-01-13

* Fri Jan 09 2015 Michal Srb <msrb@redhat.com> - 0:4.11-8.12
- Mass rebuild 2015-01-09

* Wed Jan 07 2015 Michal Srb <msrb@redhat.com> - 4.11-8.11
- Migrate to .mfiles

* Tue Dec 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:4.11-8.10
- Migrate requires and build-requires to rh-java-common

* Mon Dec 15 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:4.11-8.9
- Mass rebuild 2014-12-15

* Mon Dec 15 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:4.11-8.8
- Rebuild for rh-java-common collection

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:4.11-8.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:4.11-8.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:4.11-8.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:4.11-8.4
- Remove requires on java

* Mon Feb 17 2014 Michal Srb <msrb@redhat.com> - 0:4.11-8.3
- SCL-ize BR/R

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:4.11-8.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:4.11-8.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 04.11-8
- Mass rebuild 2013-12-27

* Fri Aug 23 2013 Michal Srb <msrb@redhat.com> - 0:4.11-7
- Drop "-SNAPSHOT" from version ID
- See: https://lists.fedoraproject.org/pipermail/java-devel/2013-August/004923.html

* Mon Aug 19 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:4.11-6
- Fix version in pom.xml (#998266)

* Fri Aug 02 2013 Michal Srb <msrb@redhat.com> - 0:4.11-5
- Add create-tarball.sh script to SRPM

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:4.11-4
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Fri Jun 21 2013 Michal Srb <msrb@redhat.com> - 0:4.11-3
- Build from clean tarball

* Mon May 06 2013 Tomas Radej <tradej@redhat.com> - 0:4.11-2
- Removed uneeded dependencies

* Thu Mar 21 2013 Tomas Radej <tradej@redhat.com> - 0:4.11-1
- Updated to latest upstream version

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 18 2012 Michal Srb <msrb@redhat.com> - 0:4.10-7
- Build-time dependency perl-MD5 replaced with perl(Digest::MD5)
- Description cleanup (Resolves: #888389)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 30 2012 Krzysztof Daniel <kdaniel@redhat.com> 0:4.10-5
- Update OSGi metadata to match 4.10.0 release.

* Thu Feb 09 2012 Harald Hoyer <harald@redhat.com> 4.10-4
- removed Conflicts with itsself

* Thu Jan 26 2012 Roland Grunberg <rgrunber@redhat.com> 0:4.8.2-3
- Add OSGi metadata to junit.jar manifest.

* Thu Jan 26 2012 Tomas Radej <tradej@redhat.com> - 0:4.10-2
- Fixed versioning

* Wed Jan 25 2012 Tomas Radej <tradej@redhat.com> - 0:4.10-1
- Updated to upstream 4.10
- Obsoleted junit4
- Epoch added

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 7 2010 Alexander Kurtakov <akurtako@redhat.com> 3.8.2-7
- Drop gcj support.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.2-6.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.2-5.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.8.2-4.4
- drop repotag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.8.2-4jpp.3
- Autorebuild for GCC 4.3

* Thu Sep 20 2007 Deepak Bhole <dbhole@redhat.com> - 3.8.2-3jpp.3
- Fix location of stylesheet for javadocs

* Thu Sep 20 2007 Deepak Bhole <dbhole@redhat.com> - 3.8.2-3jpp.2
- Rebuild for ppc32 execmem issue and new build-id

* Mon Feb 12 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 3.8.2-3jpp.1.fc7
- Add dist tag

* Mon Feb 12 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 3.8.2-3jpp.1
- Committed on behalf of Tania Bento <tbento@redhat.com>
- Update per Fedora review process
- Resolves rhbz#225954

* Thu Aug 10 2006 Deepak Bhole <dbhole@redhat.com> -  0:3.8.2-3jpp.1
- Added missing requirements.

* Thu Aug 10 2006 Karsten Hopp <karsten@redhat.de> 0:3.8.2-2jpp_3fc
- Require(post/postun): coreutils

* Fri Jun 23 2006 Deepak Bhole <dbhole@redhat.com> -  0:3.8.2-2jpp_2fc
- Rebuilt.

* Thu Jun 22 2006 Deepak Bhole <dbhole@redhat.com> -  0:3.8.2-2jpp_1fc
- Upgrade to 3.8.2
- Added conditional native compilation.
- Fix path where demo is located.

* Fri Mar 03 2006 Ralph Apel <r.apel at r-apel.de> - 0:3.8.2-1jpp
- First JPP-1.7 release

* Mon Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:3.8.1-4jpp
- Rebuild with ant-1.6.2
* Fri May 09 2003 David Walluck <david@anti-microsoft.org> 0:3.8.1-3jpp
- update for JPackage 1.5

* Fri Mar 21 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> 3.8.1-2jpp
- For jpackage-utils 1.5

* Fri Sep 06 2002 Henri Gomez <hgomez@users.sourceforge.net> 3.8.1-1jpp
- 3.8.1

* Sun Sep 01 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.8-2jpp 
- used original zip file

* Thu Aug 29 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.8-1jpp 
- 3.8
- group, vendor and distribution tags

* Sat Jan 19 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-6jpp
- versioned dir for javadoc
- no dependencies for manual and javadoc packages
- stricter dependency for demo package
- additional sources in individual archives
- section macro

* Sat Dec 1 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-5jpp
- javadoc in javadoc package

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 3.7-4jpp
- fixed previous releases ...grrr

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 3.7-3jpp
- added jpp extension
- removed packager tag

* Sun Sep 30 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-2jpp
- first unified release
- s/jPackage/JPackage

* Mon Sep 17 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-1mdk
- 3.7
- vendor tag
- packager tag
- s/Copyright/License/
- truncated description to 72 columns in spec
- spec cleanup
- used versioned jar
- moved demo files to %%{_datadir}/%%{name}

* Sat Feb 17 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 3.5-1mdk
- first Mandrake release
