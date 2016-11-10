using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using log4net;

namespace UniversalRobotsConnect
{
    class SoakCommand:Command
    {
        private static readonly ILog log = LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        public SoakCommand()
        {
            log.Debug("Instantiated");
        }

        public override void Execute()
        {
            //log.Debug("Executing");

            int i = 0;

            while (i < 10)
            {
                log.Debug("I am soaking the 3D surface they gave me - at a given distance");
                Thread.Sleep(1500);
                i++;
            }
            log.Debug("DONE SOAKING");
            IsCompleted = true;
        }

        public override bool IsCompleted { get; set; }
    }
}
