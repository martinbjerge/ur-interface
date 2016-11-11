using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using log4net;

namespace UniversalRobotsConnect
{
    class ChangeToolCommand:Command
    {
        private static readonly ILog log = LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);
        private string _tempFunction;
        private string _tempToolName;
        private RobotConnector _robotConnector;

        public ChangeToolCommand(RobotConnector robotConnector, string tempFunction, string tempToolName)
        {
            _robotConnector = robotConnector;
            _tempFunction = tempFunction;
            _tempToolName = tempToolName;
            log.Debug("Instantiated");
        }

        public override void Execute()
        {
            log.Debug($"Moving to get another tool");

            string move = "def move_j():\nmovej([-2.13,-1.45,3.56,-1.75,-1.43,0.0],a=1.2,v=0.9,r=0)\nend\n";
            byte[] commandBytes = Encoding.UTF8.GetBytes(move);
            _robotConnector.RealTimeClient.Send(commandBytes);

            while (_robotConnector.RobotModel.RuntimeState != RuntimeState.Idle)
            {
               
            }

            log.Debug($"Arrived at tool position - I am {_tempFunction}ting the {_tempToolName} tool");
            Thread.Sleep(1000);

            IsCompleted = true;
        }

        public override bool IsCompleted { get; set; }
    }
}
