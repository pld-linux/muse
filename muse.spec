#
# Conditional build:
%bcond_without	fluid	# fluidsynth support

%define	qt_ver	5.1.0

Summary:	Linux Music Editor
Summary(pl.UTF-8):	Edytor muzyczny dla Linuksa
Name:		muse
Version:	4.2.1
Release:	1
License:	GPL v2
Group:		X11/Applications/Sound
Source0:	https://github.com/muse-sequencer/muse/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	7874a127d67bcae394463c486e4ce761
URL:		https://muse-sequencer.github.io/
BuildRequires:	Qt5Core-devel >= %{qt_ver}
BuildRequires:	Qt5Svg-devel >= %{qt_ver}
BuildRequires:	Qt5UiTools-devel >= %{qt_ver}
BuildRequires:	Qt5Widgets-devel >= %{qt_ver}
BuildRequires:	Qt5Xml-devel >= %{qt_ver}
BuildRequires:	alsa-lib-devel >= 1.1.3
BuildRequires:	atkmm-devel >= 1.6
BuildRequires:	cmake >= 3.10.2
BuildRequires:	dssi-devel >= 1.1.1
%{?with_fluid:BuildRequires:	fluidsynth-devel >= 2.0.0}
BuildRequires:	gtk+2-devel >= 1:2.0
BuildRequires:	gtkmm-devel >= 2.4
BuildRequires:	jack-audio-connection-kit-devel >= 0.125.0
BuildRequires:	ladspa-devel
BuildRequires:	lash-devel >= 0.2
BuildRequires:	libinstpatch-devel >= 1.1.7
BuildRequires:	liblo-devel >= 0.29
BuildRequires:	liblrdf-devel >= 0.5.0
BuildRequires:	libsamplerate-devel >= 0.1.9
BuildRequires:	libsndfile-devel >= 1.0.28
BuildRequires:	libuuid-devel >= 0.1.8
BuildRequires:	lilv-devel >= 0.24.0
BuildRequires:	lv2-devel >= 1.18.0
BuildRequires:	pkgconfig
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	qt5-build >= %{qt_ver}
BuildRequires:	qt5-linguist >= %{qt_ver}
BuildRequires:	qt5-qmake >= %{qt_ver}
BuildRequires:	rpmbuild(macros) >= 1.213
BuildRequires:	rtaudio-devel >= 5.0
BuildRequires:	rubberband-devel >= 1.8.1
BuildRequires:	serd-devel >= 0.30.0
BuildRequires:	sord-devel >= 0.16.0
Requires:	alsa-lib >= 1.1.3
Requires:	dssi >= 1.1.1
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	jack-audio-connection-kit-libs >= 0.125.0
Requires:	libinstpatch >= 1.1.7
Requires:	liblo >= 0.29
Requires:	liblrdf >= 0.5.0
Requires:	libsamplerate >= 0.1.9
Requires:	libsndfile >= 1.0.28
Requires:	lilv >= 0.24.0
Requires:	lv2 >= 1.18.0
Requires:	rubberband-libs >= 1.8.1
Requires:	serd >= 0.30.0
Requires:	sord >= 0.16.0
Suggests:	lash >= 0.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MusE is a MIDI/Audio sequencer with recording and editing
capabilities.

%description -l pl.UTF-8
MuSE jest sekwencerem MIDI/Audio z możliwościami nagrywania i edycji.

%package doc
Summary:	MusE documentation
Summary(pl.UTF-8):	Dokumentacja do MusE
Group:		Documentation

%description doc
MusE documentation.

%description doc -l pl.UTF-8
Dokumentacja do MusE.

%prep
%setup -q

%{__sed} -E -i -e '1s,#!\s*/usr/bin/python(\s|$),#!%{__python3}\1,' \
      src/utils/muse-find-unused-wavs \
      src/utils/muse-song-convert.py

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python3(\s|$),#!%{__python3}\1,' \
      src/share/scripts/ConstantLength \
      src/share/scripts/ConstantVelocityForNote \
      src/share/scripts/CreateBassline \
      src/share/scripts/DoNothing \
      src/share/scripts/Humanize \
      src/share/scripts/RandomPosition1 \
      src/share/scripts/RandomizeVelocityRelative \
      src/share/scripts/RemoveAftertouch \
      src/share/scripts/RemoveShortEvents \
      src/share/scripts/Rhythm1 \
      src/share/scripts/SpeedDouble \
      src/share/scripts/SpeedHalf \
      src/share/scripts/SwingQuantize1 \
      src/share/scripts/TempoDelay \
      src/share/scripts/Reverse \
      src/share/scripts/SpeedChange

%build
install -d src/build
cd src/build
export CFLAGS="%{rpmcflags} $(pkg-config --cflags atkmm-1.6)"
export CXXFLAGS="%{rpmcxxflags} $(pkg-config --cflags atkmm-1.6)"
%cmake \
	-DMusE_DOC_DIR="%{_docdir}/%{name}-%{version}" \
	../

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C src/build install \
	DESTDIR=$RPM_BUILD_ROOT \

%{__rm} $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/COPYING

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
%{_docdir}/%{name}-%{version}/README*
%{_docdir}/%{name}-%{version}/SECURITY
%{_docdir}/muse-4.2.1/libdivide_LICENSE
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
%attr(755,root,root) %{_bindir}/muse4
%attr(755,root,root) %{_bindir}/muse_plugin_scan
%attr(755,root,root) %{_bindir}/grepmidi
%dir %{_libdir}/%{name}-4.2
%dir %{_libdir}/%{name}-4.2/converters
%dir %{_libdir}/%{name}-4.2/modules
%dir %{_libdir}/%{name}-4.2/plugins
%dir %{_libdir}/%{name}-4.2/synthi
%attr(755,root,root) %{_libdir}/%{name}-4.2/converters/*.so
%attr(755,root,root) %{_libdir}/%{name}-4.2/modules/*.so
%attr(755,root,root) %{_libdir}/%{name}-4.2/plugins/*
%attr(755,root,root) %{_libdir}/%{name}-4.2/synthi/*
%dir %{_datadir}/%{name}-4.2
%dir %{_datadir}/%{name}-4.2/demos
%dir %{_datadir}/%{name}-4.2/drummaps
%dir %{_datadir}/%{name}-4.2/instruments
%dir %{_datadir}/%{name}-4.2/locale
%dir %{_datadir}/%{name}-4.2/metronome
%dir %{_datadir}/%{name}-4.2/plugins
%dir %{_datadir}/%{name}-4.2/presets
%dir %{_datadir}/%{name}-4.2/pybridge
%dir %{_datadir}/%{name}-4.2/rdf
%dir %{_datadir}/%{name}-4.2/scoreglyphs
%dir %{_datadir}/%{name}-4.2/scripts
%dir %{_datadir}/%{name}-4.2/templates
%dir %{_datadir}/%{name}-4.2/themes
%dir %{_datadir}/%{name}-4.2/utils
%dir %{_datadir}/%{name}-4.2/wallpapers
%{_datadir}/mime/packages/muse.xml
%{_datadir}/%{name}-4.2/splash.jpg
%{_datadir}/%{name}-4.2/didyouknow.txt
%{_datadir}/%{name}-4.2/demos/*
%{_datadir}/%{name}-4.2/drummaps/*
%{_datadir}/%{name}-4.2/instruments/*
%{_datadir}/%{name}-4.2/locale/*
%{_datadir}/%{name}-4.2/metronome/*
%{_datadir}/%{name}-4.2/plugins/*
%{_datadir}/%{name}-4.2/presets/*
%{_datadir}/%{name}-4.2/pybridge/*
%{_datadir}/%{name}-4.2/rdf/*
%{_datadir}/%{name}-4.2/scoreglyphs/*
%{_datadir}/%{name}-4.2/scripts/*
%{_datadir}/%{name}-4.2/templates/*
%{_datadir}/%{name}-4.2/themes/*
%{_datadir}/%{name}-4.2/utils/*
%{_datadir}/%{name}-4.2/wallpapers/*
%{_desktopdir}/io.github.muse_sequencer.Muse.desktop
%{_mandir}/man1/*
%{_iconsdir}/hicolor/*x*/apps/muse.png
%{_datadir}/metainfo/io.github.muse_sequencer.Muse.appdata.xml

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
