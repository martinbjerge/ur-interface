using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace RobotServer
{
    public class RobotController
    {
        public RobotModel RobotModel;
        private RobotConnector _robotConnector;

        public RobotController(string ipAddress)
        {
            RobotModel = new RobotModel();
            RobotModel.IpAddress = IPAddress.Parse(ipAddress);
            _robotConnector = new RobotConnector(RobotModel);
  
        }
    }
}
