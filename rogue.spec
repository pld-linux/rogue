Summary:	The game that started roguelike genre.
Summary(pl):	Gra, która zapocz±tkowa³a gatunek roguelike.
Name:		rogue
Version:	5.3
Release:	2
License:	GPL
Group:		Applications/Games
Group(cs):	Aplikace/Hry
Group(da):	Programmer/Spil
Group(de):	Applikationen/Spiele
Group(es):	Aplicaciones/Juegos
Group(fr):	Applications/Jeux
Group(is):	Forrit/Leikir
Group(it):	Applicazioni/Giochi
Group(ja):	¥¢¥×¥ê¥±¡¼¥·¥ç¥ó/¥²¡¼¥à
Group(no):	Applikasjoner/Spill
Group(pl):	Aplikacje/Gry
Group(pt):	Aplicações/Jogos
Group(ru):	ðÒÉÌÏÖÅÎÉÑ/éÇÒÙ
Group(sl):	Programi/Igre
Group(sv):	Tillämpningar/Spel
Group(uk):	ðÒÉËÌÁÄÎ¦ ðÒÏÇÒÁÍÉ/¶ÇÒÉ
Source0:	http://yarws.kid.waw.pl/files/%{name}.tar.z
Source1:	%{name}.desktop
Source2:	%{name}.png
Patch0:		%{name}-rip_time.patch
Patch1:		%{name}-ldflags.patch
BuildRequires:	ncurses-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_datadir	/var/games/rogue

%description
The game that started roguelike genre.

%description -l pl
Gra, która zapocz±tkowa³a gatunek roguelike.

%prep
%setup -q -c %{name}-%{version}
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

gzip -9nf README

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
%doc usr/games/rogue.instr README.gz

%{_applnkdir}/Games/Roguelike/*
%{_pixmapsdir}/*
