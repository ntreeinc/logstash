# Inspired by https://github.com/russellsimpkins/varnish-mmdb-vmod/blob/master/libmaxminddb.spec
# https://www.redhat.com/archives/rpm-list/2001-December/msg00200.html
#%define checkoutName %{name}-%{version}-%{_build_arch}-%{suffix: %{dist}}
%define checkoutName %{name}-%{version}
%define localsource %{_topdir}/../..

Name:           logstash
#This version number MUST match the logstash-${version}.tar.gz version number
Version:        2.3.4
#If you wish to publish a new snapshot to nexus you MUST up the release number
#Release:        1%{?dist}
Release:        8
Summary:        Install logstash as a service
Group:          Applications/Communications
License:        MIT
BuildArch:      noarch
URL:            https://ntree.com
Source0:	https://download.elastic.co/logstash/logstash/logstash-2.3.4.tar.gz
Patch0:		logstash-patterns.patch
AutoReqProv: no
Requires(pre): /usr/sbin/useradd, /usr/sbin/groupadd, /usr/bin/getent

#BuildRequires:  
#Requires:       httpd

%pre
#/usr/bin/getent passwd logstash || /usr/sbin/useradd logstash
/usr/bin/getent group logstash || /usr/sbin/groupadd -r logstash
/usr/bin/getent passwd logstash || /usr/sbin/useradd -r -d /opt/logstash -s /sbin/nologin -g logstash logstash

%description
Used for installing logstash as a service on older systems which do not work with the given installation options

%prep
%setup -q -c -n %{name}-%{version}
mv %{name}-%{version} %{name}
mkdir -p opt
mv %{name} opt
#rm -rf $RPM_BUILD_DIR/logstash
#zcat $RPM_SOURCE_DIR/%{name}-%{logstashversion}.tar.gz | tar -xvf -
#mv %{name}-%{logstashversion} %{name}
#mkdir opt
#cp %{name}-%{logstashversion} opt
%patch0 -p0
#%patch0 -p8

%build
echo hello build $PWD
#env


%install
echo $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT
src="%{localsource}"
cd "${src}"
make install DESTDIR="%{buildroot}"
cd $RPM_BUILD_ROOT
#if logstash user exists do nothing, if not then add a logstash user (logstash group added automatically)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/opt/logstash
/etc/defaults/logstash
/etc/init.d/logstash

%doc

%post
#service httpd configtest && service httpd graceful

%changelog
