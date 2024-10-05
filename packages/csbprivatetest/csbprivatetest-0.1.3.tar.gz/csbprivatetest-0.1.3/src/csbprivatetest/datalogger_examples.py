import georeference
import uncertainty
import math

#Common simulated data

latitude = math.radians(48.4525) 
longitude = math.radians(-68.5232)
ellipsoidal_height = -28
heading = math.radians(350)
pitch = math.radians(0.5)
roll = math.radians(1.5)
depth = 5
offset_x = 1
offset_y = 2
offset_z = 3

# ---------------------------------------------
# High-accuracy CIDCO datalogger

#Centimetric accuracy is typical when using PPP
latitude_sigma = 0.000001
longitude_sigma = 0.000001
ellipsoidal_height_sigma = 0.02

#IMU accuracy: the BNO055 datasheet gives +-1 degree on roll/pitch, and +-2 degrees on heading. We'll assume this is a 95% accuracy, or 2 sigmas
heading_sigma = math.radians(2/2)
pitch_sigma = math.radians(1/2)
roll_sigma = math.radians(1/2)

#FIXME: Imagenex 852 datasheet advertises a 1mm range resolution...which is probably not a reasonable accuracy figure...
depth_sigma = 0.001

#Offsets are measured with a total station, with millimetric accuracy
offset_x_sigma = 0.001
offset_y_sigma = 0.001
offset_z_sigma = 0.001


print("Hydroblock Uncertainty")
u = uncertainty.TotalPropagatedUncertainty()

tpu = u.compute(latitude,longitude,ellipsoidal_height,heading,pitch,roll,depth,offset_x,offset_y,offset_z,latitude_sigma,longitude_sigma,ellipsoidal_height_sigma,heading_sigma,pitch_sigma,roll_sigma,depth_sigma,offset_x_sigma,offset_y_sigma,offset_z_sigma)

print(tpu)
error_x=math.sqrt(tpu[0][0])
error_y=math.sqrt(tpu[1][1])
error_z=math.sqrt(tpu[2][2])

print(f"Approximate x error: {error_x:.3f} m")
print(f"Approximate y error: {error_y:.3f} m")
print(f"Approximate z error: {error_z:.3f} m")

print("---------------------------------------------------")

# -------------------------------------------
# Low-cost WIBL datalogger

#10m-ish error at equator for uncorrected GNSS readings
latitude_sigma = 0.0001
longitude_sigma = 0.0001
ellipsoidal_height_sigma = 1

#FIXME: what kind of IMU figures?
#IMU accuracy: the BNO055 datasheet gives +-1 degree on roll/pitch, and +-2 degrees on heading. We'll assume this is a 95% accuracy, or 2 sigmas
heading_sigma = math.radians(2/2)
pitch_sigma = math.radians(1/2)
roll_sigma = math.radians(1/2)

#FIXME: what kind of sonar ?
#Imagenex 852 datasheet advertises a 1mm range resolution...which is probably not a reasonable accuracy figure...
depth_sigma = 0.001

#FIXME: those are purely fictional
#Offsets are unknown
offset_x_sigma = 1 #Length of the boat
offset_y_sigma = 1 #Half the width
offset_z_sigma = 1 #Twice the depth of the boat assuming transducer fixed underneath


print("WIBL Uncertainty")
tpu = u.compute(latitude,longitude,ellipsoidal_height,heading,pitch,roll,depth,offset_x,offset_y,offset_z,latitude_sigma,longitude_sigma,ellipsoidal_height_sigma,heading_sigma,pitch_sigma,roll_sigma,depth_sigma,offset_x_sigma,offset_y_sigma,offset_z_sigma)

print(tpu)
error_x=math.sqrt(tpu[0][0])
error_y=math.sqrt(tpu[1][1])
error_z=math.sqrt(tpu[2][2])

print(f"Approximate x error: {error_x:.3f} m")
print(f"Approximate y error: {error_y:.3f} m")
print(f"Approximate z error: {error_z:.3f} m")

