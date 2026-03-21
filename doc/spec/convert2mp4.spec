%{!?git_tag:%{error:git_tag macro must be defined}}
%{!?git_commit:%{error:git_commit macro must be defined}}

%define name    convert2mp4
%define version %(echo %{git_tag} | sed 's/^v//')
%global release 1.dlts.git%{git_commit}%{?dist}
%define repourl https://github.com/rrasch/%{name}
%define dlibdir /usr/local/dlib/%{name}

Summary:        Convert video files to mp4 format for streaming.
Name:           %{name}
Version:        %{version}
Release:        %{release}
License:        NYU DLTS
Vendor:         NYU DLTS (rasan@nyu.edu)
Group:          Applications/Multimedia
URL:            https://github.com/rrasch/%{name}
BuildRoot:      %{_tmppath}/%{name}-root
BuildArch:      noarch
BuildRequires:  git
BuildRequires:  perl-generators
Requires:       ffmpeg
Requires:       flvcheck
Requires:       mediainfo
Requires:       perl-Image-ExifTool
Requires:       vcs
Requires:       AtomicParsley
#Requires:      HandBrake

%description
%{summary}

%prep

%build

%install
rm -rf %{buildroot}

git clone %{url}.git %{buildroot}%{dlibdir}
rm -rf %{buildroot}%{dlibdir}/.git
rm -f %{buildroot}%{dlibdir}/.gitattributes
find %{buildroot}%{dlibdir} -type d | xargs chmod 0755
find %{buildroot}%{dlibdir} -type f | xargs chmod 0644
chmod 0755 %{buildroot}%{dlibdir}/bin/*

mkdir -p %{buildroot}%{_bindir}
ln -s ../..%{dlibdir}/bin/convert2mp4.pl %{buildroot}%{_bindir}/convert2mp4
ln -s ../..%{dlibdir}/bin/create-mp4.rb  %{buildroot}%{_bindir}/create-mp4
ln -s ../..%{dlibdir}/bin/convert_iso.py %{buildroot}%{_bindir}/convert_iso

rm -r %{buildroot}%{dlibdir}/templates

mv %{buildroot}%{dlibdir}/README.md %{buildroot}%{dlibdir}/doc

%clean
rm -rf %{buildroot}

%post
CONV_CNF_FILE=%{dlibdir}/conf/%{name}.conf
TQ_CNF_FILE=/content/prod/rstar/etc/task-queue.sysconfig
if [ -f $TQ_CNF_FILE ]; then
    source $TQ_CNF_FILE
    if [ -n "$PROGRESS_URL" ] && ! grep -qs '\[progress\]' $CONV_CNF_FILE; then
        cat << EOF >> $CONV_CNF_FILE
[progress]
url = $PROGRESS_URL
EOF
    fi
fi

%files
%defattr(-, root, dlib)
%dir %{dlibdir}
%config(noreplace) %{dlibdir}/conf
%{dlibdir}/presets
%{dlibdir}/bin
%{dlibdir}/doc
%{_bindir}/*

%changelog
* Fri Mar 20 2026 Rasan Rasch - 3.2.3-1
- 3.2.3
- Add convert_iso script to convert dvd iso's

* Tue May 19 2020 Rasan Rasch - 3.1.4-1
- 3.1.4
