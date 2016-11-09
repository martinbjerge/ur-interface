using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using log4net;

namespace UniversalRobotsConnect
{
    public class RealTimeClient
    {
        private static readonly ILog log = LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        private const int port = 30003;
        private TcpClient _client;
        private NetworkStream _stream;
        private RealTimeClientSender _realtimeClientSender;
        private RealTimeClientReceiver _realTimeClientReceiver;
        private RobotModel _robotModel;

        public RealTimeClient(RobotModel robotModel)
        {
            _robotModel = robotModel;
            _client = new TcpClient(_robotModel.IpAddress.ToString(), port);
            _stream = _client.GetStream();

            log.Debug("Starting RealtimeClientReceiver");
            _realTimeClientReceiver = new RealTimeClientReceiver(_stream);
            log.Debug("Starting RealtimeClientSender");
            _realtimeClientSender = new RealTimeClientSender(_stream);
        }

        public void Send(byte[] payload)
        {
            _realtimeClientSender.SendData(payload);
        }

    }
}
