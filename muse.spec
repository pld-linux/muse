Summary:	Linux Music Editor
Summary(pl):	Edytor muzyczny dla Linuxa
Name:		muse
Version:	0.6.0pre8
Release:	1
License:	GPL
Group:		X11/Applications/Sound
Source0:	http://muse.seh.de/bin/%{name}-%{version}.tar.bz2
# Source0-md5: 9de8f1f413ebda34458379ba17049b3c
Source1:	%{name}.desktop
URL:		http://muse.seh.de/
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	ladcca-devel
BuildRequires:	libsndfile-devel
BuildRequires:	pkgconfig
BuildRequires:	qt-devel >= 3.1.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MusE is a MIDI/Audio sequencer with recording and editing
capabilities.

%description -l pl
MuSE jest sequencerem MIDI/Audio z mo¿liwo¶ciami nagrywania i edycji.

%prep
%setup -q

%build
rm -f missing
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}

QTDIR="%{_prefix}"
export QTDIR

CXXFLAGS="%{rpmcflags} -DNDEBUG"
# NOTE: current version doesn't work with fluidsynth
# NOTE: you _must_ compile MusE with the same compiler you used to compile QT
%configure \
	--with-qt-prefix=%{_prefix} \
	--with-qt-libraries=%{_libdir} \
	--with-qt-includes=%{_includedir}/qt \
	--disable-qttest \
	--disable-iiwusynth \
	--disable-suid-build \
	--disable-suid-install \
	--enable-patchbay \
	--with-docbook-stylesheets=%{_datadir}/sgml/docbook/dsssl-stylesheets

%{__make} CXXFLAGS="%{rpmcflags} -DNDEBUG"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_applnkdir}/Multimedia

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Multimedia

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
%{_applnkdir}/Multimedia/%{name}.desktop
%{_datadir}/muse
