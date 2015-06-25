qemu-system-x86_64 -k fr -m 2G -hda ~/Development/PackStack/centos_controller.img -enable-kvm -cpu host -boot c -net nic,macaddr=0a:51:9c:d4:05:c6 -net bridge,br=bridge0 -nographic
