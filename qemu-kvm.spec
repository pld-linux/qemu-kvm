#
# Conditional build:
%bcond_without	spice			# SPICE support
#
Summary:	QEMU CPU Emulator
Summary(pl.UTF-8):	QEMU - emulator procesora
Name:		qemu-kvm
Version:	1.0
Release:	2
License:	GPL
Group:		Applications/Emulators
Source0:	http://dl.sourceforge.net/project/kvm/qemu-kvm/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	00a825db46a70ba8ef9fc95da9cc7c1e
Source1:	http://www.linuxtogo.org/~kevin/SeaBIOS/bios.bin-1.6.3
# Source1-md5:	9d3b8a7fbd65e5250b9d005a79ffaf34
Source2:	qemu.binfmt
# Loads kvm kernel modules at boot
Source3:	kvm-modules-load.conf
# Creates /dev/kvm
Source4:	80-kvm.rules
# KSM control scripts
Source5:	ksm.service
Source6:	ksm.sysconfig
Source7:	ksmctl.c
Source8:	ksmtuned.service
Source9:	ksmtuned
Source10:	ksmtuned.conf
Source11:	qemu-guest-agent.service
Source12:	99-qemu-guest-agent.rules
Patch0:		%{name}-whitelist.patch
Patch1:		Fix_save-restore_of_in-kernel_i8259.patch
# Feature patches, should be in 1.1 before release
Patch2:		enable_architectural_PMU_cpuid_leaf.patch
Patch3:		qemu_virtio-scsi_support.patch
# Patches queued for 1.0.1 stable
Patch101:	0001-malta-Fix-regression-i8259-interrupts-did-not-work.patch
Patch102:	0002-exec.c-Fix-subpage-memory-access-to-RAM-MemoryRegion.patch
Patch103:	0003-hw-9pfs-Improve-portability-to-older-systems.patch
Patch104:	0004-hw-9pfs-use-migration-blockers-to-prevent-live-migra.patch
Patch105:	0005-hw-9pfs-Reset-server-state-during-TVERSION.patch
Patch106:	0006-hw-9pfs-Add-qdev.reset-callback-for-virtio-9p-pci-de.patch
Patch107:	0007-hw-9pfs-Use-the-correct-file-descriptor-in-Fsdriver-.patch
Patch108:	0008-hw-9pfs-replace-iovec-manipulation-with-QEMUIOVector.patch
Patch109:	0009-hw-9pfs-Use-the-correct-signed-type-for-different-va.patch
Patch110:	0010-target-i386-fix-cmpxchg-instruction-emulation.patch
Patch111:	0011-configure-Enable-build-by-default-PIE-read-only-relo.patch
Patch112:	0012-cris-Handle-conditional-stores-on-CRISv10.patch
Patch113:	0013-pc-add-pc-0.15.patch
Patch114:	0014-pc-fix-event_idx-compatibility-for-virtio-devices.patch
Patch115:	0015-Fix-parse-of-usb-device-description-with-multiple-co.patch
Patch116:	0016-usb-storage-cancel-I-O-on-reset.patch
Patch117:	0017-usb-host-properly-release-port-on-unplug-exit.patch
Patch118:	0018-usb-ohci-td.cbp-incorrectly-updated-near-page-end.patch
Patch119:	0019-target-sh4-ignore-ocbp-and-ocbwb-instructions.patch
Patch120:	0020-PPC-Fix-linker-scripts-on-ppc-hosts.patch
Patch121:	0021-qiov-prevent-double-free-or-use-after-free.patch
Patch122:	0022-coroutine-switch-per-thread-free-pool-to-a-global-po.patch
Patch123:	0023-qemu-img-rebase-Fix-for-undersized-backing-files.patch
Patch124:	0024-Documentation-Add-qemu-img-t-parameter-in-man-page.patch
Patch125:	0025-rbd-always-set-out-parameter-in-qemu_rbd_snap_list.patch
Patch126:	0026-e1000-bounds-packet-size-against-buffer-size.patch
Patch127:	virtio-blk_refuse_SG_IO_requests_with_scsi_off.patch
URL:		http://www.linux-kvm.org/
BuildRequires:	SDL-devel >= 1.2.1
BuildRequires:	alsa-lib-devel
# For Braille device support                                                        
BuildRequires:	brlapi-devel
BuildRequires:	bluez-libs-devel
# For test suite                                                                    
BuildRequires:	check-devel
BuildRequires:	gnutls-devel
BuildRequires:	ncurses-devel
BuildRequires:	pciutils-devel
BuildRequires:	perl-Encode
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	texi2html
BuildRequires:	which
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	pulseaudio-devel
# LinuxAIO support
BuildRequires:	libaio-devel
BuildRequires:	libevent-devel
# For FDT device tree support
BuildRequires:	libfdt-devel
BuildRequires:	rpmbuild(macros) >= 1.644
%if %{with spice}
BuildRequires:	spice-protocol
BuildRequires:	spice-server-devel
%endif
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Provides:	group(kvm)
Requires:	SDL >= 1.2.1
Requires:	systemd-units >= 38
Obsoletes:	qemu < %{version}
Obsoletes:	kvm
Provides:	qemu = %{version}-%{release}
# sparc is currently unsupported (missing cpu_get_real_ticks() impl in vl.c)
ExclusiveArch:	%{ix86} %{x8664} %{?with_userspace:ppc}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# some PPC/SPARC boot image in ELF format
%define		_noautostrip	.*%{_datadir}/qemu/.*

%description
QEMU is a FAST! processor emulator. By using dynamic translation it
achieves a reasonnable speed while being easy to port on new host
CPUs. QEMU has two operating modes:

- User mode emulation. In this mode, QEMU can launch Linux processes
  compiled for one CPU on another CPU. Linux system calls are converted
  because of endianness and 32/64 bit mismatches. Wine (Windows
  emulation) and DOSEMU (DOS emulation) are the main targets for QEMU.

- Full system emulation. In this mode, QEMU emulates a full system,
  including a processor and various peripherials. It can also be used to
  provide virtual hosting of several virtual PC on a single server.

%description -l pl.UTF-8
QEMU to szybki(!) emulator procesora. Poprzez użycie dynamicznego
tłumaczenia osiąga rozsądną szybkość i jest łatwy do przeportowania,
aby działał na kolejnych procesorach. QEMU ma dwa tryby pracy:

- Emulacja trybu użytkownika. W tym trybie QEMU może uruchamiać
  procesy linuksowe skompilowane dla jednego procesora na innym
  procesorze. Linuksowe wywołania systemowe są tłumaczone ze względu na
  niezgodność kolejności bajtów w słowie i 32/64-bitowego rozmiaru
  słowa. Wine (emulacja Windows) i DOSEMU (emulacja DOS-a) to główne
  cele QEMU.

- Pełna emulacja systemu. W tym trybie QEMU emuluje cały system,
  włączając w to procesor i różne urządzenia peryferyjne. Może być także
  używane do wirtualnego hostowania kilku wirtualnych pecetów na
  pojedynczym serwerze.

%package guest-agent
Summary:	QEMU guest agent
Group:		Daemons
Requires:	systemd-units >= 38

%description guest-agent
QEMU is a generic and open source processor emulator which achieves
a good emulation speed by using dynamic translation.

This package provides an agent to run inside guests, which
communicates with the host over a virtio-serial channel named
"org.qemu.guest_agent.0"

This package does not need to be installed on the host OS.

%prep
%setup -q
%patch0 -p1

%patch1 -p1
%patch2 -p1
%patch3 -p1

%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1
%patch111 -p1
%patch112 -p1
%patch113 -p1
%patch114 -p1
%patch115 -p1
%patch116 -p1
%patch117 -p1
%patch118 -p1
%patch119 -p1
%patch120 -p1
%patch121 -p1
%patch122 -p1
%patch123 -p1
%patch124 -p1
%patch125 -p1
%patch126 -p1
%patch127 -p1

cp -a %{SOURCE1} pc-bios/bios.bin

# workaround for conflict with alsa/error.h
ln -s ../error.h qapi/error.h

%build
%ifarch %{ix86} %{x8664}
./configure \
	--target-list="x86_64-softmmu" \
	--extra-cflags="%{rpmcflags} -I/usr/include/ncurses" \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--cc="%{__cc}" \
	--host-cc="%{__cc}" \
	--enable-vnc \
	--enable-vnc-tls \
	--enable-vnc-sasl \
	--enable-vnc-jpeg \
	--enable-vnc-png \
	--enable-vnc-thread \
	--enable-curses \
	--enable-bluez \
	--enable-kvm-device-assignment \
	--enable-kvm-pit \
	--enable-system \
	--enable-user \
	--enable-mixemu \
	--enable-uuid \
	--enable-attr \
	--enable-vhost-net \
	--enable-smartcard \
	--enable-guest-agent \
	--enable-docs \
	--audio-drv-list="alsa,pa,sdl,oss" \
	--audio-card-list="ac97,es1370,sb16,cs4231a,adlib,gus,hda" \
	--interp-prefix=%{_prefix}/qemu-%%M \
	%{__enable_disable spice} \
	--disable-strip

%{__make} V=99
cp -a x86_64-softmmu/qemu-system-x86_64 qemu-kvm
%{__make} clean V=99
%endif

./configure \
	--target-list="" \
	--extra-cflags="%{rpmcflags} -I/usr/include/ncurses" \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--cc="%{__cc}" \
	--host-cc="%{__cc}" \
	--enable-vnc \
	--enable-vnc-tls \
	--enable-vnc-sasl \
	--enable-vnc-jpeg \
	--enable-vnc-png \
	--enable-vnc-thread \
	--enable-curses \
	--enable-bluez \
	--disable-kvm \
	--enable-system \
	--enable-user \
	--enable-mixemu \
	--enable-uuid \
	--enable-attr \
	--enable-vhost-net \
	--enable-smartcard \
	--enable-guest-agent \
	--enable-docs \
	--audio-drv-list="alsa,pa,sdl,oss" \
	--audio-card-list="ac97,es1370,sb16,cs4231a,adlib,gus,hda" \
	--interp-prefix=%{_prefix}/qemu-%%M \
%ifarch %{ix86} %{x8664}
	%{__enable_disable spice} \
%endif
	--disable-strip

%{__make} V=99

gcc %{SOURCE7} %{rpmcflags} -g -o ksmctl

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{systemdunitdir},/usr/lib/binfmt.d} \
	$RPM_BUILD_ROOT/etc/{sysconfig,udev/rules.d,modules-load.d} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/sasl,%{_sbindir}}

%{__make} install \
	V=99 \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/qemu-ifup
#!/bin/sh

EOF

install -p qemu.sasl $RPM_BUILD_ROOT%{_sysconfdir}/sasl/qemu.conf

install -p %{SOURCE5} $RPM_BUILD_ROOT%{systemdunitdir}/ksm.service
install -p %{SOURCE6} $RPM_BUILD_ROOT/etc/sysconfig/ksm
install -p ksmctl $RPM_BUILD_ROOT%{_sbindir}

install -p %{SOURCE8} $RPM_BUILD_ROOT%{systemdunitdir}/ksmtuned.service
install -p %{SOURCE9} $RPM_BUILD_ROOT%{_sbindir}/ksmtuned
install -p %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/ksmtuned.conf

%ifarch %{ix86} %{x8664}
install qemu-kvm $RPM_BUILD_ROOT%{_bindir}/qemu-system-x86_64
ln -s qemu-system-x86_64 $RPM_BUILD_ROOT%{_bindir}/qemu-kvm
install kvm/kvm_stat $RPM_BUILD_ROOT%{_bindir}
install -p %{SOURCE3} $RPM_BUILD_ROOT/etc/modules-load.d/kvm.conf
install -p %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d
%endif

# For the qemu-guest-agent subpackage install the systemd
# service and udev rules.
install -p %{SOURCE11} $RPM_BUILD_ROOT%{systemdunitdir}
install -p %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d

for i in dummy \
%ifnarch %{ix86} %{x8664}
    qemu-i386 \
%endif
%ifnarch arm
    qemu-arm \
%endif
%ifnarch ppc ppc64
    qemu-ppc \
%endif
%ifnarch sparc sparc64
    qemu-sparc \
%endif
%ifnarch sh4
    qemu-sh4 \
%endif
; do
	test $i = dummy && continue
	grep /$i:\$ %{SOURCE2} > $RPM_BUILD_ROOT/usr/lib/binfmt.d/$i.conf
done < %{SOURCE2}

# already packaged
%{__rm} $RPM_BUILD_ROOT%{_docdir}/qemu/qemu-{doc,tech}.html

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 160 kvm
%groupadd -g 276 qemu
%useradd -u 276 -g qemu -G kvm -c "QEMU User" qemu

%post
%systemd_post ksm.service
%systemd_post ksmtuned.service
%systemd_post systemd-binfmt.service

%preun
%systemd_preun ksm.service
%systemd_preun ksmtuned.service

%postun
if [ "$1" = "0" ]; then
	%userremove qemu
	%groupremove qemu
	%groupremove kvm
fi
%systemd_reload
%systemd_post systemd-binfmt.service

%triggerpostun -- %{name} < 1.0
%systemd_trigger ksm.service
%systemd_trigger ksmtuned.service

%post guest-agent
%systemd_reload

%preun guest-agent
%systemd_preun qemu-guest-agent.service

%postun guest-agent
%systemd_reload

%files
%defattr(644,root,root,755)
%doc README qemu-doc.html qemu-tech.html
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/qemu-ifup
%dir %{_sysconfdir}/qemu
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/qemu/target-*.conf
%config(noreplace) %verify(not md5 mtime size) /etc/ksmtuned.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sasl/qemu.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ksm
%{systemdunitdir}/ksm.service
%{systemdunitdir}/ksmtuned.service
%ifarch %{ix86} %{x8664}
%config(noreplace) %verify(not md5 mtime size) /etc/modules-load.d/kvm.conf
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/80-kvm.rules
%attr(755,root,root) %{_bindir}/qemu-kvm
%endif
%attr(755,root,root) %{_bindir}/kvm_stat
%attr(755,root,root) %{_sbindir}/ksmctl
%attr(755,root,root) %{_sbindir}/ksmtuned
%attr(755,root,root) %{_bindir}/qemu-alpha
%attr(755,root,root) %{_bindir}/qemu-arm
%attr(755,root,root) %{_bindir}/qemu-armeb
%attr(755,root,root) %{_bindir}/qemu-cris
%attr(755,root,root) %{_bindir}/qemu-i386
%attr(755,root,root) %{_bindir}/qemu-img
%attr(755,root,root) %{_bindir}/qemu-io
%attr(755,root,root) %{_bindir}/qemu-m68k
%attr(755,root,root) %{_bindir}/qemu-microblaze
%attr(755,root,root) %{_bindir}/qemu-microblazeel
%attr(755,root,root) %{_bindir}/qemu-mips
%attr(755,root,root) %{_bindir}/qemu-mipsel
%attr(755,root,root) %{_bindir}/qemu-nbd
%attr(755,root,root) %{_bindir}/qemu-ppc
%attr(755,root,root) %{_bindir}/qemu-ppc64
%attr(755,root,root) %{_bindir}/qemu-ppc64abi32
%attr(755,root,root) %{_bindir}/qemu-s390x
%attr(755,root,root) %{_bindir}/qemu-sh4
%attr(755,root,root) %{_bindir}/qemu-sh4eb
%attr(755,root,root) %{_bindir}/qemu-sparc
%attr(755,root,root) %{_bindir}/qemu-sparc32plus
%attr(755,root,root) %{_bindir}/qemu-sparc64
%attr(755,root,root) %{_bindir}/qemu-system-alpha
%attr(755,root,root) %{_bindir}/qemu-system-arm
%attr(755,root,root) %{_bindir}/qemu-system-cris
%attr(755,root,root) %{_bindir}/qemu-system-i386
%attr(755,root,root) %{_bindir}/qemu-system-lm32
%attr(755,root,root) %{_bindir}/qemu-system-m68k
%attr(755,root,root) %{_bindir}/qemu-system-microblaze
%attr(755,root,root) %{_bindir}/qemu-system-microblazeel
%attr(755,root,root) %{_bindir}/qemu-system-mips
%attr(755,root,root) %{_bindir}/qemu-system-mips64
%attr(755,root,root) %{_bindir}/qemu-system-mips64el
%attr(755,root,root) %{_bindir}/qemu-system-mipsel
%attr(755,root,root) %{_bindir}/qemu-system-ppc
%attr(755,root,root) %{_bindir}/qemu-system-ppc64
%attr(755,root,root) %{_bindir}/qemu-system-ppcemb
%attr(755,root,root) %{_bindir}/qemu-system-s390x
%attr(755,root,root) %{_bindir}/qemu-system-sh4
%attr(755,root,root) %{_bindir}/qemu-system-sh4eb
%attr(755,root,root) %{_bindir}/qemu-system-sparc
%attr(755,root,root) %{_bindir}/qemu-system-sparc64
%attr(755,root,root) %{_bindir}/qemu-system-x86_64
%attr(755,root,root) %{_bindir}/qemu-system-xtensa
%attr(755,root,root) %{_bindir}/qemu-system-xtensaeb
%attr(755,root,root) %{_bindir}/qemu-unicore32
%attr(755,root,root) %{_bindir}/qemu-x86_64
/usr/lib/binfmt.d/qemu-arm.conf
/usr/lib/binfmt.d/qemu-ppc.conf
/usr/lib/binfmt.d/qemu-sh4.conf
/usr/lib/binfmt.d/qemu-sparc.conf
%{_datadir}/qemu
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/qemu-img.1*
%{_mandir}/man8/qemu-nbd.8*

%files guest-agent
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/99-qemu-guest-agent.rules
%{systemdunitdir}/qemu-guest-agent.service
%attr(755,root,root) %{_bindir}/qemu-ga
