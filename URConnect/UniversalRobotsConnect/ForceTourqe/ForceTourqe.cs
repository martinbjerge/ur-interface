using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using log4net;

namespace UniversalRobotsConnect
{
    class ForceTourqe
    {
        private static readonly ILog log = LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        private const int port = 63351;
        private TcpClient _client;
        private NetworkStream _stream;
        private ForceTourqeSender _forceTourqeSender;
        private ForceTourqeReceiver _forceTourqeReceiver;
        private RobotModel _robotModel;

        public ForceTourqe(RobotModel robotModel)
        {
            _robotModel = robotModel;
            _client = new TcpClient(_robotModel.IpAddress.ToString(), port);
            _stream = _client.GetStream();

            log.Debug("Starting ForceTourqeReceiver");
            _forceTourqeReceiver = new ForceTourqeReceiver(_stream, _robotModel);
            log.Debug("Starting ForceTourqeSender");
            _forceTourqeSender = new ForceTourqeSender(_stream);
        }

    }
}
