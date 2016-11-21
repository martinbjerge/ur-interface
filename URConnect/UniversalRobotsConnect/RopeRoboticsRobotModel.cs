using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UniversalRobotsConnect
{
    public class RopeRoboticsRobotModel:RobotModel
    {
        public RopeRoboticsRobotModel()
        {
            //Load config    
        }




        public double LaserSensorDistance
        {
            get
            {
                // the current range is 4[mA] to 20[mA]
                double sensor_min_curr = 4;
                double sensor_max_curr = 20;
                //the test range, 0.1[m] to 0.5[m]
                double sensor_min_dist = 0.1;
                double sensor_max_dist = 0.5;
                
                return (StandardAnalogInput0-sensor_min_curr) * (sensor_max_dist-sensor_min_dist) / (sensor_max_curr-sensor_min_curr) + sensor_min_dist ;
            }
            
        }
    }
}
