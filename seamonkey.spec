%define homepage http://russianfedora.ru/
%define default_bookmarks_file %{_datadir}/bookmarks/default-bookmarks.html
%define cairo_version 0.5

%define minimum_build_nspr_version 4.8.9
%define minimum_build_nss_version 3.13.1

%define build_langpacks 1

%define _unpackaged_files_terminate_build 0
%define builddir %{_builddir}/%{name}-%{version}
%define mozdir %{_libdir}/seamonkey-%{version}
%define sources_subdir comm-release


Name:           seamonkey
Summary:        Web browser, e-mail, news, IRC client, HTML editor
Version:        2.7.1
Release:        1%{?dist}.R
URL:            http://www.mozilla.org/projects/seamonkey/
License:        MPLv1.1
Group:          Applications/Internet

Source0:        ftp://ftp.mozilla.org/pub/seamonkey/releases/%{version}/source/seamonkey-%{version}.source.tar.bz2
Source1:        seamonkey-langpacks-%{version}-20120214.tar.xz
Source2:        seamonkey-icon.png
Source3:        seamonkey.sh.in
Source4:        seamonkey.desktop
Source7:        seamonkey-make-package.pl
Source10:       seamonkey-mozconfig
Source12:       seamonkey-mail.desktop
Source13:       seamonkey-mail-icon.png
Source17:       mozilla-psm-exclude-list
Source18:       mozilla-xpcom-exclude-list
Source20:       seamonkey-fedora-default-prefs.js
Source100:      find-external-requires

Patch1:         xulrunner-10.0-gcc47.patch
Patch5:         seamonkey-8.0-enable-addons.patch

Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  zlib-devel
BuildRequires:  zip
BuildRequires:  libIDL-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gtk2-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  gnome-vfs2-devel
BuildRequires:  libgnome-devel
BuildRequires:  libgnomeui-devel
BuildRequires:  krb5-devel
BuildRequires:  pango-devel
BuildRequires:  freetype-devel >= 2.1.9
BuildRequires:  glib2-devel
BuildRequires:  libXt-devel
BuildRequires:  libXrender-devel
BuildRequires:  fileutils
BuildRequires:  perl
BuildRequires:  alsa-lib-devel
BuildRequires:  hunspell-devel
BuildRequires:  system-bookmarks
BuildRequires:  libnotify-devel
BuildRequires:  yasm
BuildRequires:  mesa-libGL-devel
Requires:       system-bookmarks
Requires:       mozilla-filesystem

Obsoletes: seamonkey-chat
Obsoletes: seamonkey-devel
Obsoletes: seamonkey-dom-inspector
Obsoletes: seamonkey-js-debugger
Obsoletes: seamonkey-mail



AutoProv: 0
%define _use_internal_dependency_generator 0
%define __find_requires %{SOURCE100}


%description
SeaMonkey is an all-in-one Internet application suite. It includes 
a browser, mail/news client, IRC client, JavaScript debugger, and 
a tool to inspect the DOM for web pages. It is derived from the 
application formerly known as Mozilla Application Suite.
 

%prep

%setup -q -c
cd %{sources_subdir}

%if 0%{?fedora} >= 17
cd mozilla
%patch1 -p1 -b .gcc47
cd ..
%endif

%patch5 -p2 -b .addons

%{__rm} -f .mozconfig
%{__cp} %{SOURCE10} .mozconfig

%build
cd %{sources_subdir}

# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
#
# Disable C++ exceptions since Mozilla code is not exception-safe
#
MOZ_OPT_FLAGS=$(echo $RPM_OPT_FLAGS | \
                     %{__sed} -e 's/-Wall//' -e 's/-fexceptions/-fno-exceptions/g')
export CFLAGS=$MOZ_OPT_FLAGS
export CXXFLAGS=$MOZ_OPT_FLAGS

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

MOZ_SMP_FLAGS=-j1
%ifnarch ppc ppc64 s390 s390x
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -gt 1 ] && MOZ_SMP_FLAGS=-j2
%endif

make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS"

%install
%{__rm} -rf $RPM_BUILD_ROOT
cd %{sources_subdir}

DESTDIR=$RPM_BUILD_ROOT make install

# fix omni.jar to actually work
pushd mozilla/dist/bin
zip -d $RPM_BUILD_ROOT/%{mozdir}/omni.ja components/browser.xpt components/mail.xpt components/components.manifest chrome/localized.manifest chrome/nonlocalized.manifest
zip -9r $RPM_BUILD_ROOT/%{mozdir}/omni.ja chrome.manifest components/*.xpt chrome/*.manifest components/*.manifest components/*.js
popd

# create a list of all of the different package and the files that
# will hold them

%{__rm} -f %{builddir}/seamonkey.list

echo %defattr\(-,root,root\) > %{builddir}/seamonkey.list

# we don't want to ship mozilla's default sidebar components
%{__rm} -f $RPM_BUILD_ROOT/%{mozdir}/searchplugins/bugzilla.gif
%{__rm} -f $RPM_BUILD_ROOT/%{mozdir}/searchplugins/bugzilla.src
%{__rm} -f $RPM_BUILD_ROOT/%{mozdir}/searchplugins/dmoz.gif
%{__rm} -f $RPM_BUILD_ROOT/%{mozdir}/searchplugins/dmoz.src
%{__rm} -f $RPM_BUILD_ROOT/%{mozdir}/searchplugins/lxrmozilla.gif
%{__rm} -f $RPM_BUILD_ROOT/%{mozdir}/searchplugins/lxrmozilla.src
%{__rm} -f $RPM_BUILD_ROOT/%{mozdir}/searchplugins/mozilla.gif
%{__rm} -f $RPM_BUILD_ROOT/%{mozdir}/searchplugins/mozilla.src

## Copy over missing components
#install -c -m 644 mozilla/dist/bin/components/*.xpt \
#                  $RPM_BUILD_ROOT/%{mozdir}/components

# build all of the default browser components 
# base Seamonkey package (seamonkey.list) 
%{SOURCE7} --package xpcom --output-file %{builddir}/seamonkey.list \
    --package-file suite/installer/package-manifest \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir} \
    --exclude-file=%{SOURCE18}

%{SOURCE7} --package browser --output-file %{builddir}/seamonkey.list \
    --package-file suite/installer/package-manifest \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir}

%{SOURCE7} --package spellcheck --output-file %{builddir}/seamonkey.list \
    --package-file suite/installer/package-manifest \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir}

%{SOURCE7} --package psm --output-file %{builddir}/seamonkey.list \
    --package-file suite/installer/package-manifest \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir} \
    --exclude-file=%{SOURCE17}

%{SOURCE7} --package mail --output-file %{builddir}/seamonkey.list \
    --package-file suite/installer/package-manifest \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir}

%{SOURCE7} --package chatzilla --output-file %{builddir}/seamonkey.list \
    --package-file suite/installer/package-manifest \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir}

%{SOURCE7} --package venkman --output-file %{builddir}/seamonkey.list \
    --package-file suite/installer/package-manifest \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir}

%{SOURCE7} --package inspector --output-file %{builddir}/seamonkey.list \
    --package-file suite/installer/package-manifest \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir}

echo > ../%{name}.lang
%if %{build_langpacks}
# Install langpacks 
%{__mkdir_p} $RPM_BUILD_ROOT/%{mozdir}/extensions
%{__tar} xf %{SOURCE1}
for langpack in `ls seamonkey-langpacks/*.xpi`; do
  language=$(basename $langpack .xpi | sed 's/^seamonkey-//' | sed 's/\.langpack$//' | sed 's/\([0-9]\.\)*//')
  extensiondir=$RPM_BUILD_ROOT/%{mozdir}/extensions/langpack-$language@seamonkey.mozilla.org
  %{__mkdir_p} $extensiondir
  unzip $langpack -d $extensiondir
  find $extensiondir -type f | xargs chmod 644

#  tmpdir=`mktemp -d %{name}.XXXXXXXX`
#  langtmp=$tmpdir/%{name}/langpack-$language
#  %{__mkdir_p} $langtmp
  jarfile=$extensiondir/chrome/$language.jar
#  unzip $jarfile -d $langtmp

#  sed -i -e "s|browser.startup.homepage.*$|browser.startup.homepage=%{homepage}|g;" \
#         $langtmp/locale/$language/navigator-region/region.properties
  sed -i -e "s|browser.startup.homepage.*$|browser.startup.homepage=%{homepage}|g;" \
         $extensiondir/chrome/$language/locale/$language/navigator-region/region.properties

#  find $langtmp -type f | xargs chmod 644
#  %{__rm} -rf $jarfile
#  cd $langtmp
  cd $extensiondir/chrome/$language
  zip -r -D $jarfile locale
  cd -
#  %{__rm} -rf $tmpdir

  language=`echo $language | sed -e 's/-/_/g'`
  extensiondir=`echo $extensiondir | sed -e "s,^$RPM_BUILD_ROOT,,"`
  echo "%%lang($language) $extensiondir" >> ../%{name}.lang
done
%{__rm} -rf firefox-langpacks
%endif # build_langpacks

# set up our desktop files
%{__mkdir_p} $RPM_BUILD_ROOT/%{_datadir}/pixmaps/

# install desktop files in correct directory
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/applications/
desktop-file-install --vendor mozilla \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications \
    --add-category X-Fedora \
    --add-category Application \
    --add-category Network \
    %{SOURCE4}
desktop-file-install --vendor mozilla \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications \
    --add-category X-Fedora \
    --add-category Application \
    --add-category Network \
    %{SOURCE12}

install -c -m 644 %{SOURCE2} %{SOURCE13} \
  $RPM_BUILD_ROOT/%{_datadir}/pixmaps/

if [ ! -d $RPM_BUILD_ROOT/%{mozdir}/plugins/ ]; then
  mkdir -m 755 $RPM_BUILD_ROOT/%{mozdir}/plugins
fi

# install our seamonkey.sh file
rm -rf $RPM_BUILD_ROOT/usr/bin/seamonkey
cat %{SOURCE3} | sed -e 's/MOZILLA_VERSION/%{version}/g' \
		     -e 's,LIBDIR,%{_libdir},g' > \
  $RPM_BUILD_ROOT/usr/bin/seamonkey

chmod 755 $RPM_BUILD_ROOT/usr/bin/seamonkey

# set up our default preferences
%{__cat} %{SOURCE20} | %{__sed} -e 's,SEAMONKEY_RPM_VR,%{version}-%{release},g' > \
        $RPM_BUILD_ROOT/fc-default-prefs
%{__cp} $RPM_BUILD_ROOT/fc-default-prefs $RPM_BUILD_ROOT/%{mozdir}/defaults/pref/all-fedora.js
%{__rm} $RPM_BUILD_ROOT/fc-default-prefs

# set up our default bookmarks
%{__rm} -f $RPM_BUILD_ROOT/%{mozdir}/defaults/profile/bookmarks.html
ln -s %{default_bookmarks_file} $RPM_BUILD_ROOT/%{mozdir}/defaults/profile/bookmarks.html

rm -f $RPM_BUILD_ROOT%{mozappdir}/*.chk

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post
update-desktop-database %{_datadir}/applications

%postun
update-desktop-database %{_datadir}/applications


%files -f seamonkey.list
%defattr(-,root,root)
%{_bindir}/seamonkey
%{_datadir}/pixmaps/seamonkey-icon.png
%{_datadir}/pixmaps/seamonkey-mail-icon.png

# search engines
%{mozdir}/searchplugins/*.xml

# dictionaries
%{mozdir}/dictionaries/*

# Profile?
%{mozdir}/defaults/profile/*

# some rest
%{mozdir}/omni.ja
%{mozdir}/chrome.manifest
%{mozdir}/components/binary.manifest
#%{mozdir}/components/*.xpt
%{mozdir}/components/*.so
%{mozdir}/defaults/messenger/mailViews.dat
%{mozdir}/extensions/*

#%doc %{_mandir}/man1/seamonkey.1.gz

%dir %{mozdir}
%dir %{mozdir}/defaults/pref
%dir %{mozdir}/defaults/profile
%dir %{mozdir}/defaults/messenger
%dir %{mozdir}/defaults

%dir %{mozdir}/chrome/icons/default
%dir %{mozdir}/chrome/icons
%dir %{mozdir}/chrome


%dir %{mozdir}/components
%dir %{mozdir}/searchplugins

%dir %{mozdir}/isp
%dir %{mozdir}/dictionaries

%dir %{mozdir}/plugins

%{mozdir}/defaults/pref/all-fedora.js

%{_datadir}/applications/mozilla-%{name}.desktop
%{_datadir}/applications/mozilla-%{name}-mail.desktop

%ghost %{mozdir}/removed-files


%changelog
* Wed Feb 22 2012 Arkady L. Shane <ashejn@russianfedora.ru> 2.7.1-1.R
- rebuilt for EL6

* Tue Feb 14 2012 Martin Stransky <stransky@redhat.com> 2.7.1-1
- Update to 2.7.1

* Mon Feb  6 2012 Martin Stransky <stransky@redhat.com> 2.7-2
- gcc 4.7 build fixes

* Fri Feb  3 2012 Martin Stransky <stransky@redhat.com> 2.7-1
- Update to 2.7

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 14 2011 Martin Stransky <stransky@redhat.com> 2.5-2
- Fixed langpacks

* Thu Dec  8 2011 Martin Stransky <stransky@redhat.com> 2.5-1
- Update to 2.5

* Fri Oct 14 2011 Dan Horák <dan[at]danny.cz> - 2.4.1-3
- fix build on secondary arches

* Tue Oct 11 2011 Kai Engert <kaie@redhat.com> - 2.4.1-2
- Update to 2.4.1

* Tue Sep 06 2011 Kai Engert <kaie@redhat.com> - 2.3.3-2
- Update to 2.3.3
 
* Sun Aug 21 2011 Kai Engert <kaie@redhat.com> - 2.3-2
- Update to 2.3
 
* Wed May 25 2011 Caolán McNamara <caolanm@redhat.com> - 2.0.14-2
- rebuild for new hunspell

* Fri Apr 29 2011 Jan Horak <jhorak@redhat.com> - 2.0.14-1
- Update to 2.0.14

* Sat Apr  9 2011 Christopher Aillon <caillon@redhat.com> 2.0.13-1
- Update to 2.0.13

* Mon Mar  7 2011 Martin Stransky <stransky@redhat.com> 2.0.12-1
- Update to 2.0.12

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 04 2011 Adel Gadllah <adel.gadllah@gmail.com> 2.0.11-3
- BR dbus-glib-devel

* Tue Jan 04 2011 Adel Gadllah <adel.gadllah@gmail.com> 2.0.11-2
- disabled system cairo, breaks animated gifs (rhbz#628331)

* Mon Dec 13 2010 Martin Stransky <stransky@redhat.com> 2.0.11-1
- Update to 2.0.11

* Mon Nov 1 2010 Martin Stransky <stransky@redhat.com> 2.0.10-1
- Update to 2.0.10

* Thu Oct 21 2010 Martin Stransky <stransky@redhat.com> 2.0.9-1
- Update to 2.0.9

* Wed Oct 13 2010 Martin Stransky <stransky@redhat.com> 2.0.8-2
- Added fix for mozbz#522635

* Wed Sep 22 2010 Martin Stransky <stransky@redhat.com> 2.0.8-1
- Update to 2.0.8

* Tue Jul 20 2010 Martin Stransky <stransky@redhat.com> 2.0.6-1
- Update to 2.0.6

* Wed Jun 23 2010 Martin Stransky <stransky@redhat.com> 2.0.5-1
- Update to 2.0.5

* Fri Apr 01 2010 Martin Stransky <stransky@redhat.com> 2.0.4-1
- Update to 2.0.4

* Wed Feb 17 2010 Martin Stransky <stransky@redhat.com> 2.0.3-1
- Update to 2.0.3

* Thu Dec 17 2009 Jan Horak <jhorak@redhat.com> - 2.0.1-1
- Update to 2.0.1

* Tue Oct 27 2009 Martin Stransky <stransky@redhat.com> 2.0-7
- Update to 2.0

* Tue Oct 21 2009 Martin Stransky <stransky@redhat.com> 2.0-6
- Fixed launcher script

* Tue Oct 19 2009 Martin Stransky <stransky@redhat.com> 2.0-5
- Update to 2.0 RC2

* Tue Oct 13 2009 Martin Stransky <stransky@redhat.com> 2.0-4
- Update to 2.0 RC1

* Wed Sep 23 2009 Martin Stransky <stransky@redhat.com> 2.0-3.beta2
- Update to 2.0 beta 2

* Thu Aug 6 2009 Martin Stransky <stransky@redhat.com> 2.0-2.beta1
- Added fix for #437596

* Wed Jul 22 2009 Martin Stransky <stransky@redhat.com> 2.0-1.beta1
- Update to 2.0 beta 1

* Fri Jul 10 2009 Martin Stransky <stransky@redhat.com> 1.1.17-1
- Update to 1.1.17

* Thu Jun 18 2009 Kai Engert <kaie@redhat.com> 1.1.16-3
- fix categories in desktop files

* Wed May 7 2009 Kai Engert <kaie@redhat.com> 1.1.16-2
- Update to 1.1.16

* Wed May 6 2009 Martin Stransky <stransky@redhat.com> 1.1.15-4
- build with -fno-strict-aliasing (#468415)

* Fri Mar 27 2009 Christopher Aillon <caillon@redhat.com> - 1.15.1-3
- Add patches for MFSA-2009-12, MFSA-2009-13

* Wed Mar 25 2009 Christopher Aillon <caillon@redhat.com> - 1.15.1-2
- Update default homepage

* Wed Mar  4 2009 Fedora Security Response Team <fedora-security-list@redhat.com> - 1.1.15-1
- Update to 1.1.15

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Christopher Aillon <caillon@redhat.com> - 1.1.14-3
- Drop explicit requirement on desktop-file-utils

* Wed Jan 07 2009 Christopher Aillon <caillon@redhat.com> - 1.1.14-2
- Disable the crash dialog

* Wed Dec 17 2008 Kai Engert <kengert@redhat.com> - 1.1.14-1
- Update to 1.1.14
* Thu Dec 11 2008 Kai Engert <kengert@redhat.com> - 1.1.13-1
- Update to 1.1.13
- own additional directories, bug 474039
* Thu Sep 25 2008 Christopher Aillon <caillon@redhat.com> - 1.1.12-1
- Update to 1.1.12
* Sat Jul  6 2008 Christopher Aillon <caillon@redhat.com> - 1.1.10-1
- Update to 1.1.10
- Use bullet characters to match GTK+
* Wed Apr 30 2008 Christopher Aillon <caillon@redhat.com> - 1.1.9-4
- Require mozilla-filesystem and drop its requires
* Thu Apr 17 2008 Kai Engert <kengert@redhat.com> - 1.1.9-3
- add several upstream patches, not yet released:
  425576 (crash), 323508, 378132, 390295, 421622
* Fri Mar 28 2008 Kai Engert <kengert@redhat.com> - 1.1.9-2
- SeaMonkey 1.1.9
* Sat Mar 15 2008 Christopher Aillon <caillon@redhat.com> - 1.1.8-6
- Use the Fedora system bookmarks as default
* Sat Mar 15 2008 Christopher Aillon <caillon@redhat.com> - 1.1.8-5
- Avoid conflicts between gecko debuginfo packages
* Thu Feb 14 2008 Kai Engert <kengert@redhat.com> - 1.1.8-4
- remove workaround for 432138, use upstream patch
* Sat Feb 09 2008 Kai Engert <kengert@redhat.com> - 1.1.8-3
- make it build with nss 3.12, mozilla bug 399589
- work around an issue with gcc 4.3.0, redhat bug 432138
* Fri Feb 08 2008 Kai Engert <kengert@redhat.com> - 1.1.8-2
- SeaMonkey 1.1.8
* Mon Jan 07 2008 Kai Engert <kengert@redhat.com> - 1.1.7-4
- Create and own /etc/skel/.mozilla
* Mon Dec 03 2007 Kai Engert <kengert@redhat.com> - 1.1.7-3
- fix dependencies, requires nspr 4.6.99 / nss 3.11.99
* Sun Dec 02 2007 Kai Engert <kengert@redhat.com> - 1.1.7-2
- SeaMonkey 1.1.7
* Mon Nov 05 2007 Kai Engert <kengert@redhat.com> - 1.1.6-2
- SeaMonkey 1.1.6
* Fri Oct 19 2007 Kai Engert <kengert@redhat.com> - 1.1.5-2
- SeaMonkey 1.1.5
* Mon Sep 10 2007 Martin Stransky <stransky@redhat.com> 1.1.3-8
- added fix for #246248 - firefox crashes when searching for word "do"
* Tue Aug 28 2007 Kai Engert <kengert@redhat.com> - 1.1.3-7
- Updated license tag
* Mon Aug 7 2007 Martin Stransky <stransky@redhat.com> 1.1.3-6
- removed plugin configuration utility
* Mon Aug 6 2007 Martin Stransky <stransky@redhat.com> 1.1.3-5
- unwrapped plugins moved to the old location
* Mon Jul 30 2007 Martin Stransky <stransky@redhat.com> 1.1.3-4
- added nspluginwrapper support
* Fri Jul 27 2007 Martin Stransky <stransky@redhat.com> - 1.1.3-3
- added pango patches
* Fri Jul 20 2007 Kai Engert <kengert@redhat.com> - 1.1.3-2
- SeaMonkey 1.1.3
* Thu May 31 2007 Kai Engert <kengert@redhat.com> 1.1.2-2
- SeaMonkey 1.1.2
* Wed Feb 28 2007 Kai Engert <kengert@redhat.com> 1.1.1-2
- SeaMonkey 1.1.1
* Wed Feb 07 2007 Kai Engert <kengert@redhat.com> 1.1-2
- Update to SeaMonkey 1.1
- Pull in patches used by Firefox Fedora RPM package.
- Fix the DND implementation to not grab, so it works with new GTK+.
- Fix upgrade path from FC-5 by obsoleting the seamonkey subset
  packages which recently obsoleted mozilla in FC-5.
* Sat Dec 23 2006 Kai Engert <kengert@redhat.com> 1.0.7-1
- SeaMonkey 1.0.7
* Fri Nov 10 2006 Kai Engert <kengert@redhat.com> 1.0.6-2
- Do not run regchrome.
- Fix some .dat and .rdf ghost files.
* Thu Nov 09 2006 Kai Engert <kengert@redhat.com> 1.0.6-1
- SeaMonkey 1.0.6
* Thu Sep 14 2006 Kai Engert <kengert@redhat.com> 1.0.5-1
- SeaMonkey 1.0.5
* Wed Sep 06 2006 Kai Engert <kengert@redhat.com> 1.0.4-8
- patch5 -p0
* Wed Sep 06 2006 Kai Engert <kengert@redhat.com> 1.0.4-7
- Synch patches with those found in the Firefox package.
- Add missing, clean up BuildRequires
- Use --enable-system-cairo
- Use a dynamic approach to require at least the NSPR/NSS 
  library release used at build time.
* Tue Aug 15 2006 Kai Engert <kengert@redhat.com> 1.0.4-6
- Yet another forgotten patch file.
* Tue Aug 15 2006 Kai Engert <kengert@redhat.com> 1.0.4-5
- Commit forgotten visibility patch file.
* Thu Aug 04 2006 Kai Engert <kengert@redhat.com> 1.0.4-4
- Use a different patch to disable visibility.
* Thu Aug 04 2006 Kai Engert <kengert@redhat.com> 1.0.4-3
- Fix a build failure in mailnews mime code.
* Thu Aug 03 2006 Kai Engert <kengert@redhat.com> 1.0.4-2
- SeaMonkey 1.0.4
* Wed Jun 07 2006 Kai Engert <kengert@redhat.com> 1.0.2-1
- Update to SeaMonkey 1.0.2 release
* Fri Apr 14 2006 Kai Engert <kengert@redhat.com> 1.0.1-1
- Update to SeaMonkey 1.0.1 release
* Tue Apr 11 2006 Kai Engert <kengert@redhat.com> 1.0-11
- Fix PreReq statements
* Tue Apr 11 2006 Kai Engert <kengert@redhat.com> 1.0-10
- Added libXt-devel BuildRequires
* Mon Apr 10 2006 Kai Engert <kengert@redhat.com> 1.0-9
- Added dist suffix to release
* Fri Mar 17 2006 Kai Engert <kengert@redhat.com> 1.0-8
- Changed license to MPL
* Tue Mar 14 2006 Kai Engert <kengert@redhat.com> 1.0-7
- updated %files section, removed %preun,
- removed explicit nspr/nss requires
* Thu Mar 02 2006 Kai Engert <kengert@redhat.com> 1.0-6
- Use a single package for all included applications.
- Make sure installed JavaScript files are not executable.
- Disable AutoProv, use find-external-requires.
* Fri Feb 10 2006 Kai Engert <kengert@redhat.com> 1.0-4
- Addressed several review comments, see bugzilla.redhat.com #179802.
* Sat Jan 28 2006 Kai Engert <kengert@redhat.com> 1.0-1
- Initial version based on Seamonkey 1.0, using a combination of patches 
  from Mozilla 1.7.x, Firefox 1.5 and Thunderbird 1.5 RPM packages.
