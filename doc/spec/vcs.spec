%define name	vcs
%define version	1.13.4
%define release	1.dlts%{?dist}

Summary:	Create video contact sheeets.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPLv2+
Group:		Applications/Multimedia
URL:		http://p.outlyer.net/vcs/
Source:		http://p.outlyer.net/%{name}/files/%{name}-%{version}.tar.gz
Patch:		%{name}-%{version}.patch
BuildRoot:	%{_tmppath}/%{name}-root
BuildArch:	noarch
Requires:	ffmpeg
Requires:	ImageMagick

%description
Video Contact Sheet *NIX (vcs for short) is a script that creates a
contact sheet (preview) from videos by taking still captures
distributed over the length of the video. The output image contains
useful information on the video such as codecs, file size, screen
size, frame rate, and length. It requires MPlayer or FFmpeg and
ImageMagick. It is confirmed to work on Linux and FreeBSD, and
possibly other POSIX/UNIX systems.

%prep
%autosetup -p1

%build

%install
rm -rf %{buildroot}
%makeinstall

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc CHANGELOG
%doc examples/vcs.conf.example
%{_datadir}/%{name}
%{_bindir}/*
%{_mandir}/*/*

%changelog
