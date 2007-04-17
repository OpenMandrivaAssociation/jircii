%define section         free
%define sleep_version   1:2.1-0.b14
%define gcj_support     1

Name:           jircii
Version:        41
Release:        %mkrel 1
Epoch:          1
Summary:        An Internet Relay Chat (IRC) client for Windows, MacOS X, and Linux
License:        Artistic
URL:            http://jirc.hick.org/jirc/
Group:          Development/Java
#Vendor:        JPackage Project
#Distribution:  JPackage
Source0:        http://jirc.hick.org/download/rsmudge_irc032507.tgz
Source1:        %{name}-script
Source2:        jicon16x16.png
Source3:        jicon32x32.png
Source4:        jicon48x48.png
Source5:        %{name}.desktop
Source100:      http://jirc.hick.org/download/scripts/away.irc
Source101:      http://jirc.hick.org/download/scripts/bitchx.irc
Source102:      http://jirc.hick.org/download/scripts/flash.irc
Source103:      http://jirc.hick.org/download/scripts/neo-jircii.irc
Source104:      http://jirc.hick.org/download/scripts/quote.irc
Source105:      http://jirc.hick.org/download/scripts/xdcc.irc
Source106:      http://jirc.hick.org/download/scripts/sditopicbar.irc
Source200:      http://jirc.hick.org/download/themes/mIRC.thm
Patch0:         %{name}-build.patch
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires:       jpackage-utils >= 0:1.5
Requires:       sleep >= %{sleep_version}
BuildRequires:  ant >= 0:1.6
BuildRequires:  desktop-file-utils
BuildRequires:  java-javadoc
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  sleep >= %{sleep_version}
BuildRequires:  sleep-javadoc >= %{sleep_version}
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel >= 0:1.4.2
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
jIRCii is an Internet Relay Chat client (IRC) for Windows, MacOS X, 
and Linux.

jIRCii provides an irc experience similar to ircii, hADES, and 
BitchX with the advantages of a solid user interface. Features 
include DCC/CTCP support, multiple server connections, IRC over SSL 
support, tab key nickname completion, and over 75 built-in commands. 
jIRCii is fully scriptable using sleep, a Perl-like language.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Documentation

%description    javadoc
Javadoc for %{name}.

%prep
%setup -q -n rsmudge_irc
%patch -p1
%{_bindir}/find . -name '*.jar' | %{_bindir}/xargs -t %{__rm}
%{__mv} src/rero/dialogs/AboutWindow.java src/rero/dialogs/AboutWindow.java.orig
%{_bindir}/iconv -t utf8 -f iso-8859-1 -o src/rero/dialogs/AboutWindow.java src/rero/dialogs/AboutWindow.java.orig

%build
export CLASSPATH=$(build-classpath sleep)
%{ant} -Djava.javadoc=%{_javadocdir}/java -Dsleep.javadoc=%{_javadocdir}/sleep jar

%install
%{__rm} -rf %{buildroot}

# jars
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a jerk.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

# data
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}/scripts
%{__cp} -a %{SOURCE100} %{SOURCE101} %{SOURCE102} %{SOURCE103} %{SOURCE104} %{SOURCE105} %{SOURCE106} %{buildroot}%{_datadir}/%{name}/scripts
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}/themes
%{__cp} -a %{SOURCE200} %{buildroot}%{_datadir}/%{name}/themes

# scripts
%{__mkdir_p} %{buildroot}%{_bindir}
%{__install} -p -m 755 %{SOURCE1} %{buildroot}%{_bindir}/%{name}

# javadoc
%{__mv} src/rero/dialogs/AboutWindow.java src/rero/dialogs/AboutWindow.java.orig
%{ant} -Djava.javadoc=%{_javadocdir}/java -Dsleep.javadoc=%{_javadocdir}/sleep docs
%{__mv} src/rero/dialogs/AboutWindow.java.orig src/rero/dialogs/AboutWindow.java
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})
%{__rm} -r docs/api

# freedesktop.org menu entry
%{_bindir}/desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Internet-Chat" \
  --dir %{buildroot}%{_datadir}/applications %{SOURCE5}

# icons for freedesktop.org and legacy menu entries
%{__install} -D -p -m 644 %{SOURCE2} %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{__install} -D -p -m 644 %{SOURCE3} %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{__install} -D -p -m 644 %{SOURCE4} %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{__install} -D -p -m 644 %{SOURCE4} %{buildroot}%{_datadir}/pixmaps/%{name}.png

%{__mkdir_p} %{buildroot}%{_sysconfdir}
%{__cat} > %{buildroot}%{_sysconfdir}/%{name}.conf << EOF
JAVA_HOME=%{_jvmdir}/java-1.4.2-jamvm-1.4.2.0
EOF

%{__perl} -pi -e 's/\r$//g' resources/toplevel/license.txt

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%post
%if %{gcj_support}
%{update_gcjdb}
%endif
%{update_desktop_database}
%update_icon_cache hicolor

%postun
%if %{gcj_support}
%{clean_gcjdb}
%endif
%{clean_desktop_database}
%clean_icon_cache hicolor

%files
%defattr(0644,root,root,0755)
%doc docs/* resources/toplevel/{*.txt,docs}
%attr(0755,root,root) %{_bindir}/*
%{_javadir}/%{name}.jar
%{_javadir}//%{name}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*.jar.*
%endif
%{_datadir}/%{name}
%{_datadir}/applications/*
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%config(noreplace) %{_sysconfdir}/%{name}.conf

%files javadoc
%defattr(0644,root,root,0755)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%doc %dir %{_javadocdir}/%{name}


