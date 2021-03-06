Summary:	hatari - an Atari ST and STE emulator for Linux
Summary(pl.UTF-8):	hatari - emulator Atari ST i STE dla Linuksa
Name:		hatari
Version:	1.5.0
Release:	1
License:	GPL v2+
Group:		Applications/Emulators
Source0:	http://download.berlios.de/hatari/%{name}-%{version}.tar.bz2
# Source0-md5:	16277cff73ec3a342b87b7b7ea3932f4
Patch0:		%{name}-useless_files.patch
Patch1:		%{name}-python_init.patch
Patch2:		%{name}-desktop.patch
URL:		http://hatari.sourceforge.net/
BuildRequires:	SDL-devel >= 1.2.0
BuildRequires:	cmake >= 2.6
BuildRequires:	libpng-devel
BuildRequires:	pkgconfig
BuildRequires:	portaudio-devel
BuildRequires:	python >= 2
BuildRequires:	readline-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.577
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	zlib-devel
Requires:	python >= 1:2.4
Requires:	python-pygtk-gtk >= 2:2.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Hatari is an Atari ST and STE emulator for Linux and other systems
that are supported by the SDL library. Hatari supports the emulation
of most of the ST and STE hardware.

%description -l pl.UTF-8
Hatari jest emulatorem Atari ST i STE dla Linuksa i innych systemów
obsługiwanych przez bibliotekę SDL. Hatari emuluje większość sprzętu
Atari ST i STE.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

sed -i -e '1s,#!/usr/bin/env python,#!/usr/bin/python,' python-ui/*.py tools/hconsole/*.py

%build
install -d build
cd build
%cmake .. \
	-DBUILD_SHARED_LIBS:BOOL=OFF \
	-DCMAKE_C_FLAGS_RELEASE="-DNDEBUG"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/fr/man1

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install doc/fr/hatari.1	$RPM_BUILD_ROOT%{_mandir}/fr/man1

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}/hatariui
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}/hatariui
%py_postclean %{_datadir}/%{name}/hatariui

for f in README TODO ; do
	mv python-ui/${f} python-ui/${f}-ui
done
mv tools/hconsole/{release-notes.txt,release-notes-hconsole.txt}
mv python-ui/{release-notes.txt,release-notes-ui.txt}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc readme.txt doc/{authors,changelog,emutos,keymap-sample,memory-usage,midi-linux,release-notes,todo}.txt doc/{compatibility,manual}.html tools/hconsole/release-notes-hconsole.txt python-ui/{README-ui,TODO-ui,release-notes-ui.txt}
%attr(755,root,root) %{_bindir}/atari-hd-image
%attr(755,root,root) %{_bindir}/hatari
%attr(755,root,root) %{_bindir}/hatariui
%attr(755,root,root) %{_bindir}/hmsa
%attr(755,root,root) %{_bindir}/zip2st
%{_datadir}/%{name}
%{_mandir}/man1/atari-hd-image.1*
%{_mandir}/man1/hatariui.1*
%{_mandir}/man1/hconsole.1*
%{_mandir}/man1/hmsa.1*
%{_mandir}/man1/zip2st.1*
%lang(fr) %{_mandir}/fr/man1/hatari.1*
%{_desktopdir}/hatariui.desktop
%{_iconsdir}/hicolor/32x32/apps/hatari-icon.png
