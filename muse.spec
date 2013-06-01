#
# Conditional build:
%bcond_without	fluid	# disable fluidsynth support

%ifnarch %{ix86} %{x8664}
%undefine	with_fluid	# fluidsynth support disabled for arch !ix86 !amd64
%endif

Summary:	Linux Music Editor
Summary(pl.UTF-8):	Edytor muzyczny dla Linuksa
Name:		muse
Version:	2.1.2
Release:	2
License:	GPL
Group:		X11/Applications/Sound
Source0:	http://downloads.sourceforge.net/lmuse/%{name}-%{version}.tar.gz
# Source0-md5:	ad917335ac05a3d62e3cd073af901001
Source1:	%{name}.desktop
Patch0:		%{name}-CMakeLists.txt.patch
URL:		http://muse.seh.de/
BuildRequires:	QtDesigner-devel
BuildRequires:	QtSvg-devel
BuildRequires:	QtUiTools-devel
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	cmake >= 2.8.0
BuildRequires:	dssi-devel >= 0.9.0
%{?with_fluid:BuildRequires:	fluidsynth-devel >= 0.9.0}
BuildRequires:	jack-audio-connection-kit-devel >= 0.103
BuildRequires:	ladspa-devel
BuildRequires:	lash-devel >= 0.2
BuildRequires:	liblo >= 0.23
BuildRequires:	libsamplerate-devel >= 0.1.0
BuildRequires:	libsndfile-devel >= 1.0.25
BuildRequires:	libuuid-devel >= 0.1.8
BuildRequires:	rpmbuild(macros) >= 1.213
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	lash
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MusE is a MIDI/Audio sequencer with recording and editing
capabilities.

%description -l pl.UTF-8
MuSE jest sekwencerem MIDI/Audio z możliwościami nagrywania i edycji.

%package doc
Summary:	Manual for %{name}
Summary(pl.UTF-8):	Podręcznik dla MusE
Group:		Documentation

%description doc
Documentation for %{name}.

%description doc -l pl.UTF-8
Dokumentacja do anta.

%prep
%setup -q
%patch0 -p0

%build
install -d build
cd build
%cmake \
	../

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT \

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -p packaging/muse_icon.png $RPM_BUILD_ROOT%{_pixmapsdir}/muse.png

rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/synthi/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc ChangeLog README  README.de README.effects-rack README.instruments README.ladspaguis README.shortcuts README.softsynth README.translate README.usage SECURITY NEWS COPYING AUTHORS
%attr(755,root,root) %{_bindir}/muse2
%attr(755,root,root) %{_bindir}/grepmidi
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/modules
%dir %{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/synthi
%attr(755,root,root) %{_libdir}/%{name}/modules/*.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/*
%attr(755,root,root) %{_libdir}/%{name}/synthi/*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/demos
%dir %{_datadir}/%{name}/drummaps
%dir %{_datadir}/%{name}/instruments
%dir %{_datadir}/%{name}/locale
%dir %{_datadir}/%{name}/plugins
%dir %{_datadir}/%{name}/presets
%dir %{_datadir}/%{name}/pybridge
%dir %{_datadir}/%{name}/scoreglyphs
%dir %{_datadir}/%{name}/scripts
%dir %{_datadir}/%{name}/templates
%dir %{_datadir}/%{name}/themes
%dir %{_datadir}/%{name}/utils
%dir %{_datadir}/%{name}/wallpapers
%{_datadir}/mime/packages/muse.xml
%{_datadir}/muse/didyouknow.txt
%{_datadir}/muse/splash.png
%{_datadir}/%{name}/demos/*
%{_datadir}/%{name}/drummaps/*
%{_datadir}/%{name}/instruments/*
%{_datadir}/%{name}/locale/*
%{_datadir}/%{name}/plugins/*
%{_datadir}/%{name}/presets/*
%{_datadir}/%{name}/pybridge/*
%{_datadir}/%{name}/scoreglyphs/*
%{_datadir}/%{name}/scripts/*
%{_datadir}/%{name}/templates/*
%{_datadir}/%{name}/themes/*
%{_datadir}/%{name}/utils/*
%{_datadir}/%{name}/wallpapers/*
%{_desktopdir}/muse.desktop
%{_pixmapsdir}/muse.png
%{_mandir}/man1/*
%{_iconsdir}/hicolor/64x64/apps/muse_icon.png

%files doc
%defattr(644,root,root,755)
%dir %{_docdir}/%{name}
%dir %{_docdir}/%{name}/muse_html
%dir %{_docdir}/%{name}/muse_html/single
%dir %{_docdir}/%{name}/muse_html/split
%dir %{_docdir}/%{name}/muse_html/single/documentation
%dir %{_docdir}/%{name}/muse_html/single/developer_docs
%dir %{_docdir}/%{name}/muse_html/split/documentation
%dir %{_docdir}/%{name}/muse_html/split/developer_docs
%dir %{_docdir}/%{name}/muse_pdf
%{_docdir}/%{name}/muse_pdf/*.pdf
%{_docdir}/%{name}/muse_html/single/documentation/*
%{_docdir}/%{name}/muse_html/single/developer_docs/*
%{_docdir}/%{name}/muse_html/split/documentation/*
%{_docdir}/%{name}/muse_html/split/developer_docs/*


