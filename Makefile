
compile:
	gprbuild
record:
	touch dummy.txt
	while rr record ./bin/rr_demo-main ; do true ; done
replay:
	rr replay -s 12345
setup:
	echo 1 | sudo tee /proc/sys/kernel/perf_event_paranoid
	
						
