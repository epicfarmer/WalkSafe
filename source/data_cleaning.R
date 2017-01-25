library(pryr)
library(dplyr)
library(readr)
library(ggplot2)
setwd('data')
list.files()[grepl('*.csv',list.files())] ->all_files
all_data = list()
real_data = data_frame(table=all_files)
for(file in all_files){
	all_data[[file]] = readr::read_csv(file) %>% mutate(table=file)
}
clean_data = data_frame()
all_data[['Adult_Day_Care_Facilities.csv']] %>% select(`Location 1`,table,name) -> clean_data
all_data[['Assisted_Living_Facilities.csv']] %>%
	select(`Location 1`,table,name) %>%
	full_join(clean_data) ->
	clean_data

#These are all building data
all_data[['Baltimore_City_Government_Entities.csv']] %>%
	mutate(
		name = `Formal Agency Name`,
		#`tempLocation` = sapply(strsplit(Location,"\n"),function(...){...[[3]]}),
		`Location 2` =
			sapply(
				strsplit(
					sapply(
						strsplit(
							sapply(
								strsplit(
								sapply(strsplit(Location,"\n"),function(x){x[[3]]}),
									"(",
									fixed=TRUE
								),
								function(x){x[[2]]}
							),
							")",
							fixed=TRUE
						),
						function(x){x[[1]]}
					),
					", ",
					fixed=TRUE
				),
				function(x){paste(x,collapse=" ")}
			),
		`Location 1` = paste(
			sapply(strsplit(Location,"\n"),function(...){...[[1]]}),
			sapply(strsplit(Location,"\n"),function(...){...[[2]]}),
			sep="\n"
		)
	) %>%
	select(name,`Location 1`,`Location 2`,table) %>%
	full_join(clean_data) ->
	clean_data

all_data[['bcpss_school.csv']] %>%
	mutate(`Location 1` = paste(ADDRESS,ZIPCODE,sep="\n")) %>%
	mutate(location = sapply(strsplit(sapply(strsplit(the_geom,"(",fixed=TRUE),function(...){...[[2]]}),")",fixed=TRUE),function(...){...[[1]]})) %>%
	mutate(
		`Location 2` = sapply(location,function(x){paste((rev(strsplit(x,split = ' ')[[1]])),collapse=' ')})
	) %>%
	mutate(name = NAME) %>%
	select(name,`Location 1`,`Location 2`,table) %>%
	full_join(clean_data) ->
	clean_data

#This is not building data it should be stored somwhere else.  Also, Location 1 contains GPS coordinates
#all_data[['BPD_Arrests.csv']] %>%

all_data[['BPD_Cameras.csv']] %>%
	mutate(location = sapply(strsplit(sapply(strsplit(the_geom,"(",fixed=TRUE),function(...){...[[2]]}),")",fixed=TRUE),function(...){...[[1]]})) %>%
	mutate(
		`Location 2` = sapply(location,function(x){paste((rev(strsplit(x,split = ' ')[[1]])),collapse=' ')})
	) %>%
	mutate(name = Name) %>%
	select(name,`Location 2`,table) %>%
	full_join(clean_data) ->
	clean_data

all_data[['Courthouses.csv']] %>%
	mutate(`Location 1` = paste(`Location 1`,zipCode,sep="")) %>%
	select(name,`Location 1`,table) %>%
	full_join(clean_data) ->
	clean_data

all_data[['crime_camera.csv']] %>%
	mutate(location = sapply(strsplit(sapply(strsplit(the_geom,"(",fixed=TRUE),function(...){...[[2]]}),")",fixed=TRUE),function(...){...[[1]]})) %>%
	mutate(
		`Location 2` = sapply(location,function(x){paste((rev(strsplit(x,split = ' ')[[1]])),collapse=' ')}),
		lat = XCOORD,
		long = YCOORD,
		name = CAM_NUM
	) %>%
	select(name,`Location 2`,table) %>%
	full_join(clean_data) ->
	clean_data

all_data[['Fire_Stations.csv']] %>%
	mutate(`Location 1` = paste(`Location 1`,zipCode,sep="")) %>%
	select(name,`Location 1`,table) %>%
	full_join(clean_data) ->
	clean_data

all_data[['Homeless_Services.csv']] %>%
	mutate(
		name = `Organization`,
		`Location 2` =
			sapply(
				strsplit(
					sapply(
						strsplit(
							sapply(
								strsplit(
								sapply(strsplit(`Location 1`,"\n"),function(x){x[[3]]}),
									"(",
									fixed=TRUE
								),
								function(x){x[[2]]}
							),
							")",
							fixed=TRUE
						),
						function(x){x[[1]]}
					),
					", ",
					fixed=TRUE
				),
				function(x){paste(x,collapse=" ")}
			),
		`Location 1` = paste(
			sapply(strsplit(`Location 1`,"\n"),function(...){...[[1]]}),
			sapply(strsplit(`Location 1`,"\n"),function(...){...[[2]]}),
			sep="\n"
		)
	) %>%
	select(name,`Location 1`,`Location 2`,table) %>%
	full_join(clean_data) ->
	clean_data

all_data[['Homeless_Shelters.csv']] %>%
	mutate(`Location 1` = paste(`Location 1`,zipCode,sep="")) %>%
	select(name,`Location 1`,table) %>%
	full_join(clean_data) ->
	clean_data

all_data[['Hospitals.csv']] %>%
  mutate(`Location 1` = paste(`Location 1`,zipCode,sep="")) %>%
  select(name,`Location 1`,table) %>%
  full_join(clean_data) ->
  clean_data

all_data[['Libraries.csv']] %>%
  mutate(`Location 1` = paste(`Location 1`,zipCode,sep="")) %>%
  select(name,`Location 1`,table) %>%
  full_join(clean_data) ->
  clean_data

all_data[['Museums.csv']] %>%
  mutate(`Location 1` = paste(`Location 1`,zipCode,sep="")) %>%
  select(name,`Location 1`,table) %>%
  full_join(clean_data) ->
  clean_data

all_data[['Nursing_Homes.csv']] %>%
  mutate(`Location 1` = paste(`Location 1`,zipCode,sep="")) %>%
  select(name,`Location 1`,table) %>%
  full_join(clean_data) ->
  clean_data

all_data[['Religious_Buildings.csv']] %>%
  mutate(`Location 1` = paste(`Location 1`,zipCode,sep="")) %>%
  select(name,`Location 1`,table) %>%
  full_join(clean_data) ->
  clean_data

all_data[['Restaurants.csv']] %>%
  mutate(`Location 1` = paste(`Location 1`,zipCode,sep="")) %>%
  select(name,`Location 1`,table) %>%
  full_join(clean_data) ->
  clean_data

all_data[['Senior_Centers.csv']] %>%
  mutate(`Location 1` = paste(`Location 1`,zipCode,sep="")) %>%
  select(name,`Location 1`,table) %>%
  full_join(clean_data) ->
  clean_data

all_data[['Vacant_Buildings.csv']] %>%
	mutate(
		`Location 2` =
			sapply(
				strsplit(
					sapply(
						strsplit(
							sapply(
								strsplit(
									Location,
									"(",
									fixed=TRUE
								),
								function(x){x[[2]]}
							),
							")",
							fixed=TRUE
						),
						function(x){x[[1]]}
					),
					", ",
					fixed=TRUE
				),
				function(x){paste(x,collapse=" ")}
			),
		`Location 1` = BuildingAddress,
		name = ReferenceID
	) %>%
  select(name,`Location 1`,`Location 2`, table) %>%
  full_join(clean_data) ->
  clean_data

#These are a bit harder to get something meaningful out of
#all_data[['Parking_Facilities.csv']]

#These are all crime-like statistics
#all_data[['BPD_Officer_Involved_Use_Of_Force.csv']]
#all_data[['BPD_Part_1_Victim_Based_Crime_Data.csv']]
#all_data[['Calls_for_Service.csv']]
#all_data[['ECB_Citations.csv']]
#all_data[['Parking_Citations.csv']]

#These are all miscellaneous other data
#all_data[['Census_Demographics__2010-2014_.csv']]
#all_data[['charm_city_circulator_route_20120126.csv']]
#all_data[['Housing_and_Community_Development__2010-2014_.csv']]

#Similar to buildings, but time dependent
#all_data[['Gun_Offenders.csv']]
#all_data[['Liquor_Licenses.csv']]

#Fields:
#table - which file it comes from
#name - the name of the building
#address - the street address
#zip - the zip code
#lat - the latitude
#long - the longitude
#c(lat,long) = ggmap::geocode(clean_data$`Location 1`


clean_data %>%
	mutate(location = strsplit(`Location 2`," ")) %>%
	filter(sapply(location,length) == 2) %>%
	mutate(
		latitude = sapply(strsplit(`Location 2`," "),function(x){as.numeric(x[[1]])}),
		longitude = sapply(strsplit(`Location 2`," "),function(x){as.numeric(x[[2]])})
	) %>%
	select(c(-`Location 1`,-`Location 2`)) ->
	filtered_clean_data

setwd('..')
source('source/reverse_geocoding.R')

filtered_clean_data %>% bind_rows(inner_join(data,clean_data)) -> final_data

final_data %>% filter(longitude > -85) -> filtered_final_data

#clean_data %>%
#	mutate(
#		lat = ggmap::geocode(`Location 1`)[[1]],
#		long = ggmap::geocode(`Location 1`)[[2]]
#	) ->
#	clean_data


min(filtered_final_data$latitude) -> ymin
max(filtered_final_data$latitude) -> ymax
min(filtered_final_data$longitude) -> xmin
max(filtered_final_data$longitude) -> xmax

f= function(table,lat,long){min(abs(lat-table$latitude) + abs(long - table$longitude))/.2705221 * 100}
tables = filtered_final_data$table %>% unique

n=100
#Note: Replace these with the actual points from the distance matrix
xseq = seq(xmin,xmax,(xmax-xmin)/(n-1))
yseq = seq(ymin,ymax,(ymax-ymin)/(n-1))
meshgrid = function(a,b){
	list(
		x=outer(b*0,a,FUN="+"),
		y=outer(b,a*0,FUN="+")
	)
}
XY = meshgrid(xseq,yseq)
X = as.vector(XY$x)
Y = as.vector(XY$y)
tmp = list()
for(row in tables){
	partial(f,table = filter(filtered_final_data,table==row)) -> g
	F <- mapply(
		g,
		long=X,
		lat=Y
	)
	data_frame(X,Y,F) -> tmp[[row]]
}
X2 = X[F!= 0]
Y2 = Y[F!= 0]
F2 = F[F!= 0]
tmp2 = list()
for(row in tables){
  partial(f,table = filter(filtered_final_data,table==row)) -> g
  F2 <- mapply(
    g,
    long=X2,
    lat=Y2
  )
  data_frame(X2,Y2,F2) -> tmp2[[row]]
}
#filtered_final_data %>% filter(table == 'Museums.csv') -> museums

read_csv('BPD_Part_1_Victim_Based_Crime_Data.csv') %>%
  filter(!is.na(`Location 1`)) %>%
  mutate(
    location = sapply(
      strsplit(
        sapply(
          strsplit(
            `Location 1`,
            split = ")",
            fixed=TRUE
          ),
          function(x){
            x[[1]]
          }
        ),
        split="(",
        fixed=TRUE
      ),
      function(x){
        x[[2]]
      }
    )
  ) %>%
  mutate(
    latitude = sapply(strsplit(location,split = ", ",fixed=TRUE),function(x){as.numeric(x[[1]])}),
    longitude = sapply(strsplit(location,split = ", ",fixed=TRUE),function(x){as.numeric(x[[2]])})
  ) %>%
  filter(latitude < 40) ->
  output

f2 = function(table,lat,long){sum(((lat - table$latitude)^2 + (long - table$longitude)^2)<.00001)}
partial(f2,table=output)->g
F = mapply(g,long=X,lat=Y)
all_data_frame = as_data_frame(tmp[[1]])
for(i in 2:length(tmp)){
  all_data_frame %>% inner_join(tmp[[i]],by=c('X','Y')) -> all_data_frame
}

F2 = mapply(g,long=X2,lat=Y2)
all_data_frame2 = as_data_frame(tmp2[[1]])
for(i in 2:length(tmp2)){
  all_data_frame2 %>% inner_join(tmp2[[i]],by=c('X2','Y2')) -> all_data_frame2
}

library(mgcv)
final_data_frame = all_data_frame %>% bind_cols(data_frame(output=F))
eqn = paste("output~",paste(colnames(final_data_frame)[1:(length(final_data_frame)-1)],collapse=' + '))

final_data_frame2 = all_data_frame2 %>% bind_cols(data_frame(output=F2))
eqn2 = paste("output~",paste(colnames(final_data_frame2)[1:(length(final_data_frame2)-1)],collapse=' + '))

gam(formula = formula(eqn),data = final_data_frame,family=poisson) -> model
ggplot(data_frame(X,Y,G= predict(model,type='response'))) + geom_raster(aes(x=X,y=Y,fill=G)) + scale_fill_gradient(low = 'blue',high='orange',limits=c(0,1500))

gam(formula = formula(eqn2),data = final_data_frame2,family=poisson) -> model2
ggplot(data_frame(X,Y,G= predict(model2,type='response'))) + geom_raster(aes(x=X,y=Y,fill=G)) + scale_fill_gradient(low = 'blue',high='orange',limits=c(0,1500))

ggplot(data_frame(X2,Y2,G=F2)) + geom_raster(aes(x=X2,y=Y2,fill=G)) + scale_fill_gradient(low = 'blue',high='orange',limits=c(0,1500))
