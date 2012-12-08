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

# debug package is empty and rpmlint rejects build

%define _enable_debug_packages %{nil}
%define debug_package %{nil}

%define distver 1.7
%define section free

%define	gcj_support 0
%define sdk_provider	openjdk
%ifnarch %{ix86} x86_64
%define sdk_provider	gcj
%endif

Name:           jpackage-utils
Version:        1.7.5
Release:        4.12
Epoch:          0
Summary:        JPackage utilities
License:        BSD-style
URL:            http://www.jpackage.org/
Source0:        %{name}-%{version}.tar.bz2
Source1:        classpath.security
Source2:        %{name}-README
Source3:        abs2rel.sh
Source4:        abs2rel.lua
Source10:	jpackage.generic.macros
Source11:	jpackage.override.mandriva.macros
Patch0:		java-functions-openjdk.patch
Patch1:         %{name}-enable-gcj-support.patch
Patch2:         %{name}-own-mavendirs.patch
Patch3:         %{name}-prefer-jre.patch
Patch4:         %{name}-set-classpath.patch

Group:          Development/Java
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
# (anssi 12/2007): No longer noarch as different JDK is used on x86(_64) than
# on other archs.
#BuildArch:      noarch
AutoReqProv:    no
%if 0
BuildRequires:  %{__awk}, %{__grep}
Requires:       /bin/egrep, %{__sed}, %{__perl}
%endif
Requires(post): rpm-helper
# Contains invalid alternatives setup that breaks keytool symlink
Conflicts:      kaffe-devel < 1.1.8-0.20070217.2

%description
Utilities for the JPackage Project:

* %{_bindir}/build-classpath
                                build the Java classpath in a portable manner
* %{_bindir}/build-jar-repository
                                build a jar repository in a portable manner
* %{_bindir}/rebuild-jar-repository
                                rebuild a jar repository in a portable manner
                                (after a jvm change...)
* %{_bindir}/build-classpath-directory
                                build the Java classpath from a directory
* %{_bindir}/diff-jars
                                show jar content differences
* %{_bindir}/jvmjar
                                install jvm extensions
* %{_bindir}/create-jar-links
                                create custom jar links
* %{_bindir}/clean-binary-files
                                remove binary files from sources
* %{_bindir}/check-binary-files
                                check for presence of unexpected binary files
* %{_datadir}/java-utils/java-functions
                                shell script functions library for Java
                                applications
* %{_sysconfdir}/java/jpackage-release
                                string identifying the currently installed
                                JPackage release
* %{_sysconfdir}/java/java.conf
                                system-wide Java configuration file
* %{_sysconfdir}/rpm/macros.d/jpackage.macros
                                RPM macros for Java packagers and developers
* %{_docdir}/%{name}/jpackage-policy
                                Java packaging policy for packagers and
                                developers

It also contains the license, man pages, documentation, XSL files of general
use with maven2, a header file for spec files etc.

%package -n java-rpmbuild
Summary:	Java SDK for building Mandriva java rpm packages
Group:		Development/Java
Requires:	java-devel-%{sdk_provider}
Requires:	jpackage-utils = %{version}

%description -n java-rpmbuild
Contains links that set up the default java SDK which is used for
building Mandriva rpm packages of java software.

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1
%{__perl} -pi -e 's/(^%%_[ml]*iconsdir)/#\1/g' misc/macros.jpackage
%{__perl} -pi -e 's/(^%%_menudir)/#\1/' misc/macros.jpackage
%{__perl} -pi -e 's|jre/sh|jre/bin|g' java-utils/java-functions 
cp %{SOURCE2} .

%build
echo "JPackage release %{distver} (%{distribution}) for %{_target_cpu}" \
 > etc/jpackage-release


%install
rm -rf $RPM_BUILD_ROOT

# Pull macros out of macros.jpackage and emulate them during install for
# smooth bootstrapping experience.
for dir in \
    jvmdir jvmjardir jvmprivdir \
    jvmlibdir jvmdatadir jvmsysconfdir \
    jvmcommonlibdir jvmcommondatadir jvmcommonsysconfdir \
    javadir jnidir javadocdir mavenpomdir \
    mavendepmapdir mavendepmapfragdir; do
  export _${dir}=$(rpm --eval $(%{__grep} -E "^%_${dir}\b" \
    misc/macros.jpackage | %{__awk} '{ print $2 }'))
done

install -dm 755 ${RPM_BUILD_ROOT}${_jvmdir}
install -dm 755 ${RPM_BUILD_ROOT}${_jvmjardir}
install -dm 755 ${RPM_BUILD_ROOT}${_jvmprivdir}
install -dm 755 ${RPM_BUILD_ROOT}${_jvmlibdir}
install -dm 755 ${RPM_BUILD_ROOT}${_jvmdatadir}
install -dm 755 ${RPM_BUILD_ROOT}${_jvmsysconfdir}
install -dm 755 ${RPM_BUILD_ROOT}${_jvmcommonlibdir}
install -dm 755 ${RPM_BUILD_ROOT}${_jvmcommondatadir}
install -dm 755 ${RPM_BUILD_ROOT}${_jvmcommonsysconfdir}
install -dm 755 ${RPM_BUILD_ROOT}${_javadir}
install -dm 755 ${RPM_BUILD_ROOT}${_javadir}-utils
install -dm 755 ${RPM_BUILD_ROOT}${_javadir}-ext
install -dm 755 ${RPM_BUILD_ROOT}${_javadir}-{1.3.1,1.4.0,1.4.1,1.4.2}
install -dm 755 ${RPM_BUILD_ROOT}${_javadir}-{1.5.0,1.6.0,1.7.0}
install -dm 755 ${RPM_BUILD_ROOT}${_jnidir}
install -dm 755 ${RPM_BUILD_ROOT}${_jnidir}-ext
install -dm 755 ${RPM_BUILD_ROOT}${_jnidir}-{1.3.1,1.4.0,1.4.1,1.4.2}
install -dm 755 ${RPM_BUILD_ROOT}${_jnidir}-{1.5.0,1.6.0,1.7.0}
install -dm 755 ${RPM_BUILD_ROOT}${_javadocdir}
install -dm 755 ${RPM_BUILD_ROOT}${_mavenpomdir}
install -dm 755 ${RPM_BUILD_ROOT}${_mavendepmapfragdir}

pushd bin
for i in *; do
	install -pm 755 -D $i ${RPM_BUILD_ROOT}%{_bindir}/$i
done
popd
install -m644 etc/font.properties -D ${RPM_BUILD_ROOT}%{_sysconfdir}/java/font.properties

# Install abs2rel scripts
install -pm 755 %{SOURCE3}  ${RPM_BUILD_ROOT}%{_javadir}-utils
install -pm 644 %{SOURCE4} ${RPM_BUILD_ROOT}%{_javadir}-utils

# Create an initial (empty) depmap
echo -e "<dependencies>\\n" \
  > ${RPM_BUILD_ROOT}${_mavendepmapdir}/maven2-depmap.xml
echo -e "</dependencies>\\n" \
  >> ${RPM_BUILD_ROOT}${_mavendepmapdir}/maven2-depmap.xml

cat > etc/java.conf << EOF
# System-wide Java configuration file                                -*- sh -*-
#
# JPackage Project <http://www.jpackage.org/>

# Location of jar files on the system
JAVA_LIBDIR=${_javadir}

# Location of arch-specific jar files on the system
JNI_LIBDIR=${_jnidir}

# Root of all JVM installations
JVM_ROOT=${_jvmdir}

# You can define a system-wide JVM root here if you're not using the
# default one.
#
# If you have the a base JRE package installed
# (e.g. java-1.6.0-openjdk):
#JAVA_HOME=\$JVM_ROOT/jre
#
# If you have the a devel JDK package installed
# (e.g. java-1.6.0-openjdk-devel):
#JAVA_HOME=\$JVM_ROOT/java

# Options to pass to the java interpreter
JAVACMD_OPTS=
EOF

install -pm 644 etc/java.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/java/java.conf
install -pm 644 etc/jpackage-release -D ${RPM_BUILD_ROOT}%{_sysconfdir}/java/jpackage-release
install -pm 644 java-utils/java-functions -D ${RPM_BUILD_ROOT}${_javadir}-utils
install -m644 misc/macros.jpackage -D ${RPM_BUILD_ROOT}%{_sysconfdir}/rpm/macros.d/jpackage.macros
install -m644 %{SOURCE10} -D %{buildroot}%{_sysconfdir}/rpm/macros.d/jpackage.generic.macros
install -m644 %{SOURCE11} -D %{buildroot}%{_sysconfdir}/rpm/macros.d/jpackage.override.mandriva.macros

%{__mkdir_p} ${RPM_BUILD_ROOT}%{_mandir}/man1
install -pm 644 man/* ${RPM_BUILD_ROOT}%{_mandir}/man1
%{__mkdir_p} ${RPM_BUILD_ROOT}${_javadir}-utils/xml
install -pm 644 xml/* ${RPM_BUILD_ROOT}${_javadir}-utils/xml

ln -s java-%{sdk_provider} %{buildroot}${_jvmdir}/java-rpmbuild
ln -s java-%{sdk_provider} %{buildroot}${_jvmjardir}/java-rpmbuild

## BEGIN GCJ/CLASSPATH SPECIFIC ##
%{__mkdir_p} %{buildroot}%{_libdir}/security
%{__cp} -a %{SOURCE1} %{buildroot}%{_libdir}/security/classpath.security.real

%{__mkdir_p} %{buildroot}%{_bindir}
%{__cat} > %{buildroot}%{_bindir}/rebuild-security-providers << EOF
#!/bin/sh
# Rebuild the list of security providers classpath.security

cat %{_libdir}/security/classpath.security \
  | grep -v "^security.provider." \
  > %{_libdir}/security/classpath.security.bak
mv -f %{_libdir}/security/classpath.security.bak \
  %{_libdir}/security/classpath.security

providers=\$(ls %{_sysconfdir}/java/security/security.d | sort \
  | awk -F- '{ print \$2 }')
count=0
for provider in \$providers
do
  case \$provider in
  *.rpmsave|*.rpmorig|*.rpmnew|*~|*.orig|*.bak)
  ;;
  *)
  count=\$((count + 1))
  echo "security.provider."\$count"="\$provider \
    >> %{_libdir}/security/classpath.security
  ;;
  esac
done
EOF

%{__mkdir_p} %{buildroot}%{_sysconfdir}/java/security/security.d
pushd  %{buildroot}%{_sysconfdir}/java/security/security.d
touch 1000-gnu.java.security.provider.Gnu
touch 1500-org.bouncycastle.jce.provider.BouncyCastleProvider
touch 2000-gnu.javax.crypto.jce.GnuCrypto
touch 3000-gnu.javax.crypto.jce.GnuSasl
touch 4000-gnu.javax.net.ssl.provider.Jessie
touch 5000-gnu.javax.security.auth.callback.GnuCallbacks
popd

%{__mkdir_p} %{buildroot}%{_libdir}
%{__cat} > %{buildroot}%{_libdir}/logging.properties.real << EOF
# Default logging properties.
# See javadoc in java.util.logging.LogManager to information on
# overriding these settings.  Most of the defaults are compiled in, so
# this file is fairly minimal.

# Send log records to System.err, default to OFF instead of INFO.
handlers = java.util.logging.ConsoleHandler
.level = OFF
EOF

%{__mkdir_p} %{buildroot}%{_javadir}/gcj-endorsed
## END GCJ/CLASSPATH SPECIFIC ##


cat <<EOF > %{name}-%{version}.files
%{_bindir}/*
%{_mandir}/man1/*
%dir %{_sysconfdir}/java
%if %{gcj_support}
%{_sysconfdir}/java/security
%endif
%dir ${_jvmdir}
%dir ${_jvmjardir}
%dir ${_jvmprivdir}
# %dir ${_jvmlibdir}
%dir ${_jvmdatadir}
%dir ${_jvmsysconfdir}
%dir ${_jvmcommonlibdir}
%dir ${_jvmcommondatadir}
%dir ${_jvmcommonsysconfdir}
%dir ${_javadir}
%dir ${_javadir}-*
%dir ${_jnidir}
%dir ${_jnidir}-*
%dir ${_javadocdir}
%dir %{_datadir}/maven2
%dir ${_mavenpomdir}
%dir ${_mavendepmapdir}
%dir ${_mavendepmapfragdir}
${_javadir}-utils/*
%config %{_sysconfdir}/java/jpackage-release
%config(noreplace) %{_sysconfdir}/java/java.conf
%config(noreplace) %{_sysconfdir}/java/font.properties
%{_sysconfdir}/rpm/macros.d/jpackage.*macros
%config(noreplace) ${_mavendepmapdir}/maven2-depmap.xml
%dir %{_libdir}/security
%{_libdir}/security/classpath.security.real
%dir %{_sysconfdir}/java/security
%dir %{_sysconfdir}/java/security/security.d
%{_sysconfdir}/java/security/security.d/*
%{_libdir}/logging.properties.real
%dir %{_javadir}/gcj-endorsed
EOF

cat <<EOF > java-rpmbuild-%{version}.files
${_jvmdir}/java-rpmbuild
${_jvmjardir}/java-rpmbuild
EOF

chmod 644 doc/* etc/httpd-javadoc.conf

%post
%{__cp} -af %{_libdir}/security/classpath.security.real %{_libdir}/security/classpath.security
%{__cp} -af %{_libdir}/logging.properties.real %{_libdir}/logging.properties
if [ -x %{_bindir}/rebuild-security-providers ]; then
  %{_bindir}/rebuild-security-providers
fi

%triggerin -- libgcj12-base
%{__cp} -af %{_libdir}/security/classpath.security.real %{_libdir}/security/classpath.security
%{__cp} -af %{_libdir}/logging.properties.real %{_libdir}/logging.properties

%triggerpostun -- libgcj12-base
%{__cp} -af %{_libdir}/security/classpath.security.real %{_libdir}/security/classpath.security
%{__cp} -af %{_libdir}/logging.properties.real %{_libdir}/logging.properties
# caused by triggerin:
%{__rm} -f %{_libdir}/security/classpath.security.rpmsave

%files -f %{name}-%{version}.files
%defattr(-,root,root,-)
%doc jpackage-utils-README LICENSE.txt HEADER.JPP doc/* etc/httpd-javadoc.conf

%files -n java-rpmbuild -f java-rpmbuild-%{version}.files
%defattr(-,root,root)


%changelog
* Tue May 10 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 0:1.7.5-4.11
+ Revision: 673335
- disable gcj support
- try some best effort at syncing up with jpackage..

* Fri Apr 08 2011 Paulo Andrade <pcpa@mandriva.com.br> 0:1.7.5-4.0.8
+ Revision: 651849
- Use libdir for java files, following default gcc-java install

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.7.5-4.0.7mdv2011.0
+ Revision: 606104
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.7.5-4.0.6mdv2010.1
+ Revision: 523087
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:1.7.5-4.0.5mdv2010.0
+ Revision: 425466
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0:1.7.5-4.0.4mdv2009.1
+ Revision: 351312
- rebuild

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 0:1.7.5-4.0.3mdv2009.0
+ Revision: 264755
- rebuild early 2009.0 package (before pixel changes)
- remove URL from description

* Sat May 24 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.7.5-1.0.3mdv2009.0
+ Revision: 210827
- disable default gcj_support

* Sat May 10 2008 David Walluck <walluck@mandriva.org> 0:1.7.5-1.0.2mdv2009.0
+ Revision: 205356
- use openjdk instead of icedtea for java-rpmbuild

* Tue Apr 22 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.7.5-1.0.1mdv2009.0
+ Revision: 196510
- new version

* Mon Feb 18 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.7.4-2.0.3mdv2008.1
+ Revision: 170647
- add temp patch to detect the latest openjdk version reporting changes

* Thu Jan 10 2008 David Walluck <walluck@mandriva.org> 0:1.7.4-2.0.2mdv2008.1
+ Revision: 147446
- bump release

* Wed Jan 09 2008 David Walluck <walluck@mandriva.org> 0:1.7.4-2.0.1mdv2008.1
+ Revision: 147379
- 1.7.4-2jpp
- remove jpackage-utils-1.7.4-fix-macros.patch (fixed upstream)
- remove jpackage-utils-1.7.3-gcj-macros.patch (already an external source)
- comment out file-based (Build)Requires

* Thu Jan 03 2008 Anssi Hannula <anssi@mandriva.org> 0:1.7.4-1.0.3mdv2008.1
+ Revision: 141083
- add missing backslash to macros file (P1, fixes the message
  "error: Macro %% has illegal name (%%define)")

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Jan 02 2008 Anssi Hannula <anssi@mandriva.org> 0:1.7.4-1.0.2mdv2008.1
+ Revision: 140685
- use find -delete instead of broken xargs in jpackage.generic.macros

* Wed Jan 02 2008 David Walluck <walluck@mandriva.org> 0:1.7.4-1.0.1mdv2008.1
+ Revision: 140664
- 1.7.4
- fix %%gcj_native in jpackage.generic.macros
- use xargs instead of 'find -exec' in jpackage.generic.macros

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.7.3-12mdv2008.1
+ Revision: 120804
- introduce java-rpmbuild package that contains links to the JDK used
  for building java packages
- set icedtea as default on ix86 and x86_64, gcj on others (thus this
  package is no longer noarch)
- fix documentation path in description

* Thu Sep 20 2007 Anssi Hannula <anssi@mandriva.org> 0:1.7.3-11mdv2008.0
+ Revision: 91545
- conflict with old kaffe-devel to prevent keytool breakage
- do not mark macro and security provider files as config files

* Thu Jul 05 2007 Anssi Hannula <anssi@mandriva.org> 0:1.7.3-10mdv2008.0
+ Revision: 48364
- redefine %%java as well as it was not obeying %%java_home

* Thu Jun 28 2007 Anssi Hannula <anssi@mandriva.org> 0:1.7.3-9mdv2008.0
+ Revision: 45430
- workaround disappearance of property files during libgcj7-base removal
  (related to a workaround of bug #23693)

* Thu Jun 28 2007 Anssi Hannula <anssi@mandriva.org> 0:1.7.3-8mdv2008.0
+ Revision: 45415
- drop ghosts, they caused conflicts
- always use gcj when building packages

* Thu Jun 28 2007 David Walluck <walluck@mandriva.org> 0:1.7.3-7mdv2008.0
+ Revision: 45406
- add java 1.7 support

* Wed Jun 27 2007 Anssi Hannula <anssi@mandriva.org> 0:1.7.3-6mdv2008.0
+ Revision: 45187
- use trigger instead of require on libgcj7-base to workaround #23693

* Wed Jun 27 2007 Anssi Hannula <anssi@mandriva.org> 0:1.7.3-5mdv2008.0
+ Revision: 44928
- do not set JAVA_HOME in /etc/java/java.conf by default (and certainly
  not to a one which is only provided by java-devel packages)

* Thu May 03 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 0:1.7.3-4mdv2008.0
+ Revision: 21529
- Changed JAVA_HOME value in default /etc/java/java.conf from
  JVM_ROOT/java-gcj to JVM_ROOT/java (solution reported on cooker
  ML). Closes #30541.


* Sun Mar 04 2007 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.7.3-3mdv2007.0
+ Revision: 132585
- move new macros to separate macros file to avoid patch need (S10)
- add %%remove_java_binaries & %%create_jar_links macros
- start on work with jpackage improval (see http://wiki.mandriva.com/en/Policies/Java/JPackage):
  o add gcj macros (P0)
  o enable gcj usage in mandriva specific macros (S11)

* Fri Dec 15 2006 David Walluck <walluck@mandriva.org> 0:1.7.3-1mdv2007.1
+ Revision: 97197
- 1.7.3
- Import jpackage-utils

* Sat Sep 02 2006 David Walluck <walluck@mandriva.org> 0:1.7.0-1.4mdv2007.0
- add support for java 1.6.0

* Fri Aug 04 2006 David Walluck <walluck@mandriva.org> 0:1.7.0-1.3mdv2007.0
- update classpath.security and use workaround for libgcj

* Fri Jul 28 2006 David Walluck <walluck@mandriva.org> 0:1.7.0-1.2mdv2007.0
- remove common classpath/gcj files until workaround is found

* Thu May 25 2006 David Walluck <walluck@mandriva.org> 0:1.7.0-1.1mdv2007.0
- 1.7.0
- update files in %%{_sysconfdir}/java/security/security.d

* Mon Apr 24 2006 David Walluck <walluck@mandriva.org> 0:1.6.6-1.3mdk
- add %%{_bindir}/rebuild-security-providers
- add %%{_sysconfdir}/java/security/security.d and files

* Mon Jan 30 2006 David Walluck <walluck@mandriva.org> 0:1.6.6-1.2mdk
- fix path to jre

* Mon Sep 19 2005 David Walluck <walluck@mandriva.org> 0:1.6.6-1.1mdk
- 1.6.6

* Sun Sep 18 2005 David Walluck <walluck@mandriva.org> 0:1.6.5-1.1mdk
- use perl instead of patch
- set default jvm to gcj

* Mon Sep 12 2005 Pascal Terjan <pterjan@mandriva.org> 0:1.6.4-1.5mdk
- don't undefine _menudir and icondir when they exist. There is no
  need for a test in the patch as this rpm is intended for Mandriva only

* Sat Sep 10 2005 David Walluck <walluck@mandriva.org> 0:1.6.4-1.4mdk
- replace menudir patch with more generic macros patch

* Fri Sep 09 2005 David Walluck <walluck@mandriva.org> 0:1.6.4-1.3mdk
- bzip2 menudir patch

* Fri Sep 09 2005 Oden Eriksson <oeriksson@mandriva.com> 0:1.6.4-1.2mdk
- fix _menudir

* Wed Sep 07 2005 David Walluck <walluck@mandriva.org> 0:1.6.4-1.1mdk
- 1.6.4
- move gcj-specific stuff to java-gcj-compat

* Thu May 19 2005 David Walluck <walluck@mandriva.org> 0:1.6.3-1.4mdk
- install macros.jpackage as jpackage.macros
- add %%post scriptlet which removes macros.jpackage references from rpmrc

* Wed May 18 2005 David Walluck <walluck@mandriva.org> 0:1.6.3-1.3mdk
- move macros.jpackage to %%{_sysconfdir}/rpm/macros.d
- remove scriptlets

* Sun May 08 2005 David Walluck <walluck@mandriva.org> 0:1.6.3-1.2mdk
- don't provide java-javadoc in this package

* Fri May 06 2005 David Walluck <walluck@mandriva.org> 0:1.6.3-1.1mdk
- release

* Thu Apr 28 2005 Thomas Fitzsimmons <fitzsim@redhat.com> - 0:1.6.3-1jpp_1rh
- Import jpackage-utils 0:1.6.3-1jpp from jpackage.org.
- Add rebuild-security-providers script.
- Install security directory in /etc.
- Remove homedir patch.
- Don't look for LICENSE.txt.

* Fri Jan 28 2005 Nicolas Mailhot <nim at jpackage.org> - 0:1.6.3-1jpp
- prefer full JVM to JRE when not specified (my bad, sorry)
- remove LICENSE.txt as it does not seem to exist in the jpp16 branch anymore

* Sat Jan 15 2005 Nicolas Mailhot <nim at jpackage.org> - 0:1.6.2-1jpp
Happy new year jpackagers!
- No longer define JAVA_HOME in default shipped java.conf (me)
- Search if $JVM_ROOT/jre or $JVM_ROOT/java exist in functions if JAVA_HOME is
  not defined in java.conf (me)
- Source ~/.java/java.conf in addition to /etc/java/java.conf in functions 
  (me)
- Make find-jar use the same error code as build-classpath (Joe Wortmann)
  (note however find-jar was never intended to use directly in scripts, it's
   a low-level way to test the search engine)
- Change macros slightly so they no longer wreak havoc on x86_64 systems
  (Thomas Fitzsimmons for Red Hat)
  This is probably only a short-term fix since we've yet to decide how to 
  handle real x86_64 JVMs cleanly.

* Sat Dec 04 2004 Ville Skyttä <scop at jpackage.org> - 0:1.6.1-1jpp
- java-functions (set_jvm_dirs): try "java -fullversion" before
  "java -version" for performance, improve regexps, use sed from $PATH.
- Include correct specfile in tarball.

* Tue Nov 02 2004 Nicolas Mailhot <nim@jpackage.org> - 0:1.6.0-2jpp
- fix missing %%{_jnidir} in file list

* Wed Oct 13 2004 Ville Skyttä <scop at jpackage.org> - 0:1.6.0-1jpp
- Start preparing for JPackage 1.6:
  - License change: jpackage-utils >= 1.6.0 is available under the (BSD-like)
    JPackage License.  See included LICENSE.txt.
  - Remove support for Java < 1.4 (dirs only for now).
  - Remove java_home.list and support for it.
- Add support for installing jpackage.macros into Asianux's rpm config,
  thanks to Robert Ottenhag for the info.

* Tue Aug 24 2004 Randy Watler <rwatler at finali.com> - 0:1.5.38-2jpp
- Rebuild with ant-1.6.2

* Tue Jun 08 2004 Ville Skyttä <scop at jpackage.org> - 0:1.5.38-1jpp
- Update java_home.list with Sun's default 1.5.0beta2 location.
- Nuke extra copy of java.conf from tarball.

* Thu May 27 2004 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net> - 0:1.5.37-1jpp
- add the --preserve-naming switch to build-jar-repository, and document it
  (following a discussion with Chip Turner)

* Fri May 07 2004 Ville Skyttä <scop at jpackage.org> - 0:1.5.36-1jpp
- Fix bootstrap problem by ensuring that build time macro expansion for
  %%{_sysconfdir}/java.conf uses macros defined in this package and does not
  rely on the macros being already defined.
- Include correct spec file in tarball.

* Wed May 05 2004 David Walluck <david@jpackage.org> 0:1.5.35-1jpp
- expand macros in %%{_sysconfdir}/java.conf

* Fri Mar 26 2004 Ville Skyttä <scop at jpackage.org> - 0:1.5.34-1jpp
- Update java_home.list with Sun's default 1.4.2_04, 1.4.1_07, 1.3.1_10
  and 1.3.1_11 locations.

