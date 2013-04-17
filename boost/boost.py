#!/usr/bin/env python2
import urllib, os

buildPath = os.getcwd()
def get_version_string():
	with open( os.path.join( buildPath, 'boost', 'version.hpp' ), 'r' ) as version_file:
		for line in version_file:
			if line.startswith( '#define BOOST_VERSION ' ):
				return line.split()[2]
	return None

strVersion = get_version_string()
assert strVersion is not None
patch = int(strVersion) % 100
minor = int(strVersion) / 100 % 1000
major = int(strVersion) / 100000
tag = 'boost_' + str(major) + '.' + str(minor) + '.' + str(patch)
config_uri = 'https://raw.github.com/abergmeier/emscripten-libs/' + tag + '/boost/boost.pc'
pc_path = os.path.join(buildPath, 'boost.pc')
urllib.urlretrieve( config_uri, pc_path )

