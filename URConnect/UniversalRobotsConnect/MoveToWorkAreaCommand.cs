using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using log4net;

namespace UniversalRobotsConnect
{
    class MoveToWorkAreaCommand:Command
    {
        private static readonly ILog log = LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);
        private RobotConnector _robotConnector;

        public MoveToWorkAreaCommand(RobotConnector robotConnector)
        {
            _robotConnector = robotConnector;
            log.Debug("Instantiated");
        }

        public override void Execute()
        {
            


            log.Debug("MOVING TO WORK AREA");
            string move = "def move_j():\nmovej([-2.7,-0.454,0.87,-1.989,-1.58,0.524],a=1.2,v=0.9,r=0)\nend\n";
            byte[] commandBytes = Encoding.UTF8.GetBytes(move);
            while (_robotConnector.RobotModel.RuntimeState != RuntimeState.Idle)
            {
            }

//            io

//            string move = "def move_j():\nmovej([-2.7,-0.454,0.87,-1.989,-1.58,0.524],a=1.2,v=0.9,r=0)\nend\n";
//            byte[] commandBytes = Encoding.UTF8.GetBytes(move);
//            while (_robotConnector.RobotModel.RuntimeState != RuntimeState.Idle)
//            {
//            }

////            dfsdf
//            string move = "def move_j():\nmovej([-2.7,-0.454,0.87,-1.989,-1.58,0.524],a=1.2,v=0.9,r=0)\nend\n";
//            byte[] commandBytes = Encoding.UTF8.GetBytes(move);
//            while (_robotConnector.RobotModel.RuntimeState != RuntimeState.Idle)
//            {
//            }

//            string move = "def move_j():\nmovej([-2.7,-0.454,0.87,-1.989,-1.58,0.524],a=1.2,v=0.9,r=0)\nend\n";
//            byte[] commandBytes = Encoding.UTF8.GetBytes(move);
//            while (_robotConnector.RobotModel.RuntimeState != RuntimeState.Idle)
//            {
//            }

//            _robotConnector.RealTimeClient.Send(commandBytes);
//            while (_robotConnector.RobotModel.RuntimeState != RuntimeState.Idle)
//            {
//            }

            log.Debug($"Arrived at work area");
            IsCompleted = true;
        }

        public override bool IsCompleted { get; set; }
    }
}
