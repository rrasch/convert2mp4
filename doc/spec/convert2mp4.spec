%define gitver	.git.%(date +"%Y%m%d")
%define name	convert2mp4
%define version	3.0.6
%define release	1.dlts%{?gitver}%{?dist}
%define dlibdir	/usr/local/dlib/%{name}

Summary:	Convert video file to mp4 for HIDVL streaming.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	NYU DLTS
Vendor:		NYU DLTS (rasan@nyu.edu)
Group:		Applications/Multimedia
URL:		https://github.com/rrasch/%{name}
BuildRoot:	%{_tmppath}/%{name}-root
BuildArch:	noarch
%if 0%{?fedora} > 0 || 0%{?centos} > 0
BuildRequires:	git
%endif
Requires:	ffmpeg >= 2.1.4
Requires:	flvcheck
Requires:	mediainfo
Requires:	perl-Image-ExifTool
Requires:	vcs

%description
%{summary}

%prep

%build

%install
rm -rf %{buildroot}

git clone %{url}.git %{buildroot}%{dlibdir}
rm -rf %{buildroot}%{dlibdir}/.git
find %{buildroot}%{dlibdir} -type d | xargs chmod 0755
find %{buildroot}%{dlibdir} -type f | xargs chmod 0644
chmod 0755 %{buildroot}%{dlibdir}/bin/*

mkdir -p %{buildroot}%{_bindir}
ln -s ../..%{dlibdir}/bin/convert2mp4.pl %{buildroot}%{_bindir}/convert2mp4
ln -s ../..%{dlibdir}/bin/create-mp4.rb  %{buildroot}%{_bindir}/create-mp4

rm -r %{buildroot}%{dlibdir}/templates

mv %{buildroot}%{dlibdir}/README.md %{buildroot}%{dlibdir}/doc

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, dlib)
%dir %{dlibdir}
%config(noreplace) %{dlibdir}/conf
%{dlibdir}/presets
%{dlibdir}/bin
%{dlibdir}/doc
%{_bindir}/*

%changelog
