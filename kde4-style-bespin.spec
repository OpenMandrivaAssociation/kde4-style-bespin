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




%changelog
* Sun May 08 2011 John Balcaen <mikala@mandriva.org> 0.1-0.1355svn.1mdv2011.0
+ Revision: 672499
- Update tarball to revision 1355
- Add patch to use SCALE for kplashx
- Add tibanna subpackage (kdm,ksplash only kdm is enable currently)

* Wed Dec 08 2010 John Balcaen <mikala@mandriva.org> 0.1-0.1308svn.1mdv2011.0
+ Revision: 616311
- Update to revision 1308
- fix file list
- rediff patch0

  + Oden Eriksson <oeriksson@mandriva.com>
    - the mass rebuild of 2010.1 packages

* Wed Apr 28 2010 John Balcaen <mikala@mandriva.org> 0.1-0.1085svn.1mdv2010.1
+ Revision: 540612
- Update to revision 1058
- drop patch1 (merged upstream)
- rediff patch0

* Fri Apr 23 2010 John Balcaen <mikala@mandriva.org> 0.1-0.1076svn.1mdv2010.1
+ Revision: 538197
- Update to revision 1076
- drop Source2 (picture is now generated by upstream script)
- rediff patch1

* Mon Apr 12 2010 John Balcaen <mikala@mandriva.org> 0.1-0.1068svn.1mdv2010.1
+ Revision: 533615
- Update to revision 1068
- drop patch2 (merge upstream)
- rediff patch1
- enable again translucient windows

* Thu Mar 25 2010 John Balcaen <mikala@mandriva.org> 0.1-0.1043svn.3mdv2010.1
+ Revision: 527324
- Update patch2 to fix truncated ksplash

* Sun Mar 21 2010 John Balcaen <mikala@mandriva.org> 0.1-0.1043svn.2mdv2010.1
+ Revision: 525970
- Add preview pic for ksplash subpackage
- Add preview pic for kdm subpackage
- Add more resolution for ksplash
- Minor changes in folder name
- Disable translucient windows

* Thu Mar 18 2010 John Balcaen <mikala@mandriva.org> 0.1-0.1043svn.1mdv2010.1
+ Revision: 524928
- Provide an icon subpackage
-For the moment provide only ksplash in 1600x1200
-Fix License
- Add kdm subpackage
  Add a suggest on kdm subpackage
- Add a suggest for ksplash subpackage
- Update to 1043
- Add bespin ksplash
- Enable translucient windows on build

* Mon Mar 01 2010 John Balcaen <mikala@mandriva.org> 0.1-0.1031svn.1mdv2010.1
+ Revision: 513031
- Update to revision 1031

* Wed Jan 20 2010 John Balcaen <mikala@mandriva.org> 0.1-0.983svn.1mdv2010.1
+ Revision: 493946
- Update svn to revision 983
- Fix files list

* Tue Oct 06 2009 John Balcaen <mikala@mandriva.org> 0.1-0.708svn.1mdv2010.0
+ Revision: 454406
- Update to revision 708 (fix a crash in amarok caused by bespin)

* Wed Sep 23 2009 John Balcaen <mikala@mandriva.org> 0.1-0.636svn.2mdv2010.0
+ Revision: 447740
- Fix typo in description

* Tue Sep 22 2009 John Balcaen <mikala@mandriva.org> 0.1-0.636svn.1mdv2010.0
+ Revision: 447269
- Update to svn revision 636
- Split package in 3 ( kde4-style-bespin,plasma-applet-xbar,bespin-completion)
- Add presets in kd4-style-bespin documentation
- Add bespin mandir

* Sun Sep 20 2009 John Balcaen <mikala@mandriva.org> 0.1-0.622svn.1mdv2010.0
+ Revision: 444826
- Update to last svn (r622)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Nicolas Lécureuil <nlecureuil@mandriva.com>
    - Use kde packages layout

* Sun Feb 01 2009 Olivier Thauvin <nanardon@mandriva.org> 0.1-0.398svn.1mdv2009.1
+ Revision: 335912
- import kde4-style-bespin


* Sat Jan 31 2009 Romain Dep. <rom1dep@gmail.com> 0.1-0.398svn.1mdv2009.0
+ revision 398

* Sun Jan 25 2009 Romain Dep. <rom1dep@gmail.com> 0.1-0.392svn.1mdv2009.0
+ revision 392

* Sat Jan 24 2009 Romain Dep. <rom1dep@gmail.com> 0.1-0.391svn.1mdv2009.0
+ revision 391

* Thu Jan 15 2009 Oliver Burger <rpm@mandrivauser.de> 0.1-0.386svn.1mud2009.0
- initial package for Mandriva Linux
- based upon spec by Peter Schwanemann <Nasenbaer@drehatlas.de>
