#Imports
import pygeoip
import re

#city
def geo_city(x):
  
  #Read in MaxMind binary files, storing in memory for speed
  ip4_geo = pygeoip.GeoIP(filename = "/usr/share/GeoIP/GeoIPCity.dat", flags = 1)
  ip6_geo = pygeoip.GeoIP(filename = "/usr/share/GeoIP/GeoLiteCityv6.dat", flags = 1)

  #Create output object
  output = []
  
  for entry in x:
  
    #If it's IPV6, use the 6 method
    if(re.search(":",entry)):
      
      try:
        output.append(ip6_geo.record_by_addr(entry)['city'])
      except:
        output.append("Invalid")
    
    #4, use 4.
    else:
      
      try:
        output.append(ip4_geo.record_by_addr(entry)['city'])
      except:
        output.append("Invalid")
  
  #Done
  return output

#country
def geo_country(x):
  
  #Read in MaxMind binary files, storing in memory for speed
  ip4_geo = pygeoip.GeoIP(filename = "/usr/share/GeoIP/GeoIP.dat", flags = 1)
  ip6_geo = pygeoip.GeoIP(filename = "/usr/share/GeoIP/GeoIPv6.dat", flags = 1)
  
  #Create output list
  output = []
  
  #For each entry, retrieve the country code and replace
  for entry in x:
    
    #If it's IPV6, use the 6 method
    if(re.search(":",entry)):
      
      try:
        output.append(ip6_geo.country_code_by_addr(entry))
      except:
        output.append("Invalid")
    
    #4, use 4.
    else:
      
      try:
        output.append(ip4_geo.country_code_by_addr(entry))
      except:
        output.append("Invalid")
        
    #Done
    return output


#tz
def geo_tz(x):
  
  #Read in MaxMind binary files, storing in memory for speed
  ip4_geo = pygeoip.GeoIP(filename = "/usr/share/GeoIP/GeoIPCity.dat", flags = 1)
  ip6_geo = pygeoip.GeoIP(filename = "/usr/share/GeoIP/GeoLiteCityv6.dat", flags = 1)
  
  #Create output list
  output = []
  
  #For each entry, retrieve the country code and replace
  for entry in x:
    
    #If it's IPV6, use the 6 method
    if(re.search(":",entry)):
      
      try:
        output.append(ip6_geo.time_zone_by_addr(entry))
      except:
        output.append("Invalid")
    
    #4, use 4.
    else:
      
      try:
        output.append(ip4_geo.time_zone_by_addr(entry))
      except:
        output.append("Invalid")
        
    #Done
    return output
    
