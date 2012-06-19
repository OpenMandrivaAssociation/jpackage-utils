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

%define distver 1.7
%define section free

%define	gcj_support 0
%define sdk_provider	openjdk
%ifnarch %{ix86} x86_64
%define sdk_provider	gcj
%endif

%define _enable_debug_packages %{nil}
%define debug_package %{nil}

Name:           jpackage-utils
Version:        1.7.5
Release:        4.14
Group:          Development/Java
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

Requires:       coreutils
Requires:       javapackages-tools

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
rm -rf %{buildroot}

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

install -dm 755 %{buildroot}${_jvmdir}
install -dm 755 %{buildroot}${_jvmjardir}
install -dm 755 %{buildroot}${_jvmprivdir}
install -dm 755 %{buildroot}${_jvmlibdir}
install -dm 755 %{buildroot}${_jvmdatadir}
install -dm 755 %{buildroot}${_jvmsysconfdir}
install -dm 755 %{buildroot}${_jvmcommonlibdir}
install -dm 755 %{buildroot}${_jvmcommondatadir}
install -dm 755 %{buildroot}${_jvmcommonsysconfdir}
install -dm 755 %{buildroot}${_javadir}
install -dm 755 %{buildroot}${_javadir}-utils
install -dm 755 %{buildroot}${_javadir}-ext
install -dm 755 %{buildroot}${_javadir}-{1.3.1,1.4.0,1.4.1,1.4.2}
install -dm 755 %{buildroot}${_javadir}-{1.5.0,1.6.0,1.7.0}
install -dm 755 %{buildroot}${_jnidir}
install -dm 755 %{buildroot}${_jnidir}-ext
install -dm 755 %{buildroot}${_jnidir}-{1.3.1,1.4.0,1.4.1,1.4.2}
install -dm 755 %{buildroot}${_jnidir}-{1.5.0,1.6.0,1.7.0}
install -dm 755 %{buildroot}${_javadocdir}
install -dm 755 %{buildroot}${_mavenpomdir}
install -dm 755 %{buildroot}${_mavendepmapfragdir}

pushd bin
for i in *; do
	install -pm 755 -D $i %{buildroot}%{_bindir}/$i
done
popd
install -m644 etc/font.properties -D %{buildroot}%{_sysconfdir}/java/font.properties

# Install abs2rel scripts
install -pm 755 %{SOURCE3}  %{buildroot}%{_javadir}-utils
install -pm 644 %{SOURCE4} %{buildroot}%{_javadir}-utils

# Create an initial (empty) depmap
echo -e "<dependencies>\\n" \
  > %{buildroot}${_mavendepmapdir}/maven2-depmap.xml
echo -e "</dependencies>\\n" \
  >> %{buildroot}${_mavendepmapdir}/maven2-depmap.xml

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

install -pm 644 etc/java.conf %{buildroot}%{_sysconfdir}/java/java.conf
install -pm 644 etc/jpackage-release -D %{buildroot}%{_sysconfdir}/java/jpackage-release
install -pm 644 java-utils/java-functions -D %{buildroot}${_javadir}-utils
install -m644 misc/macros.jpackage -D %{buildroot}%{_sysconfdir}/rpm/macros.d/jpackage.macros
install -m644 %{SOURCE10} -D %{buildroot}%{_sysconfdir}/rpm/macros.d/jpackage.generic.macros
install -m644 %{SOURCE11} -D %{buildroot}%{_sysconfdir}/rpm/macros.d/jpackage.override.mandriva.macros

%{__mkdir_p} %{buildroot}%{_mandir}/man1
install -pm 644 man/* %{buildroot}%{_mandir}/man1
%{__mkdir_p} %{buildroot}${_javadir}-utils/xml
install -pm 644 xml/* %{buildroot}${_javadir}-utils/xml

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
touch 2000-gnu.javax.crypto.jce.GnuCryptojava
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
