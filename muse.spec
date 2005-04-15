#
# Conditional build:
%bcond_with	ladcca	# enable ladcca support
%bcond_with	pch	# enable gcc 3.4.x pch support
%bcond_without	fluid	# disable fluidsynth support

%ifnarch %{ix86} amd64
%undefine	with_fluid	# fluidsynth support disabled for arch !ix86 !amd64
%endif

#
Summary:	Linux Music Editor
Summary(pl):	Edytor muzyczny dla Linuksa
Name:		muse
Version:	0.7.1
Release:	0.3
License:	GPL
Group:		X11/Applications/Sound
Source0:	http://dl.sourceforge.net/lmuse/%{name}-%{version}.tar.bz2
# Source0-md5:	0e47ab9ba98d230e4fd7ea7ef40ed37c
Source1:	%{name}.desktop
Patch0:		%{name}-libtool.patch
URL:		http://muse.seh.de/
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_fluid:BuildRequires:	fluidsynth-devel >= 1.0.0}
BuildRequires:	jack-audio-connection-kit-devel
%{?with_ladcca:BuildRequires:	ladcca-devel}
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	doxygen
BuildRequires:	libsamplerate-devel >= 0.1.0
BuildRequires:	libsndfile-devel
BuildRequires:	libtool
BuildRequires:	openjade
BuildRequires:	pkgconfig
BuildRequires:	qt-designer-libs
BuildRequires:	qt-devel >= 3.2.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MusE is a MIDI/Audio sequencer with recording and editing
capabilities.

%description -l pl
MuSE jest sekwencerem MIDI/Audio z mo¿liwo¶ciami nagrywania i edycji.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}

QTDIR="%{_prefix}"
export QTDIR

# NOTE: you _must_ compile MusE with the same compiler you used to compile Qt
%configure \
	%{?!with_ladcca:--disable-ladcca} \
	%{?!with_fluid:--disable-fluidsynth} \
	%{?with_pch:--enable-pch} \
	--disable-suid-build \
	--disable-suid-install \
	--enable-patchbay \
	--with-docbook-stylesheets=%{_datadir}/sgml/docbook/dsssl-stylesheets \
	--with-qt-includes=%{_includedir}/qt \
	--with-qt-libraries=%{_libdir} \
	--with-qt-prefix=%{_prefix}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	SUIDINSTALL="no"

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install packaging/muse_icon.png $RPM_BUILD_ROOT%{_pixmapsdir}/muse.png

rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/synthi/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README README.softsynth SECURITY
%attr(755,root,root) %{_bindir}/muse
%attr(755,root,root) %{_bindir}/grepmidi
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/qtplugins
%dir %{_libdir}/%{name}/synthi
%attr(755,root,root) %{_libdir}/%{name}/plugins/*
%attr(755,root,root) %{_libdir}/%{name}/qtplugins/designer/*
%attr(755,root,root) %{_libdir}/%{name}/synthi/*
%{_desktopdir}/muse.desktop
%{_pixmapsdir}/muse.png
%{_datadir}/muse
