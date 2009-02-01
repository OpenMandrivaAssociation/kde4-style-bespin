# Download information:
# svn co https://cloudcity.svn.sourceforge.net/svnroot/cloudcity
# tar cf cloudcity-0.1.386svn.tar cloudcity
# bzip2 cloudcity-0.1.386svn.tar

%define svn	398
%define srcname	cloudcity

Name: kde4-style-bespin
Summary: Bespin is a native style for QT/ KDE4
Version: 0.1
Release: %mkrel 0.%{svn}svn.1
Source0: %{srcname}-%{version}.%{svn}svn.tar.bz2
URL: http://cloudcity.sourceforge.net/
Group: Graphical desktop/KDE
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
License: LGPLv3+

BuildRequires: kdebase4-workspace-devel
Obsoletes: kde4-kwin-style-bespin < %version-%release
Obsoletes: kde4-theme-bespin 
#< %version-%release

%description
Bespin is a native style for QT/ KDE4

The name is nothing about Quantum Mechanics, but just refers to the Cloud City
from StarWars - Episode V "The Empire Strikes Back"


%files
%defattr(-,root,root)
%doc README
%{_kde_bindir}/bespin
%{_kde_libdir}/qt4/plugins/styles/libbespin.so
%{_kde_libdir}/kde4/plasma_applet_xbar.so
%{_kde_libdir}/kde4/kstyle_bespin_config.so
%{_kde_libdir}/kde4/kwin3_bespin.so
%{_kde_libdir}/kde4/kwin_bespin_config.so
%{_kde_appsdir}/kwin/bespin.desktop
%{_kde_appsdir}/kstyle/themes/bespin.themerc
%{_kde_datadir}/kde4/services/plasma-applet-xbar.desktop

#--------------------------------------------------------------------

%prep
%setup -q -n %{srcname}

%build
%cmake_kde4
%make

%install
rm -rf %{buildroot}
cd build
%makeinstall_std

%clean 
rm -rf %{buildroot}
