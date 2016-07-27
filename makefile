package_name=logstash
patch_name=logstash-patterns
source_name=logstash

RPM_BASE=${PWD}/build/rpm

raw_spec=$(package_name).spec
processed_spec=$(RPM_BASE)/SPECS/$(package_name).spec

raw_patch=${patch_name}.patch
raw_source=${source_name}.tar.gz

VERSION=$(shell grep ^Version: logstash.spec | sed -r s/^Version:\ +//g)
RELEASE=$(shell grep ^Release: logstash.spec | sed -r s/^Release:\ +//g)

source_name_version="${source_name}-${VERSION}"

test:
	scripts/nexus-publish "$(VERSION)" "$(RELEASE)" "$(RPM_BASE)/RPMS/noarch/"*rpm '$(package_name)'

clean:
	rm -rf "$(RPM_BASE)"

rpmdirs:
	mkdir -p "${RPM_BASE}/SOURCES" "${RPM_BASE}/BUILD" "${RPM_BASE}/BUILDROOT" "${RPM_BASE}/RPMS/noarch" "${RPM_BASE}/SPECS"

$(processed_spec): rpmdirs $(raw_spec)
	#perl -pe "s/^Version:.*/Version: $(VERSION)/" "$(raw_spec)" > "$(processed_spec)"
	cp $(raw_spec) $(processed_spec)
	cp ${raw_patch} ${RPM_BASE}/SOURCES/
	#cp ${raw_source} ${RPM_BASE}/SOURCES/

rpm: rpmdirs $(processed_spec)
	spectool --define "_topdir ${PWD}/build/rpm" -C 'build/rpm/SOURCES' -g logstash.spec 
	rpmbuild --define "_topdir ${PWD}/build/rpm"  -bb "$(processed_spec)"

install:
	mkdir -p '$(DESTDIR)'
	cp -r build/rpm/BUILD/${source_name_version}/* '$(DESTDIR)/'
	cp -r src/* '$(DESTDIR)/'

publish-snapshot: rpm
	scripts/nexus-publish "$(VERSION)" "$(RELEASE)" "$(RPM_BASE)/RPMS/noarch/"*rpm '$(package_name)'

publish-release: rpm
	scripts/nexus-publish "$(VERSION)" "" "$(RPM_BASE)/RPMS/noarch/"*rpm '$(package_name)'

#bump-and-tag:
#	scripts/bump-and-tag
