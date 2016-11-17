using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UniversalRobotsConnect.Types
{
    public class SafetyStatus
    {
        public bool NormalMode { get; set; }

        public bool ReducedMode { get; set; }

        public bool ProtectiveStopped { get; set; }

        public bool RecoveryMode { get; set; }

        public bool SafeguardStopped { get; set; }

        public bool SystemEmergencyStopped { get; set; }

        public bool RobotEmergencyStopped { get; set; }

        public bool EmergencyStopped { get; set; }

        public bool Violation { get; set; }

        public bool Fault { get; set; }

        public bool StoppedDueToSafety { get; set; }
    }
}
