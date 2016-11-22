using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UniversalRobotsConnect.IOs
{
    public class IOUnitBase
    {
        public IOUnitBase(string ioPort)
        {
            IOPort = ioPort;
        }

        public IOUnitBase()
        {
            
        }

        public string IOPort { get; set; }
    }
}
