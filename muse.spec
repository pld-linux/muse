#
# Conditional build:
%bcond_with ladcca	# enable ladcca support
%bcond_without jack	# disable jack support
%bcond_without fluid	# disable fluidsynth support
#
Summary:	Linux Music Editor
Summary(pl):	Edytor muzyczny dla Linuxa
Name:		muse
Version:	0.6.1
Release:	1
License:	GPL
Group:		X11/Applications/Sound
Source0:	http://muse.seh.de/bin/%{name}-%{version}.tar.bz2
# Source0-md5:	059f1818b41a9392c3fbe1bb54101432
Source1:	%{name}.desktop
Patch0:		%{name}-qt_designer_version.patch
URL:		http://muse.seh.de/
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_fluid:BuildRequires:	fluidsynth-devel >= 1.0.0}
%{?with_jack:BuildRequires:	jack-audio-connection-kit-devel}
%{?with_ladcca:BuildRequires:	ladcca-devel}
BuildRequires:	libsndfile-devel
BuildRequires:	pkgconfig
BuildRequires:	qt-devel >= 3.1.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MusE is a MIDI/Audio sequencer with recording and editing
capabilities.

%description -l pl
MuSE jest sequencerem MIDI/Audio z możliwościami nagrywania i edycji.

%prep
%setup -q
%patch0 -p1

%build
rm -f missing
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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README README.softsynth SECURITY
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/synthi
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so
%attr(755,root,root) %{_libdir}/%{name}/synthi/*
%{_desktopdir}/*.desktop
%{_datadir}/muse
