%define default_bookmarks_file %{_datadir}/bookmarks/default-bookmarks.html
%define desktop_file_utils_version 0.9
%define cairo_version 0.5

%define minimum_build_nspr_version 4.7.2
%define minimum_build_nss_version 3.12

%define _unpackaged_files_terminate_build 0
%define builddir %{_builddir}/%{name}-%{version}
%define mozdir %{_libdir}/seamonkey-%{version}

Name:           seamonkey
Summary:        Web browser, e-mail, news, IRC client, HTML editor
Version:        1.1.17
Release:        1%{?dist}
URL:            http://www.mozilla.org/projects/seamonkey/
License:        MPLv1.1
Group:          Applications/Internet

Source0:        seamonkey-%{version}.source.tar.bz2
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

Patch1:         firefox-1.0-prdtoa.patch
Patch2:         firefox-2.0-link-layout.patch
Patch3:         seamonkey-1.1.9plus.patch
Patch21:        firefox-0.7.3-default-plugin-less-annoying.patch
Patch22:        firefox-0.7.3-psfonts.patch
Patch41:        firefox-2.0.0.4-undo-uriloader.patch
Patch42:        firefox-1.1-uriloader.patch
Patch81:        firefox-1.5-nopangoxft.patch
Patch83:        firefox-1.5-pango-cursor-position.patch
Patch84:        firefox-2.0-pango-printing.patch
Patch85:        firefox-2.0-pango-ligatures.patch
Patch86:        firefox-1.5-pango-cursor-position-more.patch
Patch87:        firefox-1.5-pango-justified-range.patch
Patch88:        firefox-1.5-pango-underline.patch
Patch91:        thunderbird-0.7.3-gnome-uriloader.patch
Patch100:       firefox-1.5-bullet-bill.patch
Patch102:       firefox-1.5-theme-change.patch
Patch220:       seamonkey-fedora-home-page.patch
Patch225:       mozilla-nspr-packages.patch
Patch301:       mozilla-1.7.3-gnome-vfs-default-app.patch
Patch304:       mozilla-1.7.5-g-application-name.patch

Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  nspr-devel >= %{minimum_build_nspr_version}
BuildRequires:  nss-devel >= %{minimum_build_nss_version}
BuildRequires:  cairo-devel >= %{cairo_version}
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  zlib-devel
BuildRequires:  zip
BuildRequires:  libIDL-devel
BuildRequires:  desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires:  gtk2-devel
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
BuildRequires:  system-bookmarks
Requires:       system-bookmarks
Requires:       mozilla-filesystem

Obsoletes: seamonkey-chat
Obsoletes: seamonkey-devel
Obsoletes: seamonkey-dom-inspector
Obsoletes: seamonkey-js-debugger
Obsoletes: seamonkey-mail

PreReq:         desktop-file-utils >= %{desktop_file_utils_version}

#%global nspr_build_time_version %(nspr-config --version)

#%if "%{?nspr_build_time_version}" > "0"
#Requires: nspr >= %{nspr_build_time_version}
#%else
Requires: nspr >= %{minimum_build_nspr_version}
#%endif

#%global nss_build_time_version %(nss-config --version)

#%if "%{?nss_build_time_version}" > "0"
#Requires: nss >= %{nss_build_time_version}
#%else
Requires: nss >= %{minimum_build_nss_version}
#%endif


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
cd mozilla
%patch1  -p0
%patch2  -p1
#%patch3  -p1
%patch22 -p1
%patch41 -p1
%patch42 -p0
%patch81 -p1
%patch83 -p1
%patch84 -p0
%patch85 -p1
%patch86 -p1
%patch87 -p1
%patch88 -p1
%patch91 -p1 -b .gnome-uriloader
%patch100 -p1 -b .bullet-bill
%patch102 -p0 -b .theme-change
%patch220 -p1
%patch225 -p1
%patch301 -p1
%patch304 -p0

%{__rm} -f .mozconfig
%{__cp} %{SOURCE10} .mozconfig

%build
cd mozilla

# Set up build flags (#468415)
OPT_FLAGS="$RPM_OPT_FLAGS"
OPT_FLAGS+=" -fno-strict-aliasing"

XCFLAGS=-g \
CFLAGS=-g \
%ifarch ia64 ppc
CXXFLAGS="-fno-inline -g" \
%else
CXXFLAGS=-g \
%endif
BUILD_OFFICIAL=1 MOZILLA_OFFICIAL=1 \
./configure --prefix=%{_prefix} --libdir=%{_libdir} \
--with-default-mozilla-five-home=%{mozdir} \
--mandir=%{_mandir} \
--enable-optimize="$OPT_FLAGS"

BUILD_OFFICIAL=1 MOZILLA_OFFICIAL=1 make export
BUILD_OFFICIAL=1 MOZILLA_OFFICIAL=1 make %{?_smp_mflags} libs

%install
%{__rm} -rf $RPM_BUILD_ROOT
cd mozilla

BUILD_OFFICIAL=1 MOZILLA_OFFICIAL=1 \
	DESTDIR=$RPM_BUILD_ROOT \
	make install

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

# build all of the default browser components
# base Seamonkey package (seamonkey.list)
%{SOURCE7} --package langenus --output-file %{builddir}/seamonkey.list \
    --package-file xpinstall/packager/packages-unix \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir}

%{SOURCE7} --package regus --output-file %{builddir}/seamonkey.list \
    --package-file xpinstall/packager/packages-unix \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir}

%{SOURCE7} --package deflenus --output-file %{builddir}/seamonkey.list \
    --package-file xpinstall/packager/packages-unix \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir}

%{SOURCE7} --package xpcom --output-file %{builddir}/seamonkey.list \
    --package-file xpinstall/packager/packages-unix \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir} \
    --exclude-file=%{SOURCE18}

%{SOURCE7} --package browser --output-file %{builddir}/seamonkey.list \
    --package-file xpinstall/packager/packages-unix \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir}

%{SOURCE7} --package spellcheck --output-file %{builddir}/seamonkey.list \
    --package-file xpinstall/packager/packages-unix \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir}

%{SOURCE7} --package psm --output-file %{builddir}/seamonkey.list \
    --package-file xpinstall/packager/packages-unix \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir} \
    --exclude-file=%{SOURCE17}

%{SOURCE7} --package mail --output-file %{builddir}/seamonkey.list \
    --package-file xpinstall/packager/packages-unix \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir}

%{SOURCE7} --package chatzilla --output-file %{builddir}/seamonkey.list \
    --package-file xpinstall/packager/packages-unix \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir}

%{SOURCE7} --package venkman --output-file %{builddir}/seamonkey.list \
    --package-file xpinstall/packager/packages-unix \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir}

%{SOURCE7} --package inspector --output-file %{builddir}/seamonkey.list \
    --package-file xpinstall/packager/packages-unix \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir}

# build our initial component and chrome registry

pushd `pwd`
  cd $RPM_BUILD_ROOT/%{mozdir}

  # save a copy of the default installed-chrome.txt file before we
  # muck with it
  mkdir chrome/lang
  cp chrome/installed-chrome.txt chrome/lang/

  # set up the default skin and locale to trigger the generation of
  # the user-locales and users-skins.rdf
  echo "skin,install,select,classic/1.0" >> chrome/installed-chrome.txt
  echo "locale,install,select,en-US" >> chrome/installed-chrome.txt

  # save the defaults in a file that will be used later to rebuild the
  # installed-chrome.txt file
  echo "skin,install,select,classic/1.0" >> chrome/lang/default.txt
  echo "locale,install,select,en-US" >> chrome/lang/default.txt

  # fix permissions of the chrome directories
  /usr/bin/find . -type d -perm 0700 -exec chmod 755 {} \; || :

  # We don't want JS files to be executable
  /usr/bin/find . -type f -name \*.js -exec chmod 644 {} \; || :
popd

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

# ghost files
touch $RPM_BUILD_ROOT%{mozdir}/chrome/chrome.rdf
for overlay in {"browser","communicator","cookie","editor","global","inspector","messenger","navigator"}; do
   %{__mkdir_p} $RPM_BUILD_ROOT%{mozdir}/chrome/overlayinfo/$overlay/content
  touch $RPM_BUILD_ROOT%{mozdir}/chrome/overlayinfo/$overlay/content/overlays.rdf
done
for overlay in {"browser","global"}; do
   %{__mkdir_p} $RPM_BUILD_ROOT%{mozdir}/chrome/overlayinfo/$overlay/skin
  touch $RPM_BUILD_ROOT%{mozdir}/chrome/overlayinfo/$overlay/skin/stylesheets.rdf
done
touch $RPM_BUILD_ROOT%{mozdir}/chrome/chrome.rdf
%{__mkdir_p} $RPM_BUILD_ROOT%{mozdir}/components/myspell
touch $RPM_BUILD_ROOT%{mozdir}/components/compreg.dat
touch $RPM_BUILD_ROOT%{mozdir}/components/xpti.dat


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

%ghost %{mozdir}/components/compreg.dat
%ghost %{mozdir}/components/xpti.dat

%doc %{_mandir}/man1/seamonkey.1.gz

%dir %{mozdir}
%dir %{mozdir}/init.d
%dir %{mozdir}/defaults/pref
%dir %{mozdir}/defaults/profile
%dir %{mozdir}/defaults/profile/US
%dir %{mozdir}/defaults/wallet
%dir %{mozdir}/defaults/autoconfig
%dir %{mozdir}/defaults/messenger/US
%dir %{mozdir}/defaults/messenger
%dir %{mozdir}/defaults

%dir %{mozdir}/chrome/icons/default
%dir %{mozdir}/chrome/icons
%dir %{mozdir}/chrome/lang
%dir %{mozdir}/chrome

%dir %{mozdir}/res/dtd
%dir %{mozdir}/res/fonts
%dir %{mozdir}/res

%dir %{mozdir}/components/myspell
%dir %{mozdir}/components
%dir %{mozdir}/searchplugins

%dir %{mozdir}/plugins
%dir %{mozdir}/res/html
%dir %{mozdir}/res/samples
%dir %{mozdir}/res/entityTables

%verify (not md5 mtime size) %{mozdir}/chrome/installed-chrome.txt
%{mozdir}/chrome/lang/installed-chrome.txt
%{mozdir}/chrome/lang/default.txt

%{mozdir}/defaults/pref/all-fedora.js

%ghost %{mozdir}/chrome/chrome.rdf

%ghost %{mozdir}/chrome/overlayinfo/browser/skin/stylesheets.rdf
%ghost %{mozdir}/chrome/overlayinfo/global/skin/stylesheets.rdf

%ghost %{mozdir}/chrome/overlayinfo/browser/content/overlays.rdf
%ghost %{mozdir}/chrome/overlayinfo/communicator/content/overlays.rdf
%ghost %{mozdir}/chrome/overlayinfo/global/content/overlays.rdf
%ghost %{mozdir}/chrome/overlayinfo/editor/content/overlays.rdf
%ghost %{mozdir}/chrome/overlayinfo/navigator/content/overlays.rdf
%ghost %{mozdir}/chrome/overlayinfo/cookie/content/overlays.rdf

%ghost %{mozdir}/chrome/overlayinfo/messenger/content/overlays.rdf
%ghost %{mozdir}/chrome/overlayinfo/inspector/content/overlays.rdf

%dir %{mozdir}/chrome/overlayinfo/browser/content
%dir %{mozdir}/chrome/overlayinfo/browser/skin
%dir %{mozdir}/chrome/overlayinfo/browser
%dir %{mozdir}/chrome/overlayinfo/global/content
%dir %{mozdir}/chrome/overlayinfo/global/skin
%dir %{mozdir}/chrome/overlayinfo/global
%dir %{mozdir}/chrome/overlayinfo/communicator/content
%dir %{mozdir}/chrome/overlayinfo/communicator
%dir %{mozdir}/chrome/overlayinfo/editor/content
%dir %{mozdir}/chrome/overlayinfo/editor
%dir %{mozdir}/chrome/overlayinfo/navigator/content
%dir %{mozdir}/chrome/overlayinfo/navigator
%dir %{mozdir}/chrome/overlayinfo/cookie/content
%dir %{mozdir}/chrome/overlayinfo/cookie

%dir %{mozdir}/chrome/overlayinfo/messenger/content
%dir %{mozdir}/chrome/overlayinfo/messenger

%dir %{mozdir}/chrome/overlayinfo/inspector/content
%dir %{mozdir}/chrome/overlayinfo/inspector

%dir %{mozdir}/chrome/overlayinfo
%dir %{mozdir}/greprefs

%{_datadir}/applications/mozilla-%{name}.desktop
%{_datadir}/applications/mozilla-%{name}-mail.desktop


%changelog
* Fri Jul 10 2009 Martin Stransky <stransky@redhat.com> 1.1.17-1
- Update to 1.1.17

* Wed May 7 2009 Kai Engert <kaie@redhat.com> 1.1.16-1
- Update to 1.1.16

* Fri Mar 27 2009 Christopher Aillon <caillon@redhat.com> - 1.15.1-3
- Add patches for MFSA-2009-12, MFSA-2009-13

* Wed Mar 25 2009 Christopher Aillon <caillon@redhat.com> - 1.15.1-2
- Update default homepage

* Wed Mar  4 2009 Fedora Security Response Team <fedora-security-list@redhat.com> - 1.1.15-1
- Update to 1.1.15

* Mon Jan 8 2009 Martin Stransky <stransky@redhat.com> 1.1.14-4
- build with -fno-strict-aliasing (#468415)

* Wed Jan 07 2009 Christopher Aillon <caillon@redhat.com> - 1.1.14-3
- Disable the crash dialog

* Mon Jan 5 2009 Martin Stransky <stransky@redhat.com> 1.1.14-2
- disabled -O2 optimalization for i386 as a workaround for #468415
* Wed Dec 17 2008 Kai Engert <kengert@redhat.com> - 1.1.14-1
- Update to 1.1.14
* Wed Nov 12 2008 Christopher Aillon <caillon@redhat.com> - 1.1.13-1
- Update to 1.1.13
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
