using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using log4net;
using log4net.Config;

namespace RobotServer
{
    public class RobotController
    {
        public readonly RobotModel RobotModel;
        private RobotConnector _robotConnector;
        private static readonly ILog log = LogManager.GetLogger(typeof(RobotController));

        public RobotController(string ipAddress)
        {
            //BasicConfigurator.Configure();
            FileInfo logFileInfo = new FileInfo(@"C:\SourceCode\ur-interface\URConnect\RobotServer\bin\Debug\Resources\logConfig.xml");
            XmlConfigurator.Configure(logFileInfo);
            
            log.Debug("Started Logging");

            RobotModel = new RobotModel();
            log.Debug("Started Robot Model");
            RobotModel.IpAddress = IPAddress.Parse(ipAddress);
            _robotConnector = new RobotConnector(RobotModel);
  
        }
    }
}
