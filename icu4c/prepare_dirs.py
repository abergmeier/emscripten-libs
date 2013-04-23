import shutil, os, subprocess

BUILD_SRC = 'src_build'
HOST_SRC  = 'src_host'

dirs = [ BUILD_SRC, HOST_SRC ]

for dir in dirs:
	try:
		os.makedirs( dir )
	except os.error:
		pass

"""
def isolate_files():
	move_files = []
	for entry in os.listdir( '.' ):
		if entry in [BUILD_SRC, HOST_SRC]:
			continue
		move_files.append( entry )

	try:
		os.makedirs( BUILD_SRC )
	except os.error:
		pass

	# move all files to BUILD_SRC
	for entry in move_files:
		shutil.move( entry, BUILD_SRC )


def copy_build_to_host():
	try:
		# copytree doesn't want tree
		shutil.rmtree( HOST_SRC )
	except os.error:
		pass

	# make a copy in HOST_SRC
	shutil.copytree( BUILD_SRC, HOST_SRC )
"""

def config():
	prefix = os.environ['EMSCRIPTEN_SYSTEM_ROOT']
	common_configure_args = [ '\'' + os.path.abspath( os.path.join('source', 'configure')) + '\'',
	                          '--prefix=\'' + prefix + '\'',
	                          '--enable-static',
	                          '--disable-shared',
	                          '--disable-dyload',
	                          '--disable-renaming',
	                          '--with-data-packaging=static',
	                          'CXXFLAGS=\'-DU_USING_ICU_NAMESPACE=0\'',
	                          'CPPFLAGS=\'-DU_DISABLE_RENAMING=1\'' ]


	abs_build_src = os.path.abspath( BUILD_SRC )
	return { 'common': { 'config': common_configure_args
	         },
	         'build' : { 'path': { 'rel': BUILD_SRC,
	                               'abs': abs_build_src
	                     },
	                     'config': common_configure_args
	         },
	         'host'  : { 'path': { 'rel': HOST_SRC,
	                               'abs': os.path.abspath( HOST_SRC )
	                     },
	                     'config': common_configure_args + ['--host=i386-pc-linux-gnu', '--with-cross-build=\'' + abs_build_src + '\'' ]
	         }
	}

#isolate_files()
#copy_build_to_host()
systems = config()
def build_path( what ):
	return systems[what]['path']['abs']

assert( os.path.isdir(build_path('build')) )
assert( os.path.isdir(build_path('host' )) )

def config_command( what ):
	return systems[what]['config']

make_command = [ 'emmake', 'make' ]

subprocess.check_call( config_command('build')   , shell=True, cwd=build_path('build') )
print 1
subprocess.check_call( make_command              , cwd=build_path('build') )
print 2
subprocess.check_call( ' '.join(['emconfigure'] + config_command('host')), shell=True, cwd=build_path('host') )
print 3
subprocess.check_call( make_command              , cwd=build_path('host' ) )
print 4
subprocess.check_call( make_command + ['install'], cwd=build_path('host' ) )
print 5

