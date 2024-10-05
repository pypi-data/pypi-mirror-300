import math
import numpy as np

class Georeference:
	# Convert WGS84 lat/lon to ECEF
	def llh2ecef(self,latitude,longitude,ellipsoidal_height):
		return np.array([
			(6378137.0 / (math.sqrt(1 - (0.081819190842622 ** 2) * (math.sin(latitude) ** 2))) + ellipsoidal_height) * math.cos(latitude) * math.cos(longitude),
			(6378137.0 / (math.sqrt(1 - (0.081819190842622 ** 2) * (math.sin(latitude) ** 2))) + ellipsoidal_height) * math.cos(latitude) * math.sin(longitude),
			(6378137.0 / (math.sqrt(1 - (0.081819190842622 ** 2) * (math.sin(latitude) ** 2))) * (1 - (0.081819190842622 **2)) + ellipsoidal_height) * math.sin(latitude)
		])


	# Computes the position of a sonar sounding in the ECEF frame
	def compute(self,latitude,longitude,ellipsoidal_height,heading,pitch,roll,depth,offset_x,offset_y,offset_z):
		# Compute frame conversion matrix between local (NED) and terrestrial (ECEF) frames
		self.ned_2_ecef=np.array([
			[-math.cos(longitude)*math.sin(latitude),-math.sin(longitude),-math.cos(latitude)*math.cos(longitude)],
			[-math.sin(latitude)*math.sin(longitude),math.cos(longitude),-math.cos(latitude)*math.sin(longitude)],
			[math.cos(latitude),0,-math.sin(latitude)]
		])

		# Compute motion compensation matrix
		self.imu_2_ned=np.array([
			[math.cos(heading)*math.cos(pitch), math.cos(heading)*math.sin(pitch)*math.sin(roll)-math.cos(roll)*math.sin(heading), math.cos(heading)*math.cos(roll)*math.sin(pitch)+math.sin(roll)*math.sin(heading)],
			[math.cos(pitch)*math.sin(heading), math.cos(heading)*math.cos(roll)+math.sin(pitch)*math.sin(roll)*math.sin(heading), math.sin(heading)*math.cos(roll)*math.sin(pitch)-math.cos(heading)*math.sin(roll)],
			[-math.sin(pitch),  math.cos(pitch) * math.sin(roll), math.cos(roll) * math.cos(pitch)]
		]);

		# Sum the position, offset and depth vectors in the same frame (ECEF)
		return self.llh2ecef(latitude,longitude,ellipsoidal_height) + np.matmul(np.matmul(self.ned_2_ecef,self.imu_2_ned) , (np.array([offset_x,offset_y,offset_z]) + np.array([0,0,depth])));


