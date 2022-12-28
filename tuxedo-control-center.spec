Name:           tuxedo-control-center
Version:        1.2.3
Release:        1%{?dist}
Summary:        TUXEDO Control Center Application

License:        GPL-3.0
URL:            https://www.tuxedocomputers.com
Source0:        %{name}-%{version}.tar.gz

#BuildRoot:      ~/rpmbuild/
Group:          default
Vendor:         TUXEDO Computers GmbH <tux@tuxedocomputers.com>
Packager:       TUXEDO Computers GmbH <tux@tuxedocomputers.com>

Requires:       tuxedo-keyboard >= 3.1.2
Requires:       libappindicator
Obsoletes:      tuxedofancontrol <= 0.1.9

%define __os_install_post %{nil}
%global tccdir opt/tuxedo-control-center

%description
TUXEDO Control Center Application

%prep
%setup -q

%install
mkdir -p %{buildroot}%{_exec_prefix}/local/bin

mkdir -p %{buildroot}%{_datadir}/applications
cp usr/share/applications/tuxedo-control-center.desktop %{buildroot}%{_datadir}/applications/tuxedo-control-center.desktop

mkdir -p %{buildroot}%{_datadir}/icons
cp -r usr/share/icons/* %{buildroot}%{_datadir}/icons/

mkdir -p %{buildroot}/%{tccdir}
cp -r %{tccdir}/* %{buildroot}/%{tccdir}/

mkdir -p %{buildroot}/%{tccdir}/resources/dist/tuxedo-control-center/data/service
#install -m 0775 opt/tuxedo-control-center/resources/dist/tuxedo-control-center/data/service/tccd %{buildroot}/opt/tuxedo-control-center/resources/dist/tuxedo-control-center/data/service/tccd
cp %{tccdir}/resources/dist/tuxedo-control-center/data/service/tccd %{buildroot}/%{tccdir}/resources/dist/tuxedo-control-center/data/service/tccd


%post
#!/bin/bash

# In case TFC service is active, deactivate
systemctl stop tuxedofancontrol || true
systemctl disable tuxedofancontrol || true

systemctl stop tccd || true

DIST_DATA=/%{tccdir}/resources/dist/tuxedo-control-center/data/dist-data

rm %{_datadir}/applications/tuxedo-control-center.desktop || true
cp ${DIST_DATA}/tuxedo-control-center.desktop %{_datadir}/applications/tuxedo-control-center.desktop || true

mkdir -p /etc/skel/.config/autostart || true
cp ${DIST_DATA}/tuxedo-control-center-tray.desktop /etc/skel/.config/autostart/tuxedo-control-center-tray.desktop || true

cp ${DIST_DATA}/com.tuxedocomputers.tccd.policy %{_datadir}/polkit-1/actions/com.tuxedocomputers.tccd.policy || true
cp ${DIST_DATA}/com.tuxedocomputers.tccd.conf %{_datadir}/dbus-1/system.d/com.tuxedocomputers.tccd.conf || true

# Copy and enable services
cp ${DIST_DATA}/tccd.service /etc/systemd/system/tccd.service || true
cp ${DIST_DATA}/tccd-sleep.service /etc/systemd/system/tccd-sleep.service || true
systemctl daemon-reload
systemctl enable tccd tccd-sleep
systemctl restart tccd

# chmod +x /opt/tuxedocc/resources/output/dist/data/tuxedocc-pkexec
ln -s /%{tccdir}/tuxedo-control-center /usr/bin/tuxedo-control-center || true

%preun
#!/bin/bash

# On RPM update don't remove anything
if [ "$1" -gt 0 2>/dev/null ]; then
    exit 0
fi

# Stop, disable and remove services
systemctl disable tccd tccd-sleep || true
systemctl stop tccd || true
rm /etc/systemd/system/tccd.service || true
rm /etc/systemd/system/tccd-sleep.service || true
systemctl daemon-reload || true

# Remove log and config files (unless deb upgrade)
if [ "$1" != "upgrade" ]; then
    rm -rf /var/log/tcc/ || true
    rm -rf /var/log/tccd/ || true
    rm -rf /etc/tcc/ || true
fi

# Remove link to GUI
rm -rf %{_bindir}/tuxedo-control-center || true

# Remove policy kit and desktop files
rm %{_datadir}/polkit-1/actions/com.tuxedocomputers.tccd.policy || true
rm %{_datadir}/applications/tuxedo-control-center.desktop || true
rm %{_sysconfdir}/skel/.config/autostart/tuxedo-control-center-tray.desktop || true
rm %{_datadir}/dbus-1/system.d/com.tuxedocomputers.tccd.conf || true


%postun
#!/bin/bash
# Delete the link to the binary
rm -f '/usr/local/bin/tuxedo-control-center'

%files
%defattr(-,root,root,-)
/%{tccdir}/LICENSE.electron.txt
/%{tccdir}/LICENSES.chromium.html
/%{tccdir}/chrome-sandbox
/%{tccdir}/chrome_100_percent.pak
/%{tccdir}/chrome_200_percent.pak
/%{tccdir}/icudtl.dat
/%{tccdir}/libEGL.so
/%{tccdir}/libGLESv2.so
/%{tccdir}/libffmpeg.so
/%{tccdir}/libvk_swiftshader.so
/%{tccdir}/libvulkan.so.1
/%{tccdir}/locales/am.pak
/%{tccdir}/locales/ar.pak
/%{tccdir}/locales/bg.pak
/%{tccdir}/locales/bn.pak
/%{tccdir}/locales/ca.pak
/%{tccdir}/locales/cs.pak
/%{tccdir}/locales/da.pak
/%{tccdir}/locales/de.pak
/%{tccdir}/locales/el.pak
/%{tccdir}/locales/en-GB.pak
/%{tccdir}/locales/en-US.pak
/%{tccdir}/locales/es-419.pak
/%{tccdir}/locales/es.pak
/%{tccdir}/locales/et.pak
/%{tccdir}/locales/fa.pak
/%{tccdir}/locales/fi.pak
/%{tccdir}/locales/fil.pak
/%{tccdir}/locales/fr.pak
/%{tccdir}/locales/gu.pak
/%{tccdir}/locales/he.pak
/%{tccdir}/locales/hi.pak
/%{tccdir}/locales/hr.pak
/%{tccdir}/locales/hu.pak
/%{tccdir}/locales/id.pak
/%{tccdir}/locales/it.pak
/%{tccdir}/locales/ja.pak
/%{tccdir}/locales/kn.pak
/%{tccdir}/locales/ko.pak
/%{tccdir}/locales/lt.pak
/%{tccdir}/locales/lv.pak
/%{tccdir}/locales/ml.pak
/%{tccdir}/locales/mr.pak
/%{tccdir}/locales/ms.pak
/%{tccdir}/locales/nb.pak
/%{tccdir}/locales/nl.pak
/%{tccdir}/locales/pl.pak
/%{tccdir}/locales/pt-BR.pak
/%{tccdir}/locales/pt-PT.pak
/%{tccdir}/locales/ro.pak
/%{tccdir}/locales/ru.pak
/%{tccdir}/locales/sk.pak
/%{tccdir}/locales/sl.pak
/%{tccdir}/locales/sr.pak
/%{tccdir}/locales/sv.pak
/%{tccdir}/locales/sw.pak
/%{tccdir}/locales/ta.pak
/%{tccdir}/locales/te.pak
/%{tccdir}/locales/th.pak
/%{tccdir}/locales/tr.pak
/%{tccdir}/locales/uk.pak
/%{tccdir}/locales/vi.pak
/%{tccdir}/locales/zh-CN.pak
/%{tccdir}/locales/zh-TW.pak
/%{tccdir}/resources.pak
/%{tccdir}/resources/app.asar
/%{tccdir}/resources/dist/tuxedo-control-center/data/dist-data/com.tuxedocomputers.tccd.conf
/%{tccdir}/resources/dist/tuxedo-control-center/data/dist-data/com.tuxedocomputers.tccd.policy
/%{tccdir}/resources/dist/tuxedo-control-center/data/dist-data/tccd-sleep.service
/%{tccdir}/resources/dist/tuxedo-control-center/data/dist-data/tccd.service
/%{tccdir}/resources/dist/tuxedo-control-center/data/dist-data/tuxedo-control-center-tray.desktop
/%{tccdir}/resources/dist/tuxedo-control-center/data/dist-data/tuxedo-control-center.desktop
/%{tccdir}/resources/dist/tuxedo-control-center/data/dist-data/tuxedo-control-center_256.svg
/%{tccdir}/resources/dist/tuxedo-control-center/data/service/TuxedoIOAPI.node
/%{tccdir}/resources/dist/tuxedo-control-center/data/service/tccd
/%{tccdir}/snapshot_blob.bin
/%{tccdir}/swiftshader/libEGL.so
/%{tccdir}/swiftshader/libGLESv2.so
/%{tccdir}/tuxedo-control-center
/%{tccdir}/v8_context_snapshot.bin
/%{tccdir}/vk_swiftshader_icd.json
%{_datadir}/applications/tuxedo-control-center.desktop
%{_datadir}/icons/hicolor/128x128/apps/tuxedo-control-center.png
%{_datadir}/icons/hicolor/16x16/apps/tuxedo-control-center.png
%{_datadir}/icons/hicolor/24x24/apps/tuxedo-control-center.png
%{_datadir}/icons/hicolor/256x256/apps/tuxedo-control-center.png
%{_datadir}/icons/hicolor/32x32/apps/tuxedo-control-center.png
%{_datadir}/icons/hicolor/48x48/apps/tuxedo-control-center.png
%{_datadir}/icons/hicolor/64x64/apps/tuxedo-control-center.png
%{_datadir}/icons/hicolor/96x96/apps/tuxedo-control-center.png


%changelog
* Thu Dec 22 2022 kallepm
- Update to release v1.2.3
* Thu Nov 24 2022 kallepm
- Update to release v1.2.2
* Tue Jun 21 2022 kallepm
- Update to release v1.1.4
* Fri Apr 15 2022 kallepm
- Update to release v1.1.3
* Wed Dec 08 2021 kallepm
- Update to release v1.1.2
* Sun Nov 28 2021 kallepm
- Update to release v1.1.1
* Mon Aug 30 2021 kallepm
- Update to release v1.1.0
* Fri May 21 2021 kallepm
- Update to release v1.0.14
* Sun Apr 25 2021 kallepm
- Update to release v1.0.13
* Sun Apr 11 2021 kallepm
- Update to release v1.0.12
* Fri Apr 09 2021 kallepm
- Initial Fedora build
