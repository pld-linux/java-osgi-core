#
# Conditional build:
%bcond_with	javadoc		# don't build javadoc

%define		srcname	osgi.core
%include	/usr/lib/rpm/macros.java
Summary:	OSGi Service Platform Core API (Companion Code)
Name:		java-osgi-core
Version:	4.3.1
Release:	1
License:	Apache v2.0
Group:		Libraries/Java
URL:		http://www.osgi.org/Specifications/HomePage
Source0:	http://www.osgi.org/download/r4v43/osgi.core-%{version}.jar
# Source0-md5:	5a9d55c73d7f477cfbcb8d7adfec3deb
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
%if %(locale -a | grep -q '^en_US$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
Requires:	jpackage-utils
Requires:	jre
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OSGi Service Platform Release 4 Core Interfaces and Classes.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
API documentation for %{name}.

%prep
%setup -qc

%build
install -d target

# source code not US-ASCII
export LC_ALL=en_US

topdir=${PWD:-$(pwd)}
cd OSGI-OPT/src
%javac -cp $CLASSPATH $(find -name '*.java')
%jar cfm $topdir/target/%{srcname}-%{version}.jar $topdir/META-INF/MANIFEST.MF $(find -name '*.class')

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p target/%{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a target/site/api*/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc LICENSE
%{_javadir}/osgi.core.jar
%{_javadir}/osgi.core-%{version}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
