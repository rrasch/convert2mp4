%global __brp_check_rpaths %{nil}
%global _missing_build_ids_terminate_build %{nil}

%define name	flvcheck
%define version	1.0
%define release	1.dlts%{?dist}

Summary:	Verify video files for Adobe Media Server.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Adobe Systems Incorporated	
Group:		Applications/Multimedia
URL:		http://www.adobe.com/products/adobe-media-server-family/tool-downloads.html
Source:		flv_check1_0.zip
BuildRoot:	%{_tmppath}/%{name}-root


%description
FLVCheck lets you verify that a video file will run properly on
Adobe Media Server. The tool supports MP4 and FLV files and can be
used in Windows® or Linux®.

%prep
%setup -n FLVCheck1.0

%build

%install
rm -rf %{buildroot}
install -D -m 0755 adobe/fms/externaltools/FLVCheck/linux/flvcheck %{buildroot}%{_bindir}/flvcheck

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc adobe/fms/documentation/FLVCheck_Readme.pdf
%{_bindir}/*

%changelog
