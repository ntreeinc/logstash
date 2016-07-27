# Inspired by https://github.com/russellsimpkins/varnish-mmdb-vmod/blob/master/libmaxminddb.spec
# https://www.redhat.com/archives/rpm-list/2001-December/msg00200.html
#%define checkoutName %{name}-%{version}-%{_build_arch}-%{suffix: %{dist}}
%define checkoutName %{name}-%{version}
%define localsource %{_topdir}/../..

Name:           logstash
Version:        2.3.4
#Release:        1%{?dist}
Release:        0
Summary:        Salestree Webserver Config
Group:          Applications/Communications
License:        MIT
BuildArch:      noarch
URL:            https://ntree.com
Source0:	https://download.elastic.co/logstash/logstash/logstash-2.3.4.tar.gz
Patch0:		logstash-patterns.patch
AutoReqProv: no

#BuildRequires:  
#Requires:       httpd

%description
First rpm spec file

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
