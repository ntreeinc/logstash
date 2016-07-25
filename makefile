package_name=logstash
patch_name=logstash-patterns
source_name=logstash-2.3.4

RPM_BASE=${PWD}/build/rpm

raw_spec=$(package_name).spec
processed_spec=$(RPM_BASE)/SPECS/$(package_name).spec

raw_patch=${patch_name}.patch

raw_source=${source_name}.tar.gz

VERSION:=$(shell scripts/get-version)

clean:
	rm -rf "$(RPM_BASE)"

rpmdirs:
	mkdir -p "${RPM_BASE}/SOURCES" "${RPM_BASE}/BUILD" "${RPM_BASE}/BUILDROOT" "${RPM_BASE}/RPMS/noarch" "${RPM_BASE}/SPECS"

$(processed_spec): rpmdirs $(raw_spec)
	perl -pe "s/^Version:.*/Version: $(VERSION)/" "$(raw_spec)" > "$(processed_spec)"
	cp ${raw_patch} ${RPM_BASE}/SOURCES/
	cp ${raw_source} ${RPM_BASE}/SOURCES/

rpm: rpmdirs $(processed_spec)
	rpmbuild --define "_topdir ${PWD}/build/rpm"  -bb "$(processed_spec)"

#install:
#	mkdir -p '$(DESTDIR)'
#	cp -r src/* '$(DESTDIR)/'

publish-rpm: rpm
	scripts/nexus-publish $(VERSION) "$(RPM_BASE)/RPMS/noarch/"*rpm '$(package_name)'

bump-and-tag:
	scripts/bump-and-tag
