Series-tools will consist of several handy tools, which are designed to make it easier to manage local collections of television series. Currently, only one such tool is available called getnext.

getnext
=======

Getnext does one thing and does that well: it downloads the next available episode to the current directory. It does so by analyzing the file names looking for certain patterns (currently three of them) used for metadata storage. In its current state, getnext takes the following assumptions for granted:

 - the source for new episodes is located in the .src subdirectory of the working directory (e.g. mounted via sshfs)
 - the episodes are reachable directly under .src (i.e. no sub-directories by seasons), sub-directories for each episode are allowed though
 - the latest locally stored episode is located in the working directory

Example of a valid directory structure
--------------------------------------

	working_dir/
		.src/
			series.2x09.mkv
			series.s02e10.i-love-winrar/
				series.i-love-winrar.rar
				series.i-love-winrar.r01
				...
			...
		series.115.ogg
		series.2x09.mkv
		...

In this example, getnext would recognize that the next episode to be downloaded is the 10th from season 2 and it needs to be extracted from RAR.
