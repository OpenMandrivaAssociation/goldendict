#define distsuffix edm
%define _requires_exceptions  libtiff.so.4

Name: 		goldendict
Version: 	1.0.1
Release: 	%mkrel 1
Summary: 	Dictionary Lookup Program
Summary(ru):	Электронный словарь GoldenDict
Group:   	Office
License: 	GPL
URL:     	http://goldendict.berlios.de
Source:  	%name-%version-src.tar.bz2
Source2: 	%{name}_icons.tar.bz2
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root

BuildRequires:	libhunspell-devel, libqt4-devel, libvorbis-devel, phonon-devel, libqt4-devel, libxtst6-devel
BuildRequires:	zlib1-devel

%description
Feature-rich dictionary lookup program.
    * Use of WebKit for an accurate articles' representation, complete with
      all formatting, colors, images and links.
    * Support of multiple dictionary file formats:
      * Babylon .BGL files
      * StarDict .ifo/.dict/.idx/.syn dictionaries
      * Dictd .index/.dict(.dz) dictionary files
      * ABBYY Lingvo .dsl source files
      * ABBYY Lingvo .lsa/.dat audio archives
    * Support for Wikipedia, Wiktionary or any other MediaWiki-based sites
    * Scan popup functionality. A small window pops up with translation of a
      word chosen from antoher application.
    * And much more...

%description -l ru

GoldenDict — свободная оболочка для электронных словарей с открытым исходным кодом, поддерживающая многие форматы словарей ABBYY Lingvo, StarDict, Babylon, Dictd, а также произвольных словарных веб-сайтов (Википедия, Викисловарь и др.).

Особенности:

* Вывод отформатированных статей с ссылками и картинками с помощью движка WebKit.
* При поиске слов с ошибками используется система морфологии на основе свободной программы для проверки орфографии Hunspell.
* Индексирование директорий со звуковыми файлами для формирования словарей с произношением слов.
* При поиске перевода пробелы, знаки пунктуации, диакритические знаки и регистр символов в поисковой фразе не играют роли.
* При выделении текста появляется всплывающее окно перевода.


%prep
rm -rf %{buildroot}
mkdir %{buildroot}
cd %{buildroot}
#setup -q -n goldendict

tar --bzip2 -xf %{SOURCE0}
tar --bzip2 -xf %{SOURCE2}

%build
#configure
qmake
%make

%install

export DONT_STRIP=1

rm -rf %{buildroot}

mkdir -p %{buildroot}/opt/%{name}-%{version}

mkdir -p %{buildroot}/usr/bin

mkdir -p %buildroot/%_miconsdir \
	 %buildroot/%_liconsdir \
	 %buildroot/%_iconsdir
	
#install -m 644 %{name}-16.png %buildroot/%{_miconsdir}/%{name}.png
#install -m 644 %{name}-32.png %buildroot/%{_iconsdir}/%{name}.png
#install -m 644 %{name}-48.png %buildroot/%{_liconsdir}/%{name}.png


#xdg menu
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Type=Application
Terminal=false
Categories=Office;Dictionary;Education;Qt;Applications
Name=GoldenDict
GenericName=Multiformat Dictionary
GenericName[ru]=Мультиформатный словарь
Comment=GoldenDict
Encoding=UTF-8
Icon=goldendict.png
Exec=goldendict
EOF

#make Excutable
mkdir -p %{buildroot}%{_bindir}
cat > $RPM_BUILD_ROOT%{_bindir}/%{name} << EOF
#!/bin/sh
cd /opt/goldendict-0.9.0
./goldendict.sh
cd /
EOF

chmod 0755 $RPM_BUILD_ROOT%{_bindir}/%{name}

cp -af ./ %{buildroot}/opt/%{name}-%{version}

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig


%files
%defattr(-,root,root,0755)
%_bindir/%{name}
%dir /opt/%{name}-%{version}
/opt/%{name}-%{version}/
%{_datadir}/applications/%name.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_libdir}/debug/



