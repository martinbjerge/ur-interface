using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UniversalRobotsConnect.Types
{
    public class URControlVersion
    {
        public int Major { get; private set; }

        public int Minor { get; private set; }

        public int Bugfix { get; private set; }

        public int Build { get; private set; }

        public URControlVersion(int major, int minor, int bugfix, int build)
        {
            Major = major;
            Minor = minor;
            Bugfix = bugfix;
            Build = build;
        }
    }
}
