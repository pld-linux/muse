#
# Conditional build:
%bcond_without	fluid	# disable fluidsynth support

%ifnarch %{ix86} %{x8664}
%undefine	with_fluid	# fluidsynth support disabled for arch !ix86 !amd64
%endif

Summary:	Linux Music Editor
Summary(pl.UTF-8):	Edytor muzyczny dla Linuksa
Name:		muse
Version:	3.0.2
Release:	1
License:	GPL v2
Group:		X11/Applications/Sound
Source0:	http://downloads.sourceforge.net/lmuse/%{name}-%{version}.tar.gz
# Source0-md5:	6e992f0f9d58adc3a2e2444dece37dfe
Source1:	%{name}.desktop
Patch0:		missing_includes.patch
Patch1:		fluidsynth2.patch
URL:		http://muse.seh.de/
BuildRequires:	QtDesigner-devel
BuildRequires:	QtSvg-devel
BuildRequires:	QtUiTools-devel
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	cmake >= 2.8.0
BuildRequires:	dssi-devel >= 0.9.0
%{?with_fluid:BuildRequires:	fluidsynth-devel >= 2.0.0}
BuildRequires:	gtkmm-devel
BuildRequires:	jack-audio-connection-kit-devel >= 0.103
BuildRequires:	ladspa-devel
BuildRequires:	lash-devel >= 0.2
BuildRequires:	liblo >= 0.23
BuildRequires:	libsamplerate-devel >= 0.1.0
BuildRequires:	libsndfile-devel >= 1.0.25
BuildRequires:	libuuid-devel >= 0.1.8
BuildRequires:	lilv-devel >= 0.22.0
BuildRequires:	lv2-devel >= 1.12.0
BuildRequires:	rpmbuild(macros) >= 1.213
BuildRequires:	rtaudio-devel >= 4.0
BuildRequires:	sord-devel >= 0.14.0
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Suggests:	lash
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
%patch0 -p1
%patch1 -p2

%build
install -d build
cd build
%cmake \
	-DMusE_DOC_DIR="%{_docdir}/%{name}-%{version}" \
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
rm -f $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/COPYING

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
# do not use %doc, as it would remove files which are already there
%{_docdir}/%{name}-%{version}/AUTHORS
%{_docdir}/%{name}-%{version}/ChangeLog
%{_docdir}/%{name}-%{version}/NEWS
%{_docdir}/%{name}-%{version}/README*
%{_docdir}/%{name}-%{version}/SECURITY
%dir %{_docdir}/%{name}-%{version}/deicsonze
%{_docdir}/%{name}-%{version}/deicsonze/*
%dir %{_docdir}/%{name}-%{version}/fluidsynth
%{_docdir}/%{name}-%{version}/fluidsynth/*
%dir %{_docdir}/%{name}-%{version}/freeverb
%{_docdir}/%{name}-%{version}/freeverb/*
%dir %{_docdir}/%{name}-%{version}/simpledrums
%{_docdir}/%{name}-%{version}/simpledrums/*
%dir %{_docdir}/%{name}-%{version}/vam
%{_docdir}/%{name}-%{version}/vam/*
%attr(755,root,root) %{_bindir}/muse3
%attr(755,root,root) %{_bindir}/grepmidi
%dir %{_libdir}/%{name}-3.0
%dir %{_libdir}/%{name}-3.0/modules
%dir %{_libdir}/%{name}-3.0/plugins
%dir %{_libdir}/%{name}-3.0/synthi
%attr(755,root,root) %{_libdir}/%{name}-3.0/modules/*.so
%attr(755,root,root) %{_libdir}/%{name}-3.0/plugins/*
%attr(755,root,root) %{_libdir}/%{name}-3.0/synthi/*
%dir %{_datadir}/%{name}-3.0
%dir %{_datadir}/%{name}-3.0/demos
%dir %{_datadir}/%{name}-3.0/drummaps
%dir %{_datadir}/%{name}-3.0/instruments
%dir %{_datadir}/%{name}-3.0/locale
%dir %{_datadir}/%{name}-3.0/metronome
%dir %{_datadir}/%{name}-3.0/plugins
%dir %{_datadir}/%{name}-3.0/presets
%dir %{_datadir}/%{name}-3.0/pybridge
%dir %{_datadir}/%{name}-3.0/scoreglyphs
%dir %{_datadir}/%{name}-3.0/scripts
%dir %{_datadir}/%{name}-3.0/templates
%dir %{_datadir}/%{name}-3.0/themes
%dir %{_datadir}/%{name}-3.0/utils
%dir %{_datadir}/%{name}-3.0/wallpapers
%{_datadir}/mime/packages/muse.xml
%{_datadir}/%{name}-3.0/didyouknow.txt
%{_datadir}/%{name}-3.0/splash.png
%{_datadir}/%{name}-3.0/demos/*
%{_datadir}/%{name}-3.0/drummaps/*
%{_datadir}/%{name}-3.0/instruments/*
%{_datadir}/%{name}-3.0/locale/*
%{_datadir}/%{name}-3.0/metronome/*
%{_datadir}/%{name}-3.0/plugins/*
%{_datadir}/%{name}-3.0/presets/*
%{_datadir}/%{name}-3.0/pybridge/*
%{_datadir}/%{name}-3.0/scoreglyphs/*
%{_datadir}/%{name}-3.0/scripts/*
%{_datadir}/%{name}-3.0/templates/*
%{_datadir}/%{name}-3.0/themes/*
%{_datadir}/%{name}-3.0/utils/*
%{_datadir}/%{name}-3.0/wallpapers/*
%{_desktopdir}/muse.desktop
%{_pixmapsdir}/muse.png
%{_mandir}/man1/*
%{_iconsdir}/hicolor/64x64/apps/muse_icon.png
/usr/share/metainfo/muse.appdata.xml

%files doc
%defattr(644,root,root,755)
%dir %{_docdir}/%{name}-%{version}
%dir %{_docdir}/%{name}-%{version}/muse_html
%dir %{_docdir}/%{name}-%{version}/muse_html/single
%dir %{_docdir}/%{name}-%{version}/muse_html/split
%dir %{_docdir}/%{name}-%{version}/muse_html/single/documentation
%dir %{_docdir}/%{name}-%{version}/muse_html/single/developer_docs
%dir %{_docdir}/%{name}-%{version}/muse_html/split/documentation
%dir %{_docdir}/%{name}-%{version}/muse_html/split/developer_docs
%dir %{_docdir}/%{name}-%{version}/muse_pdf
%{_docdir}/%{name}-%{version}/muse_pdf/*.pdf
%{_docdir}/%{name}-%{version}/muse_html/single/documentation/*
%{_docdir}/%{name}-%{version}/muse_html/single/developer_docs/*
%{_docdir}/%{name}-%{version}/muse_html/split/documentation/*
%{_docdir}/%{name}-%{version}/muse_html/split/developer_docs/*


