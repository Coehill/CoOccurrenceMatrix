===================================
	Coursework Collection
===================================

The image collection, containing 10,000 images annotated using 100 tags, is stored in 3 databse tables and is presented in 2 different formats:
- MySQL database, entire database (mysql folder)
- 3 Comma seperated files, 1 for each table (csv folder)

===================================
			Tables
===================================
- photos (id int,width int,height int,title string,uploaded datetime)
- photos_tags (photoid int, tag string)
- tags (tag string, num_photos int)

If there are any issues, please contact p.mcparlane.1@research.gla.ac.uk