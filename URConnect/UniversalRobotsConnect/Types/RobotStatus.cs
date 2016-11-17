using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UniversalRobotsConnect.Types
{
    public class RobotStatus
    {
        public bool PowerOn { get; set; }

        public bool ProgramRunning { get; set; }

        public bool TeachButtonPressed { get; set; }

        public bool PowerButtonPressed { get; set; }
    }
}
