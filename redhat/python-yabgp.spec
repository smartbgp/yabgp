%{!?__python2:        %global __python2 /usr/bin/python2}
%{!?python2_sitelib:  %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           python-yabgp
Version:        0.1.4
Release:        0%{?dist}
Summary:        Yet Another BGP (Border Gateway Protocol) Python Implementation

Group:          Development/Libraries
License:        APLv2
URL:            http://yabgp.readthedocs.org/en/latest/
Source0:        https://github.com/smartbgp/yabgp/archive/v%{version}.tar.gz
Source1:        yabgp.service
BuildArch:      noarch
Provides:       yabgp-libs

BuildRequires:  python-setuptools
Requires:       python2 >= 2.6
#Requires:       python-pbr >= 0.5.21, python-pymongo >= 3.0.3, python-netaddr >= 0.7.12, python-flask >= 0.10.1, python-pika >= 0.9.14, python-flask-httpauth >= 2.5.0, python-twisted >= 15.0.0, python-oslo-config >= 1.6.0

%description
YABGP python module

%package -n yabgp
Summary:        Yet Another BGP (Border Gateway Protocol)
Group:          Applications/Internet
BuildRequires:  systemd-units
Requires:       systemd, yabgp-libs == %{version}

%description -n yabgp
YABGP is a yet another Python implementation for BGP Protocol. It can be used 
to establish BGP connections with all kinds of routers (include real 
Cisco/HuaWei/Juniper routers and some router simulators like GNS3) and 
receive/parse BGP messages for future analysis.

%prep
%autosetup -n yabgp-%{version}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --root ${RPM_BUILD_ROOT}

# fix file locations
mv ${RPM_BUILD_ROOT}/usr/bin ${RPM_BUILD_ROOT}%{_sbindir}
mv ${RPM_BUILD_ROOT}/usr/etc  ${RPM_BUILD_ROOT}/%{_sysconfdir}

install -d %{buildroot}/%{_unitdir}
install %{SOURCE1} %{buildroot}/%{_unitdir}/

%post -n yabgp
%systemd_post yabgp.service

%preun -n yabgp
%systemd_preun yabgp.service

%postun -n yabgp
%systemd_postun_with_restart yabgp.service

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*
%doc LICENSE README.rst requirements.txt

%files -n yabgp
%defattr(-,root,root,-)
%attr(755, root, root) %{_sbindir}/yabgpd
%dir %{_sysconfdir}/yabgp
%attr(744, root, root) %{_sysconfdir}/yabgp/*
%{_unitdir}/yabgp.service
%doc LICENSE README.rst

%changelog
