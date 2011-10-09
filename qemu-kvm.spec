#
# TODO:
# - update patches
# - move qemu-ga to subpackage (works only on guest system)
#
# Conditional build:
%bcond_with	cflags_passing		# with passing rpmcflags to Makefiles
%bcond_with	dosguest		# add special patch when use with DOS as guest os
%bcond_with	nosdlgui		# do not use SDL gui (use X11 instead)
%bcond_without	spice			# SPICE support
#
Summary:	QEMU CPU Emulator
Summary(pl.UTF-8):	QEMU - emulator procesora
Name:		qemu-kvm
Version:	0.15.0
Release:	4
License:	GPL
Group:		Applications/Emulators
Source0:	http://dl.sourceforge.net/project/kvm/qemu-kvm/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b45b0deebba4ce47dcaaab3807f6ed47
Source1:	http://www.linuxtogo.org/~kevin/SeaBIOS/bios.bin-1.6.3
# Source1-md5:	9d3b8a7fbd65e5250b9d005a79ffaf34
Patch0:		%{name}-ncurses.patch
Patch1:		%{name}-nosdlgui.patch
#Patch2:		%{name}-pci.patch
Patch3:		%{name}-whitelist.patch
URL:		http://www.linux-kvm.org/
BuildRequires:	SDL-devel >= 1.2.1
BuildRequires:	alsa-lib-devel
BuildRequires:	bluez-libs-devel
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
%if %{with spice}
BuildRequires:	spice-protocol
BuildRequires:	spice-server-devel
%endif
Requires:	SDL >= 1.2.1
Obsoletes:	qemu < %{version}
Provides:	qemu = %{version}-%{release}
# sparc is currently unsupported (missing cpu_get_real_ticks() impl in vl.c)
ExclusiveArch:	%{ix86} %{x8664} %{?with_userspace:ppc}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautostrip	.*%{_datadir}/qemu/openbios-.*
# some PPC/SPARC boot image in ELF format

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

%prep
%setup -q
%patch0 -p1
#%patch2 -p1
%patch3 -p1

%{?with_nosdlgui:%patch1 -p1}

%{__sed} -i -e 's/sdl_static=yes/sdl_static=no/' configure
%{__sed} -i 's/.*MAKE) -C kqemu$//' Makefile

# cannot use optflags on x86 - they cause "no register to spill" errors
%if %{with cflags_passing}
%{__sed} -i -e 's/-g $CFLAGS/-Wall %{rpmcflags}/' configure
%else
%{__sed} -i 's/-g $CFLAGS/-Wall -fno-var-tracking-assignments/' configure
%endif

cp -a %{SOURCE1} pc-bios/bios.bin

# workaround for conflict with alsa/error.h
ln -s ../error.h qapi/error.h

%build
# --extra-cflags don't work (overridden by CFLAGS in Makefile*)
# they can be passed if the cflags_passing bcond is used
./configure \
	--target-list="" \
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
	--audio-drv-list="alsa,oss,pa,sdl" \
	--audio-card-list="ac97,es1370,sb16,cs4231a,adlib,gus,hda" \
	--interp-prefix=%{_prefix}/qemu-%%M \
	%{__enable_disable spice} \
	--disable-strip \
	--disable-usb-redir

%{__make} V=99

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	V=99 \
	DESTDIR=$RPM_BUILD_ROOT

ln -s qemu-system-x86_64 $RPM_BUILD_ROOT%{_bindir}/qemu-kvm

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/qemu-ifup
#!/bin/sh

EOF

# already packaged
rm -rf $RPM_BUILD_ROOT%{_docdir}/qemu/qemu-{doc,tech}.html

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README qemu-doc.html qemu-tech.html
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/qemu-ifup
%dir %{_sysconfdir}/qemu
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/qemu/target-*.conf
%attr(755,root,root) %{_bindir}/qemu
%attr(755,root,root) %{_bindir}/qemu-alpha
%attr(755,root,root) %{_bindir}/qemu-arm
%attr(755,root,root) %{_bindir}/qemu-armeb
%attr(755,root,root) %{_bindir}/qemu-cris
%attr(755,root,root) %{_bindir}/qemu-ga
%attr(755,root,root) %{_bindir}/qemu-i386
%attr(755,root,root) %{_bindir}/qemu-img
%attr(755,root,root) %{_bindir}/qemu-io
%attr(755,root,root) %{_bindir}/qemu-kvm
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
%attr(755,root,root) %{_bindir}/qemu-system-arm
%attr(755,root,root) %{_bindir}/qemu-system-cris
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
%attr(755,root,root) %{_bindir}/qemu-unicore32
%attr(755,root,root) %{_bindir}/qemu-x86_64
%{_datadir}/qemu
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/qemu-img.1*
%{_mandir}/man8/qemu-nbd.8*
