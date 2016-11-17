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
            // init pos
            // GetProgram from mønster  (fra movel eller move et eller andet)
            // send program
            // vendt på at RuntimeState = Idle

            //tænd damp
            // check damp er tændt
            // GetMønster  (list af poses)
            // GetProgram from mønster  (fra movel eller move et eller andet)
            // send program
            // vendt på at RuntimeState = Idle
            // sluk damp
            //  check at damp er lukket
            //Færdig
            // Move to neutral
            // GetProgram from mønster  (fra movel eller move et eller andet)
            // send program
            // vendt på at RuntimeState = Idle


            //while(




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
