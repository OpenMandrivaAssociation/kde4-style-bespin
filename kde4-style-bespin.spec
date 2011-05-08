# Download information:
# svn export https://cloudcity.svn.sourceforge.net/svnroot/cloudcity
# tar -caf cloudcity-0.1.1355svn.tar.xz cloudcity


%define svn	1355
%define srcname	cloudcity
%define enable_translucient 1
%define tibanna_ksplash 0
%define tibanna_kdm 1

Name:		kde4-style-bespin
Summary:	Bespin is a native style for QT/ KDE4
Version:	0.1
Release:	%mkrel 0.%{svn}svn.1
Source0:	%{srcname}-%{version}.%{svn}svn.tar.xz
# Patch0 is here to fix the default comment in icon theme & finally avoid to source the config file
# since we're providing the necessary data directly in the script
Source1:	screenshot.png.bz2
Patch0:		bespin-svn-mdv-fix-icon-and-comment-in-kde-icons-scripts.patch
Patch1:		bespin-svn-mga-use-scale-for-background-in-ksplash-generation.patch
URL:		http://cloudcity.sourceforge.net/
Group:		Graphical desktop/KDE
License:	LGPLv2
BuildRequires:	kdebase4-workspace-devel
# needed to generate the ksplash
BuildRequires:	imagemagick
# need to generate the icons pack
BuildRequires:	inkscape
BuildRequires:	bash
Obsoletes:	kde4-kwin-style-bespin < %version-%release
Obsoletes:	kde4-theme-bespin
Suggests:	kde4-style-bespin-ksplash
Suggests:	kde4-style-bespin-kdm
Suggests:	kde4-style-bespin-icons
Suggests:	plasma-applet-xbar
%if %tibanna_ksplash
Suggests:	kde4-style-tibanna-ksplash
%endif
%if %tibanna_kdm
Suggests:	kde4-style-tibanna-kdm
%endif


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
%_mandir/man1/bespin.1.*

#---------------------------------------------------------------------

%package -n 	plasma-applet-xbar
Summary:	Xbar applet for Bespin style
Group:		Graphical desktop/KDE
Requires:	kdebase4-workspace
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
Requires:	bash
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
Requires:	kdebase4-workspace
%description	ksplash
This package provide a bespin ksplash theme

%files	ksplash
%defattr(-,root,root)
%_kde_datadir/apps/ksplash/Themes/Bespin/

#---------------------------------------------------------------------

%package	kdm
Summary:	Bespin kdm theme
Group:		Graphical desktop/KDE
Requires:	kdm
%description	kdm
This package provide a Bespin kdm theme

%files	kdm
%defattr(-,root,root)
%_kde_datadir/apps/kdm/themes/Bespin/

#--------------------------------------------------------------------
%if %tibanna_ksplash

%package -n	kde4-style-tibanna-ksplash
Summary:	Tibanna ksplash theme
Group:		Graphical desktop/KDE
Requires:	kdebase4-workspace
%description -n kde4-style-tibanna-ksplash
This package provide the tibanna ksplash theme

%files -n kde4-style-tibanna-ksplash
%defattr(-,root,root)
%_kde_datadir/apps/ksplash/Themes/tibanna/
%endif
%if %tibanna_kdm
#--------------------------------------------------------------------

%package -n kde4-style-tibanna-kdm
Summary:	Tibanna kdm theme
Group:		Graphical desktop/KDE
Requires:	kdm
%description -n kde4-style-tibanna-kdm
This package provide the tibanna kdm theme

%files -n kde4-style-tibanna-kdm
%defattr(-,root,root)
%_kde_datadir/apps/kdm/themes/tibanna/
#--------------------------------------------------------------------
%endif

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
%patch0 -p0
%patch1 -p0

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
%__install -m644 man/bespin.1 %{buildroot}/%_kde_mandir/man1
lzma %{buildroot}/%_kde_mandir/man1/bespin.1
%__install extras/bespin-compl %{buildroot}/%{_sysconfdir}/bash_completion.d

# Installing necessary files for kdm bespin theme
%__mkdir -p %{buildroot}/%_kde_datadir/apps/kdm/themes/Bespin/
%__install -m 644 kdm/*.png %{buildroot}/%_kde_datadir/apps/kdm/themes/Bespin
%__install -m 644 kdm/*.jpg %{buildroot}/%_kde_datadir/apps/kdm/themes/Bespin
%__install -m 644 kdm/*.xml %{buildroot}/%_kde_datadir/apps/kdm/themes/Bespin
%__install -m 644 kdm/KdmGreeterTheme.desktop %{buildroot}/%_kde_datadir/apps/kdm/themes/Bespin

%__bzip2 -dc %{SOURCE1} > %{buildroot}/%_kde_datadir/apps/kdm/themes/Bespin/screenshot.png





# Installation of bespin ksplash theme
%__mkdir -p %{buildroot}/%_kde_datadir/apps/ksplash/Themes/Bespin
pushd ksplash
./generate.sh 1920 1440
./generate.sh 1920 1200
./generate.sh 1920 1080
./generate.sh 1280 1024
./generate.sh 1024 600
for i in "1024x600" "1280x1024" "1920x1080" "1920x1200" "1920x1440";
do
%__install -d %{buildroot}/%_kde_datadir/apps/ksplash/Themes/Bespin/$i
%__install -m 644 -t %{buildroot}/%_kde_datadir/apps/ksplash/Themes/Bespin/$i  $i/background.png
done

%__install -m 644 -t %{buildroot}/%_kde_datadir/apps/ksplash/Themes/Bespin/1920x1440/ 1920x1440/description.txt
%__install -m 644 -t %{buildroot}/%_kde_datadir/apps/ksplash/Themes/Bespin/ *.png
%__install -m 644 -t  %{buildroot}/%_kde_datadir/apps/ksplash/Themes/Bespin/ Theme.rc
popd
%if %tibanna_ksplash
# Installation of tibanna ksplash theme
pushd ksplash/tibanna
%__mkdir -p %{buildroot}/%_kde_datadir/apps/ksplash/Themes/tibanna
./generate.sh 1920 1440
./generate.sh 1920 1200
./generate.sh 1920 1080
./generate.sh 1280 1024
./generate.sh 1024 600
for i in "1024x600" "1280x1024" "1920x1080" "1920x1200" "1920x1440";
do
%__install -d %{buildroot}/%_kde_datadir/apps/ksplash/Themes/tibanna/$i
%__install  -m 644 -t %{buildroot}/%_kde_datadir/apps/ksplash/Themes/tibanna/$i  $i/background.png
done

%__install  -m 644 -t %{buildroot}/%_kde_datadir/apps/ksplash/Themes/tibanna/1920x1440/ 1920x1440/description.txt
%__install  -m 644 -t %{buildroot}/%_kde_datadir/apps/ksplash/Themes/tibanna/ *.png
%__install  -m 644 -t %{buildroot}/%_kde_datadir/apps/ksplash/Themes/tibanna/ Theme.rc
popd
%endif
%if %tibanna_kdm
# Installation of tibanna kdm theme
%__mkdir -p %{buildroot}/%_kde_datadir/apps/kdm/themes/tibanna/
%__install kdm/tibanna/*.png %{buildroot}/%_kde_datadir/apps/kdm/themes/tibanna
%__install kdm/tibanna/*.jpg %{buildroot}/%_kde_datadir/apps/kdm/themes/tibanna
%__install kdm/tibanna/*.xml %{buildroot}/%_kde_datadir/apps/kdm/themes/tibanna
%__install kdm/tibanna/KdmGreeterTheme.desktop %{buildroot}/%_kde_datadir/apps/kdm/themes/tibanna

%endif
# Creating the icons package
pushd icons
bash ./generate_kde_icons.sh
%__mkdir -p %{buildroot}/%_kde_datadir/icons/
%__mv Bespin %{buildroot}/%_kde_datadir/icons/
popd

%clean 
%__rm -rf %{buildroot}


