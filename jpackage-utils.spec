# Copyright (c) 2000-2006, JPackage Project
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

%define distver 1.7
%define section free

Name:           jpackage-utils
Version:        1.7.3
Release:        %mkrel 10
Epoch:          0
Summary:        JPackage utilities
License:        BSD-style
URL:            http://www.jpackage.org/
Source0:        %{name}-%{version}.tar.bz2
Source1:        classpath.security
Source10:	jpackage.generic.macros
Source11:	jpackage.override.mandriva.macros
Patch0:		jpackage-utils-1.7.3-gcj-macros.patch
Group:          Development/Java
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:      noarch
AutoReqProv:    no
BuildRequires:  %{__awk}, %{__grep}
Requires:       /bin/egrep, %{__sed}, %{__perl}
Requires(post): rpm-helper

%description
Utilities for the JPackage Project <http://www.jpackage.org/>:

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
* %{_docdir}/%{name}-%{version}/jpackage-policy
                                Java packaging policy for packagers and
                                developers

It also contains the license, man pages, documentation, XSL files of general
use with maven2, a header file for spec files etc.

%prep
%setup -q

%{__perl} -pi -e 's/(^%%_[ml]*iconsdir)/#\1/g' misc/macros.jpackage
%{__perl} -pi -e 's/(^%%_menudir)/#\1/' misc/macros.jpackage
%{__perl} -pi -e 's|jre/sh|jre/bin|g' java-utils/java-functions 

%build
echo "JPackage release %{distver} (%{distribution}) for %{buildarch}" \
 > etc/jpackage-release


%install
rm -rf $RPM_BUILD_ROOT

# Pull macros out of macros.jpackage and emulate them during install for
# smooth bootstrapping experience.
for dir in \
    jvmdir jvmjardir jvmprivdir \
    jvmlibdir jvmdatadir jvmsysconfdir \
    jvmcommonlibdir jvmcommondatadir jvmcommonsysconfdir \
    javadir jnidir javadocdir mavendepmapdir; do
  export _${dir}=$(rpm --eval $(%{__grep} -E "^%_${dir}\b" misc/macros.jpackage | %{__awk} '{ print $2 }'))
done

install -dm 755 ${RPM_BUILD_ROOT}%{_bindir}
install -dm 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/{java,rpm/macros.d}
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
install -dm 755 ${RPM_BUILD_ROOT}${_jnidir}
install -dm 755 ${RPM_BUILD_ROOT}${_javadir}-{utils,ext,1.4.0,1.4.1,1.4.2,1.5.0,1.6.0,1.7.0}
install -dm 755 ${RPM_BUILD_ROOT}${_jnidir}-{ext,1.4.0,1.4.1,1.4.2,1.5.0,1.6.0,1.7.0}
install -dm 755 ${RPM_BUILD_ROOT}${_javadocdir}
install -dm 755 ${RPM_BUILD_ROOT}${_mavendepmapdir}

install -pm 755 bin/* ${RPM_BUILD_ROOT}%{_bindir}
install -pm 644 etc/font.properties ${RPM_BUILD_ROOT}%{_sysconfdir}/java

# Create an initial (empty) depmap
echo -e "<dependencies>\\n" > ${RPM_BUILD_ROOT}${_mavendepmapdir}/maven2-depmap.xml
echo -e "</dependencies>\\n" >> ${RPM_BUILD_ROOT}${_mavendepmapdir}/maven2-depmap.xml

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

# You can define a system-wide JVM root here if you're not using the default one
#JAVA_HOME=\$JVM_ROOT/jre

# Options to pass to the java interpreter
#OPTIONS="-Dgnu.java.awt.peer.gtk.Graphics=Graphics2D"
EOF

install -pm 644 etc/java.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/java
install -pm 644 etc/jpackage-release ${RPM_BUILD_ROOT}%{_sysconfdir}/java
install -pm 644 java-utils/* ${RPM_BUILD_ROOT}${_javadir}-utils
install -pm 644 misc/macros.jpackage ${RPM_BUILD_ROOT}%{_sysconfdir}/rpm/macros.d/jpackage.macros
install -m644 %{SOURCE10} -D %{buildroot}%{_sysconfdir}/rpm/macros.d/jpackage.generic.macros
install -m644 %{SOURCE11} -D %{buildroot}%{_sysconfdir}/rpm/macros.d/jpackage.override.mandriva.macros

%{__mkdir_p} ${RPM_BUILD_ROOT}%{_mandir}/man1
install -pm 644 man/* ${RPM_BUILD_ROOT}%{_mandir}/man1
%{__mkdir_p} ${RPM_BUILD_ROOT}${_javadir}-utils/xml
install -pm 644 xml/* ${RPM_BUILD_ROOT}${_javadir}-utils/xml

## BEGIN GCJ/CLASSPATH SPECIFIC ##
%{__mkdir_p} %{buildroot}%{_prefix}/lib/security
%{__cp} -a %{SOURCE1} %{buildroot}%{_prefix}/lib/security/classpath.security.real

%{__mkdir_p} %{buildroot}%{_bindir}
%{__cat} > %{buildroot}%{_bindir}/rebuild-security-providers << EOF
#!/bin/sh
# Rebuild the list of security providers classpath.security

cat %{_prefix}/lib/security/classpath.security \
  | grep -v "^security.provider." \
  > %{_prefix}/lib/security/classpath.security.bak
mv -f %{_prefix}/lib/security/classpath.security.bak \
  %{_prefix}/lib/security/classpath.security

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
    >> %{_prefix}/lib/security/classpath.security
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

%{__mkdir_p} %{buildroot}%{_prefix}/lib
%{__cat} > %{buildroot}%{_prefix}/lib/logging.properties.real << EOF
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
%attr(0755,root,root) %{_bindir}/build-classpath
%attr(0755,root,root) %{_bindir}/build-classpath-directory
%attr(0755,root,root) %{_bindir}/build-jar-repository
%attr(0755,root,root) %{_bindir}/check-binary-files
%attr(0755,root,root) %{_bindir}/clean-binary-files
%attr(0755,root,root) %{_bindir}/create-jar-links
%attr(0755,root,root) %{_bindir}/diff-jars
%attr(0755,root,root) %{_bindir}/find-jar
%attr(0755,root,root) %{_bindir}/jvmjar
%attr(0755,root,root) %{_bindir}/rebuild-jar-repository
%attr(0755,root,root) %{_bindir}/rebuild-security-providers 
%config(noreplace) %{_sysconfdir}/maven/maven2-depmap.xml
%{_mandir}/man1/build-classpath.1*
%{_mandir}/man1/build-jar-repository.1*
%{_mandir}/man1/diff-jars.1*
%{_mandir}/man1/rebuild-jar-repository.1*
%dir %{_sysconfdir}/java
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
${_javadir}-utils/*
%config(noreplace) %{_sysconfdir}/java/jpackage-release
%config(noreplace) %{_sysconfdir}/java/java.conf
%config(noreplace) %{_sysconfdir}/java/font.properties
%{_sysconfdir}/rpm/macros.d/jpackage.*macros
%dir %{_prefix}/lib/security
%{_prefix}/lib/security/classpath.security.real
%dir %{_sysconfdir}/java/security
%dir %{_sysconfdir}/java/security/security.d
%{_sysconfdir}/java/security/security.d/*
%{_prefix}/lib/logging.properties.real
%dir %{_javadir}/gcj-endorsed
EOF

chmod 644 doc/* etc/httpd-javadoc.conf

%clean
rm -rf $RPM_BUILD_ROOT


%post
if test -f "%{_libdir}/rpm/rpmrc" && egrep -q '^macrofiles:.*%{_sysconfdir}/rpm/macros\.jpackage' "%{_libdir}/rpm/rpmrc"; then
  %{__perl} -pi -e \
    's,^(macrofiles:.*):%{_sysconfdir}/rpm/macros\.jpackage,$1,' "%{_libdir}/rpm/rpmrc"
fi

%if 0
%create_ghostfile %{_prefix}/lib/security/classpath.security root root 644
%endif
%{__cp} -af %{_prefix}/lib/security/classpath.security.real %{_prefix}/lib/security/classpath.security
%{__cp} -af %{_prefix}/lib/logging.properties.real %{_prefix}/lib/logging.properties
if [ -x %{_bindir}/rebuild-security-providers ]; then
  %{_bindir}/rebuild-security-providers
fi

%triggerin -- libgcj7-base
%{__cp} -af %{_prefix}/lib/security/classpath.security.real %{_prefix}/lib/security/classpath.security
%{__cp} -af %{_prefix}/lib/logging.properties.real %{_prefix}/lib/logging.properties

%triggerpostun -- libgcj7-base
%{__cp} -af %{_prefix}/lib/security/classpath.security.real %{_prefix}/lib/security/classpath.security
%{__cp} -af %{_prefix}/lib/logging.properties.real %{_prefix}/lib/logging.properties
# caused by triggerin:
%{__rm} -f %{_prefix}/lib/security/classpath.security.rpmsave

%files -f %{name}-%{version}.files
%defattr(-,root,root,-)
%doc LICENSE.txt doc/* etc/httpd-javadoc.conf


