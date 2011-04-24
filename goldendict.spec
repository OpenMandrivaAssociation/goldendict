Name:		goldendict
Version:	1.0.1
Release:	%mkrel 2
Summary:	A feature-rich dictionary lookup program
Group:		Office
License:	GPLv3+
URL:		http://goldendict.berlios.de/
Source0:	%{name}-%{version}-src.tar.bz2

# Modify the Icon section in desktop file to comform package guideline.

BuildRequires:	qt4-devel
BuildRequires:	xtst-devel
BuildRequires:	hunspell-devel
BuildRequires:	libvorbis-devel
BuildRequires:	desktop-file-utils
BuildRequires:	phonon-devel

%description
Goldendict is a feature-rich dictionary lookup program.
The latest release has the following features:
Use of WebKit for an accurate articles' representation;
Support of multiple dictionary file formats;
Support MediaWiki-based sites to perform search;
Scan popup functionality.

%prep
%setup -q -c -n goldendict-%{version}-src

%build
# Fix the directory in goldendict.pro by removing apps
sed -i 's/share\/apps\/goldendict/share\/goldendict/g' goldendict.pro
# Fix the hunspell directory
sed -i 's|myspell/dicts|myspell|g' config.cc
# Fix prefix for /usr 
sed -i 's/usr\/local/usr/g' goldendict.pro
%qmake_qt4
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install INSTALL_ROOT=%{buildroot} INSTALL="install -p"
rm -rf %{buildroot}/%{_datadir}/app-install

# Fix the icon name in desktop file
sed -i 's/\/usr\/share\/pixmaps\/goldendict\.png/goldendict/g' %{buildroot}/%{_datadir}/applications/goldendict.desktop
# Fix the categories in desktop file
desktop-file-install	\
--add-category="Dictionary"	\
--remove-category="Education"	\
--remove-category="Applications"	\
--delete-original	\
--dir=%{buildroot}%{_datadir}/applications	\
%{buildroot}%{_datadir}/applications/goldendict.desktop
install -d %{buildroot}/%{_datadir}/goldendict/locale
install -pm 644 locale/*.qm %{buildroot}/%{_datadir}/goldendict/locale

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE.txt
%dir %{_datadir}/goldendict/
%dir %{_datadir}/goldendict/locale/
%{_bindir}/goldendict
%{_datadir}/applications/goldendict.desktop
%{_datadir}/pixmaps/goldendict.png
%{_datadir}/goldendict/locale/*.qm
