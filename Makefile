
compile:
	gprbuild

# Start a recording 
record:
	rm -rf ${HOME}/.local/share/rr/
	rm -f dummy.txt
	echo "Bug Bug">dummy.txt
	while rr record ./bin/rr_demo-main ; do \
		true ;\
		rm -rf ${HOME}/.local/share/rr/;\
	done
	rm -f dummy.txt

replay:
	rm -f dummy.txt
	rr replay -s 12345
clean:

setup::${HOME}/.gnatstudio/plug-ins/rr_actions.py
	echo 1 | sudo tee /proc/sys/kernel/perf_event_paranoid

${HOME}/.gnatstudio/plug-ins/rr_actions.py:rr_actions.py
	mkdir -p $(dir $@)
	cd $(dir $@); ln  ${CURDIR}/$(notdir $@)

