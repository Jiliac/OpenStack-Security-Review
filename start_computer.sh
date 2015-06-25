qemu-system-x86_64 -k fr -m 2G -hda ~/Development/PackStack/centos_computer.img -enable-kvm -cpu host -boot c -net nic,macaddr=0a:51:9c:d4:05:b7 -net bridge,br=bridge0 -nographic
