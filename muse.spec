#
# Conditional build:
%bcond_without	fluid	# fluidsynth support

%define	qt_ver	5.1.0

Summary:	Linux Music Editor
Summary(pl.UTF-8):	Edytor muzyczny dla Linuksa
Name:		muse
Version:	4.0.0
Release:	4
License:	GPL v2
Group:		X11/Applications/Sound
Source0:	https://github.com/muse-sequencer/muse/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	2cb1904a93c9cc06abea9f01959d2de7
URL:		https://muse-sequencer.github.io/
BuildRequires:	Qt5Core-devel >= %{qt_ver}
BuildRequires:	Qt5Svg-devel >= %{qt_ver}
BuildRequires:	Qt5UiTools-devel >= %{qt_ver}
BuildRequires:	Qt5Widgets-devel >= %{qt_ver}
BuildRequires:	Qt5Xml-devel >= %{qt_ver}
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
BuildRequires:	qt5-build >= %{qt_ver}
BuildRequires:	qt5-linguist >= %{qt_ver}
BuildRequires:	qt5-qmake >= %{qt_ver}
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
      src/share/scripts/TempoDelay

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
%{_docdir}/muse-4.0.0/libdivide_LICENSE
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
%dir %{_libdir}/%{name}-4.0
%dir %{_libdir}/%{name}-4.0/converters
%dir %{_libdir}/%{name}-4.0/modules
%dir %{_libdir}/%{name}-4.0/plugins
%dir %{_libdir}/%{name}-4.0/synthi
%attr(755,root,root) %{_libdir}/%{name}-4.0/converters/*.so
%attr(755,root,root) %{_libdir}/%{name}-4.0/modules/*.so
%attr(755,root,root) %{_libdir}/%{name}-4.0/plugins/*
%attr(755,root,root) %{_libdir}/%{name}-4.0/synthi/*
%dir %{_datadir}/%{name}-4.0
%dir %{_datadir}/%{name}-4.0/demos
%dir %{_datadir}/%{name}-4.0/drummaps
%dir %{_datadir}/%{name}-4.0/instruments
%dir %{_datadir}/%{name}-4.0/locale
%dir %{_datadir}/%{name}-4.0/metronome
%dir %{_datadir}/%{name}-4.0/plugins
%dir %{_datadir}/%{name}-4.0/presets
%dir %{_datadir}/%{name}-4.0/pybridge
%dir %{_datadir}/%{name}-4.0/rdf
%dir %{_datadir}/%{name}-4.0/scoreglyphs
%dir %{_datadir}/%{name}-4.0/scripts
%dir %{_datadir}/%{name}-4.0/templates
%dir %{_datadir}/%{name}-4.0/themes
%dir %{_datadir}/%{name}-4.0/utils
%dir %{_datadir}/%{name}-4.0/wallpapers
%{_datadir}/mime/packages/muse.xml
%{_datadir}/%{name}-4.0/splash.jpg
%{_datadir}/%{name}-4.0/didyouknow.txt
%{_datadir}/%{name}-4.0/demos/*
%{_datadir}/%{name}-4.0/drummaps/*
%{_datadir}/%{name}-4.0/instruments/*
%{_datadir}/%{name}-4.0/locale/*
%{_datadir}/%{name}-4.0/metronome/*
%{_datadir}/%{name}-4.0/plugins/*
%{_datadir}/%{name}-4.0/presets/*
%{_datadir}/%{name}-4.0/pybridge/*
%{_datadir}/%{name}-4.0/rdf/*
%{_datadir}/%{name}-4.0/scoreglyphs/*
%{_datadir}/%{name}-4.0/scripts/*
%{_datadir}/%{name}-4.0/templates/*
%{_datadir}/%{name}-4.0/themes/*
%{_datadir}/%{name}-4.0/utils/*
%{_datadir}/%{name}-4.0/wallpapers/*
%{_desktopdir}/org.musesequencer.Muse4.desktop
%{_mandir}/man1/*
%{_iconsdir}/hicolor/*x*/apps/muse.png
%{_datadir}/metainfo/org.musesequencer.Muse4.appdata.xml

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
