Summary:	The game that started roguelike genre.
Summary(pl):	Gra, która zapocz±tkowa³a gatunek roguelike.
Name:		rogue
Version:	5.3
Release:	6
License:	GPL
Group:		Applications/Games
Source0:	http://yarws.kid.waw.pl/files/%{name}.tar.z
Source1:	%{name}.desktop
Source2:	%{name}.png
Source3:	http://yarws.kid.waw.pl/files/%{name}_spoiler.zip
Source4:	http://home.wanadoo.nl/loche/rogue/guide.txt
Patch0:		%{name}-rip_time.patch
Patch1:		%{name}-ldflags.patch
URL:		http://home.wanadoo.nl/loche/rogue/
BuildRequires:	ncurses-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		/usr/games
%define		_datadir	/var/games/rogue

%description
A Dungeons-and-Dragons-like game using character graphics, written
under BSD Unix and subsequently ported to other Unix systems. The
original BSD `curses(3)' screen-handling package was hacked together
by Ken Arnold primarily to support games, and the development of
`rogue(6)' popularized its use. Nethack, Omega, Larn, Angband, and an
entire subgenre of computer dungeon games (all known as `roguelikes')
all took off from the inspiration provided by `rogue(6)'; the popular
Windows game Diablo, though graphics-intensive, has very similar play
logic.

%description -l pl
Gra czerpi±ca z Dungeons and Dragons u¿ywaj±ca znakowej grafiki,
napisana pod Uniksem BSD, a nastêpnie portowana na inne systemy
Uniksowe. Pocz±tkowa biblioteka obs³ugi ekranu 'curses (3)' by³a
hackowana wspólnie z Kenem Arnoldem g³ównie by wspieraæ gry, a rozwój
'rogue (6)' spopularyzowa³ j±. Nethack, Omega, Larn, Angband i ca³y
podgatunek lochowych gier komputerowych (znanych jako 'roguelike')
czerpi± inspiracjê z 'rogue (6)'. Popularna gra Diablo, mimo ogromnego
³adunku grafiki, ma bardzo podobn± logikê gry.

%package spoilers
Summary:	Spoilers for rogue
Summary(pl):	Psuje dla rogue
Group:		Applications/Games

%description spoilers
Spoilers for rogue.

%description spoilers -l pl
Psuje dla rogue.

%prep
%setup -a3 -q -c %{name}-%{version}
%patch0 -p1
%patch1 -p0

%build
for i in *.[ch]
do
	cat $i | sed 's/^#ifdef CURSES/#if 0/g' > $i.new
	cat $i.new | sed 's/^#ifndef CURSES/#if 1/g' > $i
	rm $i.new
done
cat instruct.c | sed 's@%{_prefix}/games@%{_prefix}/share/doc/%{name}-%{version}@' > instruct.c.new
cat score.c | sed 's@%{_prefix}/games@%{_datadir}@' > score.c.new
mv -f instruct.c.new instruct.c
mv -f score.c.new score.c

%{__make} CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -DUNIX -DUNIX_SYS5 -I%{_includedir}/ncurses -c" \
	LDFLAGS="%{rpmldflags} -lncurses"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir},%{_applnkdir}/Games/Roguelike,%{_pixmapsdir}}

install rogue $RPM_BUILD_ROOT%{_bindir}

touch $RPM_BUILD_ROOT%{_datadir}/rogue.scores

cp %{SOURCE4} .
gzip -9nf README guide.txt
gzip -9nf rogue.[drsw]*

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Games/Roguelike
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(2755,root,games) %{_bindir}/*
%attr(2775,root,games) %dir %{_datadir}
%attr(664,root,games) %config(noreplace) %verify(not md5 size mtime) %{_datadir}/rogue.scores

# don't gzip rogue.instr!
%doc usr/games/rogue.instr README.gz guide.txt.gz

%{_applnkdir}/Games/Roguelike/*
%{_pixmapsdir}/*

%files spoilers
%defattr(644,root,root,755)
%doc rogue.*.gz
