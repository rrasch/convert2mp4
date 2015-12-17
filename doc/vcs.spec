%define name	vcs
%define version	1.13.2
%define release	1.dlts%{?dist}

Summary:	Create video contact sheeets.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPLv2+
Group:		Applications/Multimedia
URL:		http://p.outlyer.net/vcs/
Source:		%{name}-%{version}.bash
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

%build

%install
rm -rf %{buildroot}
echo %{buildroot}
echo %{_tmppath}
install -D -m 0755 %{SOURCE0} %{buildroot}%{_bindir}/vcs

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%{_bindir}/*

%changelog
