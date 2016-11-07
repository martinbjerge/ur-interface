using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RobotServer
{
    public class RobotController
    {
        public RobotModel RobotModel;
        private RobotConnector _robotConnector;

        public RobotController()
        {
            RobotModel = new RobotModel();
            _robotConnector = new RobotConnector(RobotModel);
  
        }
    }
}
