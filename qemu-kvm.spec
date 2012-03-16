#
# Conditional build:
%bcond_without	spice			# SPICE support
#
Summary:	QEMU CPU Emulator
Summary(pl.UTF-8):	QEMU - emulator procesora
Name:		qemu-kvm
Version:	1.0
Release:	6
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
Patch4:		qemu-kvm-cflags.patch
# Update to qemu 1.0.1
Patch100:	qemu-1.0.1.patch
URL:		http://www.linux-kvm.org/
BuildRequires:	SDL-devel >= 1.2.1
BuildRequires:	alsa-lib-devel
BuildRequires:	bluez-libs-devel
BuildRequires:	brlapi-devel
BuildRequires:	ceph-devel
BuildRequires:	check-devel
BuildRequires:	gnutls-devel
BuildRequires:	libaio-devel
BuildRequires:	libevent-devel
BuildRequires:	libfdt-devel
BuildRequires:	libiscsi-devel
BuildRequires:	ncurses-devel
BuildRequires:	pciutils-devel
BuildRequires:	perl-Encode
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel
BuildRequires:	rpmbuild(macros) >= 1.644
BuildRequires:	sed >= 4.0
%if %{with spice}
BuildRequires:	spice-protocol
BuildRequires:	spice-server-devel
%endif
BuildRequires:	texi2html
BuildRequires:	usbredir-devel
BuildRequires:	which
BuildRequires:	xorg-lib-libX11-devel
Requires:	%{name}-img = %{version}-%{release}
Requires:	%{name}-system-alpha = %{version}-%{release}
Requires:	%{name}-system-arm = %{version}-%{release}
Requires:	%{name}-system-cris = %{version}-%{release}
Requires:	%{name}-system-lm32 = %{version}-%{release}
Requires:	%{name}-system-m68k = %{version}-%{release}
Requires:	%{name}-system-microblaze = %{version}-%{release}
Requires:	%{name}-system-mips = %{version}-%{release}
Requires:	%{name}-system-ppc = %{version}-%{release}
Requires:	%{name}-system-s390x = %{version}-%{release}
Requires:	%{name}-system-sh4 = %{version}-%{release}
Requires:	%{name}-system-sparc = %{version}-%{release}
Requires:	%{name}-system-x86 = %{version}-%{release}
Requires:	%{name}-system-xtensa = %{version}-%{release}
Requires:	%{name}-user = %{version}-%{release}
Provides:	qemu = %{version}-%{release}
Obsoletes:	qemu
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

%package  common
Summary:	QEMU common files needed by all QEMU targets
Group:		Development/Tools
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	SDL >= 1.2.1
Provides:	group(kvm)
Provides:	qemu-common
Requires:	systemd-units >= 38
Conflicts:	qemu-kvm < 1.0-3

%description common
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the common files needed by all QEMU targets.

%package  img
Summary:	QEMU command line tool for manipulating disk images
Group:		Development/Tools
Conflicts:	qemu-kvm < 1.0-3

%description img
This package provides a command line tool for manipulating disk images

%package user
Summary:	QEMU user mode emulation of qemu targets
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
Requires:	systemd-units >= 38

%description user
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the user mode emulation of QEMU targets.

%package system-alpha
Summary:	QEMU system emulator for alpha
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-alpha
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for alpha.

%package system-arm
Summary:	QEMU system emulator for arm
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-arm
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for arm.

%package system-cris
Summary:	QEMU system emulator for cris
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-cris
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for cris.

%package system-lm32
Summary:	QEMU system emulator for lm32
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-lm32
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for lm32.

%package system-m68k
Summary:	QEMU system emulator for m68k
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-m68k
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for m68k.

%package system-microblaze
Summary:	QEMU system emulator for microblaze
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-microblaze
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for microblaze.

%package system-mips
Summary:	QEMU system emulator for mips
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-mips
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for mips.

%package system-ppc
Summary:	QEMU system emulator for ppc
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-ppc
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for ppc.

%package system-s390x
Summary:	QEMU system emulator for s390x
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-s390x
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for s390x.

%package system-sh4
Summary:	QEMU system emulator for sh4
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-sh4
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for sh4.

%package system-sparc
Summary:	QEMU system emulator for sparc
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-sparc
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for sparc/sparc64.

%package system-x86
Summary:	QEMU system emulator for x86
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}
Obsoletes:	kvm

%description system-x86
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for x86. When being run in a
x86 machine that supports it, this package also provides the KVM
virtualization platform.

%package system-xtensa
Summary:	QEMU system emulator for xtensa
Group:		Development/Tools
Requires:	%{name}-common = %{version}-%{release}

%description system-xtensa
QEMU is a generic and open source processor emulator which achieves a
good emulation speed by using dynamic translation.

This package provides the system emulator for xtensa.

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
%patch4 -p1

%patch100 -p1

cp -a %{SOURCE1} pc-bios/bios.bin

# workaround for conflict with alsa/error.h
ln -s ../error.h qapi/error.h

%build
%ifarch %{ix86} %{x8664}
./configure \
	--target-list="x86_64-softmmu" \
	--extra-cflags="%{rpmcflags} -I/usr/include/ncurses" \
	--extra-ldflags="%{rpmldflags}" \
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
	--extra-ldflags="%{rpmldflags}" \
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

%pre common
%groupadd -g 160 kvm
%groupadd -g 276 qemu
%useradd -u 276 -g qemu -G kvm -c "QEMU User" qemu

%post common
%systemd_post ksm.service
%systemd_post ksmtuned.service

%preun common
%systemd_preun ksm.service
%systemd_preun ksmtuned.service

%postun common
if [ "$1" = "0" ]; then
	%userremove qemu
	%groupremove qemu
	%groupremove kvm
fi
%systemd_reload

%triggerpostun common -- %{name} < 1.0-3
%systemd_trigger ksm.service
%systemd_trigger ksmtuned.service

%post user
%systemd_post systemd-binfmt.service

%postun user
%systemd_post systemd-binfmt.service

%post guest-agent
%systemd_reload

%preun guest-agent
%systemd_preun qemu-guest-agent.service

%postun guest-agent
%systemd_reload

%files
%defattr(644,root,root,755)

%files common
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
%attr(755,root,root) %{_bindir}/qemu-nbd
%attr(755,root,root) %{_sbindir}/ksmctl
%attr(755,root,root) %{_sbindir}/ksmtuned
%{_mandir}/man1/qemu.1*
%{_mandir}/man8/qemu-nbd.8*

%dir %{_datadir}/qemu
%{_datadir}/qemu/keymaps
# various bios images
%{_datadir}/qemu/*.bin
%{_datadir}/qemu/*.rom
%{_datadir}/qemu/*.dtb
%{_datadir}/qemu/openbios-ppc
%{_datadir}/qemu/openbios-sparc*
%{_datadir}/qemu/palcode-clipper

%files img
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-img
%{_mandir}/man1/qemu-img.1*

%files user
%defattr(644,root,root,755)
/usr/lib/binfmt.d/qemu-*.conf
%attr(755,root,root) %{_bindir}/qemu-alpha
%attr(755,root,root) %{_bindir}/qemu-arm
%attr(755,root,root) %{_bindir}/qemu-armeb
%attr(755,root,root) %{_bindir}/qemu-cris
%attr(755,root,root) %{_bindir}/qemu-i386
%attr(755,root,root) %{_bindir}/qemu-io
%attr(755,root,root) %{_bindir}/qemu-m68k
%attr(755,root,root) %{_bindir}/qemu-microblaze
%attr(755,root,root) %{_bindir}/qemu-microblazeel
%attr(755,root,root) %{_bindir}/qemu-mips
%attr(755,root,root) %{_bindir}/qemu-mipsel
%attr(755,root,root) %{_bindir}/qemu-ppc
%attr(755,root,root) %{_bindir}/qemu-ppc64
%attr(755,root,root) %{_bindir}/qemu-ppc64abi32
%attr(755,root,root) %{_bindir}/qemu-s390x
%attr(755,root,root) %{_bindir}/qemu-sh4
%attr(755,root,root) %{_bindir}/qemu-sh4eb
%attr(755,root,root) %{_bindir}/qemu-sparc
%attr(755,root,root) %{_bindir}/qemu-sparc32plus
%attr(755,root,root) %{_bindir}/qemu-sparc64
%attr(755,root,root) %{_bindir}/qemu-unicore32
%attr(755,root,root) %{_bindir}/qemu-x86_64

%files system-alpha
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-alpha

%files system-arm
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-arm

%files system-cris
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-cris

%files system-lm32
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-lm32

%files system-m68k
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-m68k

%files system-microblaze
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-microblaze
%attr(755,root,root) %{_bindir}/qemu-system-microblazeel

%files system-mips
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-mips
%attr(755,root,root) %{_bindir}/qemu-system-mipsel
%attr(755,root,root) %{_bindir}/qemu-system-mips64
%attr(755,root,root) %{_bindir}/qemu-system-mips64el

%files system-ppc
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-ppc
%attr(755,root,root) %{_bindir}/qemu-system-ppc64
%attr(755,root,root) %{_bindir}/qemu-system-ppcemb

%files system-s390x
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-s390x

%files system-sh4
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-sh4
%attr(755,root,root) %{_bindir}/qemu-system-sh4eb

%files system-sparc
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-sparc
%attr(755,root,root) %{_bindir}/qemu-system-sparc64

%files system-x86
%defattr(644,root,root,755)
%ifarch %{ix86} %{x8664}
%config(noreplace) %verify(not md5 mtime size) /etc/modules-load.d/kvm.conf
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/80-kvm.rules
%endif
%attr(755,root,root) %{_bindir}/kvm_stat
%attr(755,root,root) %{_bindir}/qemu-kvm
%attr(755,root,root) %{_bindir}/qemu-system-i386
%attr(755,root,root) %{_bindir}/qemu-system-x86_64

%files system-xtensa
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qemu-system-xtensa
%attr(755,root,root) %{_bindir}/qemu-system-xtensaeb

%files guest-agent
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/99-qemu-guest-agent.rules
%{systemdunitdir}/qemu-guest-agent.service
%attr(755,root,root) %{_bindir}/qemu-ga
