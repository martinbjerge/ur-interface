using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using log4net;

namespace UniversalRobotsConnect
{
    class RealTimeClientReceiver
    {
        private static readonly ILog log = LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        internal event EventHandler<DataReceivedEventArgs> DataReceived;
        private NetworkStream _stream;
        private Thread _thread;
        //private RobotModel _robotModel;

        public RealTimeClientReceiver(NetworkStream stream) //, RobotModel robotModel)
        {
            //_robotModel = robotModel;
            _stream = stream;
            _thread = new Thread(Run);
            //_thread.Start();
        }

        private void Run()
        {
            while (true)
            {
                if (_stream.DataAvailable)
                {
                    //if (_stream.CanRead)
                    //{
                    //    byte[] myReadBuffer = new byte[4000];
                    //    StringBuilder myCompleteMessage = new StringBuilder();
                    //    int numberOfBytesRead = 0;

                    //    do
                    //    {
                    //        numberOfBytesRead = _stream.Read(myReadBuffer, 0, myReadBuffer.Length);
                    //        myCompleteMessage.AppendFormat("{0}", Encoding.ASCII.GetString(myReadBuffer, 0, numberOfBytesRead));
                    //    } while (_stream.DataAvailable);

                    //    Thread.sleep
                        

                    //    //log.Debug("RealtimeClient Received: " + myCompleteMessage);
                    //}
                    //else
                    //{
                    //    Debug.WriteLine("Sorry.  You cannot read from this NetworkStream.");
                    //    throw new SystemException();
                    //}
                }
                
            }
        }

    }
}
