###########################################################
#                                                         #
#                "Kosmos" version 1.0                     #
#                                                         #
###########################################################

import random
import os

##################### CONSTANTS ###########################

# These values determine the age of the galaxy that is generated
GALAXYSTARTAGE = 2000 # Measured in millions
GALAXYMAXAGE = 13000  # Measured in millions

# The interval in which the galaxy ages (Measured in millions of years)
GALAXYINTERVALAGE = 10

# This is the maximum number of clusters that will be generated
# DO NOT SET THIS HIGHER THAN 14 WITHOUT UPDATING THE CLUSTER
# NAME LIST!
NUMBEROFCLUSTERS = 4

# These values are used to determine the structure and organization of the galaxy.
# Do not modify these values unless you're sure of what you're doing
NUMBEROFREGIONS = 12
NUMBEROFCONSTELLATIONS = 88
NUMBEROFSTARS = 48

# Odds that a cluster of stars will be formed (Checked once every interval)
# E.g. a value of 200 means there's a 1 in 201 chance that a star cluter will
# form.
CLUSTERODDS = 200

# Odds that a star will become a neutron star after death
NEUTRONODDS = 0

# Odds that a star will form a black hole after death
BLACKHOLEODDS = 0

##########################################################



#################### NAMING LISTS ########################

# List of names for the clusters
listOfClusterNames = ["Odin", "Frigg", "Freyja", "Thor", "Loki", "Tyr", "Vidar",
                   "Hel", "Sif", "Thrud", "Ull", "Baldur", "Heimdall", "Jord"]

# List of names for the regions
listOfRegionNames = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake",
                     "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]

# List of names for the constellations
listOfConstellationNames = ["Andromedae", "Antliae", "Apodis", "Aquarii", "Aquilae", "Arae", "Arietis", "Aurigae", "Bootis", "Caeli", "Camelopardalis", "Cancri", "Canum Venaticorum", "Canis Majoris", "Canis Minoris",
                            "Capricorni", "Carinae", "Cassiopeiae", "Centauri", "Cephei", "Ceti", "Chamaeleontis", "Circini", "Columbae", "Comae Berenices", "Coronae Australis", "Coronae Borealis", "Corvi", "Crateris",
                            "Crucis", "Cygni", "Delphini", "Doradus", "Draconis", "Equulei", "Eridani", "Fornacis", "Geminorum", "Gruis", "Herculis", "Horologii", "Hydrae", "Hydri", "Indi", "Lacertae", "Leonis",
                            "Leonis Minoris", "Leporis", "Librae", "Lupi", "Lyncis", "Lyrae", "Mensae", "Microscopii", "Monocerotis", "Muscae", "Normae", "Octantis", "Ophiuchi", "Orionis", "Pavonis", "Pegasi", "Persei",
                            "Phoenicis", "Pictoris", "Piscium", "Piscis Austrini", "Puppis", "Pyxidis", "Reticuli", "Sagittae", "Sagittarii", "Scorpii", "Sculptoris", "Scuti", "Serpentis", "Sextantis", "Tauri",
                            "Telescopii", "Tranguli", "Trianguli Australis", "Tucanae", "Ursae Majoris", "Ursae Minoris", "Velorum", "Virginis", "Volantis", "Vulpeculae"]

# List of names for the stars
listOfStarNames = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", "Iota", "Kappa", "Lambda", "Mu",
                   "Nu", "Xi", "Omicron", "Pi", "Rho", "Sigma" ,"Tau" ,"Upsilon" ,"Phi" ,"Chi" ,"Psi", "Omega",
                   "A", "b", "c", "d", "e", "f", "g", "h", "i", "k", "l", "m",
                   "n", "o", "p", "q", "r", "s", "t", "u", "w", "x", "y", "z"]


#########################################################


############# INDICES AND TRACKER VARIABLES ##############

# List of all clusters
listOfClusters = []

# Number of generated stars and planets
# Currently only used to give user statistics.
numberOfStars = 0
numberOfPlanets = 0

# The age of the galaxy
galaxyAge = GALAXYSTARTAGE

#########################################################

class Cluster:
    """Serves as an owner of regions. There is a hard limit of 12 regions per cluster."""
    
    def __init__(self, name):
        self.name = name

        # List of a cluster's regions
        self.regions = []

class Region:
    """Serves as an owner of constellations. There is a hard limit of 88 constellations per region."""

    def __init__(self, name):
        self.name = name

        # List of a region's constellations
        self.constellations = []

class Constellation:
    """Serves as an owner of stars. There is a hard limit of 48 stars per constellation."""

    def __init__(self, name):
        self.name = name

        # List of a constellation's stars
        self.stars = []




        
class MSStar:
    """This defines a star and its properties"""
    
    def __init__(self, classification, mass, radius, c, a, v, d, luminosity, lifetime, temp,
                 habitableInner, habitableOuter, limitInner, limitOuter, frostline, age):
        # A temporary name is given here. The real name is given once the galaxy has aged, and old stars have died.
        self.name = "N/A"
        
        # Then we proceed as normal
        self.classification = classification
        self.mass = mass
        self.radius = radius
        self.c = c
        self.a = a
        self.v = v
        self.d = d
        self.luminosity = luminosity
        self.lifetime = lifetime
        self.temp = temp

        self.habitableInner = habitableInner
        self.habitableOuter = habitableOuter

        self.limitInner = limitInner
        self.limitOuter = limitOuter

        self.frostline = frostline

        self.age = age

        self.planets = []

class Planet:
    """This defines a planet and its properties"""
    
    def __init__(self, star, classification, distance, mass, radius, c, a, v, d, gravity):
        # A temporary name is given here. The real name is given once the galaxy has aged, and old stars have died.
        self.name = "N/A"

        # Then we proceed as normal
        self.star = star
        self.classification = classification
        self.distance = distance
        self.mass = mass
        self.radius = radius
        self.c = c
        self.a = a
        self.v = v
        self.d = d

        self.gravity = gravity

        
def nameConstellationStars(constellation):
    """This function takes a constellation and names all the stars in that constellation."""
    
    # Sort the list of the constellation's stars by luminosity
    constellation.stars.sort(key = lambda star: star.luminosity, reverse=True)

    # Now run through the list and assign the names
    i = 0
    for star in constellation.stars:
        star.name = listOfStarNames[i] + " " + constellation.name
        i = i + 1


def nameStarSystem(star):
    """This function takes a star and names all planets in that system."""

    # Sort the list of the system's planets by distance
    star.planets.sort(key = lambda planet: planet.distance)
    
    # Now run through the list and assign the names
    i = 1
    for planet in star.planets:
        planet.name = star.name + " " + str(i)
        i = i + 1
    

def generateCluster():
    """This function creates a new cluster"""

    global listOfClusterNames
    global listOfClusters

    # First we randomly pick out a name for the cluster
    randomVar = random.randint(1,len(listOfClusterNames)) - 1
    name = listOfClusterNames[randomVar]

    # Then we remove that name from the list of names
    del listOfClusterNames[randomVar]

    # Finally append the new cluster to the list of clusters
    newcluster = Cluster(name)
    listOfClusters.append(newcluster)
    
    

def generateRegion(cluster, i):
    """This fucntion creates a new region. The inputs are the owner cluster and name index."""

    global listOfRegionNames

    # First we pick the name for the region
    name = listOfRegionNames[i]

    # Finally we append the new region to the cluster's list of regions
    newregion = Region(name)
    cluster.regions.append(newregion)


def generateConstellation(region, i):
    """This function generates a new constellation. The inputs are the owner region and name index."""

    global listOfConstellationNames

    # First we pick the name for the constellation
    name = listOfConstellationNames[i]

    # Finally we append the new constellation to the region's list of constellations
    newconstellation = Constellation(name)
    region.constellations.append(newconstellation)


def generateStar(constellation):
    """This function generates all stars in a given constellation"""
    global numberOfStars
    
    # Determine the type and mass of star:
    i = random.uniform(0.0,100.0)
    if   (i < 0.00003):
        classification = "O"
        mass = random.uniform(16, 50)
    elif (i < 0.13):
        classification = "B"
        mass = random.uniform(2.1,16)
    elif (i < 0.73):
        classification = "A"
        mass = random.uniform(1.4,2.1)
    elif (i < 3.73):
        classification = "F"
        mass = random.uniform(1.04,1.4)
    elif (i < 10.33):
        classification = "G"
        mass = random.uniform(0.8,1.04)
    elif (i < 22.43):
        classification = "K"
        mass = random.uniform(0.45,0.8)
    else:
        classification = "M"
        mass = random.uniform(0.08,0.45)

    mass = round(mass, 2)
    if (random.randint(0,999) < 96):
        classification = "White Dwarf"
        mass = random.uniform(0.17,1.4)
        mass = round(mass, 2)

    # Determine the radius
    if (mass < 1): radius  = mass ** 0.8
    elif (mass > 1): radius = mass ** 0.5
    else:          radius = mass
    if (classification == "White Dwarf"):
        radius = 0.00915 * (mass ** (-0.33))

    radius = round(radius, 5)

    # Determine the circumference, area, volume, density
    c = radius
    a = radius ** 2
    a = round(a, 8)
    v = radius ** 3
    v = round(v, 8)
    d = mass/v
    d = round(d, 2)

    # Determine the luminosity
    luminosity = mass ** 3.5
    luminosity = round(luminosity, 4)

    # Determine lifetime
    lifetime = mass/luminosity * 10000
    lifetime = round(lifetime)

    # Determine the surface temperature
    temp = ((luminosity/(radius ** 2)) ** 0.25) * 5778
    temp = round(temp)

    # Determine the habitable zone
    habitableInner = round( (luminosity/1.1) ** 0.5, 2 )
    habitableOuter = round( (luminosity/0.53) ** 0.5, 2 )

    # Determine the inner and outer limits of the solar system
    limitInner = round( 0.1*mass, 2 )
    limitOuter = round( 40*mass, 2 )

    # Check that the habitable zone does not fall outside this limit
    if (habitableInner >= limitOuter) or (habitableOuter <= limitInner):
        habitableInner = "N/A"
        habitableOuter = "N/A"

    # Determine the frostline
    frostline = round( 4.85 * (luminosity ** 0.5) ,2)

    # Set its age
    age = 0
    
    newstar = MSStar(classification, mass, radius, c, a, v, d, luminosity, lifetime, temp,
                           habitableInner, habitableOuter, limitInner, limitOuter, frostline, age)

    constellation.stars.append(newstar)

    numberOfStars = numberOfStars + 1
    # Generate planets
    #generatePlanets(newstar)


def generatePlanets(star):
    global numberOfPlanets

    i = 1
    gasgiants = True
    
    distance = star.frostline + random.uniform(0.014*star.frostline,0.14*star.frostline)
    distance = round(distance, 2)


    if (( ((star.classification != "M" and star.classification != "K") or random.randint(0,59) == 0)
             and ((star.classification != "A" and star.classification != "F" and star.classification != "G")
                  or random.randint(0,15) == 0)
             and ((star.classification != "B" and star.classification != "O")
                  or random.randint(0,5) == 0) ) == False):
        gasgiants = False
    if (star.classification == "White Dwarf"):
        gasgiants = False
        
    while(distance < star.limitOuter and gasgiants == True):
        classification = "Gas Giant"

        mass = random.uniform(10.1, 1000) # Span of earth masses for gas giants


        mass = mass / 317.94
        mass = round(mass, 2)

        # These are all measured in Jupiter values
        radius = 22.6 * (mass ** (-0.0886))
        radius = round(radius, 2)
        c = round(radius, 2)
        a = round(radius ** 2, 3)
        v = round(radius ** 3, 4)
        d = round(mass / v, 4)


        gravity = "N/A"
        
        newplanet = Planet(star, classification, distance, mass, radius, c, a, v, d, gravity)
        star.planets.append(newplanet)

        distance = distance * random.uniform(1.4,2.0)
        distance = round(distance,2)
        i = i + 1

    i = 1

    distance = (star.frostline + random.uniform(0.014*star.frostline,0.14*star.frostline)) / random.uniform(1.4,2.0)
    distance = round(distance, 2)
    
    while(distance > star.limitInner):
        if (star.classification == "A" or star.classification == "O" or star.classification == "B" or star.classification == "White Dwarf"):
            break

        classification = "Planet"

        mass = random.uniform(0.1, 10) # Span of earth masses for non-gas giants
        mass = round(mass, 2)


        # These are all measured in Earth values
        if (mass < 1):
            radius = mass ** 0.3
        else:
            radius = mass ** 0.5

        radius = round(radius, 2)
        c = round(radius, 2)
        a = round(radius ** 2, 3)
        v = round(radius ** 3, 4)
        d = round(mass / v, 4)

        gravity = mass / (radius ** 2)
        gravity = round(gravity,2)
        
        newplanet = Planet(star, classification, distance, mass, radius, c, a, v, d, gravity)


        i = i + 1
        distance = distance / random.uniform(1.4,2.0)
        distance = round(distance, 2)
        if ( (newplanet.distance - distance) > 0.15 ):
            star.planets.append(newplanet)
            numberOfPlanets = numberOfPlanets + 1
        else:
            break

def makeDwarf(star, mass=0):
    """Turns a star of arbitrary type into a dwarf star"""

    # Mass will not be set when creating a white dwarf
    if (mass == 0):
        # Determine the mass
        star.classification = "White Dwarf"
        star.mass = random.uniform(0.17,1.4)
        star.mass = round(star.mass, 2)
    # So if it is, we're makign a neutron star
    else:
        star.classification = "Neutron Star"
        star.mass = random.uniform(1.4,3)
        star.mass = round(star.mass, 2)

    # Determine the radius
    star.radius = 0.00915 * (star.mass ** (-0.33))

    star.radius = round(star.radius, 5)

    # Determine the circumference, area, volume, density
    star.c = star.radius
    star.a = star.radius ** 2
    star.a = round(star.a, 8)
    star.v = star.radius ** 3
    star.v = round(star.v, 8)
    star.d = star.mass/star.v
    star.d = round(star.d, 2)

    # Determine the luminosity
    star.luminosity = star.mass ** 3.5
    star.luminosity = round(star.luminosity, 4)

    # Determine lifetime
    star.lifetime = star.mass/star.luminosity * 10000
    star.lifetime = round(star.lifetime)

    # If it's a neutron star
    if (mass != 0):
        star.lifetime = "N/A"
        star.age = "N/A"

    # Determine the surface temperature
    star.temp = ((star.luminosity/(star.radius ** 2)) ** 0.25) * 5778
    star.temp = round(star.temp)

    # Determine the habitable zone
    star.habitableInner = round( (star.luminosity/1.1) ** 0.5, 2 )
    star.habitableOuter = round( (star.luminosity/0.53) ** 0.5, 2 )

    # Determine the inner and outer limits of the solar system
    star.limitInner = round( 0.1*star.mass, 2 )
    star.limitOuter = round( 40*star.mass, 2 )

    # Check that the habitable zone does not fall outside this limit
    if (star.habitableInner >= star.limitOuter) or (star.habitableOuter <= star.limitInner):
        star.habitableInner = "N/A"
        star.habitableOuter = "N/A"

    # Determine the frostline
    star.frostline = round( 4.85 * (star.luminosity ** 0.5) ,2)


def makeBlackHole(star):
    """This function creates a black hole from a star"""

    # First we determine the black hole's mass
    star.mass = star.mass / 4
    
    # Next we set the classification and radius
    star.classification = "Black Hole"

    star.radius = 2.95 * star.mass # Measured in kilometers!
    star.radius = round(star.radius, 5)

    # Determine the circumference, area, volume, density
    star.c = star.radius
    star.a = star.radius ** 2
    star.a = round(star.a, 8)
    star.v = star.radius ** 3
    star.v = round(star.v, 8)
    star.d = star.mass/star.v
    star.d = round(star.d, 2)

    # Set values that are not applicable
    star.luminosity = 0
    star.lifetime = "N/A"
    star.temp = "N/A"
    star.habitableInner = "N/A"
    star.habitableOuter = "N/A"
    star.age = "N/A"
    star.frostline = "N/A"

    # Determine the inner and outer limits of the solar system
    star.limitInner = round( 0.1*star.mass, 2 )
    star.limitOuter = round( 40*star.mass, 2 )
   



def ageGalaxy():
    """This function ages the entire galaxy one interval"""
    global galaxyAge
    global GALAXYINTERVALAGE
    global numberOfStars
    
    for cluster in listOfClusters:
        for region in cluster.regions:
            for constellation in region.constellations:
                for star in constellation.stars:
                    # Age every star in the galaxy that is not a special type
                    if (star.classification != "Neutron Star" and star.classification != "Black Hole"):
                        star.age = star.age + GALAXYINTERVALAGE

                        # Check if the star needs to die
                        if (star.age > star.lifetime):
                            if (star.classification == "White Dwarf"):
                                # If it is a white dwarf remove it
                                constellation.stars.remove(star)
                                numberOfStars = numberOfStars - 1
                                
                                # If it's a normal star, turn it into a white dwarf
                            elif (star.mass < 10):
                                # TO-DO: Make stars go through stages where they are first red giants
                                makeDwarf(star)
                                # If it's a more massive star turn it into a neutron star
                            elif (star.mass >= 10 and star.mass < 20):
                                if (random.randint(0, NEUTRONODDS) == 0):
                                    makeDwarf(star, star.mass)
                                else:
                                    constellation.stars.remove(star)
                                    numberOfstars = numberOfStars - 1
                                    # If it's even more massive turn it into a black hole
                            elif (star.mass >= 20):
                                if (random.randint(0, BLACKHOLEODDS) == 0):
                                    makeBlackHole(star)
                                else:
                                    constellation.stars.remove(star)
                                    numberOfStars = numberOfStars - 1
                            else:
                                print("something whent wrong!")

                        
    galaxyAge = galaxyAge + GALAXYINTERVALAGE
    
    



# Create the galaxy
print("Generating galaxy...")
while ( (len(listOfClusters) < NUMBEROFCLUSTERS) and (galaxyAge < GALAXYMAXAGE)):

    # This value keeps track of the completion percentage and prints it to the user
    done = len(listOfClusters)/NUMBEROFCLUSTERS
    done = round(done, 2) * 100
    print(str(done) + "%", end="\r")

    # Check is a cluster is supposed to be created, and if so, fill it with stars
    if (random.randint(0, CLUSTERODDS) == 0):
        generateCluster()
        for i in range(NUMBEROFREGIONS):
            generateRegion(listOfClusters[-1], i)
            for j in range(NUMBEROFCONSTELLATIONS):
                generateConstellation(listOfClusters[-1].regions[-1], j)
                for k in range(NUMBEROFSTARS):
                    generateStar(listOfClusters[-1].regions[-1].constellations[-1])
        

    # Advance the age of the galaxy    
    ageGalaxy()

# Age the galaxy
print("\n")
print("Aging galaxy...")
while( galaxyAge < GALAXYMAXAGE):
    # Age it
    ageGalaxy()

    # Print the progress
    done = galaxyAge / GALAXYMAXAGE
    done = round(done, 2) * 100
    print(str(done) + "%", end="\r")


# Name all stars
print("\n")
print("Naming stars...")
for cluster in listOfClusters:
    for region in cluster.regions:
        for constellation in region.constellations:
            nameConstellationStars(constellation)
            

# Write the results
i = 0
habitableCounter = 0
print("Writing star data...")

# This creates the directory structure
for cluster in listOfClusters:
    os.makedirs(str(cluster.name))
    for region in cluster.regions:
        os.makedirs(str(cluster.name) + "/" + str(region.name))
        for constellation in region.constellations:
            os.makedirs(str(cluster.name) + "/" + str(region.name) + "/" + str(constellation.name))
            for star in constellation.stars:
                f = open(str(cluster.name) + "/" + str(region.name) + "/" + str(constellation.name) +
                         "/" + str(star.name),'w')
                
                # Write the star's data to its own file
                f.write("Name: " + star.name + "\n")
                f.write("Age: " + str(star.age) + " millions of years\n")
                f.write("Type: " + star.classification + "\n")
                f.write("Mass: " + str(star.mass) + " solar masses\n")
                f.write("Radius: " + str(star.radius) + " solar radii\n")
                f.write("Circumference: " + str(star.c) + " solar circumferences\n")
                f.write("Area: " + str(star.a) + " solar area\n")
                f.write("Volume: " + str(star.v) + " solar volumes\n")
                f.write("Density: " + str(star.d) + " solar densities\n")
                f.write("Luminosity: " + str(star.luminosity) + " times as luminous as the sun\n")
                f.write("Lifetime: " + str(star.lifetime) + " millions of years\n")
                f.write("Surface temperature: " + str(star.temp) + " kelvin\n")
                f.write("Stellar limit: " + str(star.limitInner) + "-" + str(star.limitOuter) + " AU\n")
                f.write("Habitable zone: " + str(star.habitableInner) + "-" + str(star.habitableOuter) +
                        " AU\n")
                f.write("Frost line: " + str(star.frostline) + " AU\n")

                # Report the progress to the user
                i = i + 1
                done = i / numberOfStars
                done = round(done, 2)
                print(str(done) + "%", end="\r")

        
#        for p in m.planets:
#            f = open(str(n.name) + "/" + str(m.name) + "/" + str(p.name),'w')
#            f.write("Name: " + p.name + "\n")
#            f.write("Type: " + p.classification + "\n")
#            f.write("Distance: " + str(p.distance) + " AU\n")
#
#            if (p.classification == "Planet"):
#                f.write("Mass: " + str(p.mass) + " Earth masses.\n")
#                f.write("Radius: " + str(p.radius) + " Earth radii.\n")
#                f.write("Circumference" + str(p.c) + " Earth circumferences\n")
#                f.write("Area: " + str(p.a) + " Earth area\n")
#                f.write("Volume: " + str(p.v) + " Earth volumes\n")
#                f.write("Density: " + str(p.d) + " Earth densities\n")
#            if (p.classification == "Gas Giant"):
#                f.write("Mass: " + str(p.mass) + " Jupiter masses.\n")
#                f.write("Radius: " + str(p.radius) + " Jupiter radii.\n")
#                f.write("Circumference" + str(p.c) + " Jupiter circumferences\n")
#                f.write("Area: " + str(p.a) + " Jupiter area\n")
#                f.write("Volume: " + str(p.v) + " Jupiter volumes\n")
#                f.write("Density: " + str(p.d) + " Jupiter densities\n")
#            f.write("Gravity: " + str(p.gravity) + " times Earth's gravity\n")
#
#            if (m.habitableInner != "N/A" and m.habitableOuter != "N/A"):
#                if (p.distance < m.habitableOuter and p.distance > m.habitableInner):
#                    f.write("Planet is habitable!")
#                    habitableCounter = habitableCounter + 1
#            

print("\n")
print("Done!")
print("Number of planets: " + str(numberOfPlanets) + "\n")
print("Number of habitable planets: " + str(habitableCounter) + "\n")
print("Average number of planets per star: " + str(round(numberOfPlanets / numberOfStars, 1)))
f.close
