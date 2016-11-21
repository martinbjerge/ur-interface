using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using log4net;
using log4net.Config;

namespace UniversalRobotsConnect
{
    public class RobotConnector
    {
        public RopeRoboticsRobotModel RobotModel;
        public RTDE RTDE;
        public RealTimeClient RealTimeClient;
        private ForceTourqe ForceTourqe;
        public DashboardClient DashboardClient;

        private static readonly ILog log = LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        public RobotConnector(string ipAddress, bool hasForceTorque)
        {
            FileInfo logFileInfo = new FileInfo(@"C:\SourceCode\ur-interface\URConnect\UniversalRobotsConnect\bin\Debug\Resources\logConfig.xml");
            XmlConfigurator.Configure(logFileInfo);

            log.Debug("Started Logging");

            RobotModel = new RopeRoboticsRobotModel();
            log.Debug("Started Robot Model");
            RobotModel.IpAddress = IPAddress.Parse(ipAddress);

            RTDE = new RTDE(RobotModel);
            RealTimeClient = new RealTimeClient(RobotModel);
            if (hasForceTorque)
            {
                ForceTourqe = new ForceTourqe(RobotModel);
            }
            DashboardClient = new DashboardClient(RobotModel);
        }
    }
}
