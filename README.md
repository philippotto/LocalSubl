# LocalSubl

On some linux systems, invoking subl via command line creates separate Sublime Text process which has several drawbacks.
As a dirty workaround, this package opens a socket and listens to requests to open files.
These requests can be issued by invoking `lsub.sh $filename` (lsub should be put into PATH).