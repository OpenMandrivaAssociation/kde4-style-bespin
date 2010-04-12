# Download information:
# svn co https://cloudcity.svn.sourceforge.net/svnroot/cloudcity
# cd cloudcity && find . -name .svn |xargs rm -rf && cd ..
# tar -caf cloudcity-0.1.1068svn.tar.lzma cloudcity


%define svn	1068
%define srcname	cloudcity
%define enable_translucient 1
Name:		kde4-style-bespin
Summary:	Bespin is a native style for QT/ KDE4
Version:	0.1
Release:	%mkrel 0.%{svn}svn.1
Source0:	%{srcname}-%{version}.%{svn}svn.tar.lzma
# Patch0 is here to fix the default comment in icon theme & finally avoid to source the config file
# since we're providing the necessary data directly in the script
Source1:	screenshot.png.bz2
Source2:	Preview.png.bz2
Patch0:		bespin-svn-mdv-fix-icon-and-comment-in-kde-icons-scripts.patch
Patch1:		bespin-svn-mdv-fix-ksplash-themerc.patch
URL:		http://cloudcity.sourceforge.net/
Group:		Graphical desktop/KDE
License:	LGPLv2
BuildRequires:	kdebase4-workspace-devel
# needed to generate the ksplash
BuildRequires:	imagemagick
# need to generate the icons pack
BuildRequires:	inkscape
Obsoletes:	kde4-kwin-style-bespin < %version-%release
Obsoletes:	kde4-theme-bespin
Suggests:	kde4-style-bespin-ksplash
Suggests:	kde4-style-bespin-kdm
Suggests:	kde4-style-bespin-icons
Suggests:	plasma-applet-xbar

%description
Bespin is a native style for QT/ KDE4

The name is nothing about Quantum Mechanics, but just refers to the
Cloud City from StarWars - Episode V "The Empire Strikes Back"

Some presets can be found in /usr/share/doc/%{name}


%files
%defattr(-,root,root)
%doc README INSTALL COPYING COPYING.LIB presets/
%_kde_bindir/bespin
%_kde_libdir/libQtBespin.so
%_kde_libdir/qt4/plugins/styles/libbespin.so
%_kde_libdir/kde4/kstyle_bespin_config.so
%_kde_libdir/kde4/kwin3_bespin.so
%_kde_libdir/kde4/kwin_bespin_config.so
%_kde_appsdir/kwin/bespin.desktop
%_kde_appsdir/kstyle/themes/bespin.themerc
%_mandir/man1/bespin.1.lzma

#---------------------------------------------------------------------

%package -n 	plasma-applet-xbar
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

%package -n 	bespin-bash-completion
Summary:	Bash Completion for bespin
Group:		Development/Other
Requires:	bash-completion
%description -n bespin-bash-completion
Bash completion for the "bespin" tool, written by Franz Fellner

%files -n bespin-bash-completion
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/bash_completion.d/bespin-compl

#--------------------------------------------------------------------

%package	ksplash
Summary:	Bespin ksplash theme
Group:		Graphical desktop/KDE
%description	ksplash
This package provide a bespin kdm theme

%files	ksplash
%defattr(-,root,root)
%_kde_datadir/apps/ksplash/Themes/Bespin/

#--------------------------------------------------------------------

%package	kdm
Summary:	Bespin kdm theme
Group:		Graphical desktop/KDE
%description	kdm
This package provide a Bespin kdm theme

%files	kdm
%defattr(-,root,root)
%_kde_datadir/apps/kdm/themes/Bespin/

#--------------------------------------------------------------------

%package	icons
Summary:	Bespin icons theme
Group:		Graphical desktop/KDE
%description	icons
This package provide a Bespin icons theme

%files	icons
%defattr(-,root,root)
%_kde_datadir/icons/Bespin/

#--------------------------------------------------------------------

%prep
%setup -q -n %{srcname}
%patch0 -p 0
%patch1 -p 0


%build
%if %{enable_translucient}
 %cmake_kde4 -DENABLE_ARGB=on
%else 
 %cmake_kde4
%endif 

%make

%install
%__rm -rf %{buildroot}
%{makeinstall_std} -C build

# Installing necessary files for bespin-completion
%__mkdir -p %{buildroot}/%{_sysconfdir}/bash_completion.d
%__mkdir -p %{buildroot}/%_kde_mandir/man1
%__cp man/bespin.1 %{buildroot}/%_kde_mandir/man1
lzma %{buildroot}/%_kde_mandir/man1/bespin.1
%__cp extras/bespin-compl %{buildroot}/%{_sysconfdir}/bash_completion.d

# Installing necessary files for kdm bespin theme
%__mkdir -p %{buildroot}/%_kde_datadir/apps/kdm/themes/Bespin
cp -rf kdm/* %{buildroot}/%_kde_datadir/apps/kdm/themes/Bespin
%__bzip2 -dc %{SOURCE1} > %{buildroot}/%_kde_datadir/apps/kdm/themes/Bespin/screenshot.png

# Installing necessary files for ksplash bespin theme
%__mkdir -p %{buildroot}/%_kde_datadir/apps/ksplash/Themes/Bespin
cd ksplash
./generate.sh 600 400
./generate.sh 800 600
./generate.sh 1024 768
./generate.sh 1280 1024
./generate.sh 1600 1200
./generate.sh 1680 1050
./generate.sh 1920 1200
%__bzip2 -dc %{SOURCE2} > %{buildroot}/%_kde_datadir/apps/ksplash/Themes/Bespin/Preview.png
%__cp -rf . %{buildroot}/%_kde_datadir/apps/ksplash/Themes/Bespin/
cd ..

# Creating the icons package
cd icons
./generate_kde_icons.sh
%__mkdir -p %{buildroot}/%_kde_datadir/icons/
%__mv Bespin %{buildroot}/%_kde_datadir/icons/
cd ..

%clean 
%__rm -rf %{buildroot}
