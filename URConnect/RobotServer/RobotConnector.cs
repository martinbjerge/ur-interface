using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace RobotServer
{
    class RobotConnector
    {
        public RobotModel RobotModel;
        //private RealTimeClient _realTimeClient;
        private RTDE _rtde;
        private RealTimeClient _realTimeClient;

        
        public RobotConnector(RobotModel robotModel)
        {
            RobotModel = robotModel;
            

        
            //_realTimeClient = new RealTimeClient(RobotModel.IpAddress, RobotModel.Password);
            _rtde = new RTDE(RobotModel);
            _realTimeClient = new RealTimeClient(RobotModel.IpAddress);
        }
    }
}
