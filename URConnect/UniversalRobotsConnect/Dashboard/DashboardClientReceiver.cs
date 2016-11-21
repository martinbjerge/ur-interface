using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using log4net;

namespace UniversalRobotsConnect
{
    class DashboardClientReceiver
    {
        private static readonly ILog log = LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);
        private NetworkStream _stream;
        private Thread _thread;

        public DashboardClientReceiver(NetworkStream _stream)
        {
            this._stream = _stream;
            //_robotModel = robotModel;
            _thread = new Thread(Run);
            _thread.Start();
        }

        private void Run()
        {
            //while (true)
            //{
            //    if (_stream.DataAvailable)
            //    {
            //        if (_stream.CanRead)
            //        {
            //            byte[] myReadBuffer = new byte[400];
            //            StringBuilder myCompleteMessage = new StringBuilder();
            //            int numberOfBytesRead = 0;

            //            do
            //            {
            //                numberOfBytesRead = _stream.Read(myReadBuffer, 0, myReadBuffer.Length);
            //                myCompleteMessage.AppendFormat("{0}", Encoding.ASCII.GetString(myReadBuffer, 0, numberOfBytesRead));
            //            } while (_stream.DataAvailable);

            //            //log.Debug("Force Tourqe Received: " + myCompleteMessage);
            //            //DecodePacage(myCompleteMessage.ToString());
            //        }
            //        else
            //        {
            //            log.Error("Can not read from this network stream");
            //            throw new SystemException();
            //        }
            //    }
            //}
        }
    }
}
