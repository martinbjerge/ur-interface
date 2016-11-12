using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using log4net;

namespace UniversalRobotsConnect
{
    class MoveToHomePositionCommand:Command
    {
        private static readonly ILog log = LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);
        private RobotConnector _robotConnector;
        public MoveToHomePositionCommand(RobotConnector robotConnector)
        {
            _robotConnector = robotConnector;
            log.Debug("Instantiated");
        }

        public override void Execute()
        {
            //log.Debug("Executing");
            string move = "def move_j():\nmovej([1.5,0.0,-3.14,-0.5,0.0,0.0],a=1.2,v=0.9,r=0)\nend\n";
            byte[] commandBytes = Encoding.UTF8.GetBytes(move);
            _robotConnector.RealTimeClient.Send(commandBytes);
            log.Debug("Moving to storage position");
            while (_robotConnector.RobotModel.RuntimeState != RuntimeState.Idle)
            {
                
            }
            log.Debug("WE ARE DONE .. GOING HOME");
            IsCompleted = true;
        }

        public override bool IsCompleted { get; set; }


    }
}
