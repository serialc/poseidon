# Poseidon, extracts maps from neptun map image tiles
# http://neptun.unamur.be/items/browse?collection=30
import Image, re, sys, os, urllib2

print("Poseidon, extracts maps from neptun map image tiles.\nSee http://neptun.unamur.be/items/browse?collection=30\n")

# Max tile group search - increase if you get only partial image
max_tile_groups = 3

# Tile sizes
size = 256

######################################################################
# Part 1 - Setup, read inputs
######################################################################
# read inputs either passed as argumenents or prompted
# Code: 6/007 - clean to format '6-7'
# Zoom level

# Get arguments from command line or interactively
if len(sys.argv) == 4:
	name, code, zoom = sys.argv[1:4]
elif len(sys.argv) == 5:
	name, code, zoom, size = sys.argv[1:5]
elif sys.argv[1] == '--help':
	print("Command format:")
        print("python Poseiden.py")
        exit("python Poseiden.py 'name' 'map code' 'zoom level' [optional tile size-256 default]\n")

elif len(sys.argv) == 1:
	try:
		name = raw_input("Enter map name:")
		code = raw_input("Enter map code (e.g., 6/007):")
		zoom = int(raw_input("Zoom level (test with 1 first):"))
	except NameError:
		print("Hmmm you are using Python 3.x perhaps...")
		name = input("Enter map name:")
		code = input("Enter map code (e.g., 6/007):")
		zoom = int(input("Zoom level (test with 1 first):"))
else:
	exit("Command format:\n python Poseiden.py 'name' 'map code' 'zoom level' 'optional tile size-256 default'")

# make directory to hold tiles and result
base_path = name
try:
	os.makedirs(base_path + '/tiles')
except:
	print("Folder already exists, this may overwrite data.")

# format code for url
code = code.lower().replace('0','').replace('/','-')

# create base url
base_url = "http://webapps.fundp.ac.be/bib/zoom/rca-" + code + "_img/TileGroup"

######################################################################
# Part 2 - retrieve tiles
######################################################################

tile_group = 0
valid_tg = False

x = 0
# go through columns
while True:
	y = 0
	# go through rows, down column
	while True:
		print(str(x) + ',' + str(y))
		
		# check if file exists locally
		if not os.path.exists(base_path + '/tiles/' + name + '_' + str(zoom) + '-' + str(x) + '-' + str(y) + '.jpg'):
			# check if it is available online
			try:
				res = urllib2.urlopen(base_url + str(tile_group) + '/' + str(zoom) + '-' + str(x) + '-' + str(y) + '.jpg')
			except urllib2.HTTPError:
				print("Searching for new tile group")
				valid_tg = False

				# search other tile groups for piece
				for tile_number in range(max_tile_groups + 1):
					try:
						res = urllib2.urlopen(base_url + str(tile_number) + '/' + str(zoom) + '-' + str(x) + '-' + str(y) + '.jpg')

						# found a working tile group, save and exit this nexted loop
						tile_group = tile_number
						valid_tg = True
						print("Using new tile group:" + str(tile_group))
						break

					except urllib2.HTTPError:
						# try the next tile group
						continue
						
			  
				if valid_tg == False:
					print("End of column")
					break
		
			# file exists, we download it -> res
			f = open(base_path + '/tiles/' + name + '_' + str(zoom) + '-' + str(x) + '-' + str(y) + '.jpg', 'wb')
			f.write(res.read())
			f.close()
		
		# increment y
		y = y + 1

	# if there is no more columns or rows, quit
	if valid_tg == False and y == 0:
		print("Finished processing grid.")
		break

	# increment x
	x = x + 1

######################################################################
# Part 3 - combine tiles to make an image
######################################################################

# file name base
fnbase = base_path + '/tiles/' + name + '_' + str(zoom) + '-'

# determine number of tiles in x,y dimension
xr = 0
yr = 0
for fn in os.listdir(base_path + '/tiles'):
	the_regex = name + '_' + str(zoom) + '\-(\d+)-(\d+)' 
	xymatch = re.match(the_regex, fn)
	if xymatch:
		# save the largest index x,y numbers
		if int(xymatch.group(1)) > xr:
			xr = int(xymatch.group(1))
		if int(xymatch.group(2)) > yr:
			yr = int(xymatch.group(2))

# Increase xr, yr because 0 indexed filenames
xr += 1
yr += 1

print("Image dimension in tiles is " + str(xr) + " by " + str(yr))

# create blank image
mosaic = Image.new("RGB", (xr * size, yr * size))

last_col_tile_width = size
last_row_tile_width = size
# actually build the image
for x in range(xr):
	for y in range(yr):
		tile = Image.open(fnbase + str(x) + '-' + str(y) + '.jpg')
		mosaic.paste(tile, (x * size, y * size))
		
		# get the size of the non-standard tile - this is the edge
		# x/last column
		if tile.size[0] < size:
			last_col_tile_width = tile.size[0]
		# y/last row
		if tile.size[1] < size:
			last_row_tile_width = tile.size[1]
			
mosaic = mosaic.crop((0,0,
	(xr - 1) * size + last_col_tile_width,
	(yr - 1) * size + last_row_tile_width))
mosaic.save(base_path + '/' + name + '_zoom-' + str(zoom) + '.jpg')
