using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UniversalRobotsConnect.IOs
{
    public class LaserRangeSensor:IOUnitBase
    {
        public LaserRangeSensor(string ioPort):base(ioPort) //StandardAnalogInput0
        {
            
        }

        public double MinimumCurrent { get; set; }      //  4
        public double MaximumCurrent { get; set; }      //  20
        public double MinimumDistance { get; set; }     //  0.1
        public double MaximumDistance { get; set; }     //  0.5



                     
    }
}
