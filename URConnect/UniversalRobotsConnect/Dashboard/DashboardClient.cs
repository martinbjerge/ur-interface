using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using log4net;

namespace UniversalRobotsConnect
{
    public class DashboardClient
    {
        private static readonly ILog log = LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        private const int port = 29999;
        private TcpClient _client;
        private NetworkStream _stream;
        private DashboardClientSender _dashboardClientSender;
        private DashboardClientReceiver _dashboardClientReceiver;
        private RobotModel _robotModel;

        public DashboardClient(RobotModel robotModel)
        {
            _robotModel = robotModel;
            _client = new TcpClient(_robotModel.IpAddress.ToString(), port);
            _stream = _client.GetStream();

            log.Debug("Starting DashboardClientReceiver");
            _dashboardClientReceiver = new DashboardClientReceiver(_stream/*, _robotModel*/);
            log.Debug("Starting DashboardClientSender");
            _dashboardClientSender = new DashboardClientSender(_stream);


        }

        public void UnlockProtectiveStop()
        { 
            _dashboardClientSender.SendData(Encoding.UTF8.GetBytes("unlock protective stop\n"));
        }

        public void CloseSafetyPopup()
        {
            _dashboardClientSender.SendData(Encoding.UTF8.GetBytes("close safety popup\n"));
        }

        public void PowerOn()
        {
            _dashboardClientSender.SendData(Encoding.UTF8.GetBytes("power on\n"));
        }

        public void PowerOff()
        {
            _dashboardClientSender.SendData(Encoding.UTF8.GetBytes("power off\n"));
        }

        public void BrakeRelease()
        {
            _dashboardClientSender.SendData(Encoding.UTF8.GetBytes("brake release\n"));
        }

        public void Stop()
        {
            _dashboardClientSender.SendData(Encoding.UTF8.GetBytes("stop\n"));
        }

        public void Shutdown()
        {
            _dashboardClientSender.SendData(Encoding.UTF8.GetBytes("shutdown\n"));
        }


    }
}
