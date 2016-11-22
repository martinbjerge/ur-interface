using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using UniversalRobotsConnect.Types;

namespace UniversalRobotsConnect.IOs
{
    public class DistanceSensor:IOUnitBase
    {
        public DistanceSensor(string ioPort):base(ioPort) //StandardAnalogInput0
        {
            
        }

        public DistanceSensor():base()
        {
            
        }

        public string ioPort { get; set; }
        public double MinimumCurrent { get; set; }      //  4
        public double MaximumCurrent { get; set; }      //  20
        public double MinimumDistance { get; set; }     //  0.1
        public double MaximumDistance { get; set; }     //  0.5

        public Vector6D TCP_Offset { get; set; }

                     
    }
}
