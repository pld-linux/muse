#
# Conditional build:
%bcond_with ladcca	# enable ladcca support
%bcond_without jack	# disable jack support
%bcond_without fluid	# disable fluidsynth support
#
Summary:	Linux Music Editor
Summary(pl):	Edytor muzyczny dla Linuxa
Name:		muse
Version:	0.6.2
Release:	1
License:	GPL
Group:		X11/Applications/Sound
Source0:	http://dl.sf.net/lmuse/%{name}-%{version}.tar.bz2
# Source0-md5:	e12491f3f399751c1648ecb55770dde0
Source1:	%{name}.desktop
URL:		http://muse.seh.de/
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_fluid:BuildRequires:	fluidsynth-devel >= 1.0.0}
%{?with_jack:BuildRequires:	jack-audio-connection-kit-devel}
%{?with_ladcca:BuildRequires:	ladcca-devel}
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	doxygen
BuildRequires:	libsndfile-devel
BuildRequires:	openjade
BuildRequires:	pkgconfig
BuildRequires:	qt-devel >= 3.1.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MusE is a MIDI/Audio sequencer with recording and editing
capabilities.

%description -l pl
MuSE jest sekwencerem MIDI/Audio z możliwościami nagrywania i edycji.

%prep
%setup -q

%build
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}

QTDIR="%{_prefix}"
export QTDIR

# NOTE: you _must_ compile MusE with the same compiler you used to compile QT
%configure \
	%{?!with_ladcca:--disable-ladcca} \
	%{?!with_fluid:--disable-fluidsynth} \
	%{?!with_jack:--disable-jack} \
	--disable-qttest \
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
install -d $RPM_BUILD_ROOT%{_desktopdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/synthi/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README README.softsynth SECURITY
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/synthi
%attr(755,root,root) %{_libdir}/%{name}/plugins/*
%attr(755,root,root) %{_libdir}/%{name}/synthi/*
%{_desktopdir}/*.desktop
%{_datadir}/muse
