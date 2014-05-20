Poseidon
========

Poseidon is Python script that extracts tiles from the NEPTUN map server and reconstitutes them as an image. 

1. Select a map you desire from [NEPTUN](http://neptun.unamur.be/items/browse?collection=30)
2. Start the script and either:

	a. pass the parameters throught the command line, or

	```
python namur_city 6/007B 2
python namur_city 6/007B 3 256
	```

	b. respond to the prompts (defining tile size is not an option).

3. Poseiden asks for:

	a. an arbitrary map name,

	b. the map code (formatted something like 6/005),
	
	c. the zoom level (1 will be a small image, 5 very large and high resolution)

It's a little ridiculous that a library university (funded by the public) is not making this data directly available.

Enjoy.
