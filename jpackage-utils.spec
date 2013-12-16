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
%global gcj_support 1

%global distver 1.7
%global section free

%global debug_package %{nil}

Name:           jpackage-utils
Version:        1.7.5
Release:        26%{?dist}
Epoch:          0
Summary:        JPackage utilities
License:        BSD
URL:            http://www.jpackage.org/
BuildArch:      noarch
Source0:        %{name}-%{version}.tar.bz2
Source1:        %{name}-README
Source2:        abs2rel.sh
Source3:        abs2rel.lua
Patch1:         %{name}-own-mavendirs.patch
Patch2:         %{name}-prefer-jre.patch
Patch3:         %{name}-set-classpath.patch
Patch5:         %{name}-build-classpath-symlink-fix.patch
Patch6:         %{name}-update-maven-depmap.patch


Requires:       coreutils
Requires:       javapackages-tools
# abs2rel is implemented in lua
Requires:       lua

# for noarch->arch change
Obsoletes:      %{name} < 0:1.7.5-9

%description
Utilities for the JPackage Project <http://www.jpackage.org/>.

It contains also the License, man pages, documentation, XSL files of general
use with maven2, a header file for spec files, etc. Please See
the %{_docdir}/%{name}-%{version}/%{name}-README file for more
information.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1
%patch6

cp -p %{SOURCE1} %{SOURCE2} %{SOURCE3} .

%build
echo "JPackage release %{distver} (%{distribution}) for %{buildarch}" \
 > etc/jpackage-release


%install
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

install -dm 755 ${RPM_BUILD_ROOT}%{_bindir}
install -dm 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/{java,rpm}
%if %{gcj_support}
install -dm 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/java/security
install -dm 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/java/security/security.d
%endif
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
install -dm 755 ${RPM_BUILD_ROOT}${_javadir}-{1.5.0,1.6.0,1.7.0}
install -dm 755 ${RPM_BUILD_ROOT}${_jnidir}
install -dm 755 ${RPM_BUILD_ROOT}${_jnidir}-ext
install -dm 755 ${RPM_BUILD_ROOT}${_jnidir}-{1.5.0,1.6.0,1.7.0}
install -dm 755 ${RPM_BUILD_ROOT}${_javadocdir}
install -dm 755 ${RPM_BUILD_ROOT}${_mavenpomdir}
install -dm 755 ${RPM_BUILD_ROOT}${_mavendepmapdir}
install -dm 755 ${RPM_BUILD_ROOT}${_mavendepmapfragdir}

install -pm 755 bin/* ${RPM_BUILD_ROOT}%{_bindir}
install -pm 644 etc/font.properties ${RPM_BUILD_ROOT}%{_sysconfdir}/java

# Install abs2rel scripts
install -pm 755 abs2rel.sh  ${RPM_BUILD_ROOT}%{_javadir}-utils
install -pm 644 abs2rel.lua ${RPM_BUILD_ROOT}%{_javadir}-utils

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

install -pm 644 etc/java.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/java
install -pm 644 etc/jpackage-release ${RPM_BUILD_ROOT}%{_sysconfdir}/java
install -pm 644 java-utils/* ${RPM_BUILD_ROOT}${_javadir}-utils
install -pm 644 misc/macros.jpackage ${RPM_BUILD_ROOT}%{_sysconfdir}/rpm
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_mandir}/man1
install -pm 644 man/* ${RPM_BUILD_ROOT}%{_mandir}/man1
%{__mkdir_p} ${RPM_BUILD_ROOT}${_javadir}-utils/xml
install -pm 644 xml/* ${RPM_BUILD_ROOT}${_javadir}-utils/xml


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
%dir ${_mavenpomdir}
%dir ${_mavendepmapdir}
%dir ${_mavendepmapfragdir}
${_javadir}-utils/*
%config %{_sysconfdir}/java/jpackage-release
%config(noreplace) %{_sysconfdir}/java/java.conf
%config(noreplace) %{_sysconfdir}/java/font.properties
%{_sysconfdir}/rpm/macros.jpackage
%config(noreplace) ${_mavendepmapdir}/maven2-depmap.xml
EOF

%files -f %{name}-%{version}.files
%doc %{name}-README LICENSE.txt HEADER.JPP doc/* etc/httpd-javadoc.conf
