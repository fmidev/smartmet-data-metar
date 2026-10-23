%define smartmetroot /smartmet

Name:           smartmet-data-metar
Version:        26.10.23
Release:        1%{?dist}.fmi
Summary:        SmartMet Data METAR
Group:          System Environment/Base
License:        MIT
URL:            https://github.com/fmidev/smartmet-data-metar
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       smartmet-qdtools
Requires:       lbzip2
Requires:       wget
Requires:       util-linux

%description
Downloads METAR observations from NOAA (tgftp.nws.noaa.gov) and converts
them to SmartMet querydata for the data server and the editor.

%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT

mkdir -p .%{smartmetroot}/cnf/cron/{cron.d,cron.hourly}
mkdir -p .%{smartmetroot}/data/incoming/metar
mkdir -p .%{smartmetroot}/data/gts/metar/world/querydata
mkdir -p .%{smartmetroot}/editor/in
mkdir -p .%{smartmetroot}/tmp/data/metar
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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,smartmet,smartmet,-)
%config(noreplace) %{smartmetroot}/cnf/cron/cron.d/metar.cron
%config(noreplace) %attr(0755,smartmet,smartmet) %{smartmetroot}/cnf/cron/cron.hourly/clean_data_metar
%{smartmetroot}/*

%changelog
* Fri Oct 23 2026 Mikko Visa <mikko.visa@fmi.fi> 26.10.23-1.el10.fmi
- Require smartmet-qdtools on all EL versions (was el7 only, so el8+
  builds did not pull in metar2qd)
- Replace procmail lockfile (undeclared dependency) with flock from util-linux
- Download from NOAA over https
- Harden get_metar.sh: switch to #!/bin/bash, enable set -uo pipefail,
  quote every variable expansion, replace legacy backticks with $(),
  guard TERM expansion, and clean tmp on EXIT via trap
- Create data/gts/metar/world/querydata and tmp/data/metar in spec
- Drop empty spec stanzas, write real %description
- Add CI workflow that builds RPMs for Rocky 8/9/10
* Fri Nov 10 2017 Mikko Rauhala <mikko.rauhala@fmi.fi> 17.11.10-1.el7.fmi
- Added lock file to prevent parallel runs
* Wed Nov 8 2017 Mikko Rauhala <mikko.rauhala@fmi.fi> 17.11.8-2.el7.fmi
- Fixed missing logfile location
* Wed Nov 8 2017 Mikko Rauhala <mikko.rauhala@fmi.fi> 17.11.8-1.el7.fmi
- Renamed script, improved logging
* Thu Apr 20 2017 Mikko Rauhala <mikko.rauhala@fmi.fi> 17.4.20-1.el7.fmi
- Updated script
* Wed Jan 18 2017 Mikko Rauhala <mikko.rauhala@fmi.fi> 17.1.18-1.el7.fmi
- Updated dependencies
* Wed Jun 3 2015 Santeri Oksman <santeri.oksman@fmi.fi> 15.6.3-1.el7.fmi
- RHEL 7 version
* Fri Aug 8 2014 Mikko Rauhala <mikko.rauhala@fmi.fi> 14.8.8-1.el6.fmi
- Initial build 14.8.8
