%define desktop_file_utils_version 0.9
%define cairo_version 0.5

%define minimum_build_nspr_version 4.6.1
%define minimum_build_nss_version 3.11.1

%define _unpackaged_files_terminate_build 0
%define builddir %{_builddir}/mozilla
%define mozdir %{_libdir}/seamonkey-%{version}

Name:           seamonkey
Summary:        Web browser, e-mail, news, IRC client, HTML editor
Version:        1.0.9
Release:        3%{?dist}
URL:            http://www.mozilla.org/projects/seamonkey/
License:        MPL
Group:          Applications/Internet

#Source0:        seamonkey-%{version}.source.tar.bz2
Source0:        mozilla-180-20071018.tar.bz2
Source1:        seamonkey.sh.in
Source2:        seamonkey-icon.png
Source4:        seamonkey.desktop
Source6:        nss-clobber.sh
Source7:        seamonkey-make-package.pl
Source10:       seamonkey-mozconfig
Source12:       seamonkey-mail.desktop
Source13:       seamonkey-mail-icon.png
Source17:       mozilla-psm-exclude-list
Source18:       mozilla-xpcom-exclude-list
Source19:       seamonkey-fedora-default-bookmarks.html
Source20:       seamonkey-fedora-default-prefs.js
Source100:      find-external-requires

Patch1:         firefox-1.0-prdtoa.patch
Patch2:         mozilla-version.patch
Patch3:         firefox-1.5.0.10-nss-system-nspr.patch
Patch4:         firefox-1.5.0.10-with-system-nss.patch
Patch5:         firefox-1.1-visibility.patch
Patch6:         seamonkey-1.0.1-dumpstack.patch
Patch21:        firefox-0.7.3-default-plugin-less-annoying.patch
Patch22:        firefox-0.7.3-psfonts.patch
Patch42:        firefox-1.1-uriloader.patch

Patch50:        mozilla-358594.patch
#Patch51:        mozilla-379245.patch
#Patch52:        mozilla-382532.patch
Patch53:        mozilla-178993.patch
Patch55:        mozilla-384925.patch
Patch56:        mozilla-381300.patch

Patch60:        mozilla-309322_180_att283610.patch
Patch61:        mozilla-267833.patch
Patch62:        mozilla-345305_venkmanonly.patch
Patch63:        mozilla-361745.patch
Patch64:        mozilla-362901.patch
Patch65:        mozilla-372309.patch
Patch66:        mozilla-378787.patch
Patch67:        mozilla-384105.patch
Patch68:        mozilla-386914.patch
Patch69:        mozilla-387033.patch
Patch70:        mozilla-387881.patch
Patch71:        mozilla-388121.patch
Patch72:        mozilla-388784.patch
Patch73:        mozilla-390078.patch
Patch74:        mozilla-393537.patch
Patch75:        mozilla-395942-180.patch
Patch76:        mozilla-325761.patch
Patch77:        mozilla-392149-180.patch

# font system fixes
Patch81:        firefox-1.5-nopangoxft.patch
Patch82:        firefox-1.5-pango-mathml.patch
Patch83:        firefox-1.5-pango-cursor-position.patch
Patch84:        firefox-1.5-pango-printing.patch
Patch85:        firefox-1.5-pango-cursor-position-more.patch
Patch86:        firefox-1.5-pango-justified-range.patch
Patch87:        firefox-1.5-pango-underline.patch
Patch88:        firefox-1.5-xft-rangewidth.patch

Patch101:       thunderbird-0.7.3-gnome-uriloader.patch
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

Obsoletes: seamonkey-chat
Obsoletes: seamonkey-devel
Obsoletes: seamonkey-dom-inspector
Obsoletes: seamonkey-js-debugger
Obsoletes: seamonkey-mail

PreReq:         desktop-file-utils >= %{desktop_file_utils_version}

%global nspr_build_time_version %(nspr-config --version)

%if "%{?nspr_build_time_version}" > "0"
Requires: nspr >= %{nspr_build_time_version}
%else
Requires: nspr >= %{minimum_build_nspr_version}
%endif

%global nss_build_time_version %(nss-config --version)

%if "%{?nss_build_time_version}" > "0"
Requires: nss >= %{nss_build_time_version}
%else
Requires: nss >= %{minimum_build_nss_version}
%endif


AutoProv: 0
%define _use_internal_dependency_generator 0
%define __find_requires %{SOURCE100}


%description
SeaMonkey is an all-in-one Internet application suite. It includes 
a browser, mail/news client, IRC client, JavaScript debugger, and 
a tool to inspect the DOM for web pages. It is derived from the 
application formerly known as Mozilla Application Suite.
 

%prep

%setup -q -n mozilla
%patch1  -p0
%patch2  -p2
%patch3  -p1
%patch4  -p1

# Pragma visibility is broken on most platforms for some reason.
# It works on i386 so leave it alone there.  Disable elsewhere.
# See http://gcc.gnu.org/bugzilla/show_bug.cgi?id=20297
%ifnarch i386
%patch5  -p0
%endif

%patch6 -p1
%patch21 -p1
%patch22 -p1
%patch42 -p0

%patch50 -p1
#%patch51 -p1
#%patch52 -p1
%patch53 -p1
%patch55 -p1
%patch56 -p1

%patch60 -p1
%patch61 -p1
%patch62 -p1
%patch63 -p1
%patch64 -p1
%patch65 -p1
%patch66 -p1
%patch67 -p1
%patch68 -p1
%patch69 -p1
%patch70 -p1
%patch71 -p1
%patch72 -p1
%patch73 -p1
%patch74 -p1
%patch75 -p1
%patch76 -p1
%patch77 -p1

%patch81 -p1
%patch82 -p1
%patch83 -p1
%patch84 -p1
%patch85 -p1
%patch86 -p1
%patch87 -p1
%patch88 -p1
pushd gfx/src/ps
  # This sort of sucks, but it works for now.
  ln -s ../gtk/nsFontMetricsPango.h .
  ln -s ../gtk/nsFontMetricsPango.cpp .
  ln -s ../gtk/mozilla-decoder.h .
  ln -s ../gtk/mozilla-decoder.cpp .
popd

%patch101 -p1 -b .gnome-uriloader
%patch220 -p1
%patch225 -p1
%patch301 -p1
%patch304 -p0

%{__rm} -f .mozconfig
%{__cp} %{SOURCE10} .mozconfig

# set up our default bookmarks
%{__cp} %{SOURCE19} $RPM_BUILD_DIR/mozilla/profile/defaults/bookmarks.html

sh %{SOURCE6} > /dev/null

%build

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
--mandir=%{_mandir}

BUILD_OFFICIAL=1 MOZILLA_OFFICIAL=1 make export
BUILD_OFFICIAL=1 MOZILLA_OFFICIAL=1 make %{?_smp_mflags} libs


%install
%{__rm} -rf $RPM_BUILD_ROOT

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
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir}

%{SOURCE7} --package regus --output-file %{builddir}/seamonkey.list \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir}

%{SOURCE7} --package deflenus --output-file %{builddir}/seamonkey.list \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir}

%{SOURCE7} --package xpcom --output-file %{builddir}/seamonkey.list \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir} \
    --exclude-file=%{SOURCE18}

%{SOURCE7} --package browser --output-file %{builddir}/seamonkey.list \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir}

%{SOURCE7} --package spellcheck --output-file %{builddir}/seamonkey.list \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir}

%{SOURCE7} --package psm --output-file %{builddir}/seamonkey.list \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir} \
    --exclude-file=%{SOURCE17}

%{SOURCE7} --package mail --output-file %{builddir}/seamonkey.list \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir}

%{SOURCE7} --package chatzilla --output-file %{builddir}/seamonkey.list \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir}

%{SOURCE7} --package venkman --output-file %{builddir}/seamonkey.list \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --install-dir $RPM_BUILD_ROOT/%{mozdir} \
    --install-root %{mozdir}

%{SOURCE7} --package inspector --output-file %{builddir}/seamonkey.list \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
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
cat %{SOURCE1} | sed -e 's/MOZILLA_VERSION/%{version}/g' \
		     -e 's,LIBDIR,%{_libdir},g' > \
  $RPM_BUILD_ROOT/usr/bin/seamonkey

chmod 755 $RPM_BUILD_ROOT/usr/bin/seamonkey

# set up our default preferences
%{__cat} %{SOURCE20} | %{__sed} -e 's,SEAMONKEY_RPM_VR,%{version}-%{release},g' > \
        $RPM_BUILD_ROOT/fc-default-prefs
%{__cp} $RPM_BUILD_ROOT/fc-default-prefs $RPM_BUILD_ROOT/%{mozdir}/defaults/pref/all-fedora.js
%{__rm} $RPM_BUILD_ROOT/fc-default-prefs

# we use /usr/lib/mozilla/plugins which is the version-independent
# place that plugins can be installed
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}/mozilla/plugins

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

%{_mandir}/man1/seamonkey.1.gz

%dir %{_libdir}/mozilla/plugins

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
* Thu Oct 18 2007 Martin Stransky <stransky@redhat.com> - 1.0.9-3
- Update to latest snapshot of Mozilla 1.8.0 branch
- added pathes for Mozilla bugs 267833,309322,345305,361745,
  362901,372309,378787,381300,384105,386914,387033,387881,388121,388784
  390078,393537,395942,325761,392149
* Fri Jul 20 2007 Kai Engert <kengert@redhat.com> - 1.0.9-2
- Add a patch to stick with gecko version 1.8.0.12
- Update to latest snapshot of Mozilla 1.8.0 branch
- Include patches for Mozilla bugs 379245, 384925, 178993,
  381300 (+382686), 358594 (+380933), 382532 (+382503)
* Thu May 31 2007 Kai Engert <kengert@redhat.com> 1.0.9-1
- Update to 1.0.9
* Wed Mar 01 2007 Kai Engert <kengert@redhat.com> 1.0.8-0.6.2
- SeaMonkey 1.0.8
- Synch set of patches with those used in Firefox.
* Wed Feb 07 2007 Kai Engert <kengert@redhat.com> 1.0.7-0.6.1
- Fix the DND implementation to not grab, so it works with new GTK+.
- Fix upgrade path from FC-5 by obsoleting the seamonkey subset 
  packages which recently obsoleted mozilla in FC-5.
* Sat Dec 23 2006 Kai Engert <kengert@redhat.com> 1.0.7-0.6
- SeaMonkey 1.0.7
* Thu Nov 09 2006 Kai Engert <kengert@redhat.com> 1.0.6-0.6.2
- Fix some .dat and .rdf ghost files.
* Thu Nov 09 2006 Kai Engert <kengert@redhat.com> 1.0.6-0.6.1
- Do not run regchrome.
* Thu Nov 09 2006 Kai Engert <kengert@redhat.com> 1.0.6-0.6
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
