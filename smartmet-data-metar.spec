%define smartmetroot /smartmet

Name:           smartmet-data-metar
Version:        17.11.10
Release:        1%{?dist}.fmi
Summary:        SmartMet Data METAR
Group:          System Environment/Base
License:        MIT
URL:            https://github.com/fmidev/smartmet-data-metar
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

%{?el6:Requires: smartmet-qdconversion}
%{?el7:Requires: smartmet-qdtools}
Requires:	lbzip2
Requires:       wget

%description
SmartMet Data Ingestion Module for METAR observations

%prep

%build

%pre

%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT

mkdir -p .%{smartmetroot}/cnf/cron/{cron.d,cron.hourly}
mkdir -p .%{smartmetroot}/data/incoming/metar
mkdir -p .%{smartmetroot}/editor/in
mkdir -p .%{smartmetroot}/logs/data
mkdir -p .%{smartmetroot}/run/data/metar/bin

cat > %{buildroot}%{smartmetroot}/cnf/cron/cron.d/metar.cron <<EOF
*/20 * * * * /smartmet/run/data/metar/bin/get_metar.sh
EOF

cat > %{buildroot}%{smartmetroot}/cnf/cron/cron.hourly/clean_data_metar <<EOF
#!/bin/sh
# Clean METAR data
cleaner -maxfiles 2 '_metar.sqd' %{smartmetroot}/data/gts/metar
cleaner -maxfiles 2 '_metar.sqd' %{smartmetroot}/editor/in
EOF

install -m 755 %_topdir/SOURCES/smartmet-data-metar/get_metar.sh %{buildroot}%{smartmetroot}/run/data/metar/bin/

%post

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,smartmet,smartmet,-)
%config(noreplace) %{smartmetroot}/cnf/cron/cron.d/metar.cron
%config(noreplace) %attr(0755,smartmet,smartmet) %{smartmetroot}/cnf/cron/cron.hourly/clean_data_metar
%{smartmetroot}/*

%changelog
* Fri Nov 10 2017 Mikko Rauhala <mikko.rauhala@fmi.fi> 17.11.10-1%{?dist}.fmi
- Added lock file to prevent parallel runs
* Wed Nov 8 2017 Mikko Rauhala <mikko.rauhala@fmi.fi> 17.11.8-2%{?dist}.fmi
- Fixed missing logfile location
* Wed Nov 8 2017 Mikko Rauhala <mikko.rauhala@fmi.fi> 17.11.8-1%{?dist}.fmi
- Renamed script, improved logging
* Thu Apr 20 2017 Mikko Rauhala <mikko.rauhala@fmi.fi> 17.4.20-1%{?dist}.fmi
- Updated script
* Wed Jan 18 2017 Mikko Rauhala <mikko.rauhala@fmi.fi> 17.1.18-1%{?dist}.fmi
- Updated dependencies
* Wed Jun 3 2015 Santeri Oksman <santeri.oksman@fmi.fi> 15.6.3-1%{?dist}.fmi
- RHEL 7 version
* Fri Aug 8 2014 Mikko Rauhala <mikko.rauhala@fmi.fi> 14.8.8-1%{?dist}.fmi
- Initial build 14.8.8
