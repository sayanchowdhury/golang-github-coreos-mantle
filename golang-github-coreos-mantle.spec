# If any of the following macros should be set otherwise,
# you can wrap any of them with the following conditions:
# - %%if 0%%{centos} == 7
# - %%if 0%%{?rhel} == 7
# - %%if 0%%{?fedora} == 23
# Or just test for particular distribution:
# - %%if 0%%{centos}
# - %%if 0%%{?rhel}
# - %%if 0%%{?fedora}
#
# Be aware, on centos, both %%rhel and %%centos are set. If you want to test
# rhel specific macros, you can use %%if 0%%{?rhel} && 0%%{?centos} == 0 condition.
# (Don't forget to replace double percentage symbol with single one in order to apply a condition)

# Generate devel rpm
%global with_devel 0
# Build project from bundled dependencies
%global with_bundled 1
# Build with debug info rpm
%global with_debug 1
# Run tests in check section
%global with_check 1
# Generate unit-test rpm
%global with_unit_test 1

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%endif

%global provider        github
%global provider_tld    com
%global project         coreos
%global repo            mantle
# https://github.com/coreos/mantle
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          490b74e13080d984385ccc2daec22d995a483d3f
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           golang-%{provider}-%{project}-%{repo}
Version:        0
Release:        0.1.git%{shortcommit}%{?dist}
Summary:        Collection of tools for managing cloud images.
License:        ASL2.0
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

# Main packages BuildRequires
%if ! 0%{?with_bundled}
# cmd/plume/specs.go
BuildRequires: golang(github.com/spf13/pflag)
# cmd/plume/index.go
BuildRequires: golang(github.com/spf13/cobra)
BuildRequires: golang(golang.org/x/net/context)
# cmd/kola/bootchart.go
BuildRequires: golang(github.com/spf13/cobra)
# cmd/cork/download.go
BuildRequires: golang(github.com/spf13/cobra)
# cmd/cork/build.go
BuildRequires: golang(github.com/spf13/cobra)
# cmd/kola/console.go
BuildRequires: golang(github.com/spf13/cobra)
# cmd/kola/spawn.go
BuildRequires: golang(github.com/spf13/cobra)
BuildRequires: golang(golang.org/x/crypto/ssh)
BuildRequires: golang(golang.org/x/crypto/ssh/agent)
# cmd/plume/prerelease.go
BuildRequires: golang(github.com/Azure/azure-sdk-for-go/management/storageservice)
BuildRequires: golang(github.com/Microsoft/azure-vhd-utils/vhdcore/validator)
BuildRequires: golang(github.com/spf13/cobra)
BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(google.golang.org/api/storage/v1)
# network/ntp/_ntpd/ntpd.go
BuildRequires: golang(github.com/coreos/pkg/capnslog)
# cmd/gangue/gangue.go
BuildRequires: golang(github.com/spf13/cobra)
# cmd/kolet/kolet.go
BuildRequires: golang(github.com/coreos/pkg/capnslog)
BuildRequires: golang(github.com/spf13/cobra)
# cmd/plume/release.go
BuildRequires: golang(github.com/spf13/cobra)
BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(google.golang.org/api/compute/v1)
BuildRequires: golang(google.golang.org/api/storage/v1)
# cmd/kola/kola.go
BuildRequires: golang(github.com/coreos/pkg/capnslog)
BuildRequires: golang(github.com/spf13/cobra)
# cmd/plume/plume.go
BuildRequires: golang(github.com/coreos/pkg/capnslog)
BuildRequires: golang(github.com/spf13/cobra)
# cmd/ore/ore.go
BuildRequires: golang(github.com/spf13/cobra)
# cmd/kola/updatepayload.go
BuildRequires: golang(github.com/spf13/cobra)
BuildRequires: golang(golang.org/x/crypto/ssh/agent)
# cmd/cork/cork.go
BuildRequires: golang(github.com/coreos/pkg/capnslog)
BuildRequires: golang(github.com/spf13/cobra)
# update/_dump/main.go
BuildRequires: golang(github.com/golang/protobuf/proto)
# cmd/cork/downloadimage.go
BuildRequires: golang(github.com/spf13/cobra)
# cmd/cork/create.go
BuildRequires: golang(github.com/coreos/go-semver/semver)
BuildRequires: golang(github.com/spf13/cobra)
BuildRequires: golang(github.com/spf13/pflag)

# Remaining dependencies not included in main packages
BuildRequires: golang(github.com/aws/aws-sdk-go/aws)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/awserr)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/client)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/credentials)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/endpoints)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/request)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/session)
BuildRequires: golang(github.com/aws/aws-sdk-go/service/ec2)
BuildRequires: golang(github.com/aws/aws-sdk-go/service/iam)
BuildRequires: golang(github.com/aws/aws-sdk-go/service/s3)
BuildRequires: golang(github.com/aws/aws-sdk-go/service/s3/s3manager)
BuildRequires: golang(github.com/aws/aws-sdk-go/service/sts)
BuildRequires: golang(github.com/Azure/azure-sdk-for-go/management)
BuildRequires: golang(github.com/Azure/azure-sdk-for-go/management/location)
BuildRequires: golang(github.com/Azure/azure-sdk-for-go/storage)
BuildRequires: golang(github.com/coreos/container-linux-config-transpiler/config)
BuildRequires: golang(github.com/coreos/container-linux-config-transpiler/config/platform)
BuildRequires: golang(github.com/coreos/coreos-cloudinit/config)
BuildRequires: golang(github.com/coreos/etcd/etcdserver)
BuildRequires: golang(github.com/coreos/etcd/etcdserver/api/v2http)
BuildRequires: golang(github.com/coreos/etcd/pkg/types)
BuildRequires: golang(github.com/coreos/go-omaha/omaha)
BuildRequires: golang(github.com/coreos/ignition/config/shared/errors)
BuildRequires: golang(github.com/coreos/ignition/config/v1)
BuildRequires: golang(github.com/coreos/ignition/config/v1/types)
BuildRequires: golang(github.com/coreos/ignition/config/v2_0)
BuildRequires: golang(github.com/coreos/ignition/config/v2_0/types)
BuildRequires: golang(github.com/coreos/ignition/config/v2_1)
BuildRequires: golang(github.com/coreos/ignition/config/v2_1/types)
BuildRequires: golang(github.com/coreos/ignition/config/v2_2)
BuildRequires: golang(github.com/coreos/ignition/config/v2_2/types)
BuildRequires: golang(github.com/coreos/ignition/config/v2_3)
BuildRequires: golang(github.com/coreos/ignition/config/v2_3/types)
BuildRequires: golang(github.com/coreos/ioprogress)
BuildRequires: golang(github.com/coreos/pkg/multierror)
BuildRequires: golang(github.com/digitalocean/godo)
BuildRequires: golang(github.com/godbus/dbus)
BuildRequires: golang(github.com/kballard/go-shellquote)
BuildRequires: golang(github.com/Microsoft/azure-vhd-utils/upload)
BuildRequires: golang(github.com/Microsoft/azure-vhd-utils/upload/metadata)
BuildRequires: golang(github.com/Microsoft/azure-vhd-utils/vhdcore/common)
BuildRequires: golang(github.com/Microsoft/azure-vhd-utils/vhdcore/diskstream)
BuildRequires: golang(github.com/packethost/packngo)
BuildRequires: golang(github.com/pborman/uuid)
BuildRequires: golang(github.com/pin/tftp)
BuildRequires: golang(github.com/vincent-petithory/dataurl)
BuildRequires: golang(github.com/vishvananda/netlink)
BuildRequires: golang(github.com/vishvananda/netns)
BuildRequires: golang(github.com/vmware/govmomi)
BuildRequires: golang(github.com/vmware/govmomi/find)
BuildRequires: golang(github.com/vmware/govmomi/object)
BuildRequires: golang(github.com/vmware/govmomi/ovf)
BuildRequires: golang(github.com/vmware/govmomi/vim25)
BuildRequires: golang(github.com/vmware/govmomi/vim25/mo)
BuildRequires: golang(github.com/vmware/govmomi/vim25/progress)
BuildRequires: golang(github.com/vmware/govmomi/vim25/soap)
BuildRequires: golang(github.com/vmware/govmomi/vim25/types)
BuildRequires: golang(golang.org/x/crypto/openpgp)
BuildRequires: golang(golang.org/x/crypto/ssh/terminal)
BuildRequires: golang(golang.org/x/oauth2)
BuildRequires: golang(golang.org/x/oauth2/google)
BuildRequires: golang(golang.org/x/sys/unix)
BuildRequires: golang(google.golang.org/api/googleapi)
%endif

# Main package Provides (via parsedeps.go)
%if 0%{?with_bundled}
Provides: bundled(golang(github.com/aws/aws-sdk-go/aws/awserr)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/aws/awsutil)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/aws/client/metadata)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/aws/client)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/aws/corehandlers)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/aws/credentials/ec2rolecreds)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/aws/credentials/endpointcreds)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/aws/credentials/stscreds)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/aws/credentials)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/aws/defaults)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/aws/ec2metadata)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/aws/endpoints)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/aws/request)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/aws/session)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/aws/signer/v4)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/aws)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/private/protocol/ec2query)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/private/protocol/query/queryutil)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/private/protocol/query)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/private/protocol/rest)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/private/protocol/restxml)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/private/protocol)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/private/protocol/xml/xmlutil)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/service/ec2)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/service/iam)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/service/s3/s3iface)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/service/s3/s3manager)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/service/s3)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/aws/aws-sdk-go/service/sts)) = %{version}-40bc7761a9f06daa574d20f2ad5454db02a05953
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/management/location)) = %{version}-f8b0607613f19ae9509b5ed6fbfda56caf06d59d
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/management/storageservice)) = %{version}-f8b0607613f19ae9509b5ed6fbfda56caf06d59d
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/management)) = %{version}-f8b0607613f19ae9509b5ed6fbfda56caf06d59d
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/storage)) = %{version}-f8b0607613f19ae9509b5ed6fbfda56caf06d59d
Provides: bundled(golang(github.com/beorn7/perks/quantile)) = %{version}-3a771d992973f24aa725d07868b467d1ddfceafb
Provides: bundled(golang(github.com/coreos/container-linux-config-transpiler/config/astyaml)) = %{version}-73f2769c53710f016a6036f4803ac5af1fbe23ea
Provides: bundled(golang(github.com/coreos/container-linux-config-transpiler/config/platform)) = %{version}-73f2769c53710f016a6036f4803ac5af1fbe23ea
Provides: bundled(golang(github.com/coreos/container-linux-config-transpiler/config/templating)) = %{version}-73f2769c53710f016a6036f4803ac5af1fbe23ea
Provides: bundled(golang(github.com/coreos/container-linux-config-transpiler/config/types/util)) = %{version}-73f2769c53710f016a6036f4803ac5af1fbe23ea
Provides: bundled(golang(github.com/coreos/container-linux-config-transpiler/config/types)) = %{version}-73f2769c53710f016a6036f4803ac5af1fbe23ea
Provides: bundled(golang(github.com/coreos/container-linux-config-transpiler/config)) = %{version}-73f2769c53710f016a6036f4803ac5af1fbe23ea
Provides: bundled(golang(github.com/coreos/container-linux-config-transpiler/internal/util)) = %{version}-73f2769c53710f016a6036f4803ac5af1fbe23ea
Provides: bundled(golang(github.com/coreos/coreos-cloudinit/config)) = %{version}-4c333e657bfbaa8f6594298b48324f45e6bf5961
Provides: bundled(golang(github.com/coreos/etcd/alarm)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/auth/authpb)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/auth)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/clientv3)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/client)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/compactor)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/discovery)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/error)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/etcdserver/api/etcdhttp)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/etcdserver/api/v2http/httptypes)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/etcdserver/api/v2http)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/etcdserver/api/v3rpc/rpctypes)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/etcdserver/api)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/etcdserver/auth)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/etcdserver/etcdserverpb)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/etcdserver/membership)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/etcdserver/stats)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/etcdserver)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/lease/leasehttp)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/lease/leasepb)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/lease)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/mvcc/backend)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/mvcc/mvccpb)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/mvcc)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/pkg/adt)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/pkg/contention)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/pkg/cpuutil)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/pkg/crc)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/pkg/fileutil)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/pkg/httputil)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/pkg/idutil)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/pkg/ioutil)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/pkg/logutil)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/pkg/netutil)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/pkg/pathutil)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/pkg/pbutil)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/pkg/runtime)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/pkg/schedule)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/pkg/srv)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/pkg/tlsutil)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/pkg/transport)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/pkg/types)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/pkg/wait)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/rafthttp)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/raft/raftpb)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/raft)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/snap/snappb)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/snap)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/store)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/version)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/wal)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/etcd/wal/walpb)) = %{version}-fca8add78a9d926166eb739b8e4a124434025ba3
Provides: bundled(golang(github.com/coreos/go-omaha/omaha)) = %{version}-f8acb2d7b76c4156223538ca1806a888e764af3d
Provides: bundled(golang(github.com/coreos/go-semver/semver)) = %{version}-5e3acbb5668c4c3deb4842615c4098eb61fb6b1e
Provides: bundled(golang(github.com/coreos/go-systemd/journal)) = %{version}-9002847aa1425fb6ac49077c0a630b3b67e0fbfd
Provides: bundled(golang(github.com/coreos/go-systemd/unit)) = %{version}-9002847aa1425fb6ac49077c0a630b3b67e0fbfd
Provides: bundled(golang(github.com/coreos/ignition/config/shared/errors)) = %{version}-2a88cd95b6812a70a7dad150f4cb18c5f028bc22
Provides: bundled(golang(github.com/coreos/ignition/config/shared/validations)) = %{version}-2a88cd95b6812a70a7dad150f4cb18c5f028bc22
Provides: bundled(golang(github.com/coreos/ignition/config/util)) = %{version}-2a88cd95b6812a70a7dad150f4cb18c5f028bc22
Provides: bundled(golang(github.com/coreos/ignition/config/v1/types)) = %{version}-2a88cd95b6812a70a7dad150f4cb18c5f028bc22
Provides: bundled(golang(github.com/coreos/ignition/config/v1)) = %{version}-2a88cd95b6812a70a7dad150f4cb18c5f028bc22
Provides: bundled(golang(github.com/coreos/ignition/config/v2_0/types)) = %{version}-2a88cd95b6812a70a7dad150f4cb18c5f028bc22
Provides: bundled(golang(github.com/coreos/ignition/config/v2_0)) = %{version}-2a88cd95b6812a70a7dad150f4cb18c5f028bc22
Provides: bundled(golang(github.com/coreos/ignition/config/v2_1/types)) = %{version}-2a88cd95b6812a70a7dad150f4cb18c5f028bc22
Provides: bundled(golang(github.com/coreos/ignition/config/v2_1)) = %{version}-2a88cd95b6812a70a7dad150f4cb18c5f028bc22
Provides: bundled(golang(github.com/coreos/ignition/config/v2_2/types)) = %{version}-2a88cd95b6812a70a7dad150f4cb18c5f028bc22
Provides: bundled(golang(github.com/coreos/ignition/config/v2_2)) = %{version}-2a88cd95b6812a70a7dad150f4cb18c5f028bc22
Provides: bundled(golang(github.com/coreos/ignition/config/v2_3/types)) = %{version}-2a88cd95b6812a70a7dad150f4cb18c5f028bc22
Provides: bundled(golang(github.com/coreos/ignition/config/v2_3)) = %{version}-2a88cd95b6812a70a7dad150f4cb18c5f028bc22
Provides: bundled(golang(github.com/coreos/ignition/config/v2_4_experimental/types)) = %{version}-2a88cd95b6812a70a7dad150f4cb18c5f028bc22
Provides: bundled(golang(github.com/coreos/ignition/config/validate/astjson)) = %{version}-2a88cd95b6812a70a7dad150f4cb18c5f028bc22
Provides: bundled(golang(github.com/coreos/ignition/config/validate/astnode)) = %{version}-2a88cd95b6812a70a7dad150f4cb18c5f028bc22
Provides: bundled(golang(github.com/coreos/ignition/config/validate/report)) = %{version}-2a88cd95b6812a70a7dad150f4cb18c5f028bc22
Provides: bundled(golang(github.com/coreos/ignition/config/validate)) = %{version}-2a88cd95b6812a70a7dad150f4cb18c5f028bc22
Provides: bundled(golang(github.com/coreos/pkg/capnslog)) = %{version}-447b7ec906e523386d9c53be15b55a8ae86ea944
Provides: bundled(golang(github.com/coreos/pkg/multierror)) = %{version}-447b7ec906e523386d9c53be15b55a8ae86ea944
Provides: bundled(golang(github.com/cpuguy83/go-md2man/md2man)) = %{version}-71acacd42f85e5e82f70a55327789582a5200a90
Provides: bundled(golang(github.com/digitalocean/godo/context)) = %{version}-7a32b5ce17203924a21366d5031032fd326d5051
Provides: bundled(golang(github.com/gogo/protobuf/gogoproto)) = %{version}-342cbe0a04158f6dcb03ca0079991a51a4248c02
Provides: bundled(golang(github.com/gogo/protobuf/protoc-gen-gogo/descriptor)) = %{version}-342cbe0a04158f6dcb03ca0079991a51a4248c02
Provides: bundled(golang(github.com/gogo/protobuf/proto)) = %{version}-342cbe0a04158f6dcb03ca0079991a51a4248c02
Provides: bundled(golang(github.com/golang/protobuf/proto)) = %{version}-8616e8ee5e20a1704615e6c8d7afcdac06087a67
Provides: bundled(golang(github.com/golang/protobuf/ptypes/any)) = %{version}-8616e8ee5e20a1704615e6c8d7afcdac06087a67
Provides: bundled(golang(github.com/golang/protobuf/ptypes/duration)) = %{version}-8616e8ee5e20a1704615e6c8d7afcdac06087a67
Provides: bundled(golang(github.com/golang/protobuf/ptypes/timestamp)) = %{version}-8616e8ee5e20a1704615e6c8d7afcdac06087a67
Provides: bundled(golang(github.com/golang/protobuf/ptypes)) = %{version}-8616e8ee5e20a1704615e6c8d7afcdac06087a67
Provides: bundled(golang(github.com/google/go-querystring/query)) = %{version}-44c6ddd0a2342c386950e880b658017258da92fc
Provides: bundled(golang(github.com/kylelemons/godebug/diff)) = %{version}-21cb3784d9bda523911b96719efba02b7e983256
Provides: bundled(golang(github.com/kylelemons/godebug/pretty)) = %{version}-21cb3784d9bda523911b96719efba02b7e983256
Provides: bundled(golang(github.com/matttproud/golang_protobuf_extensions/pbutil)) = %{version}-c12348ce28de40eed0136aa2b644d0ee0650e56c
Provides: bundled(golang(github.com/Microsoft/azure-vhd-utils/upload/concurrent)) = %{version}-43293b8d76460dd25093d216c95abc79342e1657
Provides: bundled(golang(github.com/Microsoft/azure-vhd-utils/upload/metadata)) = %{version}-43293b8d76460dd25093d216c95abc79342e1657
Provides: bundled(golang(github.com/Microsoft/azure-vhd-utils/upload/progress)) = %{version}-43293b8d76460dd25093d216c95abc79342e1657
Provides: bundled(golang(github.com/Microsoft/azure-vhd-utils/upload)) = %{version}-43293b8d76460dd25093d216c95abc79342e1657
Provides: bundled(golang(github.com/Microsoft/azure-vhd-utils/vhdcore/bat)) = %{version}-43293b8d76460dd25093d216c95abc79342e1657
Provides: bundled(golang(github.com/Microsoft/azure-vhd-utils/vhdcore/block/bitmap)) = %{version}-43293b8d76460dd25093d216c95abc79342e1657
Provides: bundled(golang(github.com/Microsoft/azure-vhd-utils/vhdcore/block)) = %{version}-43293b8d76460dd25093d216c95abc79342e1657
Provides: bundled(golang(github.com/Microsoft/azure-vhd-utils/vhdcore/common)) = %{version}-43293b8d76460dd25093d216c95abc79342e1657
Provides: bundled(golang(github.com/Microsoft/azure-vhd-utils/vhdcore/diskstream)) = %{version}-43293b8d76460dd25093d216c95abc79342e1657
Provides: bundled(golang(github.com/Microsoft/azure-vhd-utils/vhdcore/footer)) = %{version}-43293b8d76460dd25093d216c95abc79342e1657
Provides: bundled(golang(github.com/Microsoft/azure-vhd-utils/vhdcore/header/parentlocator)) = %{version}-43293b8d76460dd25093d216c95abc79342e1657
Provides: bundled(golang(github.com/Microsoft/azure-vhd-utils/vhdcore/header)) = %{version}-43293b8d76460dd25093d216c95abc79342e1657
Provides: bundled(golang(github.com/Microsoft/azure-vhd-utils/vhdcore/reader)) = %{version}-43293b8d76460dd25093d216c95abc79342e1657
Provides: bundled(golang(github.com/Microsoft/azure-vhd-utils/vhdcore/validator)) = %{version}-43293b8d76460dd25093d216c95abc79342e1657
Provides: bundled(golang(github.com/Microsoft/azure-vhd-utils/vhdcore)) = %{version}-43293b8d76460dd25093d216c95abc79342e1657
Provides: bundled(golang(github.com/Microsoft/azure-vhd-utils/vhdcore/vhdfile)) = %{version}-43293b8d76460dd25093d216c95abc79342e1657
Provides: bundled(golang(github.com/Microsoft/azure-vhd-utils/vhdcore/writer)) = %{version}-43293b8d76460dd25093d216c95abc79342e1657
Provides: bundled(golang(github.com/pin/tftp/netascii)) = %{version}-9ea92f6b1029bc1bf3072bba195c84bb9b0370e3
Provides: bundled(golang(github.com/prometheus/client_golang/prometheus/promhttp)) = %{version}-5cec1d0429b02e4323e042eb04dafdb079ddf568
Provides: bundled(golang(github.com/prometheus/client_golang/prometheus)) = %{version}-5cec1d0429b02e4323e042eb04dafdb079ddf568
Provides: bundled(golang(github.com/prometheus/client_model/go)) = %{version}-6f3806018612930941127f2a7c6c453ba2c527d2
Provides: bundled(golang(github.com/prometheus/common/expfmt)) = %{version}-e3fb1a1acd7605367a2b378bc2e2f893c05174b7
Provides: bundled(golang(github.com/prometheus/common/internal/bitbucket.org/ww/goautoneg)) = %{version}-e3fb1a1acd7605367a2b378bc2e2f893c05174b7
Provides: bundled(golang(github.com/prometheus/common/model)) = %{version}-e3fb1a1acd7605367a2b378bc2e2f893c05174b7
Provides: bundled(golang(github.com/prometheus/procfs/xfs)) = %{version}-a6e9df898b1336106c743392c48ee0b71f5c4efa
Provides: bundled(golang(github.com/ugorji/go/codec)) = %{version}-bdcc60b419d136a85cdf2e7cbcac34b3f1cd6e57
Provides: bundled(golang(github.com/vishvananda/netlink/nl)) = %{version}-2e9d285a7160e1c65e1eab8238faf2d6a0dc9a4a
Provides: bundled(golang(github.com/vmware/govmomi/find)) = %{version}-b63044e5f833781eb7b305bc035392480ee06a82
Provides: bundled(golang(github.com/vmware/govmomi/list)) = %{version}-b63044e5f833781eb7b305bc035392480ee06a82
Provides: bundled(golang(github.com/vmware/govmomi/object)) = %{version}-b63044e5f833781eb7b305bc035392480ee06a82
Provides: bundled(golang(github.com/vmware/govmomi/ovf)) = %{version}-b63044e5f833781eb7b305bc035392480ee06a82
Provides: bundled(golang(github.com/vmware/govmomi/property)) = %{version}-b63044e5f833781eb7b305bc035392480ee06a82
Provides: bundled(golang(github.com/vmware/govmomi/session)) = %{version}-b63044e5f833781eb7b305bc035392480ee06a82
Provides: bundled(golang(github.com/vmware/govmomi/task)) = %{version}-b63044e5f833781eb7b305bc035392480ee06a82
Provides: bundled(golang(github.com/vmware/govmomi/vim25/debug)) = %{version}-b63044e5f833781eb7b305bc035392480ee06a82
Provides: bundled(golang(github.com/vmware/govmomi/vim25/methods)) = %{version}-b63044e5f833781eb7b305bc035392480ee06a82
Provides: bundled(golang(github.com/vmware/govmomi/vim25/mo)) = %{version}-b63044e5f833781eb7b305bc035392480ee06a82
Provides: bundled(golang(github.com/vmware/govmomi/vim25/progress)) = %{version}-b63044e5f833781eb7b305bc035392480ee06a82
Provides: bundled(golang(github.com/vmware/govmomi/vim25/soap)) = %{version}-b63044e5f833781eb7b305bc035392480ee06a82
Provides: bundled(golang(github.com/vmware/govmomi/vim25/types)) = %{version}-b63044e5f833781eb7b305bc035392480ee06a82
Provides: bundled(golang(github.com/vmware/govmomi/vim25)) = %{version}-b63044e5f833781eb7b305bc035392480ee06a82
Provides: bundled(golang(github.com/vmware/govmomi/vim25/xml)) = %{version}-b63044e5f833781eb7b305bc035392480ee06a82
Provides: bundled(golang(go4.org/errorutil)) = %{version}-03efcb870d84809319ea509714dd6d19a1498483
Provides: bundled(golang(golang.org/x/crypto/bcrypt)) = %{version}-119f50887f8fe324fe2386421c27a11af014b64e
Provides: bundled(golang(golang.org/x/crypto/blowfish)) = %{version}-119f50887f8fe324fe2386421c27a11af014b64e
Provides: bundled(golang(golang.org/x/crypto/cast5)) = %{version}-119f50887f8fe324fe2386421c27a11af014b64e
Provides: bundled(golang(golang.org/x/crypto/curve25519)) = %{version}-119f50887f8fe324fe2386421c27a11af014b64e
Provides: bundled(golang(golang.org/x/crypto/ed25519/internal/edwards25519)) = %{version}-119f50887f8fe324fe2386421c27a11af014b64e
Provides: bundled(golang(golang.org/x/crypto/ed25519)) = %{version}-119f50887f8fe324fe2386421c27a11af014b64e
Provides: bundled(golang(golang.org/x/crypto/openpgp/armor)) = %{version}-119f50887f8fe324fe2386421c27a11af014b64e
Provides: bundled(golang(golang.org/x/crypto/openpgp/elgamal)) = %{version}-119f50887f8fe324fe2386421c27a11af014b64e
Provides: bundled(golang(golang.org/x/crypto/openpgp/errors)) = %{version}-119f50887f8fe324fe2386421c27a11af014b64e
Provides: bundled(golang(golang.org/x/crypto/openpgp/packet)) = %{version}-119f50887f8fe324fe2386421c27a11af014b64e
Provides: bundled(golang(golang.org/x/crypto/openpgp/s2k)) = %{version}-119f50887f8fe324fe2386421c27a11af014b64e
Provides: bundled(golang(golang.org/x/crypto/openpgp)) = %{version}-119f50887f8fe324fe2386421c27a11af014b64e
Provides: bundled(golang(golang.org/x/crypto/pkcs12/internal/rc2)) = %{version}-119f50887f8fe324fe2386421c27a11af014b64e
Provides: bundled(golang(golang.org/x/crypto/pkcs12)) = %{version}-119f50887f8fe324fe2386421c27a11af014b64e
Provides: bundled(golang(golang.org/x/crypto/ssh/agent)) = %{version}-119f50887f8fe324fe2386421c27a11af014b64e
Provides: bundled(golang(golang.org/x/crypto/ssh/terminal)) = %{version}-119f50887f8fe324fe2386421c27a11af014b64e
Provides: bundled(golang(golang.org/x/crypto/ssh)) = %{version}-119f50887f8fe324fe2386421c27a11af014b64e
Provides: bundled(golang(golang.org/x/net/bpf)) = %{version}-66aacef3dd8a676686c7ae3716979581e8b03c47
Provides: bundled(golang(golang.org/x/net/context/ctxhttp)) = %{version}-66aacef3dd8a676686c7ae3716979581e8b03c47
Provides: bundled(golang(golang.org/x/net/context)) = %{version}-66aacef3dd8a676686c7ae3716979581e8b03c47
Provides: bundled(golang(golang.org/x/net/http2/hpack)) = %{version}-66aacef3dd8a676686c7ae3716979581e8b03c47
Provides: bundled(golang(golang.org/x/net/http2)) = %{version}-66aacef3dd8a676686c7ae3716979581e8b03c47
Provides: bundled(golang(golang.org/x/net/idna)) = %{version}-66aacef3dd8a676686c7ae3716979581e8b03c47
Provides: bundled(golang(golang.org/x/net/internal/iana)) = %{version}-66aacef3dd8a676686c7ae3716979581e8b03c47
Provides: bundled(golang(golang.org/x/net/internal/socket)) = %{version}-66aacef3dd8a676686c7ae3716979581e8b03c47
Provides: bundled(golang(golang.org/x/net/internal/timeseries)) = %{version}-66aacef3dd8a676686c7ae3716979581e8b03c47
Provides: bundled(golang(golang.org/x/net/ipv4)) = %{version}-66aacef3dd8a676686c7ae3716979581e8b03c47
Provides: bundled(golang(golang.org/x/net/ipv6)) = %{version}-66aacef3dd8a676686c7ae3716979581e8b03c47
Provides: bundled(golang(golang.org/x/net/lex/httplex)) = %{version}-66aacef3dd8a676686c7ae3716979581e8b03c47
Provides: bundled(golang(golang.org/x/net/trace)) = %{version}-66aacef3dd8a676686c7ae3716979581e8b03c47
Provides: bundled(golang(golang.org/x/oauth2/google)) = %{version}-045497edb6234273d67dbc25da3f2ddbc4c4cacf
Provides: bundled(golang(golang.org/x/oauth2/internal)) = %{version}-045497edb6234273d67dbc25da3f2ddbc4c4cacf
Provides: bundled(golang(golang.org/x/oauth2/jws)) = %{version}-045497edb6234273d67dbc25da3f2ddbc4c4cacf
Provides: bundled(golang(golang.org/x/oauth2/jwt)) = %{version}-045497edb6234273d67dbc25da3f2ddbc4c4cacf
Provides: bundled(golang(golang.org/x/sys/unix)) = %{version}-c2ed4eda69e7f62900806e4cd6e45f0429f859fa
Provides: bundled(golang(golang.org/x/text/secure/bidirule)) = %{version}-b19bf474d317b857955b12035d2c5acb57ce8b01
Provides: bundled(golang(golang.org/x/text/transform)) = %{version}-b19bf474d317b857955b12035d2c5acb57ce8b01
Provides: bundled(golang(golang.org/x/text/unicode/bidi)) = %{version}-b19bf474d317b857955b12035d2c5acb57ce8b01
Provides: bundled(golang(golang.org/x/text/unicode/norm)) = %{version}-b19bf474d317b857955b12035d2c5acb57ce8b01
Provides: bundled(golang(golang.org/x/time/rate)) = %{version}-c06e80d9300e4443158a03817b8a8cb37d230320
Provides: bundled(golang(google.golang.org/api/compute/v1)) = %{version}-c858ef4400610cbfd097ffc5f5c6e4a1a51eac86
Provides: bundled(golang(google.golang.org/api/gensupport)) = %{version}-c858ef4400610cbfd097ffc5f5c6e4a1a51eac86
Provides: bundled(golang(google.golang.org/api/googleapi/internal/uritemplates)) = %{version}-c858ef4400610cbfd097ffc5f5c6e4a1a51eac86
Provides: bundled(golang(google.golang.org/api/googleapi)) = %{version}-c858ef4400610cbfd097ffc5f5c6e4a1a51eac86
Provides: bundled(golang(google.golang.org/api/storage/v1)) = %{version}-c858ef4400610cbfd097ffc5f5c6e4a1a51eac86
Provides: bundled(golang(google.golang.org/appengine/internal/app_identity)) = %{version}-a37df1387b4521194676d88c79230c613610d5f4
Provides: bundled(golang(google.golang.org/appengine/internal/base)) = %{version}-a37df1387b4521194676d88c79230c613610d5f4
Provides: bundled(golang(google.golang.org/appengine/internal/datastore)) = %{version}-a37df1387b4521194676d88c79230c613610d5f4
Provides: bundled(golang(google.golang.org/appengine/internal/log)) = %{version}-a37df1387b4521194676d88c79230c613610d5f4
Provides: bundled(golang(google.golang.org/appengine/internal/modules)) = %{version}-a37df1387b4521194676d88c79230c613610d5f4
Provides: bundled(golang(google.golang.org/appengine/internal/remote_api)) = %{version}-a37df1387b4521194676d88c79230c613610d5f4
Provides: bundled(golang(google.golang.org/appengine/internal/urlfetch)) = %{version}-a37df1387b4521194676d88c79230c613610d5f4
Provides: bundled(golang(google.golang.org/appengine/internal)) = %{version}-a37df1387b4521194676d88c79230c613610d5f4
Provides: bundled(golang(google.golang.org/appengine/urlfetch)) = %{version}-a37df1387b4521194676d88c79230c613610d5f4
Provides: bundled(golang(google.golang.org/cloud/compute/metadata)) = %{version}-022eb1645b78acb655755a0c1e185c68cd5c8eb3
Provides: bundled(golang(google.golang.org/genproto/googleapis/rpc/status)) = %{version}-09f6ed296fc66555a25fe4ce95173148778dfa85
Provides: bundled(golang(google.golang.org/grpc/balancer)) = %{version}-5b3c4e850e90a4cf6a20ebd46c8b32a0a3afcb9e
Provides: bundled(golang(google.golang.org/grpc/codes)) = %{version}-5b3c4e850e90a4cf6a20ebd46c8b32a0a3afcb9e
Provides: bundled(golang(google.golang.org/grpc/connectivity)) = %{version}-5b3c4e850e90a4cf6a20ebd46c8b32a0a3afcb9e
Provides: bundled(golang(google.golang.org/grpc/credentials)) = %{version}-5b3c4e850e90a4cf6a20ebd46c8b32a0a3afcb9e
Provides: bundled(golang(google.golang.org/grpc/grpclb/grpc_lb_v1/messages)) = %{version}-5b3c4e850e90a4cf6a20ebd46c8b32a0a3afcb9e
Provides: bundled(golang(google.golang.org/grpc/grpclog)) = %{version}-5b3c4e850e90a4cf6a20ebd46c8b32a0a3afcb9e
Provides: bundled(golang(google.golang.org/grpc/health/grpc_health_v1)) = %{version}-5b3c4e850e90a4cf6a20ebd46c8b32a0a3afcb9e
Provides: bundled(golang(google.golang.org/grpc/health)) = %{version}-5b3c4e850e90a4cf6a20ebd46c8b32a0a3afcb9e
Provides: bundled(golang(google.golang.org/grpc/internal)) = %{version}-5b3c4e850e90a4cf6a20ebd46c8b32a0a3afcb9e
Provides: bundled(golang(google.golang.org/grpc/keepalive)) = %{version}-5b3c4e850e90a4cf6a20ebd46c8b32a0a3afcb9e
Provides: bundled(golang(google.golang.org/grpc/metadata)) = %{version}-5b3c4e850e90a4cf6a20ebd46c8b32a0a3afcb9e
Provides: bundled(golang(google.golang.org/grpc/naming)) = %{version}-5b3c4e850e90a4cf6a20ebd46c8b32a0a3afcb9e
Provides: bundled(golang(google.golang.org/grpc/peer)) = %{version}-5b3c4e850e90a4cf6a20ebd46c8b32a0a3afcb9e
Provides: bundled(golang(google.golang.org/grpc/resolver)) = %{version}-5b3c4e850e90a4cf6a20ebd46c8b32a0a3afcb9e
Provides: bundled(golang(google.golang.org/grpc/stats)) = %{version}-5b3c4e850e90a4cf6a20ebd46c8b32a0a3afcb9e
Provides: bundled(golang(google.golang.org/grpc/status)) = %{version}-5b3c4e850e90a4cf6a20ebd46c8b32a0a3afcb9e
Provides: bundled(golang(google.golang.org/grpc/tap)) = %{version}-5b3c4e850e90a4cf6a20ebd46c8b32a0a3afcb9e
Provides: bundled(golang(google.golang.org/grpc/transport)) = %{version}-5b3c4e850e90a4cf6a20ebd46c8b32a0a3afcb9e
%endif

%description
%{summary}

%if 0%{?with_devel}
%package devel
Summary:       %{summary}
BuildArch:     noarch

# devel subpackage BuildRequires
%if 0%{?with_check} && ! 0%{?with_bundled}
BuildRequires: golang(github.com/Azure/azure-sdk-for-go/management)
BuildRequires: golang(github.com/Azure/azure-sdk-for-go/management/location)
BuildRequires: golang(github.com/Azure/azure-sdk-for-go/management/storageservice)
BuildRequires: golang(github.com/Azure/azure-sdk-for-go/storage)
BuildRequires: golang(github.com/Microsoft/azure-vhd-utils/upload)
BuildRequires: golang(github.com/Microsoft/azure-vhd-utils/upload/metadata)
BuildRequires: golang(github.com/Microsoft/azure-vhd-utils/vhdcore/common)
BuildRequires: golang(github.com/Microsoft/azure-vhd-utils/vhdcore/diskstream)
BuildRequires: golang(github.com/Microsoft/azure-vhd-utils/vhdcore/validator)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/awserr)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/client)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/credentials)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/endpoints)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/request)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/session)
BuildRequires: golang(github.com/aws/aws-sdk-go/service/ec2)
BuildRequires: golang(github.com/aws/aws-sdk-go/service/iam)
BuildRequires: golang(github.com/aws/aws-sdk-go/service/s3)
BuildRequires: golang(github.com/aws/aws-sdk-go/service/s3/s3manager)
BuildRequires: golang(github.com/aws/aws-sdk-go/service/sts)
BuildRequires: golang(github.com/coreos/container-linux-config-transpiler/config)
BuildRequires: golang(github.com/coreos/container-linux-config-transpiler/config/platform)
BuildRequires: golang(github.com/coreos/coreos-cloudinit/config)
BuildRequires: golang(github.com/coreos/etcd/etcdserver)
BuildRequires: golang(github.com/coreos/etcd/etcdserver/api/v2http)
BuildRequires: golang(github.com/coreos/etcd/pkg/types)
BuildRequires: golang(github.com/coreos/go-omaha/omaha)
BuildRequires: golang(github.com/coreos/go-semver/semver)
BuildRequires: golang(github.com/coreos/ignition/config/shared/errors)
BuildRequires: golang(github.com/coreos/ignition/config/v1)
BuildRequires: golang(github.com/coreos/ignition/config/v1/types)
BuildRequires: golang(github.com/coreos/ignition/config/v2_0)
BuildRequires: golang(github.com/coreos/ignition/config/v2_0/types)
BuildRequires: golang(github.com/coreos/ignition/config/v2_1)
BuildRequires: golang(github.com/coreos/ignition/config/v2_1/types)
BuildRequires: golang(github.com/coreos/ignition/config/v2_2)
BuildRequires: golang(github.com/coreos/ignition/config/v2_2/types)
BuildRequires: golang(github.com/coreos/ignition/config/v2_3)
BuildRequires: golang(github.com/coreos/ignition/config/v2_3/types)
BuildRequires: golang(github.com/coreos/ioprogress)
BuildRequires: golang(github.com/coreos/pkg/capnslog)
BuildRequires: golang(github.com/coreos/pkg/multierror)
BuildRequires: golang(github.com/digitalocean/godo)
BuildRequires: golang(github.com/godbus/dbus)
BuildRequires: golang(github.com/golang/protobuf/proto)
BuildRequires: golang(github.com/kballard/go-shellquote)
BuildRequires: golang(github.com/packethost/packngo)
BuildRequires: golang(github.com/pborman/uuid)
BuildRequires: golang(github.com/pin/tftp)
BuildRequires: golang(github.com/spf13/cobra)
BuildRequires: golang(github.com/vincent-petithory/dataurl)
BuildRequires: golang(github.com/vishvananda/netlink)
BuildRequires: golang(github.com/vishvananda/netns)
BuildRequires: golang(github.com/vmware/govmomi)
BuildRequires: golang(github.com/vmware/govmomi/find)
BuildRequires: golang(github.com/vmware/govmomi/object)
BuildRequires: golang(github.com/vmware/govmomi/ovf)
BuildRequires: golang(github.com/vmware/govmomi/vim25)
BuildRequires: golang(github.com/vmware/govmomi/vim25/mo)
BuildRequires: golang(github.com/vmware/govmomi/vim25/progress)
BuildRequires: golang(github.com/vmware/govmomi/vim25/soap)
BuildRequires: golang(github.com/vmware/govmomi/vim25/types)
BuildRequires: golang(golang.org/x/crypto/openpgp)
BuildRequires: golang(golang.org/x/crypto/ssh)
BuildRequires: golang(golang.org/x/crypto/ssh/agent)
BuildRequires: golang(golang.org/x/crypto/ssh/terminal)
BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(golang.org/x/oauth2)
BuildRequires: golang(golang.org/x/oauth2/google)
BuildRequires: golang(golang.org/x/sys/unix)
BuildRequires: golang(google.golang.org/api/compute/v1)
BuildRequires: golang(google.golang.org/api/googleapi)
BuildRequires: golang(google.golang.org/api/storage/v1)
%endif

# devel subpackage Requires
Requires:      golang(github.com/Azure/azure-sdk-for-go/management)
Requires:      golang(github.com/Azure/azure-sdk-for-go/management/location)
Requires:      golang(github.com/Azure/azure-sdk-for-go/management/storageservice)
Requires:      golang(github.com/Azure/azure-sdk-for-go/storage)
Requires:      golang(github.com/Microsoft/azure-vhd-utils/upload)
Requires:      golang(github.com/Microsoft/azure-vhd-utils/upload/metadata)
Requires:      golang(github.com/Microsoft/azure-vhd-utils/vhdcore/common)
Requires:      golang(github.com/Microsoft/azure-vhd-utils/vhdcore/diskstream)
Requires:      golang(github.com/Microsoft/azure-vhd-utils/vhdcore/validator)
Requires:      golang(github.com/aws/aws-sdk-go/aws)
Requires:      golang(github.com/aws/aws-sdk-go/aws/awserr)
Requires:      golang(github.com/aws/aws-sdk-go/aws/client)
Requires:      golang(github.com/aws/aws-sdk-go/aws/credentials)
Requires:      golang(github.com/aws/aws-sdk-go/aws/endpoints)
Requires:      golang(github.com/aws/aws-sdk-go/aws/request)
Requires:      golang(github.com/aws/aws-sdk-go/aws/session)
Requires:      golang(github.com/aws/aws-sdk-go/service/ec2)
Requires:      golang(github.com/aws/aws-sdk-go/service/iam)
Requires:      golang(github.com/aws/aws-sdk-go/service/s3)
Requires:      golang(github.com/aws/aws-sdk-go/service/s3/s3manager)
Requires:      golang(github.com/aws/aws-sdk-go/service/sts)
Requires:      golang(github.com/coreos/container-linux-config-transpiler/config)
Requires:      golang(github.com/coreos/container-linux-config-transpiler/config/platform)
Requires:      golang(github.com/coreos/coreos-cloudinit/config)
Requires:      golang(github.com/coreos/etcd/etcdserver)
Requires:      golang(github.com/coreos/etcd/etcdserver/api/v2http)
Requires:      golang(github.com/coreos/etcd/pkg/types)
Requires:      golang(github.com/coreos/go-omaha/omaha)
Requires:      golang(github.com/coreos/go-semver/semver)
Requires:      golang(github.com/coreos/ignition/config/shared/errors)
Requires:      golang(github.com/coreos/ignition/config/v1)
Requires:      golang(github.com/coreos/ignition/config/v1/types)
Requires:      golang(github.com/coreos/ignition/config/v2_0)
Requires:      golang(github.com/coreos/ignition/config/v2_0/types)
Requires:      golang(github.com/coreos/ignition/config/v2_1)
Requires:      golang(github.com/coreos/ignition/config/v2_1/types)
Requires:      golang(github.com/coreos/ignition/config/v2_2)
Requires:      golang(github.com/coreos/ignition/config/v2_2/types)
Requires:      golang(github.com/coreos/ignition/config/v2_3)
Requires:      golang(github.com/coreos/ignition/config/v2_3/types)
Requires:      golang(github.com/coreos/ioprogress)
Requires:      golang(github.com/coreos/pkg/capnslog)
Requires:      golang(github.com/coreos/pkg/multierror)
Requires:      golang(github.com/digitalocean/godo)
Requires:      golang(github.com/godbus/dbus)
Requires:      golang(github.com/golang/protobuf/proto)
Requires:      golang(github.com/kballard/go-shellquote)
Requires:      golang(github.com/packethost/packngo)
Requires:      golang(github.com/pborman/uuid)
Requires:      golang(github.com/pin/tftp)
Requires:      golang(github.com/spf13/cobra)
Requires:      golang(github.com/vincent-petithory/dataurl)
Requires:      golang(github.com/vishvananda/netlink)
Requires:      golang(github.com/vishvananda/netns)
Requires:      golang(github.com/vmware/govmomi)
Requires:      golang(github.com/vmware/govmomi/find)
Requires:      golang(github.com/vmware/govmomi/object)
Requires:      golang(github.com/vmware/govmomi/ovf)
Requires:      golang(github.com/vmware/govmomi/vim25)
Requires:      golang(github.com/vmware/govmomi/vim25/mo)
Requires:      golang(github.com/vmware/govmomi/vim25/progress)
Requires:      golang(github.com/vmware/govmomi/vim25/soap)
Requires:      golang(github.com/vmware/govmomi/vim25/types)
Requires:      golang(golang.org/x/crypto/openpgp)
Requires:      golang(golang.org/x/crypto/ssh)
Requires:      golang(golang.org/x/crypto/ssh/agent)
Requires:      golang(golang.org/x/crypto/ssh/terminal)
Requires:      golang(golang.org/x/net/context)
Requires:      golang(golang.org/x/oauth2)
Requires:      golang(golang.org/x/oauth2/google)
Requires:      golang(golang.org/x/sys/unix)
Requires:      golang(google.golang.org/api/compute/v1)
Requires:      golang(google.golang.org/api/googleapi)
Requires:      golang(google.golang.org/api/storage/v1)

# devel subpackage Provides
Provides:      golang(%{import_path}/auth) = %{version}-%{release}
Provides:      golang(%{import_path}/cli) = %{version}-%{release}
Provides:      golang(%{import_path}/cmd/ore/aws) = %{version}-%{release}
Provides:      golang(%{import_path}/cmd/ore/azure) = %{version}-%{release}
Provides:      golang(%{import_path}/cmd/ore/do) = %{version}-%{release}
Provides:      golang(%{import_path}/cmd/ore/esx) = %{version}-%{release}
Provides:      golang(%{import_path}/cmd/ore/gcloud) = %{version}-%{release}
Provides:      golang(%{import_path}/cmd/ore/packet) = %{version}-%{release}
Provides:      golang(%{import_path}/harness) = %{version}-%{release}
Provides:      golang(%{import_path}/harness/reporters) = %{version}-%{release}
Provides:      golang(%{import_path}/harness/testresult) = %{version}-%{release}
Provides:      golang(%{import_path}/kola) = %{version}-%{release}
Provides:      golang(%{import_path}/kola/cluster) = %{version}-%{release}
Provides:      golang(%{import_path}/kola/register) = %{version}-%{release}
Provides:      golang(%{import_path}/kola/registry) = %{version}-%{release}
Provides:      golang(%{import_path}/kola/tests/coretest) = %{version}-%{release}
Provides:      golang(%{import_path}/kola/tests/crio) = %{version}-%{release}
Provides:      golang(%{import_path}/kola/tests/docker) = %{version}-%{release}
Provides:      golang(%{import_path}/kola/tests/etcd) = %{version}-%{release}
Provides:      golang(%{import_path}/kola/tests/flannel) = %{version}-%{release}
Provides:      golang(%{import_path}/kola/tests/ignition) = %{version}-%{release}
Provides:      golang(%{import_path}/kola/tests/kubernetes) = %{version}-%{release}
Provides:      golang(%{import_path}/kola/tests/locksmith) = %{version}-%{release}
Provides:      golang(%{import_path}/kola/tests/metadata) = %{version}-%{release}
Provides:      golang(%{import_path}/kola/tests/misc) = %{version}-%{release}
Provides:      golang(%{import_path}/kola/tests/ostree) = %{version}-%{release}
Provides:      golang(%{import_path}/kola/tests/packages) = %{version}-%{release}
Provides:      golang(%{import_path}/kola/tests/podman) = %{version}-%{release}
Provides:      golang(%{import_path}/kola/tests/rkt) = %{version}-%{release}
Provides:      golang(%{import_path}/kola/tests/rpmostree) = %{version}-%{release}
Provides:      golang(%{import_path}/kola/tests/systemd) = %{version}-%{release}
Provides:      golang(%{import_path}/kola/tests/torcx) = %{version}-%{release}
Provides:      golang(%{import_path}/kola/tests/update) = %{version}-%{release}
Provides:      golang(%{import_path}/kola/tests/util) = %{version}-%{release}
Provides:      golang(%{import_path}/kola/torcx) = %{version}-%{release}
Provides:      golang(%{import_path}/lang) = %{version}-%{release}
Provides:      golang(%{import_path}/lang/bufpipe) = %{version}-%{release}
Provides:      golang(%{import_path}/lang/destructor) = %{version}-%{release}
Provides:      golang(%{import_path}/lang/maps) = %{version}-%{release}
Provides:      golang(%{import_path}/lang/natsort) = %{version}-%{release}
Provides:      golang(%{import_path}/lang/reader) = %{version}-%{release}
Provides:      golang(%{import_path}/lang/worker) = %{version}-%{release}
Provides:      golang(%{import_path}/network) = %{version}-%{release}
Provides:      golang(%{import_path}/network/bufnet) = %{version}-%{release}
Provides:      golang(%{import_path}/network/journal) = %{version}-%{release}
Provides:      golang(%{import_path}/network/mockssh) = %{version}-%{release}
Provides:      golang(%{import_path}/network/neterror) = %{version}-%{release}
Provides:      golang(%{import_path}/network/ntp) = %{version}-%{release}
Provides:      golang(%{import_path}/platform) = %{version}-%{release}
Provides:      golang(%{import_path}/platform/api/aws) = %{version}-%{release}
Provides:      golang(%{import_path}/platform/api/azure) = %{version}-%{release}
Provides:      golang(%{import_path}/platform/api/do) = %{version}-%{release}
Provides:      golang(%{import_path}/platform/api/esx) = %{version}-%{release}
Provides:      golang(%{import_path}/platform/api/gcloud) = %{version}-%{release}
Provides:      golang(%{import_path}/platform/api/packet) = %{version}-%{release}
Provides:      golang(%{import_path}/platform/conf) = %{version}-%{release}
Provides:      golang(%{import_path}/platform/local) = %{version}-%{release}
Provides:      golang(%{import_path}/platform/machine/aws) = %{version}-%{release}
Provides:      golang(%{import_path}/platform/machine/do) = %{version}-%{release}
Provides:      golang(%{import_path}/platform/machine/esx) = %{version}-%{release}
Provides:      golang(%{import_path}/platform/machine/gcloud) = %{version}-%{release}
Provides:      golang(%{import_path}/platform/machine/packet) = %{version}-%{release}
Provides:      golang(%{import_path}/platform/machine/qemu) = %{version}-%{release}
Provides:      golang(%{import_path}/sdk) = %{version}-%{release}
Provides:      golang(%{import_path}/sdk/omaha) = %{version}-%{release}
Provides:      golang(%{import_path}/sdk/repo) = %{version}-%{release}
Provides:      golang(%{import_path}/storage) = %{version}-%{release}
Provides:      golang(%{import_path}/storage/index) = %{version}-%{release}
Provides:      golang(%{import_path}/system) = %{version}-%{release}
Provides:      golang(%{import_path}/system/exec) = %{version}-%{release}
Provides:      golang(%{import_path}/system/ns) = %{version}-%{release}
Provides:      golang(%{import_path}/system/targen) = %{version}-%{release}
Provides:      golang(%{import_path}/system/user) = %{version}-%{release}
Provides:      golang(%{import_path}/update) = %{version}-%{release}
Provides:      golang(%{import_path}/update/generator) = %{version}-%{release}
Provides:      golang(%{import_path}/update/metadata) = %{version}-%{release}
Provides:      golang(%{import_path}/update/signature) = %{version}-%{release}
Provides:      golang(%{import_path}/util) = %{version}-%{release}
Provides:      golang(%{import_path}/version) = %{version}-%{release}

%description devel
%{summary}

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

############## kola subpackage ##############
%package kola
Summary:   A tool for launching instances and running tests
%description kola
%{summary}

############## kolet subpackage ##############
%package kolet
Summary:  A kola agent that runs on instances
%description kolet
%{summary}

############### ore subpackage ###############
%package ore
Summary:  A tool for interfacing with cloud providers
%description ore
%{summary}

################ plume subpackage #############
%package plume
Summary: A tool for releasing cloud images
%description plume
%{summary}

################ gangue subpackage #############
%package gangue
Summary: A tool for downloading from Google Storage
%description gangue
%{summary}

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test-devel
Summary:         Unit tests for %{name} package
%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%if 0%{?with_check} && ! 0%{?with_bundled}
BuildRequires: golang(github.com/kylelemons/godebug/diff)
BuildRequires: golang(github.com/kylelemons/godebug/pretty)
BuildRequires: golang(golang.org/x/crypto/openpgp/errors)
%endif

Requires:      golang(github.com/kylelemons/godebug/diff)
Requires:      golang(github.com/kylelemons/godebug/pretty)
Requires:      golang(golang.org/x/crypto/openpgp/errors)

%description unit-test-devel
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n %{repo}-%{commit}

%build
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../ src/%{import_path}

%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
# No dependency directories so far
export GOPATH=$(pwd):%{gopath}
%endif

# Cork is not included as it is an Container Linux development tool
%gobuild -o bin/cmd/gangue %{import_path}/cmd/gangue
%gobuild -o bin/cmd/kola %{import_path}/cmd/kola
%gobuild -o bin/cmd/kolet %{import_path}/cmd/kolet
%gobuild -o bin/cmd/ore %{import_path}/cmd/ore
%gobuild -o bin/cmd/plume %{import_path}/cmd/plume

%install
install -d -p %{buildroot}%{_bindir}
install -p -m 0755 bin/cmd/gangue %{buildroot}%{_bindir}
install -p -m 0755 bin/cmd/kola %{buildroot}%{_bindir}
install -p -m 0755 bin/cmd/kolet %{buildroot}%{_bindir}
install -p -m 0755 bin/cmd/ore %{buildroot}%{_bindir}
install -p -m 0755 bin/cmd/plume %{buildroot}%{_bindir}

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . \( -iname "*.go" -or -iname "*.s" \) \! -iname "*_test.go" | grep -v "vendor") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test-devel.file-list
for file in $(find . -iname "*_test.go" | grep -v "vendor") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test-devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
# Since we aren't packaging up the vendor directory we need to link
# back to it somehow. Hack it up so that we can add the vendor
# directory from BUILD dir as a gopath to be searched when executing
# tests from the BUILDROOT dir.
ln -s ./ ./vendor/src # ./vendor/src -> ./vendor

export GOPATH=%{buildroot}/%{gopath}:$(pwd)/vendor:%{gopath}
%endif

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}/harness
%gotest %{import_path}/lang/bufpipe
%gotest %{import_path}/lang/maps
%gotest %{import_path}/lang/natsort
%gotest %{import_path}/lang/reader
%gotest %{import_path}/network
%gotest %{import_path}/network/bufnet
%gotest %{import_path}/network/journal
%gotest %{import_path}/network/mockssh
%gotest %{import_path}/network/ntp
%gotest %{import_path}/platform/conf
%gotest %{import_path}/sdk
%gotest %{import_path}/sdk/repo
%gotest %{import_path}/storage
%gotest %{import_path}/system
%gotest %{import_path}/system/exec
%gotest %{import_path}/system/targen
%gotest %{import_path}/system/user
%gotest %{import_path}/update/generator
%gotest %{import_path}/update/signature
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
%doc README.md platforms.md code-of-conduct.md runner-readme.md CONTRIBUTING.md

%files kola
%{_bindir}/kola

%files kolet
%{_bindir}/kolet

%files ore
%{_bindir}/ore

%files plume
%{_bindir}/plume

%files gangue
%{_bindir}/gangue

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE
%doc README.md platforms.md code-of-conduct.md runner-readme.md CONTRIBUTING.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test-devel -f unit-test-devel.file-list
%license LICENSE
%doc README.md platforms.md code-of-conduct.md runner-readme.md CONTRIBUTING.md
%endif

%changelog
* Fri Jan 11 2019 Sayan Chowdhury <sayanchowdhury@fedoraproject.org>
- First package for Fedora
