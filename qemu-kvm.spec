#
# TODO:
# - update patches
#
# Conditional build:
%bcond_with	cflags_passing		# with passing rpmcflags to Makefiles
%bcond_with	dosguest		# add special patch when use with DOS as guest os
%bcond_with	nosdlgui		# do not use SDL gui (use X11 instead)

Summary:	QEMU CPU Emulator
Summary(pl.UTF-8):	QEMU - emulator procesora
Name:		qemu-kvm
Version:	0.14.0
Release:	1
License:	GPL
Group:		Applications/Emulators
Source0:	http://dl.sourceforge.net/project/kvm/qemu-kvm/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4ea6f412d85a826e0b0690f5c4c59f13
Patch0:		%{name}-ncurses.patch
Patch1:		%{name}-nosdlgui.patch
Patch2:		%{name}-pci.patch
Patch3:		%{name}-whitelist.patch
URL:		http://www.linux-kvm.org/
BuildRequires:	SDL-devel >= 1.2.1
BuildRequires:	alsa-lib-devel
BuildRequires:	bluez-libs-devel
BuildRequires:	gnutls-devel
BuildRequires:	ncurses-devel
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
Requires:	SDL >= 1.2.1
Obsoletes:	qemu
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
%patch2 -p1
%patch3 -p1

%{?with_nosdlgui:%patch1 -p1}

%{__sed} -i -e 's/sdl_static=yes/sdl_static=no/' configure
%{__sed} -i 's/.*MAKE) -C kqemu$//' Makefile

# cannot use optflags on x86 - they cause "no register to spill" errors
%if %{with cflags_passing}
%{__sed} -i -e 's/-Wall -O2 -g/-Wall %{rpmcflags}/' Makefile Makefile.target
%else
%{__sed} -i 's/-Wall -O2 -g/-Wall -O2/' Makefile Makefile.target
%endif

%build
# --extra-cflags don't work (overridden by CFLAGS in Makefile*)
# they can be passed if the cflags_passing bcond is used
%ifarch %{ix86} x86_64
./configure \
        --prefix=%{_prefix} \
        --cc="%{__cc}" \
        --host-cc="%{__cc}" \
        --enable-mixemu \
        --audio-drv-list="alsa" \
        --interp-prefix=%{_libdir}/%{name}


%{__make}

cp -a x86_64-softmmu/qemu-system-x86_64 qemu-kvm

%{__make} clean

#cd kvm/user
#./configure --prefix=%{_prefix} --kerneldir=$(pwd)/../kernel/
#%{__make} kvmtrace
#cd ../../
%endif

./configure \
	--target-list="i386-softmmu x86_64-softmmu arm-softmmu cris-softmmu m68k-softmmu \
		mips-softmmu mipsel-softmmu mips64-softmmu mips64el-softmmu ppc-softmmu \
		ppcemb-softmmu ppc64-softmmu sh4-softmmu sh4eb-softmmu sparc-softmmu \
		i386-linux-user x86_64-linux-user alpha-linux-user arm-linux-user \
		armeb-linux-user cris-linux-user m68k-linux-user mips-linux-user \
		mipsel-linux-user ppc-linux-user ppc64-linux-user ppc64abi32-linux-user \
		sh4-linux-user sh4eb-linux-user sparc-linux-user sparc64-linux-user \
		sparc32plus-linux-user" \
	--prefix=%{_prefix} \
	--interp-prefix=%{_prefix}/qemu-%%M \
	--audio-drv-list=pa,sdl,alsa,oss \
	--block-drv-whitelist=bochs,cloop,cow,curl,dmg,nbd,parallels,qcow2,qcow,raw,vdi,vmdk,vpc,vvfat \
	--disable-kvm \
	--disable-strip \
	--extra-ldflags=$extraldflags \
	--extra-cflags="$RPM_OPT_FLAGS" \
	--disable-xen

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
install qemu-kvm $RPM_BUILD_ROOT/%{_bindir}

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
%attr(755,root,root) %{_bindir}/*
%{_datadir}/qemu
%{_mandir}/man1/qemu.1*
%{_mandir}/man1/qemu-img.1*
%{_mandir}/man8/qemu-nbd.8*
