# Download information:
# svn co https://cloudcity.svn.sourceforge.net/svnroot/cloudcity
# cd cloudcity && find . -name .svn |xargs rm -rf && cd ..
# tar -caf cloudcity-0.1.624svn.tar.lzma cloudcity


%define svn	708
%define srcname	cloudcity

Name: kde4-style-bespin
Summary: Bespin is a native style for QT/ KDE4
Version: 0.1
Release: %mkrel 0.%{svn}svn.1
Source0: %{srcname}-%{version}.%{svn}svn.tar.lzma
URL: http://cloudcity.sourceforge.net/
Group: Graphical desktop/KDE
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
License: LGPLv3+
BuildRequires: kdebase4-workspace-devel
Obsoletes: kde4-kwin-style-bespin < %version-%release
Obsoletes: kde4-theme-bespin
Suggests: plasma-applet-xbar
#< %version-%release

%description
Bespin is a native style for QT/ KDE4

The name is nothing about Quantum Mechanics, but just refers to the
Cloud City from StarWars - Episode V "The Empire Strikes Back"

Some presets can be found in /usr/share/doc/%{name}


%files
%defattr(-,root,root)
%doc README INSTALL COPYING COPYING.LIB presets/
%_kde_bindir/bespin
%_kde_libdir/qt4/plugins/styles/libbespin.so
%_kde_libdir/kde4/kstyle_bespin_config.so
%_kde_libdir/kde4/kwin3_bespin.so
%_kde_libdir/kde4/kwin_bespin_config.so
%_kde_appsdir/kwin/bespin.desktop
%_kde_appsdir/kstyle/themes/bespin.themerc
%_mandir/man1/bespin.1.lzma

#---------------------------------------------------------------------

%package -n plasma-applet-xbar
Summary:	Xbar applet for Bespin style
Group:		Graphical desktop/KDE
Requires:	%{name}
%description -n plasma-applet-xbar
The XBar is a Client/Server approach to a "mac-a-like" global menubar.
Currently it's only used by the Bespin Style to post apply clients to
Qt4 based applications.
The only currently existing Server is a Plasmoid.

%files -n plasma-applet-xbar
%defattr(-,root,root)
%doc XBar/xbar.txt
%_kde_libdir/kde4/plasma_applet_xbar.so
%_kde_services/plasma-applet-xbar.desktop

#---------------------------------------------------------------------

%package -n bespin-bash-completion
Summary:	Bash Completion for bespin
Group:		Development/Other
Requires:	bash-completion
%description -n bespin-bash-completion
Bash completion for the "bespin" tool, written by Franz Fellner

%files -n bespin-bash-completion
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/bash_completion.d/bespin-compl

#--------------------------------------------------------------------

%prep
%setup -q -n %{srcname}

%build
%cmake_kde4
%make

%install
%__rm -rf %{buildroot}
%{makeinstall_std} -C build

mkdir -p %{buildroot}/%{_sysconfdir}/bash_completion.d
mkdir -p %{buildroot}/%_kde_mandir/man1
cp man/bespin.1 %{buildroot}/%_kde_mandir/man1
lzma %{buildroot}/%_kde_mandir/man1/bespin.1
cp extras/bespin-compl %{buildroot}/%{_sysconfdir}/bash_completion.d

%clean 
%__rm -rf %{buildroot}