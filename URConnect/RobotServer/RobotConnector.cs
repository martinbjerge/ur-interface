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
        private RobotModel _robotModel;
        //private RealTimeClient _realTimeClient;
        private RTDE _rtde;
        private RealTimeClient _realTimeClient;

        public RobotConnector(RobotModel robotModel)
        {
            _robotModel = robotModel;
            _robotModel.IpAddress = IPAddress.Parse("172.16.92.131");

            //_realTimeClient = new RealTimeClient(_robotModel.IpAddress, _robotModel.Password);
            _rtde = new RTDE(_robotModel);
            _realTimeClient = new RealTimeClient(_robotModel.IpAddress);
        }
    }
}
