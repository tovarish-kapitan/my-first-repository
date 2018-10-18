from bs4 import BeautifulSoup

class RSD():
    def __init__(self, our_kml_file):
        self.xradar_names = []
        self.xradar_positions = []
        self.lradar_names = []
        self.lradar_positions = []
        self.target_names = []
        self.target_trajectories = []
        
        with open (our_kml_file, encoding="UTF-8") as kml:
            my_kml = BeautifulSoup(kml, features="lxml")

        a=my_kml.find("placemark")
        if a==None:
            print("There is no Placemark tags in the file")
        else:
            while a!=None:
                name=a.find("name").get_text()
               
                coord=a.find("coordinates").get_text()
                coord=coord[5:-5] #обрезаем знаки \t \n по краям и пробел в конце
                c_list=coord.split(' ')
                
                i=0
                while i < len(c_list):
                    c_list[i]=c_list[i].split(',')
                    j=0
                    while j < len(c_list[i]):
                        c_list[i][j]=float(c_list[i][j]) #все числовые строки переводим во float
                        j=j+1
                    i=i+1
                    
                if name[0]=='X':
                    long=a.find("longitude").get_text() 
                    lat=a.find("latitude").get_text()
                    alt=a.find("altitude").get_text()
                    self.xradar_names.append(name)
                    self.xradar_positions.append((float(long),float(lat),float(alt)))
                elif name[0]=='L':
                    long=a.find("longitude").get_text() 
                    lat=a.find("latitude").get_text()
                    alt=a.find("altitude").get_text()
                    self.lradar_names.append(name)
                    self.lradar_positions.append((float(long),float(lat),float(alt)))
                else:
                    self.target_names.append(name)
                    self.target_trajectories.append(c_list)

                my_kml.placemark.decompose()
                a=my_kml.find("placemark")    
